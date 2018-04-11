from pathlib import Path

from django.core.files import File

from lepidoptera.management.commands._utils import LepidopteraCommand
from lepidoptera.models import Species, SpeciesPicture


class Command(LepidopteraCommand):
    help = "Import specimen pictures (and attach them to species)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='!! CAUTION !! Truncate Specimen pictures data prior to import.',
        )

        parser.add_argument('source_picture_directory')  # May contains subfolders

    def create_specimenpicture_from_path(self, pic_absolute_path):
        filename = pic_absolute_path.name
        try:
            species_code, picture_info, picture_number = filename.split('_')

            try:
                found_species = Species.objects.get(code=species_code)

                opts = {}
                # We have a 'i' (Imago=adult stage), a Sex (M/W) and a side => Museum specimens
                if picture_info == 'iMup':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.MUSEUM_SPECIMEN,
                            'specimen_sex': SpeciesPicture.MALE,
                            'side': SpeciesPicture.UPPER}
                elif picture_info == 'iMun':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.MUSEUM_SPECIMEN,
                            'specimen_sex': SpeciesPicture.MALE,
                            'side': SpeciesPicture.UNDER}
                elif picture_info == 'iWup':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.MUSEUM_SPECIMEN,
                            'specimen_sex': SpeciesPicture.FEMALE,
                            'side': SpeciesPicture.UPPER}
                elif picture_info == 'iWun':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.MUSEUM_SPECIMEN,
                            'specimen_sex': SpeciesPicture.FEMALE,
                            'side': SpeciesPicture.UNDER}

                # We have a 'i' (Imago), a Sex (A/M/W) but no side => In vivo specimens
                elif picture_info == 'iA':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.IN_VIVO_SPECIMEN,
                            'specimen_sex': SpeciesPicture.ADULT}
                elif picture_info == 'iM':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.IN_VIVO_SPECIMEN,
                            'specimen_sex': SpeciesPicture.MALE}
                elif picture_info == 'iW':
                    opts = {'specimen_stage': SpeciesPicture.IMAGO,
                            'image_subject': SpeciesPicture.IN_VIVO_SPECIMEN,
                            'specimen_sex': SpeciesPicture.FEMALE}

                # We only have e, l, c, b, m, p => It's a pre-adult stage. No sex or side info
                elif picture_info == 'e':
                    opts = {'specimen_stage': SpeciesPicture.EGG,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}
                elif picture_info == 'l':
                    opts = {'specimen_stage': SpeciesPicture.LARVA,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}
                elif picture_info == 'c':
                    opts = {'specimen_stage': SpeciesPicture.CASE,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}
                elif picture_info == 'b':
                    opts = {'specimen_stage': SpeciesPicture.BAG,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}
                elif picture_info == 'm':
                    opts = {'specimen_stage': SpeciesPicture.MINE,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}
                elif picture_info == 'p':
                    opts = {'specimen_stage': SpeciesPicture.PUPA,
                            'image_subject': SpeciesPicture.PRE_ADULT_STAGE}

                # Other pic subjects
                elif picture_info == 'hpl':
                    opts = {'image_subject': SpeciesPicture.HOST_PLANT}
                elif picture_info == 'bio':
                    opts = {'image_subject': SpeciesPicture.BIONOMICS}
                elif picture_info == 'hab':
                    opts = {'image_subject': SpeciesPicture.HABITAT}

                if opts:  # picture info has been understood, we can create the object
                    with open(str(pic_absolute_path), 'rb') as f:
                        sp = SpeciesPicture()

                        img_data = File(f)

                        sp.species = found_species
                        sp.verbatim_image_filename = filename

                        for key, value in opts.items():
                            setattr(sp, key, value)

                        sp.image.save(filename, img_data)

                        sp.save()

                else:  # No opts means no matching case for 'picture_info'
                    msg = 'Non understood picture info for {fn}'.format(
                        fn=filename
                    )

                    self.w(self.style.WARNING(msg))

            except Species.DoesNotExist:
                msg = 'Species matching code not found: {code} ({fn})'.format(
                    code=species_code,
                    fn=filename
                )

                self.w(self.style.WARNING(msg))
        except ValueError:
            msg = 'Invalid filename format: {fn}'.format(
                fn=filename
            )

            self.w(self.style.WARNING(msg))

    def handle(self, *args, **options):
        if options['truncate']:
            self.w('Truncate Specimen Pictures', ending='')
            SpeciesPicture.objects.all().delete()
            self.w(self.style.SUCCESS('Done.'))

        self.w('Importing specimen pictures...')

        root_directory = Path(options['source_picture_directory'])
        file_list = [f for f in root_directory.resolve().glob('**/*') if f.is_file()]
        for pic in file_list:
            if pic.name.startswith('.'):
                self.w(self.style.WARNING('Skipping hidden file {}...'.format(pic)))
            else:
                self.create_specimenpicture_from_path(pic)
                self.w('.', ending='')
