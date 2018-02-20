import csv

from lepidoptera.models import Family
from ._utils import LepidopteraCommand, text_clean


class Command(LepidopteraCommand):
    help = "Add data from existing website to Django's database. Will destroy manual changes made trough the admin " \
           "interface."

    def add_arguments(self, parser):
        parser.add_argument('families_csv')

    def handle(self, *args, **options):
        with open(options['families_csv']) as families_csv_file:
            missing_families = []

            for i, families_row in enumerate(csv.DictReader(families_csv_file, delimiter=';')):
                family_name = text_clean(families_row['family'])

                try:
                    family = Family.objects.get(name=family_name)

                    if family.text == '':
                        family.text = text_clean(families_row['description'])
                    else:
                        self.w(self.style.WARNING(
                            '\nFamily: {} already has a description, not importing...'.format(family))
                        )

                    family.save()

                except Family.DoesNotExist:
                    missing_families.append(family_name)

                self.w('.', ending='')

            self.w(self.style.WARNING('\nMissing families: {}'.format(', '.join(missing_families))))