Initial data populate
=====================

- Taxonomic data comes from the access database
- Other data (distribution, ...) should be extracted from http://www.phegea.org/Checklists/Lepidoptera/Lepmain.htm
(an extracted version is in initial_data/previous_website_12jan2018, but it's better to use the data online, in case of 
updates)
- Finally, other data (pictures, ...) may be provided by the curators.

=> All this data should be reconciled in Django's database.

Deployment
==========

Create a Postgres database and reference it in settings.