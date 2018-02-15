from collections import namedtuple

from django.core.management.base import CommandError
from django.db import connection

from lepidoptera.models import Family, Status, Subfamily, Tribus, Genus, Subgenus, Species

from ._utils import LepidopteraCommand, text_clean

MODELS_TO_TRUNCATE = [Status, Family, Subfamily, Tribus, Genus, Subgenus, Species]

NULL_FAMILY_ID = 999  # A dummy family with no info, to simulate NULL values. We don't import that.
NULL_GENUS_ID = 999010


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
            cursor.execute('SELECT * FROM "tblFamilies"')
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

                                          status=Status.objects.get(verbatim_status_id=result.StatusID),

                                          # FamilyID is duplicated: a verbatim, non editable field for traceability
                                          # but also a (modifiable) display order
                                          display_order=family_id)
                    self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblSubfamilies...', ending='')
            cursor.execute('SELECT * FROM "tblSubfamilies"')
            for result in namedtuplefetchall(cursor):
                Subfamily.objects.create(verbatim_subfamily_id=result.SubfamilyID,
                                         family=Family.objects.get(verbatim_family_id=result.FamilyID),
                                         status=Status.objects.get(verbatim_status_id=result.StatusID),
                                         name=text_clean(result.SubfamilyName),
                                         author=text_clean(result.SubfamilyAuthor),

                                         vernacular_name_nl=text_clean(result.SubFamilyNameNL),
                                         vernacular_name_en=text_clean(result.SubFamilyNameEN),
                                         vernacular_name_fr=text_clean(result.SubFamilyNameFR),
                                         vernacular_name_de=text_clean(result.SubFamilyNameGE),

                                         text=text_clean(result.SubfamilyText),

                                         display_order=result.SubfamilyID)
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblTribus...', ending='')
            cursor.execute('SELECT * FROM "tblTribus"')
            for result in namedtuplefetchall(cursor):
                # Consistency check: is tribus.subfamily.family_id == tribus.family_id ?
                if result.FamilyID != Subfamily.objects.get(verbatim_subfamily_id=result.SubfamilyID).family.verbatim_family_id:
                    raise CommandError("Family/Subfamily inconsistency detected for tblTribus with ID={}".format(result.TribusID))

                Tribus.objects.create(verbatim_tribus_id=result.TribusID,
                                      subfamily=Subfamily.objects.get(verbatim_subfamily_id=result.SubfamilyID),
                                      status=Status.objects.get(verbatim_status_id=result.StatusID),
                                      name=text_clean(result.TribusName),
                                      author=text_clean(result.TribusAuthor),

                                      vernacular_name_nl=text_clean(result.TribusNameNL),
                                      vernacular_name_en=text_clean(result.TribusNameEN),
                                      vernacular_name_fr=text_clean(result.TribusNameFR),
                                      vernacular_name_de=text_clean(result.TribusNameGE),

                                      text=text_clean(result.TribusText),

                                      display_order=result.TribusID)
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblGenera...', ending='')
            cursor.execute('SELECT * FROM "tblGenera" ORDER BY "StatusID"')  # ORDER so accepted are knwon before synonyms referencing them
            for result in namedtuplefetchall(cursor):
                name = result.GenusName
                genus_id = result.GenusID

                tribus_id = result.TribusID
                subfamily_id = result.SubfamilyID
                family_id = result.FamilyID

                if genus_id != NULL_GENUS_ID:
                    # Find the parent link...
                    if tribus_id is None and subfamily_id is None and family_id is not None:
                        # We only have a family...
                        parent_link = {'family': Family.objects.get(verbatim_family_id=family_id)}
                    elif tribus_id is None and subfamily_id is not None:
                        # Slightly better, we have a subfamily
                        # consistency check: the direct family and subfamily.family should be equal
                        if family_id != Subfamily.objects.get(verbatim_subfamily_id=subfamily_id).family.verbatim_family_id:
                            raise CommandError("Subfamily/Family inconsistency at the Genus level")

                        parent_link = {'subfamily': Subfamily.objects.get(verbatim_subfamily_id=subfamily_id)}
                    elif tribus_id is not None:
                        # Even better: we have the tribus
                        # consistency check: the direct family and subfamily.family should be equal
                        if family_id != Subfamily.objects.get(
                                verbatim_subfamily_id=subfamily_id).family.verbatim_family_id:
                            raise CommandError("Subfamily/Family inconsistency at the Genus level")

                        # and direct subfamily should be equal to tribus.subfamily
                        if subfamily_id != Tribus.objects.get(
                                verbatim_tribus_id=tribus_id).subfamily.verbatim_subfamily_id:
                            raise CommandError("Tribus/Subfamily inconsistency at the Genus level")
                        parent_link = {'tribus': Tribus.objects.get(verbatim_tribus_id=tribus_id)}

                    create_opts = {'verbatim_genus_id': genus_id,
                                   'name': text_clean(name),
                                   'author': text_clean(result.GenusAuthor),

                                   'vernacular_name_nl': text_clean(result.GenusNameNL),
                                   'vernacular_name_en': text_clean(result.GenusNameEN),
                                   'vernacular_name_fr': text_clean(result.GenusNameFR),
                                   'vernacular_name_de': text_clean(result.GenusNameGE),
                                   'text': text_clean(result.GenusText),
                                   'status': Status.objects.get(verbatim_status_id=result.StatusID),
                                   'display_order': genus_id}
                    if result.GenusReferenceToHigherCategory:
                        create_opts['synonym_of'] = Genus.objects.get(verbatim_genus_id=result.GenusReferenceToHigherCategory)

                    create_opts.update(parent_link)

                    Genus.objects.create(**create_opts)
                    self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblSubgenera...', ending='')
            cursor.execute('SELECT * FROM "tblSubgenera"')
            for result in namedtuplefetchall(cursor):
                Subgenus.objects.create(verbatim_subgenus_id=result.SubgenusID,
                                        name=text_clean(result.SubgenusName),
                                        author=text_clean(result.SubgenusAuthor),

                                        vernacular_name_nl=text_clean(result.SubgenusNameNL),
                                        vernacular_name_en=text_clean(result.SubgenusNameEN),
                                        vernacular_name_fr=text_clean(result.SubgenusNameFR),
                                        vernacular_name_de=text_clean(result.SubgenusNameGE),

                                        text=text_clean(result.SubgenusText),

                                        # Currently all subgenera are only linked to a genus, so that's the only
                                        # taxonomic lin we (can) import
                                        genus=Genus.objects.get(verbatim_genus_id=result.GenusID),
                                        status=Status.objects.get(verbatim_status_id=result.StatusID),

                                        display_order=result.SubgenusID
                )
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblSpecies...', ending='')
            cursor.execute('SELECT * FROM "tblSpecies" ORDER BY "StatusID"')
            for result in namedtuplefetchall(cursor):
                subgenus_id = result.SubgenusID
                genus_id = result.GenusID

                # Find the parent link...
                if subgenus_id is None and genus_id is not None:
                    # We only have a genus...
                    parent_link = {'genus': Genus.objects.get(verbatim_genus_id=genus_id)}
                elif subgenus_id is not None:
                    # Consistency check: direct genus_id == subgenus.genus_id
                    if genus_id != Subgenus.objects.get(verbatim_subgenus_id=subgenus_id).genus.verbatim_genus_id:
                        raise CommandError("Subgenus/Genus inconsistency at the Species level. SpeciesNumber={}".format(result.SpeciesNumber))

                    parent_link = {'subgenus': Subgenus.objects.get(verbatim_subgenus_id=subgenus_id)}

                create_opts = {'verbatim_species_number': result.SpeciesNumber,
                               'name': text_clean(result.SpeciesName),
                               'code': text_clean(result.SpeciesCode),

                               'author': text_clean(result.SpeciesAuthor),

                               'vernacular_name_nl': text_clean(result.SpeciesNameNL),
                               'vernacular_name_en': text_clean(result.SpeciesNameEN),
                               'vernacular_name_fr': text_clean(result.SpeciesNameFR),
                               'vernacular_name_de': text_clean(result.SpeciesNameGE),
                               'text': text_clean(result.SpeciesText),
                               'status': Status.objects.get(verbatim_status_id=result.StatusID),
                               'display_order': result.SpeciesNumber}

                if result.ReferenceToHigherCategory:
                    create_opts['synonym_of'] = Species.objects.get(
                        verbatim_species_number=result.ReferenceToHigherCategory)

                create_opts.update(parent_link)

                Species.objects.create(**create_opts)
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))