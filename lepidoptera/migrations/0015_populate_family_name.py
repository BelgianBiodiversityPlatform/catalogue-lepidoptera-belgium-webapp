# Generated by Django 2.1 on 2018-10-12 09:17

from django.db import migrations


def noop(apps, schema_editor):
    pass


def make_sure_family_name_populated(apps, schema_editor):
    # The Genus model was recently added a new family_name denormalized field. We
    # should make sure it's initially populated before we create the views that will
    # expose its content. Therefore, we update all Genus entries...
    Genus = apps.get_model('lepidoptera', 'Genus')

    [g.save() for g in Genus.objects.all()]


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0014_auto_20181005_1242'),
    ]

    operations = [
        migrations.RunPython(make_sure_family_name_populated, noop),
    ]
