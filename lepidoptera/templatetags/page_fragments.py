from django import template
from django.utils.safestring import mark_safe

from lepidoptera.models import PageFragment
from markdownx.utils import markdownify

register = template.Library()


def _get_field_name(language_code):
    return 'content_{}'.format(language_code)


@register.simple_tag(takes_context=True)
def get_page_fragment(context, identifier):
    """Return rendered HTML for the page fragment with identifier, in the current language"""

    fragment = PageFragment.objects.get(identifier=identifier)

    return mark_safe(markdownify(fragment.get_content_in(context.request.LANGUAGE_CODE)))  # nosec
