from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from urllib.request import urlopen

from django.conf import settings
from django.contrib import admin
from django.core.files import File
from django.db.models import Q
from django.utils.translation import gettext as _

from modeltranslation.admin import TranslationAdmin
from markdownx.admin import MarkdownxModelAdmin

from lepidoptera.wikidata_utils import get_images_url_for_entity
from .models import Family, Subfamily, Tribus, Genus, Subgenus, Species, Province, TimePeriod, SpeciesPresence, \
    PageFragment, Status, Observation, HostPlantSpecies, HostPlantGenus, HostPlantFamily, Substrate, Journal, \
    Publication, SpeciesPicture

admin.site.site_header = '{} - Administration interface'.format(settings.WEBSITE_NAME)


def assign_picture_from_wikidata(modeladmin, request, queryset):
    for taxon in queryset:
        if taxon.wikidata_id:
            img_urls = get_images_url_for_entity(taxon.wikidata_id)
            if img_urls:
                img_url = img_urls[0]
                temp_img = NamedTemporaryFile(delete=True)
                temp_img.write(urlopen(img_url).read())
                temp_img.flush()
                filename_img = urlparse(img_url).path.split('/')[-1]
                taxon.representative_picture.save(filename_img, File(temp_img))
                taxon.save()


assign_picture_from_wikidata.short_description = (
    "Assign illustative picture from Wikidata (if available) to selected taxa"
)


class NotNullFilter(admin.SimpleListFilter):
    title = _('Filter title not set')

    parameter_name = 'parameter name not set'

    def lookups(self, request, model_admin):

        return (
            ('not_null', _('Not empty only')),
            ('null', _('Empty only')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'not_null':
            is_null_false = {
                self.parameter_name + "__isnull": False
            }
            exclude = {
                self.parameter_name: ""
            }
            return queryset.filter(**is_null_false).exclude(**exclude)

        if self.value() == 'null':
            is_null_true = {
                self.parameter_name + "__isnull": True
            }
            param_exact = {
                self.parameter_name + "__exact": ""
            }
            return queryset.filter(Q(**is_null_true) | Q(**param_exact))


class RepresentativePictureNotNullFilter(NotNullFilter):
    title = "representative picture"
    parameter_name = "representative_picture"


class LimitStatusChoiceMixin(object):
    """To avoid duplication: Mixin for ModelAdmin.

    If the model has a status field (FK to Status), limit choices to model.ALLOWED_VERBATIM_STATUS_IDS
    """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = Status.objects.filter(verbatim_status_id__in=self.model.ALLOWED_VERBATIM_STATUS_IDS)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SpeciesPresenceInline(admin.TabularInline):
    model = SpeciesPresence


class ObservationsInline(admin.TabularInline):
    model = Observation


class SpeciesPicturesInline(admin.TabularInline):
    model = SpeciesPicture


@admin.register(Family)
class FamilyAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_family_id', 'wikidata_id')

    list_display = ('display_order', 'name', 'author', 'text', 'wikidata_id')

    list_filter = [RepresentativePictureNotNullFilter]

    actions = [assign_picture_from_wikidata]


@admin.register(Subfamily)
class SubfamilyAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_subfamily_id', )

    list_display = ('display_order', 'name', 'family', 'author', 'status')

    list_filter = ['family']


@admin.register(Tribus)
class TribusAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_tribus_id', )

    list_display = ('display_order', 'name', 'subfamily', 'author', 'status')


@admin.register(Genus)
class GenusAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_genus_id', )

    list_display = ('display_order', 'name', 'parent_for_admin_list', 'tribus', 'author', 'status')

    fields = (('name', 'author'),
              ('status', 'synonym_of'),
              ('tribus', 'subfamily', 'family'),
              'vernacular_name',
              'text',
              'display_order',
              'verbatim_genus_id'
              )

    list_filter = (
        ('status', admin.RelatedOnlyFieldListFilter),
    )


@admin.register(Subgenus)
class SubgenusAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_subgenus_id', )

    list_display = ('display_order', 'name', 'genus', 'author', 'status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "genus":
            kwargs["queryset"] = Genus.objects.order_by('name')
        return super(SubgenusAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (('name', 'author'),
              'status',
              'genus',
              'vernacular_name',
              'text',
              'display_order',
              'verbatim_subgenus_id'
    )


@admin.register(Species)
class SpeciesAdmin(LimitStatusChoiceMixin, TranslationAdmin, MarkdownxModelAdmin):
    search_fields = ['name', 'code']

    readonly_fields = ('verbatim_species_number', 'binomial_name')

    list_display = ('display_order', 'code', 'name', 'parent_for_admin_list', 'author', 'status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "genus":
            kwargs["queryset"] = Genus.objects.order_by('name')

        if db_field.name == "subgenus":
            kwargs["queryset"] = Subgenus.objects.order_by('name')
        return super(SpeciesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (None, {
            'fields': ('verbatim_species_number',
                       'code',
                       ('name', 'author', 'binomial_name'),
                       ('status', 'synonym_of'),
                       ('subgenus', 'genus'),
                       'vernacular_name',
                       'text',

                       'larva_section_text',
                       'display_order')
        }),
        ('First mention in Belgium', {
            'fields': ('first_mention_publication', 'first_mention_page', 'first_mention_link')
        })
    )

    inlines = [SpeciesPresenceInline, ObservationsInline, SpeciesPicturesInline]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('order', 'code', 'name', 'historical', 'recent', 'polygon_reference')


@admin.register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(SpeciesPresence)
class SpeciesPresencePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('species', 'plant_species', 'plant_genus', 'substrate')


@admin.register(HostPlantSpecies)
class HostPlantSpeciesAdmin(TranslationAdmin):
    readonly_fields = ('verbatim_id', )


@admin.register(HostPlantGenus)
class HostPlantGenusAdmin(TranslationAdmin):
    readonly_fields = ('verbatim_id',)


@admin.register(HostPlantFamily)
class HostPlantFamilyAdmin(TranslationAdmin):
    readonly_fields = ('verbatim_id',)


@admin.register(Substrate)
class SubstrateAdmin(admin.ModelAdmin):
    pass


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    readonly_fields = ('verbatim_id', )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ('verbatim_id',)
    search_fields = ['title', ]

    list_display = ('title', 'author', 'journal')
    fields = (
        'author',
        'year',
        'title',
        'journal',
        'publisher',
        'volume',
        'issue',
        'page_numbers',

        'verbatim_id'
    )


@admin.register(PageFragment)
class PageFragmentAdmin(MarkdownxModelAdmin):
    list_display = ('identifier', 'content_en', 'content_nl', 'content_de', 'content_fr')


@admin.register(SpeciesPicture)
class SpeciesPictureAdmin(admin.ModelAdmin):
    list_display = ('species', 'image_subject', 'specimen_stage', 'specimen_sex', 'side')

    readonly_fields = ('verbatim_image_filename',)

    list_filter = ['image_subject']