# Generated by Django 2.1 on 2018-09-07 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0007_remove_hostplantspecies_genus_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostplantspecies',
            name='genus_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
