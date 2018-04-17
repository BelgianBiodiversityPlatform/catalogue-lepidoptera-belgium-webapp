# Generated by Django 2.0.3 on 2018-04-13 11:54

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0003_auto_20180412_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='species',
            name='larva_section_text',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='first_mention_link',
            field=models.URLField(blank=True, verbose_name='hyperlink'),
        ),
        migrations.AlterField(
            model_name='species',
            name='first_mention_page',
            field=models.CharField(blank=True, max_length=100, verbose_name='page'),
        ),
        migrations.AlterField(
            model_name='species',
            name='first_mention_publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lepidoptera.Publication', verbose_name='publication'),
        ),
    ]
