import requests

from lepidoptera.management.commands._utils import LepidopteraCommand
from lepidoptera.models import Family

QUERY_TEMPLATE = '''SELECT ?item ?itemLabel WHERE {{
  ?item rdfs:label "{family_name}"@en.
  ?item wdt:P105 wd:Q35409.
}}
'''.replace('\n', ' ')


WIKIDATA_SPARQL_ENDPOINT = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'


class Command(LepidopteraCommand):
    help = "Query wikidata with the Family name, and store the id in Family.wikidata_id if found"

    def handle(self, *args, **options):
        for family in Family.objects.all():
            query = QUERY_TEMPLATE.format(family_name=family.name)
            data = requests.get(WIKIDATA_SPARQL_ENDPOINT, params={'query': query, 'format': 'json'}).json()

            results = data['results']['bindings']
            if len(results) == 1:
                family.wikidata_id = results[0]['item']['value'].rsplit('/', 1)[-1]  # Get Wikidata URI, split for the Q identifier
                family.save()
            elif len(results) == 0:
                self.w(self.style.WARNING("Wikidata entry not found for: {}".format(family.name)))
            elif len(results) > 1:
                self.w(self.style.WARNING("Multiple Wikidata entry found for: {}".format(family.name)))
            self.w('.', ending='')