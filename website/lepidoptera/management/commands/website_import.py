import csv

from lepidoptera.models import Family, Species, SpeciesPresence, Province, TimePeriod
from ._utils import LepidopteraCommand, text_clean

SPECIES_CSV_PROVINCE_COL_NAMES = ['WV', 'OV', 'AN', 'LI', 'BR', 'HA', 'NA', 'LG', 'LX']
# province Code in CSV and initial data match so it's easier


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

    def handle(self, *args, **options):
        with open(options['families_csv']) as families_csv_file:
            self.load_families(families_csv_file)

        with open(options['species_csv']) as species_csv_file:
            self.load_species(species_csv_file)

    def load_species(self, species_csv_file):
        missing_species = []
        species_no_family_match = []
        successful_match_counter = 0
        error_in_presence_code_for = []

        for i, species_row in enumerate(csv.DictReader(species_csv_file, delimiter=';')):
            species_full_name = text_clean(species_row['sName'])
            try:
                species = Species.objects.get_with_name_and_author(species_full_name)
                if species.family.name == text_clean(species_row['family']):
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
                    species_no_family_match.append(species_full_name)

            except Species.DoesNotExist:
                missing_species.append(species_full_name)

        self.w(self.style.WARNING('\nMissing species: {}'.format(', '.join(missing_species))))
        self.w(self.style.WARNING('\nSpecies found, but the family doesn\'t match: {}'.format(', '.join(species_no_family_match))))
        self.w('Successful species match: {}'.format(successful_match_counter))
        unsuccessful_match_counter = len(species_no_family_match) + len(missing_species)
        self.w('Unsuccessful species match: {}'.format(unsuccessful_match_counter))
        self.w(self.style.WARNING('Error in the presence_code for {} '.format(
            ', '.join(error_in_presence_code_for)
        )))

    def load_families(self, families_csv_file):
        missing_families = []
        families_with_already_a_description = []

        for i, families_row in enumerate(csv.DictReader(families_csv_file, delimiter=';')):
            family_name = text_clean(families_row['family'])

            try:
                family = Family.objects.get(name=family_name)

                if family.text == '':
                    family.text = text_clean(families_row['description'])
                else:
                    families_with_already_a_description.append(family_name)

                family.save()

            except Family.DoesNotExist:
                missing_families.append(family_name)

            self.w('.', ending='')

        self.w(self.style.WARNING('\nMissing families: {}'.format(', '.join(missing_families))))
        self.w(self.style.WARNING('\nFamilies with already a description (not overwritten): {}'.format(', '.join(families_with_already_a_description))))