from collections import namedtuple

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from lepidoptera.models import Family, Status

from ._utils import LepidopteraCommand, text_clean

MODELS_TO_TRUNCATE = [Status, Family]

NULL_FAMILY_ID = 999  # A dummy family with no info, to simulate NULL values. We don't import that.


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class Command(LepidopteraCommand):
    help = "Import data from Access (tblXXXX tables) to Django's database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='!! CAUTION !! Truncate webapp data prior to import.',
        )

    def handle(self, *args, **options):
        if options['truncate']:
            for model in MODELS_TO_TRUNCATE:
                self.w('Truncate model {name}...'.format(name=model.__name__), ending='')
                model.objects.all().delete()
                self.w(self.style.SUCCESS('Done.'))

        with connection.cursor() as cursor:
            self.w('Importing from tblStatus...', ending='')
            cursor.execute('SELECT * FROM "tblStatus"')
            for result in namedtuplefetchall(cursor):
                Status.objects.create(verbatim_status_id=result.StatusID,
                                      name=text_clean(result.StatusName))

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblFamilies...', ending='')
            cursor.execute('SELECT * FROM "tblFamilies"');
            for result in namedtuplefetchall(cursor):
                family_id = result.FamilyID

                if family_id != NULL_FAMILY_ID:
                    Family.objects.create(verbatim_family_id=family_id,
                                          name=text_clean(result.FamilyName),
                                          author=text_clean(result.FamilyAuthor),

                                          vernacular_name_nl=text_clean(result.FamilyNameNL),
                                          vernacular_name_en=text_clean(result.FamilyNameEN),
                                          vernacular_name_fr=text_clean(result.FamilyNameFR),
                                          vernacular_name_de=text_clean(result.FamilyNameGE),

                                          text=text_clean(result.FamilyText),

                                          status=Status.objects.get(verbatim_status_id=result.StatusID))
                    self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))