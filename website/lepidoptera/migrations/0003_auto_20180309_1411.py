# Generated by Django 2.0.2 on 2018-03-09 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0002_auto_20180307_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostPlantFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('verbatim_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HostPlantGenus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('verbatim_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.HostPlantFamily')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HostPlantSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('verbatim_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('genus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.HostPlantGenus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_genus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.HostPlantGenus')),
                ('plant_species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.HostPlantSpecies')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Species')),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='observation',
            name='substrate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Substrate'),
        ),
    ]
