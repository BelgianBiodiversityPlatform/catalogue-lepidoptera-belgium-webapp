from django.conf import settings
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Family, Species, Province, TimePeriod, SpeciesPresence, PageFragment

admin.site.site_header = '{} - Administration interface'.format(settings.WEBSITE_NAME)

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    pass


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


class PageFragmentAdmin(MarkdownxModelAdmin):
    list_display = ('identifier', 'content_en', 'content_nl', 'content_de', 'content_fr')


admin.site.register(PageFragment, PageFragmentAdmin)