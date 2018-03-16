from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from lepidoptera.models import SpeciesPresence

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.simple_tag
def species_presence_icons(species_pk, province_id):
    presences = SpeciesPresence.objects.filter(species_id=species_pk, province_id=province_id).select_related('period')
    icon_urls = (presence.period.icon.url for presence in presences)

    imgs = ''
    for url in icon_urls:
        imgs = imgs + format_html("<img class=\"province-icon\" src=\"{0}\" />", url)

    return mark_safe(imgs)


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