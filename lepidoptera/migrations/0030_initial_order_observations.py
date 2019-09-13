# Generated by Django 2.0.13 on 2019-09-13 11:39

from django.db import migrations

def noop(apps, schema_editor):
    pass


def migrate_observation_data(apps, schema_editor):
    PlantSpeciesObservation = apps.get_model('lepidoptera', 'PlantSpeciesObservation')
    PlantGenusObservation = apps.get_model('lepidoptera', 'PlantGenusObservation')
    SubstrateObservation = apps.get_model('lepidoptera', 'SubstrateObservation')

    Species = apps.get_model('lepidoptera', 'Species')

    for lepido_species in Species.objects.all():
        for index, pso in enumerate(PlantSpeciesObservation.objects.filter(species=lepido_species)):
            pso.the_order = index
            pso.save()

        for index, pgo in enumerate(PlantGenusObservation.objects.filter(species=lepido_species)):
            pgo.the_order = index
            pgo.save()

        for index, suo in enumerate(SubstrateObservation.objects.filter(species=lepido_species)):
            suo.the_order = index
            suo.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0029_auto_20190913_1135'),
    ]

    operations = [
        migrations.RunPython(migrate_observation_data, noop),
    ]
