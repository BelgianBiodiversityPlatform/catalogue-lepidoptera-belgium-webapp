# Generated by Django 2.0.13 on 2019-08-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0021_observation_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observation',
            name='plant_genus',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='plant_species',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='species',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='substrate',
        ),
        migrations.AlterField(
            model_name='hostplantgenus',
            name='lepidoptera_species',
            field=models.ManyToManyField(through='lepidoptera.PlantGenusObservation', to='lepidoptera.Species'),
        ),
        migrations.AlterField(
            model_name='hostplantspecies',
            name='lepidoptera_species',
            field=models.ManyToManyField(through='lepidoptera.PlantSpeciesObservation', to='lepidoptera.Species'),
        ),
        migrations.AlterField(
            model_name='substrate',
            name='lepidoptera_species',
            field=models.ManyToManyField(through='lepidoptera.SubstrateObservation', to='lepidoptera.Species'),
        ),
        migrations.DeleteModel(
            name='Observation',
        ),
    ]
