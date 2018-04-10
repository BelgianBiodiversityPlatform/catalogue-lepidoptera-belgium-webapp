# Generated by Django 2.0.3 on 2018-03-28 12:20

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0003_auto_20180322_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genus',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genus',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genus',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genus',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='species',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='species',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='species',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='species',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subfamily',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subfamily',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subfamily',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subfamily',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subgenus',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subgenus',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subgenus',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subgenus',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tribus',
            name='text_de',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tribus',
            name='text_en',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tribus',
            name='text_fr',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tribus',
            name='text_nl',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]