from collections import namedtuple

from django.core.management.base import CommandError
from django.db import connection

from lepidoptera.models import Family, Status, Subfamily, Tribus, Genus, Subgenus, Species, HostPlantFamily, \
    HostPlantGenus, Substrate, Observation, HostPlantSpecies, Journal, Publication

from ._utils import LepidopteraCommand, text_clean

MODELS_TO_TRUNCATE = [Status, Family, Subfamily, Tribus, Genus, Subgenus, Species, HostPlantFamily, HostPlantGenus,
                      HostPlantSpecies, Substrate, Observation, Journal, Publication]

NULL_FAMILY_ID = 999  # A dummy family with no info, to simulate NULL values. We don't import that.
NULL_GENUS_ID = 999010
NULL_SPECIES_NUMBER = 999010010

NULL_PLANTGENUS_ID = 5020
PLANT_GENUS_IDS_TO_SKIP = (NULL_PLANTGENUS_ID, 1770)  # 1770= A weird "carnivorous" entry not referenced by any plant species


def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
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

            self.w('Importing from tblJournals...')
            cursor.execute('SELECT * FROM "tblJournals"')
            for result in namedtuplefetchall(cursor):
                Journal.objects.create(
                    verbatim_id=result.JournalID,
                    title=text_clean(result.JournalTitle)
                )
                self.w('.', ending='')
            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblPublications...')
            cursor.execute('SELECT * FROM "tblPublications"')
            for result in namedtuplefetchall(cursor):
                Publication.objects.create(
                    verbatim_id=result.PublicationID,
                    author=text_clean(result.PublicationAuthor),
                    title=text_clean(result.PublicationTitle),
                    journal=Journal.objects.get(verbatim_id=result.JournalID),
                    publisher=text_clean(result.PublicationPublisher),
                    year=text_clean(result.PublicationYear),
                    volume=text_clean(result.PublicationVolume),
                    issue=text_clean(result.PublicationIssue),
                    page_numbers=text_clean(result.PublicationPageNumbers)
                )
                self.w('.', ending='')
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

                                          text_en=text_clean(result.FamilyTextEN),
                                          text_nl=text_clean(result.FamilyTextNL),

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

                                         text_en=text_clean(result.SubfamilyTextEN),
                                         text_nl=text_clean(result.SubfamilyTextNL),

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

                                      text_en=text_clean(result.TribusTextEN),
                                      text_nl=text_clean(result.TribusTextNL),

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
                                   'text_en': text_clean(result.GenusTextEN),
                                   'text_nl': text_clean(result.GenusTextNL),
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

                                        text_en=text_clean(result.SubgenusTextEN),
                                        text_nl=text_clean(result.SubgenusTextNL),

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

                if result.SpeciesNumber != NULL_SPECIES_NUMBER:
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

                                   'text_en': text_clean(result.SpeciesTextEN),
                                   'text_nl': text_clean(result.SpeciesTextNL),

                                   'first_mention_page': text_clean(result.PublicationPage),
                                   'first_mention_link': text_clean(result.PublicationReference),

                                   'status': Status.objects.get(verbatim_status_id=result.StatusID),
                                   'display_order': result.SpeciesNumber}

                    if result.ReferenceToHigherCategory:
                        create_opts['synonym_of'] = Species.objects.get(
                            verbatim_species_number=result.ReferenceToHigherCategory)

                    if result.PublicationID:
                        create_opts['first_mention_publication'] = Publication.objects.get(
                            verbatim_id=result.PublicationID
                        )

                    create_opts.update(parent_link)

                    Species.objects.create(**create_opts)
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing Host plants and substrates')
            self.w('Importing from tblHostPlantFamilies...', ending='')
            cursor.execute('SELECT * FROM "tblHostPlantFamilies"')
            for result in namedtuplefetchall(cursor):
                HostPlantFamily.objects.create(
                    verbatim_id=result.HostPlantfamilyID,
                    name=text_clean(result.HostPlantfamilyName),

                    vernacular_name_nl=text_clean(result.HostPlantfamilyNL),
                    vernacular_name_en=text_clean(result.HostPlantfamilyEN),
                    vernacular_name_fr=text_clean(result.HostPlantfamilyFR),
                    vernacular_name_de=text_clean(result.HostPlantfamilyGE),
                )
                self.w('.', ending='')

            self.w(self.style.SUCCESS('OK'))

            self.w('Importing from tblHostPlantGenera...', ending='')
            cursor.execute('SELECT * FROM "tblHostPlantGenera"')
            for result in namedtuplefetchall(cursor):
                if int(result.HostPlantGenusID) not in PLANT_GENUS_IDS_TO_SKIP:
                    HostPlantGenus.objects.create(
                        verbatim_id=result.HostPlantGenusID,
                        name=text_clean(result.HostPlantGenusName),

                        vernacular_name_nl=text_clean(result.HostPlantGenusNameNL),
                        vernacular_name_en=text_clean(result.HostPlantGenusNameEN),
                        vernacular_name_fr=text_clean(result.HostPlantGenusNameFR),
                        vernacular_name_de=text_clean(result.HostPlantGenusNameGE),

                        author=text_clean(result.HostPlantGenusAuthor),
                        family=HostPlantFamily.objects.get(verbatim_id=result.HostPlantFamilyID)
                    )
                self.w('.', ending='')
            self.w(self.style.SUCCESS('OK'))

            self.w('Importing Host plant observations, with related species and substrates...', ending='')
            cursor.execute('SELECT * FROM "tblHostPlants", "tblHostPlantSpecies" '
                           'WHERE "HostplantID" = "HostPlantID"')
            # It's a bit messy because tblHostPlantSpecies contains plant species, but also substrates and
            # "empty species info but link to a genus" (sp., when the exact species is unknown)
            for result in namedtuplefetchall(cursor):
                observation = Observation()
                observation.species = Species.objects.get(code=text_clean(result.SpeciesCode))

                if (not result.HostPlantGenusID) or (result.HostPlantGenusID == NULL_PLANTGENUS_ID):
                    # Fake species with no Genus, it's indeed a substrate
                    observation.substrate, created = Substrate.objects.get_or_create(name=text_clean(
                        result.HostPlantName)
                    )
                elif text_clean(result.HostPlantName) == "sp.":
                    # We only know the genus
                    observation.plant_genus = HostPlantGenus.objects.get(verbatim_id=result.HostPlantGenusID)
                else:
                    # It's a "true species"
                    plant_genus = HostPlantGenus.objects.get(verbatim_id=result.HostPlantGenusID)

                    observation.plant_species, created = HostPlantSpecies.objects.get_or_create(
                        verbatim_id=result.HostPlantID,
                        name=text_clean(result.HostPlantName),
                        author=text_clean(result.HostPlantAuthor),

                        vernacular_name_nl=text_clean(result.HostPlantNameNL),
                        vernacular_name_en=text_clean(result.HostPlantNameEN),
                        vernacular_name_fr=text_clean(result.HostPlantNameFR),
                        vernacular_name_de=text_clean(result.HostPlantNameGE),

                        genus=plant_genus
                    )

                observation.save()
                self.w('.', ending='')
            self.w(self.style.SUCCESS('OK'))