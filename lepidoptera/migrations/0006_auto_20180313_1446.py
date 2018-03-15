# Generated by Django 2.0.3 on 2018-03-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0005_auto_20180309_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hostplantfamily',
            options={'ordering': ['name'], 'verbose_name_plural': 'Host plant families'},
        ),
        migrations.AlterModelOptions(
            name='hostplantgenus',
            options={'ordering': ['name'], 'verbose_name_plural': 'Host plant genera'},
        ),
        migrations.AlterModelOptions(
            name='hostplantspecies',
            options={'ordering': ['name'], 'verbose_name_plural': 'Host plant species'},
        ),
        migrations.AddField(
            model_name='hostplantspecies',
            name='lepidoptera_species',
            field=models.ManyToManyField(through='lepidoptera.Observation', to='lepidoptera.Species'),
        ),
    ]