Data extracted from the [Lepidoptera Atlas](http://www.phegea.org/Checklists/Lepidoptera/LepMain.htm)
Contents of the zip file:
* readme.md: this file
* LAFamilies.csv: the Family table
* LALiterature.csv: Literature references
* LASpecies.csv: Species table

# LAFamilies.csv
The Family table contains:
* family: the family name
* description: text describing the family
* identification: list of literature references
* nomenclature: nomenclature used for this family

# LALiterature.csv
The Literature table contains:
* code: primary key
* text: text of this reference
* markdown: the same text with, some markdown highlights

# LASpecies.csv
The Species table contains:
* family : foreign key to Families table
* code : species code, only present if a species page exists on Lepidoptera Atlas
* sName : Scientific name with authorship
* oName : Other names, list of synonyms separated by =
* Presences in Belgian Provinces, values 1 to 7 (see below)
  * WV: West-Vlaanderen
  * OV: Oost-Vlaanderen
  * AN: Antwerpen
  * LI: Limburg
  * BR: Brabant
  * HA: Hainaut
  * NA: Namur
  * LG: Liège
  * LX: Luxembourg

These values denote the presence of the species over three periods (before 1980, 1980-2004, after 2004) as follows:
1. Only present before 1980
2. present before 2004
3. Only present between 1980 and 2004
4. present since 1980
5. present during the 3 periods
6. present before 1980 and after 2004
7. Only present after 2004
