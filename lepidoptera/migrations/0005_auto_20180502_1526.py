# Generated by Django 2.0.3 on 2018-05-02 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0004_photographer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photographer',
            options={'ordering': ('full_name',)},
        ),
        migrations.AddField(
            model_name='speciespicture',
            name='photographer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lepidoptera.Photographer'),
        ),
    ]
