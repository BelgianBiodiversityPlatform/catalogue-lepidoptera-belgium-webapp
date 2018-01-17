from django.contrib import admin
from .models import Family, Species, Province, TimePeriod, SpeciesPresence


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
