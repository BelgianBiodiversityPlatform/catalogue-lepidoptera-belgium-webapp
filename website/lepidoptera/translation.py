from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import Family, Subfamily, Tribus, Genus


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
