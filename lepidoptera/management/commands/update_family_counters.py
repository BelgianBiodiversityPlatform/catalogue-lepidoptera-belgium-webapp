from django.core.management.base import BaseCommand, CommandError
from lepidoptera.models import Family


class Command(BaseCommand):
    help = 'For each Family, updates the (denormalized) species counter.'

    def handle(self, *args, **options):
        for family in Family.objects.all():
            family.update_species_counter()