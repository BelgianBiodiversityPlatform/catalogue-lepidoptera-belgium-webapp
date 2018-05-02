from denorm import denormalized, depend_on_related, CountField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from imagekit.models import ImageSpecField
from markdownx.models import MarkdownxField
from imagekit.processors import ResizeToFit


# Managers, helpers, ...
def get_verbatim_id_field():
    # Blank/NULL allowed for post-import record
    return models.IntegerField(unique=True, blank=True, null=True, help_text="From the Access database")


class SpeciesManager(models.Manager):
    def get_with_name_and_author(self, name_and_author_string):
        """Takes a string such as 'Acrolepiopsis assectella (Zeller, 1839)' and return the matching species"""

        name_part = " ".join(name_and_author_string.split(" ", 2)[:2]) # cut after second space
        name_part = name_part.strip()  # Remove leading/trailing whitespaces

        name_part_genus, name_part_species = name_part.split()

        author_part = name_and_author_string.replace(name_part, '')
        author_part = author_part.strip()

        all_matching_species = self.get_queryset().filter(name=name_part_species, author=author_part)

        # Empty queryset: raise DoesNotExists
        if len(all_matching_species) == 0:
            raise Species.DoesNotExist()
        else:
            # One or several results. Ideally, one and only one should also match the genus
            all_matching_species = [species for species in all_matching_species if species.genus_name == name_part_genus]

            if len(all_matching_species) > 1:
                raise Species.MultipleObjectsReturned
            elif len(all_matching_species) == 0:
                raise Species.DoesNotExist()

            return all_matching_species[0]


class ValidFamiliesManager(SpeciesManager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_VALID_FAMILY)


class AcceptedGenusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_VALID_GENUS)


class SynonymGenusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_GENUS_SYNONYM)


class AcceptedSpeciesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_VALID_SPECIES)


class SynonymSpeciesManager(SpeciesManager):
    def get_queryset(self):
        return super().get_queryset().filter(status__verbatim_status_id=Status.VERBATIM_ID_SPECIES_SYNONYM)


class ParentForAdminListMixin(object):
    """Exposes a parent_for_admin_list method, for polymorphic parents.

    Needs a parent() method in implementing classes.
    """
    def parent_for_admin_list(self):
        return "{name} ({rank})".format(name=self.parent, rank=self.parent.__class__.__name__)

    parent_for_admin_list.short_description = 'parent'


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

    VERBATIM_ID_VALID_SPECIES = 9
    VERBATIM_ID_SPECIES_SYNONYM = 10

    UNKNOWN = 15

    verbatim_status_id = models.IntegerField(unique=True, help_text="From the Access database")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "statuses"


class CommonTaxonomicModel(models.Model):
    """Common ground between all taxon-related models (Lepidoptera, host plants, ...)"""
    name = models.CharField(max_length=255)

    vernacular_name = models.CharField(max_length=255, blank=True)

    wikidata_id = models.CharField(max_length=255, blank=True)

    last_modified = models.DateTimeField(auto_now=True)
    denorm_always_skip = ('last_modified',)

    @property
    def suggest_type_label(self):
        return self._meta.model_name

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def html_str(self):
        return self.__str__()


class HostPlantTaxonomicModel(CommonTaxonomicModel):
    verbatim_id = get_verbatim_id_field()

    class Meta:
        abstract = True


class Substrate(models.Model):
    name = models.CharField(max_length=255)

    lepidoptera_species = models.ManyToManyField('Species', through='Observation')

    def html_str(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('substrate_page', kwargs={'substrate_id': str(self.id)})

    @property
    def suggest_type_label(self):
        return "substrate"


class TaxonomicModel(CommonTaxonomicModel):
    """Common ground between all taxon-related models (for Lepidoptera)."""
    @staticmethod
    def get_synonym_of_field():
        return models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='synonyms')

    class Meta:
        abstract = True

    # Common fields
    author = models.CharField(max_length=255)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    text = MarkdownxField(blank=True)

    display_order = models.IntegerField(unique=True)

    @property
    def all_parents(self):
        # Models subclassing must implement a .parent property (that returns None if top of the tree)
        parents = []
        model_instance = self.parent
        while model_instance is not None:
            parents = [model_instance] + parents
            model_instance = model_instance.parent
        return parents

    @property
    def all_parents_and_me(self):
        return self.all_parents + [self]

    @property
    def admin_change_url(self):
        return reverse('admin:{app_label}_{model_name}_change'.format(app_label=self._meta.app_label,
                                                                      model_name=self._meta.model_name),
                       args=(self.pk,))


class Family(DisplayOrderNavigable, TaxonomicModel):
    # Synonyms currently disabled at the family level since:
    #   - we have no data for now
    #   - this makes implementation a bit more complex (public-facing pages, validation, foreign key to self, ...)
    #   - See genus for a full implementation
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_FAMILY]

    verbatim_family_id = get_verbatim_id_field()

    representative_picture = models.ImageField(blank=True, null=True, upload_to='family_representative_pictures')
    representative_picture_thumbnail = ImageSpecField(source='representative_picture',
                                                      processors=[ResizeToFit(640, 480)],
                                                      format='JPEG',
                                                      options={'quality': 95})

    objects = models.Manager()
    valid_families_objects = ValidFamiliesManager()

    @property
    def species_count(self):
        count = 0

        for subfamily in self.subfamily_set.all():
            count = count + subfamily.species_count

        for genus in self.genus_set.all():
            count = count + genus.species_count

        return count

    def get_absolute_url(self):
        return reverse('family_page', kwargs={'family_id': str(self.id)})

    @property
    def all_species(self):
        return self.species_thru_subfamily.union(self.species_thru_genus)

    @property
    def species_thru_genus(self):
        qs = Species.objects.none()
        for genus in self.genus_set.all():
            qs = qs.union(genus.all_species)
        return qs

    @property
    def species_thru_subfamily(self):
        qs = Species.objects.none()
        for subfamily in self.subfamily_set.all():
            qs = qs.union(subfamily.all_species)
        return qs

    @property
    def parent(self):
        return None  # Top of the tree

    class Meta:
        verbose_name_plural = "families"


class Subfamily(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SUBFAMILY]

    verbatim_subfamily_id = get_verbatim_id_field()

    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    @property
    def species_count(self):
        count = 0

        for tribus in self.tribus_set.all():
            count = count + tribus.species_count

        for genus in self.genus_set.all():
            count = count + genus.species_count

        return count

    def get_absolute_url(self):
        return reverse('subfamily_page', kwargs={'subfamily_id': str(self.id)})

    @property
    def parent(self):
        return self.family

    @property
    def all_species(self):
        return self.species_thru_tribus.union(self.species_thru_genus)

    @property
    def species_thru_tribus(self):
        qs = Species.objects.none()
        for tribus in self.tribus_set.all():
            qs = qs.union(tribus.all_species)
        return qs

    @property
    def species_thru_genus(self):
        qs = Species.objects.none()
        for genus in self.genus_set.all():
            qs = qs.union(genus.all_species)
        return qs

    class Meta:
        verbose_name_plural = "subfamilies"


class Tribus(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_TRIBUS]

    verbatim_tribus_id = get_verbatim_id_field()

    subfamily = models.ForeignKey(Subfamily, on_delete=models.CASCADE)

    @property
    def species_count(self):
        count = 0
        for genus in self.genus_set.all():
            count = count + genus.species_count
        return count

    def get_absolute_url(self):
        return reverse('tribus_page', kwargs={'tribus_id': str(self.id)})

    @property
    def parent(self):
        return self.subfamily

    @property
    def all_species(self):
        return self.species_thru_genus

    @property
    def species_thru_genus(self):
        qs = Species.objects.none()
        for genus in self.genus_set.all():
            qs = qs.union(genus.all_species)
        return qs

    class Meta:
        verbose_name_plural = "tribus"


class Genus(ParentForAdminListMixin, TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_GENUS, Status.VERBATIM_ID_GENUS_SYNONYM, Status.UNKNOWN]

    verbatim_genus_id = get_verbatim_id_field()

    # Sometimes a genus appears under a tribu, but sometimes only under a subfamily or a family...
    # One and only one of those can be filled
    tribus = models.ForeignKey(Tribus, null=True, blank=True, on_delete=models.CASCADE)
    subfamily = models.ForeignKey(Subfamily, null=True, blank=True, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, null=True, blank=True, on_delete=models.CASCADE)

    synonym_of = TaxonomicModel.get_synonym_of_field()

    # Managers:
    objects = models.Manager()
    accepted_objects = AcceptedGenusManager()
    synonym_objects = SynonymGenusManager()

    direct_species_count = CountField('species_set')

    @property
    def species_count(self):
        count = self.direct_species_count
        for subgenus in self.subgenus_set.all():
            count = count + subgenus.species_count
        return count

    def get_absolute_url(self):
        return reverse('genus_page', kwargs={'genus_id': str(self.id)})

    @property
    def direct_species(self):
        """Return species directly linked to this genus"""
        return self.species_set.all()

    @property
    def all_species(self):
        return self.direct_species.union(self.species_thru_subgenus)

    @property
    def species_thru_subgenus(self):
        qs = Species.objects.none()
        for subgenus in self.subgenus_set.all():
            qs = qs.union(subgenus.all_species)
        return qs

    class Meta:
        verbose_name_plural = "genera"

    @property
    def parent(self):
        # Return the most direct parent
        return self.tribus or self.subfamily or self.family

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
        # Let's make sure model.clean() is called on each save (enable validation also for import script)
        self.full_clean()
        return super(Genus, self).save(*args, **kwargs)


class Subgenus(TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SUBGENUS]

    verbatim_subgenus_id = get_verbatim_id_field()

    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)

    species_count = CountField('species_set')

    def get_absolute_url(self):
        return reverse('subgenus_page', kwargs={'subgenus_id': str(self.id)})

    @denormalized(models.CharField, max_length=255)
    @depend_on_related('Genus')
    def genus_name(self):
        return self.genus.name

    @property
    def parent(self):
        return self.genus

    @property
    def all_species(self):
        return self.direct_species

    @property
    def direct_species(self):
        return self.species_set.all()

    class Meta:
        verbose_name_plural = "subgenera"


def validate_only_numbers_and_uppercase(value):
    if not all(c.isdigit() or c.isupper() for c in value):
        raise ValidationError("The code can only contains numbers and uppercase letters")


class Photographer(models.Model):
    full_name = models.CharField(max_length=100)

    verbatim_photographer_id = get_verbatim_id_field()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('full_name', )


class SpeciesPicture(models.Model):
    # See "Picture naming conventions.pdf" in source data Git repository.

    # Picture subject
    MUSEUM_SPECIMEN = 'MUSEUM_SPECIMEN'
    IN_VIVO_SPECIMEN = 'IN_VIVO_SPECIMEN'
    PRE_ADULT_STAGE = 'PRE_ADULT_STAGE'
    HOST_PLANT = 'HOST_PLANT'
    BIONOMICS = 'BIONOMICS'
    HABITAT = 'HABITAT'

    SUBJECT_CHOICES = (
        (MUSEUM_SPECIMEN, 'Museum specimen'),
        (IN_VIVO_SPECIMEN, 'In Vivo Specimen'),
        (PRE_ADULT_STAGE, 'Pre-adult stage'),
        (HOST_PLANT, 'Host plant'),
        (BIONOMICS, 'Bionomics'),
        (HABITAT, 'Habitat')
    )

    # Specimen stages
    IMAGO = 'i'  # Meaning adult, with wings

    # Pre-adult stages
    EGG = 'e'
    LARVA = 'l'
    CASE = 'c'
    BAG = 'b'
    MINE = 'm'
    PUPA = 'p'

    STAGES_CHOICES = (
        (IMAGO, 'Imago'),
        (EGG, 'Egg'),
        (LARVA, 'Larva'),
        (CASE, 'Case'),
        (BAG, 'Bag'),
        (MINE, 'Mine'),
        (PUPA, 'Pupa/Cocoon')
    )

    # Specimen Sex
    MALE = 'M'
    FEMALE = 'F'
    ADULT = 'A'  # Unsure M or F

    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (ADULT, 'Adult')
    )

    # Picture orientation/side
    UPPER = 'UPPER'
    UNDER = 'UNDER'

    ORIENTATION_CHOICES = (
        (UPPER, 'Upper'),
        (UNDER, 'Under')
    )

    # Fields
    species = models.ForeignKey('Species', on_delete=models.CASCADE)
    photographer = models.ForeignKey('Photographer', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to='specimen_pictures')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFit(320, 240)],
                                     format='JPEG',
                                     options={'quality': 95})
    image_admin_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFit(100, 75)],
                                     format='JPEG',
                                     options={'quality': 90})

    image_subject = models.CharField(blank=False, max_length=20, choices=SUBJECT_CHOICES)

    verbatim_image_filename = models.CharField(max_length=255)
    specimen_stage = models.CharField(max_length=1, blank=True, choices=STAGES_CHOICES)
    specimen_sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES)
    side = models.CharField(max_length=5, blank=True, choices=ORIENTATION_CHOICES)

    gallery_order = models.IntegerField(help_text="Order in various galleries. Smaller numbers comes first!")

    def html_metadata(self):
        entries = []
        if self.image_subject:
            entries.append("<b>Subject</b>: {}".format(self.get_image_subject_display()))
        if self.specimen_stage:
            entries.append("<b>Stage</b>: {}".format(self.get_specimen_stage_display()))
        if self.specimen_sex:
            entries.append("<b>Sex</b>: {}".format(self.get_specimen_sex_display()))
        if self.side:
            entries.append("<b>Side</b>: {}".format(self.get_side_display()))

        s = ','.join(entries)

        if self.photographer:
            s = "<b>© {}</b><br/>".format(self.photographer.full_name) + s

        return s

SPECIES_PAGE_SECTIONS = {
        'imago': {
            'display_name': 'Imago',
            'text_field_name': 'imago_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.IMAGO}
        },

        'egg': {
            'display_name': 'Egg',
            'text_field_name': 'egg_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.EGG}
        },

        'larva': {
            'display_name': 'Caterpillar',
            'text_field_name': 'larva_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.LARVA}
        },

        'case': {
            'display_name': 'Case',
            'text_field_name': 'case_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.CASE}
        },

        'bag': {
            'display_name': 'Bag',
            'text_field_name': 'bag_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.BAG}
        },

        'mine': {
            'display_name': 'Mine',
            'text_field_name': 'mine_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.MINE}
        },

        'cocoon': {
            'display_name': 'Cocoon/pupa',
            'text_field_name': 'cocoon_section_text',
            'picture_filters': {'specimen_stage': SpeciesPicture.PUPA}
        },

        'bionomics': {
            'display_name': 'Bionomics',
            'text_field_name': 'bionomics_section_text',
            'picture_filters': {'image_subject': SpeciesPicture.BIONOMICS}
        },

        'habitat': {
            'display_name': 'Habitat',
            'text_field_name': 'habitat_section_text',
            'picture_filters': {'image_subject': SpeciesPicture.HABITAT}
        },

    }


class Species(ParentForAdminListMixin, TaxonomicModel):
    ALLOWED_VERBATIM_STATUS_IDS = [Status.VERBATIM_ID_VALID_SPECIES, Status.VERBATIM_ID_SPECIES_SYNONYM]

    verbatim_species_number = get_verbatim_id_field()
    code = models.CharField(verbose_name='Species code', max_length=50, unique=True, validators=[
        validate_only_numbers_and_uppercase,
        MinLengthValidator(4)
    ])

    synonym_of = TaxonomicModel.get_synonym_of_field()

    # Parents: sometimes a genus, sometimes a subgenus
    subgenus = models.ForeignKey(Subgenus, null=True, blank=True, on_delete=models.CASCADE)
    genus = models.ForeignKey(Genus, null=True, blank=True, on_delete=models.CASCADE)

    # The source database contains much more (currently unused) fields, mostly text, that we decide to ignore for
    # now (focus first on taxonomy, and keep things as simple as possible)

    # Managers:
    objects = SpeciesManager()
    accepted_objects = AcceptedSpeciesManager()
    synonym_objects = SynonymSpeciesManager()

    # Publication where the species was first described in Belgium
    first_mention_publication = models.ForeignKey('Publication', null=True, blank=True, on_delete=models.CASCADE,
                                                  verbose_name='publication')
    first_mention_page = models.CharField(max_length=100, blank=True, verbose_name='page')
    first_mention_link = models.URLField(blank=True, verbose_name='hyperlink')

    imago_section_text = MarkdownxField(blank=True)
    larva_section_text = MarkdownxField(blank=True)
    egg_section_text = MarkdownxField(blank=True)
    case_section_text = MarkdownxField(blank=True)
    bag_section_text = MarkdownxField(blank=True)
    mine_section_text = MarkdownxField(blank=True)
    cocoon_section_text = MarkdownxField(blank=True)
    bionomics_section_text = MarkdownxField(blank=True)
    habitat_section_text = MarkdownxField(blank=True)

    def has_content_for_section(self, section_name):
        if section_name in SPECIES_PAGE_SECTIONS:  # Plausible requested section.

            # We have a section for a species if we have either text or pictures for it
            if (self.get_text_for_section(section_name) != '') or (self.get_pictures_for_section(section_name).count() > 0):
                return True

        return False

    def get_text_for_section(self, section_name):
        return getattr(self, SPECIES_PAGE_SECTIONS[section_name]['text_field_name'])

    def get_pictures_for_section(self, section_name):
        qs = SpeciesPicture.objects.filter(species=self).order_by('gallery_order')
        qs = qs.filter(**SPECIES_PAGE_SECTIONS[section_name]['picture_filters'])

        return qs

    def get_absolute_url(self):
        return reverse('species_page', kwargs={'species_id': str(self.id)})

    @property
    def family(self):
        for taxon in self.all_parents:
            if taxon.__class__.__name__ == 'Family':
                return taxon

    @property
    def binomial_name(self):
        return '{genus} {specific_epithet}'.format(genus=self.genus_name, specific_epithet=self.name)

    @denormalized(models.CharField, max_length=255)
    @depend_on_related('Genus')
    @depend_on_related('Subgenus')
    def genus_name(self):
        # Sometimes we need to go through subgenus to get it, sometimes it's directly available
        if self.genus:
            return self.genus.name
        else:
            return self.subgenus.genus_name

    def __str__(self):
        return self.binomial_name

    def html_str(self):
        return format_html("<i>{}</i>", self.__str__() )

    @property
    def parent(self):
        # Return the most direct parent
        return self.subgenus or self.genus

    def clean(self):
        errors_dics = {}  # we aggregate errors for a complete output

        # Should be linked to either a subgenus or a genus, not both
        fields = [self.subgenus, self.genus]
        if len([field for field in fields if field is not None]) != 1:
            errors_dics['subgenus'] = ValidationError('Choose a subgenus OR a genus', code='invalid')
            errors_dics['genus'] = ValidationError('Choose a subgenus OR a genus', code='invalid')

        # Synonym: we should know whom
        if (self.status == Status.objects.get(verbatim_status_id=Status.VERBATIM_ID_SPECIES_SYNONYM)
                and not self.synonym_of):
            errors_dics['synonym_of'] = ValidationError('If status=synonym, this field is mandatory')

        # Accepted: synonym doesn't make any sense
        if (self.status == Status.objects.get(verbatim_status_id=Status.VERBATIM_ID_VALID_SPECIES)
                and self.synonym_of):
            errors_dics['synonym_of'] = ValidationError('If status=accepted, this field shouldn\'t be used')

        if errors_dics:
            raise ValidationError(errors_dics)

    def save(self, *args, **kwargs):
        # Let's make sure model.clean() is called on each save (enable validation also for import script)
        self.full_clean()
        return super(Species, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "species"


class HostPlantFamily(HostPlantTaxonomicModel):
    class Meta:
        verbose_name_plural = "Host plant families"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('hostplant_family_page', kwargs={'family_id': str(self.id)})

    @property
    def suggest_type_label(self):
        return 'host plant species'


class HostPlantGenus(HostPlantTaxonomicModel):
    family = models.ForeignKey(HostPlantFamily, on_delete=models.CASCADE)
    author = models.CharField(max_length=255, blank=True)

    lepidoptera_species = models.ManyToManyField(Species, through='Observation')

    def get_absolute_url(self):
        return reverse('hostplant_genus_page', kwargs={'genus_id': str(self.id)})

    @property
    def suggest_type_label(self):
        return 'host plant genus'

    class Meta:
        verbose_name_plural = "Host plant genera"
        ordering = ['name']


class HostPlantSpecies(HostPlantTaxonomicModel):
    author = models.CharField(max_length=255, blank=True)
    genus = models.ForeignKey(HostPlantGenus, on_delete=models.CASCADE)

    lepidoptera_species = models.ManyToManyField(Species, through='Observation')

    @property
    def suggest_type_label(self):
        return 'host plant species'

    def get_absolute_url(self):
        return reverse('hostplant_species_page', kwargs={'species_id': str(self.id)})

    class Meta:
        verbose_name_plural = "Host plant species"
        ordering = ['name']

    def __str__(self):
        return "{} {}".format(self.genus.name, self.name)

    def html_str(self):
        return format_html("<i>{}</i>", self.__str__() )


class Observation(models.Model):
    """A (lepidoptera) species has been seen on either a plant species, either a plant genus, or a Substrate"""
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    plant_species = models.ForeignKey(HostPlantSpecies, blank=True, null=True, on_delete=models.CASCADE)
    plant_genus = models.ForeignKey(HostPlantGenus, blank=True, null=True, on_delete=models.CASCADE)
    substrate = models.ForeignKey(Substrate, blank=True, null=True, on_delete= models.CASCADE)

    def clean(self):
        errors = {}  # we aggregate errors for a complete output

        # Should be linked to either a plant species, a plant genus or a substrate
        fields = [self.plant_species_id, self.plant_genus_id, self.substrate_id]
        if len([field for field in fields if field is not None]) != 1:
            msg = 'Choose a plant species OR a genus OR a substrate'
            errors['plant_species'] = ValidationError(msg, code='invalid')
            errors['plant_genus'] = ValidationError(msg, code='invalid')
            errors['substrate'] = ValidationError(msg, code='invalid')

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Let's make sure model.clean() is called on each save (enable validation also for import script)
        self.full_clean()
        return super(Observation, self).save(*args, **kwargs)


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

    def __str__(self):
        return self.name


class TimePeriod(models.Model):
    BEFORE_1980_NAME = 'Before 1980'
    BETWEEN_1980_2004_NAME = '1980-2004'
    SINCE_2004_NAME = 'After 2004'

    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='time_period_icons')

    def __str__(self):
        return self.name


class SpeciesPresence(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('species', 'province', 'period')


class Journal(models.Model):
    verbatim_id = get_verbatim_id_field()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Publication(models.Model):
    verbatim_id = get_verbatim_id_field()
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    publisher = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=20)
    volume = models.CharField(max_length=20)
    issue = models.CharField(max_length=20, blank=True)
    page_numbers = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.title, self.author, self.year)

    class Meta:
        ordering = ['title']


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
