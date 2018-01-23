from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from lepidoptera.models import PageFragment
from markdownx.utils import markdownify

register = template.Library()


def _get_field_name(language_code):
    return 'content_{}'.format(language_code)


@register.simple_tag(takes_context=True)
def get_page_fragment(context, identifier):
    """Return rendered HTML for the page frament with identifier, in the current language"""

    fragment = PageFragment.objects.get(identifier=identifier)

    # We try to get the content in the request language, but fallback to PAGE_FRAGMENT_FALLBACK_LANGUAGE if no
    # translation exists
    translated_content = getattr(fragment,  _get_field_name(context.request.LANGUAGE_CODE))
    if translated_content == '':
        translated_content = getattr(fragment, _get_field_name(settings.PAGE_FRAGMENT_FALLBACK_LANGUAGE ))

    return mark_safe(markdownify(translated_content))
