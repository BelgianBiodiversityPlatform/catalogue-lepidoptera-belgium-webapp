from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from markdownx.models import MarkdownxField
from imagekit.processors import ResizeToFit


class Status(models.Model):
    VERBATIM_ID_VALID_FAMILY = 1
    VERBATIM_ID_FAMILY_SYNONYM = 2

    VERBATIM_ID_VALID_SUBFAMILY = 3
    VERBATIM_ID_SUBFAMILY_SYNONYM = 4

    VERBATIM_ID_VALID_GENUS = 5
    VERBATIM_ID_GENUS_SYNONYM = 6

    VERBATIM_ID_VALID_TRIBUS = 13
    VERBATIM_ID_TRIBUS_SYNONYM = 14

    VERBATIM_ID_VALID_SUBGENUS = 7
    VERBATIM_ID_SUBGENUS_SYNONYM = 8

    UNKNOWN = 15

    verbatim_status_id = models.IntegerField(unique=True, help_text="From the Access database")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "statuses"


class ValidFamiliesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_VALID_FAMILY)


class DisplayOrderNavigable(object):
    """Models that subclass this should have a 'display_order' field, provides next/prev methods."""
    def next(self):
        """Return the next instance in display_order, or None if we're the last one."""
        try:
            return self.__class__.objects.filter(display_order__gt=self.display_order).order_by('display_order')[0]
        except IndexError:
            return None

    def previous(self):
        """Return the previous instance in display_order, or None if we're the first one."""
        try:
            return self.__class__.objects.filter(display_order__lt=self.display_order).order_by('-display_order')[0]
        except IndexError:
            return None


class TaxonomicModel(models.Model):
    """Common ground between all taxon-related models."""
    @staticmethod
    def get_verbatim_id_field():
        # Blank/NULL allowed for post-import record
        return models.IntegerField(unique=True, blank=True, null=True, help_text="From the Access database")

    class Meta:
        abstract = True

    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    vernacular_name = models.CharField(max_length=255, blank=True)

    text = models.TextField(blank=True)

    display_order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Family(DisplayOrderNavigable, TaxonomicModel):
    # Synonyms currently disabled at the family level since:
    #   - we have no data for now
    #   - this makes implementation a bit more complex (public-facing pages, validation, foreign key to self, ...)
    #   - See genus for a full implementation
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_FAMILY]

    verbatim_family_id = TaxonomicModel.get_verbatim_id_field()

    representative_picture = models.ImageField(blank=True, null=True)
    representative_picture_thumbnail = ImageSpecField(source='representative_picture',
                                                      processors=[ResizeToFit(640, 480)],
                                                      format='JPEG',
                                                      options={'quality': 95})

    objects = models.Manager()
    valid_families_objects = ValidFamiliesManager()

    def get_absolute_url(self):
        return reverse('family_page', kwargs={'family_id': str(self.id)})

    # TODO: implements
    def species_count(self):
        return 0

    class Meta:
        verbose_name_plural = "families"


class Subfamily(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SUBFAMILY]

    verbatim_subfamily_id = TaxonomicModel.get_verbatim_id_field()

    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "subfamilies"


class Tribus(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_TRIBUS]

    verbatim_tribus_id = TaxonomicModel.get_verbatim_id_field()

    subfamily = models.ForeignKey(Subfamily, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "tribus"


class Genus(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_GENUS, Status.VERBATIM_ID_GENUS_SYNONYM, Status.UNKNOWN]

    verbatim_genus_id = TaxonomicModel.get_verbatim_id_field()

    # Sometimes a genus appears under a tribu, but sometimes only under a subfamily or a family...
    # One and only one of those can be filled
    tribus = models.ForeignKey(Tribus, null=True, blank=True, on_delete=models.CASCADE)
    subfamily = models.ForeignKey(Subfamily, null=True, blank=True, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, null=True, blank=True, on_delete=models.CASCADE)

    synonym_of = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "genera"

    def parent(self):
        # Return the direct parent
        return self.tribus or self.subfamily or self.family

    def parent_for_admin_list(self):
        return "{name} ({rank})".format(name=self.parent(), rank=self.parent().__class__.__name__)

    parent_for_admin_list.short_description = 'parent'

    def clean(self):
        errors_dics = {}  # we aggregate errors for a complete output

        # Should be linked to either a tribus, a family or a subfamily
        fields = [self.tribus, self.subfamily, self.family]
        if len ([field for field in fields if field is not None]) != 1:
            errors_dics['tribus'] = ValidationError('Choose a tribus OR a family OR a subfamily', code='invalid')
            errors_dics['subfamily'] = ValidationError('Choose a tribus OR a family OR a subfamily', code='invalid')
            errors_dics['family'] = ValidationError('Choose a tribus OR a family OR a subfamily', code='invalid')

        # Synonym: we should know whom
        if (self.status == Status.objects.get(verbatim_status_id=Status.VERBATIM_ID_GENUS_SYNONYM)
                and not self.synonym_of):
            errors_dics['synonym_of'] = ValidationError('If status=synonym, this field is mandatory')

        # Accepted: synonym doesn't make any sense
        if (self.status == Status.objects.get(verbatim_status_id=Status.VERBATIM_ID_VALID_GENUS)
                and self.synonym_of):
            errors_dics['synonym_of'] = ValidationError('If status=accepted, this field shouldn\'t be used')

        if errors_dics:
            raise ValidationError(errors_dics)

    def save(self, *args, **kwargs):
        # Let's make sure model.clean() is called on each save (validation also for import script)
        self.full_clean()
        return super(Genus, self).save(*args, **kwargs)


class Subgenus(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SUBGENUS]

    verbatim_subgenus_id = TaxonomicModel.get_verbatim_id_field()

    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "subgenera"


class Species(models.Model):
    name = models.CharField(max_length=255)


class Province(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    order = models.IntegerField(unique=True, help_text="In presence tables: order in which the provinces are displayed")
    historical = models.BooleanField(help_text="The province doesn't exists anymore")
    recent = models.BooleanField(help_text="The province was created at province split")

    # reference to an external polygon for map display. # Exact data source to be defined, for example BEL_adm2.shp
    # (We need to add a polygon for historical Brabant, though)
    polygon_reference = models.IntegerField(unique=True)

    class Meta:
        ordering = ['order']


class TimePeriod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField()


class SpeciesPresence(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)


class PageFragment(models.Model):
    identifier = models.SlugField(unique=True)
    content_nl = MarkdownxField(blank=True)
    content_en = MarkdownxField(blank=True)
    content_fr = MarkdownxField(blank=True)
    content_de = MarkdownxField(blank=True)

    def __str__(self):
        return self.identifier

    @staticmethod
    def _get_content_field_name(language_code):
        return 'content_{}'.format(language_code)

    def get_content_in(self, language_code):
        # We try to get the content in language_code, but fallback to settings.PAGE_FRAGMENT_FALLBACK_LANGUAGE if no
        # translation exists
        translated_content = getattr(self, PageFragment._get_content_field_name(language_code))
        if translated_content == '':
            translated_content = getattr(self,
                                         PageFragment._get_content_field_name(settings.PAGE_FRAGMENT_FALLBACK_LANGUAGE))

        return translated_content

    def clean(self):
        fallback_language_code = settings.PAGE_FRAGMENT_FALLBACK_LANGUAGE

        if getattr(self, PageFragment._get_content_field_name(fallback_language_code)) == '':
            raise ValidationError("Content is mandatory for the fallback language ({})".format(fallback_language_code))


