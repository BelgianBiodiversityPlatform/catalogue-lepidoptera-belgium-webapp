from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from lepidoptera.models import Species

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.simple_tag
def species_presence_icon(species_pk, province_code):
    presences_strings = []

    for presence in Species.objects.get(pk=species_pk).speciespresence_set.filter(province__code=province_code):
        presences_strings.append(presence.period.name)

    return ', '.join(presences_strings)

@register.simple_tag
def field_in_all_available_languages(languages, model, field_name):
    """Return something such as 'Speckled Wood (en), Bont zandoogje (nl)'"""
    s = ''

    for lang in languages:
        lang_code = lang[0]
        localized_field_name = '{field_name}_{lang_code}'.format(field_name=field_name, lang_code=lang_code)
        field_value = getattr(model, localized_field_name)

        if field_value:
            s = s + '{field_value} ({lang_code}), '.format(field_value=field_value, lang_code=lang_code)

    if s == '':
        return '/'

    return s[:-2]  # Drop the remaining ' ,'


@register.filter()
def markdown(value, arg=None):
    return mark_safe(markdownify(value))