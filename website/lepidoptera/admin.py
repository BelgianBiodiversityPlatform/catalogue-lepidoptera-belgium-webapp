from django.conf import settings
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from markdownx.admin import MarkdownxModelAdmin

from .models import Family, Species, Province, TimePeriod, SpeciesPresence, PageFragment, Status

admin.site.site_header = '{} - Administration interface'.format(settings.WEBSITE_NAME)


@admin.register(Family)
class FamilyAdmin(TranslationAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = Status.objects.filter(pk__in=Family.ALLOWED_STATUS_IDS)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    readonly_fields = ('verbatim_family_id', )
    list_display = ('name', 'author', 'status')


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