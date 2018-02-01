from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import Family, Subfamily


@register(Family)
class FamilyTranslationOptions(TranslationOptions):
    fields = ('vernacular_name',)


@register(Subfamily)
class SubfamilyTranslationOptions(TranslationOptions):
    fields = ('vernacular_name',)
