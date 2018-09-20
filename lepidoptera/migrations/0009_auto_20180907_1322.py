# Generated by Django 2.1 on 2018-09-07 11:22

from django.db import migrations


def initialize_genus_name(apps, schema_editor):
    # The (denormalized) genus_name field of HostPlantSpecies must initialized first before it can be used
    HostPlantSpecies = apps.get_model('lepidoptera', 'HostPlantSpecies')

    for species in HostPlantSpecies.objects.all():
        species.genus_name = species.genus.name  # It would be cleaner to call update_genus() but that doesn't work
                                                 # since the method wasn't present in the previous versions of the Model
        species.save(update_fields=['genus_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0008_hostplantspecies_genus_name'),
    ]

    operations = [
        migrations.RunPython(initialize_genus_name),
    ]