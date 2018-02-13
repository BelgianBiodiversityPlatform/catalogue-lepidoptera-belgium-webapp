# Generated by Django 2.0.1 on 2018-02-06 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0005_genus'),
    ]

    operations = [
        migrations.AddField(
            model_name='genus',
            name='synonym_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Genus'),
        ),
    ]
