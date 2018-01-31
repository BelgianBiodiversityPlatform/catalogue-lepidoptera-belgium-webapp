from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext as _

from modeltranslation.admin import TranslationAdmin
from markdownx.admin import MarkdownxModelAdmin

from .models import Family, Species, Province, TimePeriod, SpeciesPresence, PageFragment, Status

admin.site.site_header = '{} - Administration interface'.format(settings.WEBSITE_NAME)


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


@admin.register(Family)
class FamilyAdmin(TranslationAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = Status.objects.filter(verbatim_status_id__in=Family.ALLOWED_VERBATIM_STATUS_IDS)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    readonly_fields = ('verbatim_family_id', )

    list_display = ('display_order', 'name', 'author', 'status')

    list_filter = [RepresentativePictureNotNullFilter]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('order', 'code', 'name', 'historical', 'recent', 'polygon_reference')


@admin.register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(SpeciesPresence)
class SpeciesPresencePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    readonly_fields = ('verbatim_status_id',)


class PageFragmentAdmin(MarkdownxModelAdmin):
    list_display = ('identifier', 'content_en', 'content_nl', 'content_de', 'content_fr')


admin.site.register(PageFragment, PageFragmentAdmin)