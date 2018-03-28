from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import Family, Subfamily, Tribus, Genus, Subgenus, Species, HostPlantFamily, HostPlantGenus, \
    HostPlantSpecies


class TaxonomicTranslatableModel(TranslationOptions):
    fields = ('vernacular_name',)


class HasTranslatableTextField(TranslationOptions):
    fields = ("text", )


@register(Family)
class FamilyTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
    pass


@register(Subfamily)
class SubfamilyTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
    pass


@register(Tribus)
class TribusTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
    pass


@register(Genus)
class GenusTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
    pass


@register(Subgenus)
class SubgenusTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
    pass


@register(Species)
class SpeciesTranslationOptions(TaxonomicTranslatableModel, HasTranslatableTextField):
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
