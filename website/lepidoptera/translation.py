from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from .models import Family

@register(Family)
class FamilyTranslationOptions(TranslationOptions):
    fields = ('vernacular_name',)
