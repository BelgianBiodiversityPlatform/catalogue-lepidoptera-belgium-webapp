# Generated by Django 2.0.13 on 2019-09-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0027_auto_20190913_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plantgenusobservation',
            options={'ordering': ['the_order']},
        ),
        migrations.AlterModelOptions(
            name='substrateobservation',
            options={'ordering': ['the_order']},
        ),
        migrations.AddField(
            model_name='plantgenusobservation',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='substrateobservation',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='plantspeciesobservation',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]