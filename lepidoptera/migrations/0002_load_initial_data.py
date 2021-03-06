# Generated by Django 2.0.6 on 2018-07-12 07:28

import os
from django.core.files import File
from django.db import migrations
from django.conf import settings


def populate_all(apps, schema_editor):
    populate_provinces(apps, schema_editor)
    populate_page_fragments(apps, schema_editor)
    populate_timeperiods(apps)


def _create_timeperiod(apps, source_file_path, destination_file_name, period_name):
    # source_file_path is relative to settings.BASE_DIR
    TimePeriod = apps.get_model('lepidoptera', 'TimePeriod')

    with open(os.path.join(settings.BASE_DIR, source_file_path), 'rb') as f:
        icon_data = File(f)

        tp = TimePeriod()
        tp.name = period_name
        tp.icon.save(destination_file_name, icon_data)
        tp.save()


def populate_timeperiods(apps):
    from ..models import TimePeriod as TPDirect  # Normally we should import with apps.get_model, but constants don't work

    _create_timeperiod(apps, '../populate_data/before_1980.png', 'before_1980.png', TPDirect.BEFORE_1980_NAME)
    _create_timeperiod(apps, '../populate_data/1980_2004.png', '1980_2004.png', TPDirect.BETWEEN_1980_2004_NAME)
    _create_timeperiod(apps, '../populate_data/after_2004.png', 'after_2004.png', TPDirect.SINCE_2004_NAME)


def populate_page_fragments(apps, schema_editor):
    PageFragment = apps.get_model('lepidoptera', 'PageFragment')

    PageFragment.objects.create(identifier='welcome',
                                content_nl="""
Welkom!
-------

**Lorem ipsum dolor sit amet**, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum""",
                                content_fr="""
Bienvenue !
-----------

**Lorem ipsum** dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore """,
                                content_en="""
Welcome!
--------

**Lorem ipsum** dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
""")

    about_page_text = """
History of site/catalogue
-------------------------

Disclaimer
----------

How to cite
-----------
"""
    PageFragment.objects.create(identifier='about_page_content',
                                content_nl=about_page_text,
                                content_fr=about_page_text,
                                content_en=about_page_text,
                                content_de=about_page_text)

def populate_provinces(apps, schema_editor):
    Province = apps.get_model('lepidoptera', 'Province')

    Province.objects.create(name="West-Vlaanderen", code="WV", order=1, historical=False, recent=False,
                            polygon_reference=6)
    Province.objects.create(name="Oost-Vlaanderen", code="OV", order=5, historical=False, recent=False,
                            polygon_reference=4)
    Province.objects.create(name="Antwerpen", code="AN", order=10, historical=False, recent=False,
                            polygon_reference=2)
    Province.objects.create(name="Limburg", code="LI", order=15, historical=False, recent=False,
                            polygon_reference=10)
    Province.objects.create(name="Vlaams Brabant", code="VB", order=17, historical=False, recent=True,
                            polygon_reference=5)
    Province.objects.create(name="Brabant", code="BR", order=20, historical=True, recent=False,
                            polygon_reference=13)
    Province.objects.create(name="Brabant Wallon", code="BW", order=23, historical=False, recent=True,
                            polygon_reference=7)
    Province.objects.create(name="Hainaut", code="HA", order=25, historical=False, recent=False,
                            polygon_reference=8)
    Province.objects.create(name="Namur", code="NA", order=30, historical=False, recent=False,
                            polygon_reference=12)
    Province.objects.create(name="Liège", code="LG", order=35, historical=False, recent=False,
                            polygon_reference=9)
    Province.objects.create(name="Luxembourg", code="LX", order=40, historical=False, recent=False,
                            polygon_reference=11)


class Migration(migrations.Migration):
    dependencies = [
        ('lepidoptera', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_all),
    ]

