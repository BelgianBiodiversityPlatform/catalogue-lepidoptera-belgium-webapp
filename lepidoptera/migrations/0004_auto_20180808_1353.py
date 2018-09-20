# Generated by Django 2.0.8 on 2018-08-08 11:53

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0003_auto_20180807_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='genitalia_section_text',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
        migrations.AlterField(
            model_name='speciespicture',
            name='image_subject',
            field=models.CharField(choices=[('MUSEUM_SPECIMEN', 'Museum specimen'), ('IN_VIVO_SPECIMEN', 'In Vivo Specimen'), ('PRE_ADULT_STAGE', 'Pre-adult stage'), ('HOST_PLANT', 'Host plant'), ('BIONOMICS', 'Bionomics'), ('HABITAT', 'Habitat'), ('GENITALIA', 'Genitalia')], max_length=20),
        ),
    ]