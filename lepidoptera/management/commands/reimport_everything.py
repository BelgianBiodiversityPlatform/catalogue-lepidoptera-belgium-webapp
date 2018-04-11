from django.core.management import call_command

from lepidoptera.management.commands._utils import LepidopteraCommand


class Command(LepidopteraCommand):
    help = "(re)import everything (access, old website, wikidata, ...), overwriting the existing DB content."

    def add_arguments(self, parser):
        parser.add_argument('website_families_csv')
        parser.add_argument('website_species_csv')
        parser.add_argument('species_picture_dir')

    def handle(self, *args, **options):
        self.w("Step 1: Access import...")
        self.w("========================")
        call_command('access_import', '--truncate')

        self.w("Step 2: Website import and reconciliation...")
        self.w("============================================")
        call_command('website_import', options['website_families_csv'], options['website_species_csv'])

        self.w("Step 3: Add Wikidata identifiers...")
        self.w("===================================")
        call_command('add_wikidata_identifiers')

        self.w("Step 4: Import species pictures...")
        self.w("==================================")
        call_command('speciespictures_import', '--truncate', options['species_picture_dir'])

        self.w("Step 5: Denormalized data full rebuild...")
        self.w("=========================================")

        call_command('denorm_rebuild')

