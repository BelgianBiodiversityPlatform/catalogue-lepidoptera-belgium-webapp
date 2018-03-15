from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import Family, Subfamily, Tribus, Genus, Subgenus, Species, HostPlantFamily, HostPlantGenus, \
    HostPlantSpecies


class TaxonomicTranslatableModel(TranslationOptions):
    fields = ('vernacular_name',)


@register(Family)
class FamilyTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(Subfamily)
class SubfamilyTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(Tribus)
class TribusTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(Genus)
class GenusTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(Subgenus)
class SubgenusTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(Species)
class SpeciesTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(HostPlantFamily)
class HostPlantFamilyTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(HostPlantGenus)
class HostPlantGenusTranslationOptions(TaxonomicTranslatableModel):
    pass


@register(HostPlantSpecies)
class HostPlantSpeciesTranslationOptions(TaxonomicTranslatableModel):
    pass
