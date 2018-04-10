from django.core.management import call_command

from lepidoptera.management.commands._utils import LepidopteraCommand


class Command(LepidopteraCommand):
    help = "(re)import everything (access, old website, wikidata, ...), overwriting the existing DB content."

    def add_arguments(self, parser):
        parser.add_argument('website_families_csv')
        parser.add_argument('website_species_csv')

    def handle(self, *args, **options):
        call_command('access_import', '--truncate')
        call_command('website_import', options['website_families_csv'], options['website_species_csv'])
        call_command('add_wikidata_identifiers')
        call_command('denorm_rebuild')

