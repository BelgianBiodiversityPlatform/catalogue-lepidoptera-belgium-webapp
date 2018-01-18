from django import template
from django.utils.safestring import mark_safe

from lepidoptera.models import PageFragment
from markdownx.utils import markdownify

register = template.Library()


@register.simple_tag(takes_context=True)
def get_page_fragment(context, identifier):
    """Return rendered HTML for the page frament with identifier, in the current language"""

    fragment = PageFragment.objects.get(identifier=identifier)
    field_name = 'content_{}'.format(context.request.LANGUAGE_CODE)

    return mark_safe(markdownify(getattr(fragment, field_name)))
