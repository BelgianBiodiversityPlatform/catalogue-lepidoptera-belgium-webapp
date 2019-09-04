from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

from lepidoptera.models import Publication


class PublicationsInlineProcessor(InlineProcessor):
    @staticmethod
    def _tooltip_html_content(publication_markdwon_reference):
        try:
            pub = Publication.objects.get(markdown_reference=publication_markdwon_reference)
        except Publication.DoesNotExist:
            return 'Error: publication not found'

        return pub.formatted_reference_author_year

    def handleMatch(self, m, data):
        a = etree.Element('a')
        a.text = m.group(1)
        a.set('href', '#')
        a.set('data-toggle', 'tooltip')
        full_markdown_ref = m.group(0) # also incuding [[PUB ]]
        a.set('title', PublicationsInlineProcessor._tooltip_html_content(full_markdown_ref))
        return a, m.start(0), m.end(0)


class PublicationsExtension(Extension):
    def extendMarkdown(self, md):
        PUBLICATIONS_RE = r'\[\[PUB:([\w0-9_ -.]+)\]\]'

        publicationPattern = PublicationsInlineProcessor(PUBLICATIONS_RE)

        md.inlinePatterns.register(publicationPattern, 'lepidoptera_publications', 175)


def makeExtension(**kwargs):
    return PublicationsExtension(**kwargs)