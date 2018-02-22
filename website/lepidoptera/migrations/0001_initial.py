# Generated by Django 2.0.2 on 2018-02-22 08:56

from django.db import migrations, models
import django.db.models.deletion
import lepidoptera.models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_family_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('representative_picture', models.ImageField(blank=True, null=True, upload_to='family_representative_pictures')),
            ],
            options={
                'verbose_name_plural': 'families',
            },
            bases=(lepidoptera.models.DisplayOrderNavigable, models.Model),
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_genus_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Family')),
            ],
            options={
                'verbose_name_plural': 'genera',
            },
            bases=(lepidoptera.models.ParentForAdminListMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PageFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(unique=True)),
                ('content_nl', markdownx.models.MarkdownxField(blank=True)),
                ('content_en', markdownx.models.MarkdownxField(blank=True)),
                ('content_fr', markdownx.models.MarkdownxField(blank=True)),
                ('content_de', markdownx.models.MarkdownxField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('order', models.IntegerField(help_text='In presence tables: order in which the provinces are displayed', unique=True)),
                ('historical', models.BooleanField(help_text="The province doesn't exists anymore")),
                ('recent', models.BooleanField(help_text='The province was created at province split')),
                ('polygon_reference', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_species_number', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('genus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Genus')),
            ],
            options={
                'verbose_name_plural': 'species',
            },
            bases=(lepidoptera.models.ParentForAdminListMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SpeciesPresence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbatim_status_id', models.IntegerField(help_text='From the Access database', unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Subfamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_subfamily_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Family')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status')),
            ],
            options={
                'verbose_name_plural': 'subfamilies',
            },
        ),
        migrations.CreateModel(
            name='Subgenus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_subgenus_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('genus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Genus')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status')),
            ],
            options={
                'verbose_name_plural': 'subgenera',
            },
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='time_period_icons')),
            ],
        ),
        migrations.CreateModel(
            name='Tribus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('vernacular_name', models.CharField(blank=True, max_length=255)),
                ('vernacular_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('vernacular_name_nl', models.CharField(blank=True, max_length=255, null=True)),
                ('text', markdownx.models.MarkdownxField(blank=True)),
                ('display_order', models.IntegerField(unique=True)),
                ('verbatim_tribus_id', models.IntegerField(blank=True, help_text='From the Access database', null=True, unique=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status')),
                ('subfamily', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Subfamily')),
            ],
            options={
                'verbose_name_plural': 'tribus',
            },
        ),
        migrations.AddField(
            model_name='speciespresence',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.TimePeriod'),
        ),
        migrations.AddField(
            model_name='speciespresence',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Province'),
        ),
        migrations.AddField(
            model_name='speciespresence',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Species'),
        ),
        migrations.AddField(
            model_name='species',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status'),
        ),
        migrations.AddField(
            model_name='species',
            name='subgenus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Subgenus'),
        ),
        migrations.AddField(
            model_name='species',
            name='synonym_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='lepidoptera.Species'),
        ),
        migrations.AddField(
            model_name='genus',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status'),
        ),
        migrations.AddField(
            model_name='genus',
            name='subfamily',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Subfamily'),
        ),
        migrations.AddField(
            model_name='genus',
            name='synonym_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='lepidoptera.Genus'),
        ),
        migrations.AddField(
            model_name='genus',
            name='tribus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Tribus'),
        ),
        migrations.AddField(
            model_name='family',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Status'),
        ),
        migrations.AlterUniqueTogether(
            name='speciespresence',
            unique_together={('species', 'province', 'period')},
        ),
    ]
