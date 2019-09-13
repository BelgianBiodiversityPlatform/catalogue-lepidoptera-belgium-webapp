from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from imagekit.admin import AdminThumbnail
from markdownx import models

from modeltranslation.admin import TranslationAdmin
from markdownx.admin import MarkdownxModelAdmin

from lepidoptera.templates.widgets import LepidopteraAdminMarkdownxWidget
from .models import Family, Subfamily, Tribus, Genus, Subgenus, Species, Province, TimePeriod, SpeciesPresence, \
    PageFragment, HostPlantSpecies, HostPlantGenus, HostPlantFamily, Substrate, Journal, Publication, SpeciesPicture, \
    Photographer, PlantSpeciesObservation, PlantGenusObservation, SubstrateObservation

admin.site.site_header = '{} - Administration interface'.format(settings.WEBSITE_NAME)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """
    ModelAdmin class that prevents modifications through the admin.
    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    Source: https://gist.github.com/aaugustin/1388243
    """
    actions = None

    # We cannot call super().get_fields(request, obj) because that method calls
    # get_readonly_fields(request, obj), causing infinite recursion. Ditto for
    # super().get_form(request, obj). So we  assume the default ModelForm.
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them.
    def has_change_permission(self, request, obj=None):
        return (request.method in ['GET', 'HEAD'] and
                super().has_change_permission(request, obj))

    def has_delete_permission(self, request, obj=None):
        return False


class MyMarkdownxModelAdmin(MarkdownxModelAdmin):
    # Smaller widget
    formfield_overrides = {
        models.MarkdownxField: {'widget': LepidopteraAdminMarkdownxWidget(attrs={'rows': 5, 'cols': 40})},
    }


class SaveAndViewOnSiteMixin(object):
    class Media:
        js = (
            'lepidoptera/shortcut.js',  # app static folder
        )

    change_form_template = "lepidoptera/admin/change_form_save_view_on_site.html"

    def response_change(self, request, obj):
        res = super(SaveAndViewOnSiteMixin, self).response_change(request, obj)
        if "_save_and_view" in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            return res

    def response_add(self, request, obj, post_url_continue=None):
        res = super(SaveAndViewOnSiteMixin, self).response_add(request, obj, post_url_continue)
        if "_save_and_view" in request.POST:
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            return res


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


class SpeciesPresenceInline(admin.TabularInline):
    model = SpeciesPresence


class PlantSpeciesObservationsInline(SortableTabularInline):
    model = PlantSpeciesObservation


class PlantGenusObservationsInline(SortableTabularInline):
    model = PlantGenusObservation


class SubstratesObservationsInline(SortableTabularInline):
    model = SubstrateObservation


class SpeciesPicturesInline(admin.TabularInline):
    model = SpeciesPicture
    ordering = ['image_subject', 'specimen_stage', 'gallery_order']
    readonly_fields = ('verbatim_image_filename', 'thumbnail')
    extra = 1

    thumbnail = AdminThumbnail(image_field='image_admin_thumbnail', template='lepidoptera/imagekit/admin/thumbnail.html')

    fields = ('thumbnail', 'photographer', 'image', 'image_subject', 'specimen_stage', 'specimen_sex', 'side',
              'gallery_order', 'date', 'locality', 'comment', 'verbatim_image_filename')

    formfield_overrides = {
        models.MarkdownxField: {'widget': LepidopteraAdminMarkdownxWidget(attrs={'rows': 3, 'cols': 10})},
    }


class MyLogEntryAdmin(ReadOnlyModelAdmin):
    list_display = ('__str__', 'user', 'action_time')


admin.site.register(LogEntry, MyLogEntryAdmin)


def is_synonym(taxon):
    return taxon.is_synonym
is_synonym.short_description = 'Is a synonym?'
is_synonym.boolean = True


@admin.register(Family)
class FamilyAdmin(SaveAndViewOnSiteMixin,TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_family_id', 'wikidata_id')

    list_display = ('display_order', 'name', 'author', 'text', 'wikidata_id')

    list_filter = [RepresentativePictureNotNullFilter]


@admin.register(Subfamily)
class SubfamilyAdmin(SaveAndViewOnSiteMixin, TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_subfamily_id', )

    list_display = ('display_order', 'name', 'family', 'author')

    list_filter = ['family']


@admin.register(Tribus)
class TribusAdmin(SaveAndViewOnSiteMixin, TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_tribus_id', )

    list_display = ('display_order', 'name', 'subfamily', 'author')


@admin.register(Genus)
class GenusAdmin(SaveAndViewOnSiteMixin, TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_genus_id', )

    list_display = ('display_order', 'name', 'parent_for_admin_list', 'tribus', 'author', is_synonym)

    fields = (('name', 'author'),
              'synonym_of',
              ('tribus', 'subfamily', 'family'),
              'display_order',
              'vernacular_name',
              'text',
              'verbatim_genus_id'
              )


@admin.register(Subgenus)
class SubgenusAdmin(SaveAndViewOnSiteMixin, TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name']

    readonly_fields = ('verbatim_subgenus_id', )

    list_display = ('display_order', 'name', 'genus', 'author')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "genus":
            kwargs["queryset"] = Genus.objects.order_by('name')
        return super(SubgenusAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (('name', 'author'),
              'genus',
              'display_order',
              'vernacular_name',
              'text',
              'verbatim_subgenus_id'
    )


@admin.register(Species)
class SpeciesAdmin(NonSortableParentAdmin, SaveAndViewOnSiteMixin, TranslationAdmin, MyMarkdownxModelAdmin):
    search_fields = ['name', 'code']

    readonly_fields = ('verbatim_species_number', 'binomial_name')

    list_display = ('display_order', 'code', 'name', 'parent_for_admin_list', 'author', is_synonym)
    list_filter = ('establishment_means',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(SpeciesAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['display_order'].widget.attrs['style'] = 'width: 20em;'
        return form

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
                       'synonym_of',
                       ('subgenus', 'genus'),
                       'display_order',
                       ('establishment_means', 'establishment_date', 'establishment_remarks'),
                       'vernacular_name',
                       'text',

                       'imago_section_text',
                       'genitalia_section_text',
                       'egg_section_text',
                       'larva_section_text',
                       'case_section_text',
                       'bag_section_text',
                       'mine_section_text',
                       'cocoon_section_text',
                       'bionomics_section_text',
                       'habitat_section_text',
                       'hostplants_section_text',
                       'flightperiod_section_text')
        }),
        ('First mention in Belgium', {
            'fields': ('first_mention_publication', 'first_mention_page', 'first_mention_link')
        })
    )

    inlines = [SpeciesPresenceInline, PlantSpeciesObservationsInline, PlantGenusObservationsInline,
               SubstratesObservationsInline, SpeciesPicturesInline]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('order', 'code', 'name', 'historical', 'recent', 'polygon_reference')


@admin.register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(SpeciesPresence)
class SpeciesPresencePeriodAdmin(admin.ModelAdmin):
    pass


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
    readonly_fields = ('verbatim_id', 'markdown_reference')
    search_fields = ['title', 'author']

    list_display = ('author', 'year', 'title', 'journal')
    fields = (
        'markdown_reference',
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
class PageFragmentAdmin(MyMarkdownxModelAdmin):
    list_display = ('identifier', 'content_en', 'content_nl', 'content_de', 'content_fr')


@admin.register(SpeciesPicture)
class SpeciesPictureAdmin(MyMarkdownxModelAdmin):
    list_display = ('gallery_order', 'thumbnail', 'link_to_species', 'image_subject', 'specimen_stage', 'specimen_sex',
                    'side')

    def link_to_species(self, obj):
        link = reverse("admin:lepidoptera_species_change", args=[obj.species.id])
        return format_html('<a href="{}">{} (edit)</a>', link, obj.species.html_str())

    link_to_species.short_description = 'Species'

    thumbnail = AdminThumbnail(image_field='image_admin_thumbnail')

    readonly_fields = ('verbatim_image_filename',)

    list_filter = ['image_subject', 'specimen_stage']


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    readonly_fields = ('verbatim_photographer_id',)
