from django import template
from django.template import TemplateSyntaxError
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from lepidoptera.models import SpeciesPresence, SPECIES_PAGE_SECTIONS

register = template.Library()


@register.filter
def valid_taxa(value):
    """Given a queryset of taxa, filters so only valid taxa stays"""
    return [taxon for taxon in value if taxon.is_valid]


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


def _field_in_all_available_languages(languages, model, field_name):
    """Returns a list of dict"""
    l = []

    for lang in languages:
        lang_code = lang[0]
        localized_field_name = '{field_name}_{lang_code}'.format(field_name=field_name, lang_code=lang_code)
        field_value = getattr(model, localized_field_name)

        if field_value:
            l.append({'code': lang_code.upper(), 'value': field_value})

    return l

@register.simple_tag
def field_in_all_available_languages(languages, model, field_name):
    """Return something such as 'Speckled Wood (EN), Bont zandoogje (NL)'"""
    s = ''

    for entry in _field_in_all_available_languages(languages, model, field_name):
        s = s + '{field_value} ({lang_code}), '.format(field_value=entry['value'], lang_code=entry['code'])

    if s == '':
        return '/'

    return s[:-2]  # Drop the remaining ' ,'


@register.filter
def markdown(value, arg=None):
    return mark_safe(markdownify(value))


@register.filter
def has_content_for_section(species, section_name):
    return species.has_content_for_section(section_name)


@register.filter
def get_text_for_section(species, section_name):
    return species.get_text_for_section(section_name)


class SectionPicsNode(template.Node):
    def __init__(self, species, section_name, var_name='pics'):
        self.species = template.Variable(species)
        self.section_name = template.Variable(section_name)
        self.var_name = var_name

    def render(self, context):
        species = self.species.resolve(context)
        section_name = self.section_name.resolve(context)

        context[self.var_name] = species.get_pictures_for_section(section_name)
        return ''


@register.tag(name='section_pics')
def do_section_pics(parser, token):
    error = False
    try:
        tag_name, species, section_name, _as, var_name = token.split_contents()
        if _as != 'as':
            error = True
    except:
        error = True

    if error:
        raise(TemplateSyntaxError,
              'section_pics must be of the form, "section_pics <species> <section_name> as <var_name>"')
    else:
        return SectionPicsNode(species, section_name, var_name)


@register.simple_tag
def section_display_name(section_name):
    return mark_safe(SPECIES_PAGE_SECTIONS[section_name]['display_name'])