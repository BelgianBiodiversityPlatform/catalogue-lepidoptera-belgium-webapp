import csv
from difflib import SequenceMatcher

from lepidoptera.models import Family, Species, SpeciesPresence, Province, TimePeriod
from ._utils import LepidopteraCommand, text_clean

SPECIES_CSV_PROVINCE_COL_NAMES = ['WV', 'OV', 'AN', 'LI', 'BR', 'HA', 'NA', 'LG', 'LX']
# province Code in CSV and initial data match so it's easier

SKIP_FAMILY_CHECK = True

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def _assign_presence_to_species(species, presence_code, province_code):
    # We first drop any existing presence info for this species:
    species.speciespresence_set.filter(province__code=province_code).delete()

    present_before_1980, present_between_1980_2004, present_since_2004 = False, False, False

    if presence_code == 1:
        present_before_1980 = True
    elif presence_code == 2:
        present_before_1980 = True
        present_between_1980_2004 = True
    elif presence_code == 3:
        present_between_1980_2004 = True
    elif presence_code == 4:
        present_between_1980_2004 = True
        present_since_2004 = True
    elif presence_code == 5:
        present_before_1980 = True
        present_between_1980_2004 = True
        present_since_2004 = True
    elif presence_code == 6:
        present_before_1980 = True
        present_since_2004 = True
    elif presence_code == 7:
        present_since_2004 = True

    province = Province.objects.get(code=province_code)

    selected_periods = []

    if present_before_1980:
        selected_periods.append(TimePeriod.objects.get(name=TimePeriod.BEFORE_1980_NAME))
    if present_between_1980_2004:
        selected_periods.append(TimePeriod.objects.get(name=TimePeriod.BETWEEN_1980_2004_NAME))
    if present_since_2004:
        selected_periods.append(TimePeriod.objects.get(name=TimePeriod.SINCE_2004_NAME))

    for period in selected_periods:
        SpeciesPresence.objects.create(species=species,
                                       province=province,
                                       period=period,
                                       present=True)


class Command(LepidopteraCommand):
    help = "Add data from existing website to Django's database. Will destroy manual changes made trough the admin " \
           "interface."

    def add_arguments(self, parser):
        parser.add_argument('families_csv')
        parser.add_argument('species_csv')
        parser.add_argument('species_paragraphs_csv')

    def handle(self, *args, **options):
        with open(options['families_csv']) as families_csv_file:
            self.load_families(families_csv_file)

        with open(options['species_csv']) as species_csv_file:
            self.load_species(species_csv_file)

        with open(options['species_paragraphs_csv']) as species_paragraphs_csv_file:
            self.load_species_paragraphs(species_paragraphs_csv_file)

    def load_species_paragraphs(self, species_paragraphs_csv_file):
        self.w("Will now import species paragraphs (1-2-3) from the old website, and try to reconcile them with our new database.")
        species_ignored_multiple_matches = []
        species_not_found = []
        species_with_overwritten_text = []
        success_count = 0

        for i, species_row in enumerate(csv.DictReader(species_paragraphs_csv_file, delimiter=',')):
            species_full_name = text_clean(species_row['speciesCode'])
            try:
                species = Species.objects.get_with_name_and_author_ignore_brackets(species_full_name, ignore_author=True)

                # Save the general text from paragraph 1
                if species.text_en != '':
                    species_with_overwritten_text.append(species_full_name)
                species.text_en = text_clean(species_row['p1'])

                species.hostplants_section_text = text_clean(species_row['p2'])
                species.flightperiod_section_text = text_clean(species_row['p3'])

                species.save()
                success_count = success_count + 1
                self.w('.', ending='')
            except Species.DoesNotExist:
                species_not_found.append(species_full_name)
            except Species.MultipleObjectsReturned:
                species_ignored_multiple_matches.append(species_full_name)

        self.w(self.style.WARNING('The following species code are not found in the new website database: {}'.format(', '.join(species_not_found))))
        self.w(self.style.WARNING(
            '\nSpecies where matched failed because they were duplicates based on the full name (please enter data manually later): {}'.format(
                ', '.join(species_ignored_multiple_matches))))
        self.w(self.style.WARNING('The following species already had a general description in text_en, so it was overriden: {}'.format(
            ', '.join(species_with_overwritten_text))))
        self.w('Species paragraphs: {} species successfully imported, {} in error.'.format(success_count, len(species_not_found)))

    def load_species(self, species_csv_file):
        self.w("Will now import Species (province presence) from the old website, and try to reconcile them with our new database.")
        missing_species = []
        species_ignored_multiple_matches = []
        species_no_family_match = []
        successful_match_counter = 0
        error_in_presence_code_for = []

        for i, species_row in enumerate(csv.DictReader(species_csv_file, delimiter=';')):
            species_full_name = text_clean(species_row['sName'])
            try:
                species = Species.objects.get_with_name_and_author_ignore_brackets(species_full_name, ignore_author=True)
                if SKIP_FAMILY_CHECK or species.family.name == text_clean(species_row['family']):
                    successful_match_counter = successful_match_counter + 1

                    for province_code in SPECIES_CSV_PROVINCE_COL_NAMES:
                        presence_code = species_row[province_code]
                        if presence_code:
                            try:
                                presence_code = int(presence_code)
                                _assign_presence_to_species(species, presence_code, province_code)
                            except ValueError:
                                error_in_presence_code_for.append(species_full_name)

                else:
                    family_from_db = species.family.name
                    family_from_csv = text_clean(species_row['family'])
                    similarity_score = similar(family_from_db, family_from_csv)
                    msg = "{} vs {} (similarity: {})".format(family_from_db, family_from_csv, similarity_score)
                    species_no_family_match.append(species_full_name + "(" + msg + ")")

            except Species.DoesNotExist:
                missing_species.append(species_full_name)
            except Species.MultipleObjectsReturned:
                species_ignored_multiple_matches.append(species_full_name)

        self.w(self.style.WARNING('\nMissing species in new website database (please enter data manually later): {}'.format(', '.join(missing_species))))
        self.w(self.style.WARNING('\nSpecies where matched failed because they were duplicates based on the full name (please enter data manually later): {}'.format(', '.join(species_ignored_multiple_matches))))
        self.w(self.style.WARNING('\nSpecies found, but the family doesn\'t match (please enter data manually later): {}'.format(', '.join(species_no_family_match))))
        self.w('Successful species match: {}'.format(successful_match_counter))
        unsuccessful_match_counter = len(species_no_family_match) + len(missing_species)
        self.w('Unsuccessful species match: {}'.format(unsuccessful_match_counter))
        self.w(self.style.WARNING('Error in the presence_code for {} '.format(
            ', '.join(error_in_presence_code_for)
        )))

    def load_families(self, families_csv_file):
        self.w("Will now import Families (text description) from the old website, and try to reconcile them with our new database.")
        missing_families = []
        families_with_already_a_description = []

        for i, families_row in enumerate(csv.DictReader(families_csv_file, delimiter=';')):
            family_name = text_clean(families_row['family'])

            try:
                family = Family.objects.get(name=family_name)

                if family.text != '':
                    families_with_already_a_description.append(family_name)

                family.text_en = text_clean(families_row['description'])
                family.save()

            except Family.DoesNotExist:
                missing_families.append(family_name)

            self.w('.', ending='')

        self.w(self.style.WARNING('\nFamilies existing in the old website but missing in the new database families (please enter data manually later): {}'.format(', '.join(missing_families))))
        self.w(self.style.NOTICE('\nFamilies with already a description (description overwritten, nothing to do): {}'.format(
            ', '.join(families_with_already_a_description)))
        )
