from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from imagekit.models import ImageSpecField
from markdownx.models import MarkdownxField
from imagekit.processors import ResizeToFit


class Status(models.Model):
    VERBATIM_ID_VALID_FAMILY = 1
    VERBATIM_ID_FAMILY_SYNONYM = 2

    VERBATIM_ID_VALID_SUBFAMILY = 3
    VERBATIM_ID_SUBFAMILY_SYNONYM = 4

    verbatim_status_id = models.IntegerField(unique=True, help_text="From the Access database")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "statuses"


class ValidFamiliesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_VALID_FAMILY)


class Family(models.Model):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_FAMILY, Status.VERBATIM_ID_FAMILY_SYNONYM]

    verbatim_family_id = models.IntegerField(unique=True, help_text="From the Access database")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    vernacular_name = models.CharField(max_length=255, blank=True)

    text = models.TextField(blank=True)

    representative_picture = models.ImageField(blank=True, null=True)
    representative_picture_thumbnail = ImageSpecField(source='representative_picture',
                                                      processors=[ResizeToFit(640, 480)],
                                                      format='JPEG',
                                                      options={'quality': 95})

    display_order = models.IntegerField(unique=True)

    objects = models.Manager()
    valid_families_objects = ValidFamiliesManager()

    # TODO: implements
    def species_count(self):
        return 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "families"


class Subfamily(models.Model):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SUBFAMILY, Status.VERBATIM_ID_SUBFAMILY_SYNONYM]

    verbatim_subfamily_id = models.IntegerField(unique=True, help_text="From the Access database")

    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    vernacular_name = models.CharField(max_length=255, blank=True)

    text = models.TextField(blank=True)

    # Not sure if it'll be used, but ready just in case (same logic as families)
    display_order = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = "subfamilies"


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


