from django import template

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__


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
