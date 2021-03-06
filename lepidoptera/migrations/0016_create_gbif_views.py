# Generated by Django 2.1 on 2018-10-12 09:17

from django.db import migrations

IPT_TAXON_VIEW_DROP = """DROP VIEW ipt_lepidoptera_taxon;"""
IPT_TAXON_VIEW_CREATE = """
CREATE OR REPLACE VIEW ipt_lepidoptera_taxon AS (
    SELECT
  lepidoptera_species.id AS "taxonID",
  lepidoptera_species.last_modified::date AS "modified",
  'species' AS "taxonRank",
  'Host plant / substrate data / life stage details / ... are also available, see https://projects.biodiversity.be/lepidotera' AS "informationWithheld",
  CONCAT ('https://projects.biodiversity.be/lepidoptera/species/', lepidoptera_species.id) AS "references",
  lepidoptera_species.name AS "specificepithet",
  --- scientificName
  CASE WHEN lepidoptera_species.subgenus_id IS NOT NULL THEN lepidoptera_subgenus.genus_name
    ELSE lepidoptera_genus.name
  END AS "genus",

  CONCAT(
      CASE WHEN lepidoptera_species.subgenus_id IS NOT NULL THEN lepidoptera_subgenus.genus_name ELSE lepidoptera_genus.name END,
      ' ',
      lepidoptera_species.name,
      ' ',
      lepidoptera_species.author) AS "scientificName",

  CASE
    WHEN lepidoptera_species.subgenus_id IS NOT NULL THEN (SELECT family_name
                                                           FROM lepidoptera_genus
                                                           WHERE lepidoptera_genus.id = lepidoptera_subgenus.genus_id)
    ELSE
    (SELECT family_name
      FROM lepidoptera_genus
      WHERE lepidoptera_genus.id = lepidoptera_species.genus_id)
  END
  AS "family",

  lepidoptera_subgenus.name AS "subgenus",
  'Lepidoptera' AS "order",
  'Insecta' AS "class",
  'Animalia' AS "kingdom",
  lepidoptera_species.author AS "scientificNameAuthorship",
  'en' AS "language",
  lepidoptera_species.text_en AS "taxonRemarks",
  lepidoptera_species.synonym_of_id AS acceptedNameUsageID,
  CASE
    WHEN lepidoptera_species.synonym_of_id IS NOT NULL THEN
      'synonym'
    ELSE
      'accepted'
    END
  AS "taxonomicStatus"

FROM
  lepidoptera_species
LEFT JOIN lepidoptera_genus
    ON lepidoptera_species.genus_id = lepidoptera_genus.id
LEFT JOIN  lepidoptera_subgenus
    ON lepidoptera_species.subgenus_id = lepidoptera_subgenus.id

);
"""

IPT_DISTRIBUTION_VIEW_CREATE = """
CREATE OR REPLACE VIEW ipt_lepidoptera_distribution AS (
SELECT
  species_id AS "taxonID",
  CONCAT(lepidoptera_province.name, ' province') AS "locality",
  'BE' AS "countryCode",
  lepidoptera_timeperiod.name AS "eventDate",
  'present' AS "occurrenceStatus"
FROM lepidoptera_speciespresence
LEFT JOIN lepidoptera_province ON lepidoptera_speciespresence.province_id = lepidoptera_province.id
LEFT JOIN lepidoptera_timeperiod ON lepidoptera_speciespresence.period_id = lepidoptera_timeperiod.id
WHERE lepidoptera_speciespresence.present = TRUE
);
"""

IPT_DISTRIBUTION_VIEW_DROP = """
DROP VIEW ipt_lepidoptera_distribution;
"""

IPT_VERNACULAR_VIEW_CREATE = """
CREATE OR REPLACE VIEW ipt_lepidoptera_vernacular AS (
(SELECT
  lepidoptera_species.id AS "taxonID",
  lepidoptera_species.vernacular_name_en AS "vernacularName",
  'en' AS "language"
FROM lepidoptera_species
WHERE vernacular_name_en NOT LIKE '')

UNION

(SELECT
lepidoptera_species.id AS "taxonID",
lepidoptera_species.vernacular_name_nl AS "vernacularName",
'nl' AS "language"
FROM lepidoptera_species
WHERE vernacular_name_nl NOT LIKE '')

UNION

(SELECT
lepidoptera_species.id AS "taxonID",
lepidoptera_species.vernacular_name_fr AS "vernacularName",
'fr' AS "language"
FROM lepidoptera_species
WHERE vernacular_name_fr NOT LIKE '')

UNION

(SELECT
lepidoptera_species.id AS "taxonID",
lepidoptera_species.vernacular_name_de AS "vernacularName",
'de' AS "language"
FROM lepidoptera_species
WHERE vernacular_name_de NOT LIKE '')
);

"""

IPT_VERNACULAR_VIEW_DROP = """
DROP VIEW ipt_lepidoptera_vernacular;
"""

IPT_MULTIMEDIA_VIEW_CREATE = """
CREATE OR REPLACE VIEW ipt_lepidoptera_images AS (
SELECT
  species_id AS "taxonID",
  'Stillimage' AS "type",
  CONCAT ('https://projects.biodiversity.be/lepidoptera/media/', image) AS identifier,
  comment AS description,
  full_name AS creator,
  full_name AS "rightsHolder"

FROM lepidoptera_speciespicture
LEFT JOIN lepidoptera_photographer l on lepidoptera_speciespicture.photographer_id = l.id
);
"""

IPT_MULTIMEDIA_VIEW_DROP = """
DROP VIEW ipt_lepidoptera_images;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('lepidoptera', '0015_populate_family_name'),
    ]

    operations = [
        migrations.RunSQL(sql=IPT_TAXON_VIEW_CREATE, reverse_sql=IPT_TAXON_VIEW_DROP),
        migrations.RunSQL(sql=IPT_DISTRIBUTION_VIEW_CREATE, reverse_sql=IPT_DISTRIBUTION_VIEW_DROP),
        migrations.RunSQL(sql=IPT_VERNACULAR_VIEW_CREATE, reverse_sql=IPT_VERNACULAR_VIEW_DROP),
        migrations.RunSQL(sql=IPT_MULTIMEDIA_VIEW_CREATE, reverse_sql=IPT_MULTIMEDIA_VIEW_DROP),
    ]
