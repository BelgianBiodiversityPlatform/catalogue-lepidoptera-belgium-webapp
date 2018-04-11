Sandbox deployment/commands/...
===============================

- On git push, code is automatically deployed to sandbox.bebif.be/lepidoptera
- (status can be seen in GitLab, in "CI/CD->Jobs")
- $ ssh nnoe@sandbox.bebif.be
- Example manage.py:
    $ source /usr/local/venvs/lepidoptera/bin/activate
    $ cd /usr/local/www/sites/projects.biodiversity.be/lepidoptera/
    $ sudo -u www-lepidoptera DJANGO_SETTINGS_MODULE="website.settings.development" python manage.py check
- Use saltstack to redeploy:
    $ sudo salt-call state.apply webapps.lepidoptera

Sparql to get Wikidata info on a family:
========================================

SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label "Eriocraniidae"@en.
  ?item wdt:P105 wd:Q35409.
}

?item wdt:P105 wd:Q35409. => taxon rank is family


Data sources
============

- Taxonomic data comes from the access database.
- Other data (distribution, ...) is extracted from http://www.phegea.org/Checklists/Lepidoptera/Lepmain.htm
  (Extraction done by André in Go, resulting in CSV data files).
- During the import process, the Wikidata identifiers are added for families (experimental feature, for possible future use)
- Also, pictures provided by the curators. They are attached to the corresponding species thanks to the Species code in filename.


Deployment / Installation
=========================

A. Configuration
----------------

1) Get/clone the code
2) Create a PostgreSQL database
3) Duplicate settings_local.template.py to settings_local.py and configure the previously created database
4) $ python manage.py migrate
5) $ python manage.py denorm_init
6) $ python manage.py createsuperuser)
7) (in production:) $ python manage.py collectstatic
8) (in production:) run wsgi server

B. data populate
----------------
    
1) Import (converted) Access DB into application DB:

    $ psql -d <DATABASE_NAME> -f initial_data/access/converted/CatLepBelgium_be.sql

2) Run Django command to (re)import everything:

    $ python manage.py reimport_everything LAFamilies.csv LASpecies.csv

    (see reimport_everything.py code if you need the individual import commands)
    
To discuss with team
====================

- Role of tblCatalogue?
    - Hold imagoText/CaterpillarText/... => I'll manage on my own
    - Link pictures to those sections? => I'll manage on my own.
- What are the ProvinceID, ProvinceText, PublicationID, FlighPeriodSymbolID fields for?

- Copyright info for specimen pictures? No current place in DB for this...

- Publications: what is pagenumbers (or issue for example) used for?
- Host plant genus page: should we also show lepidoptera species that are inderectly (thru host plant species)?

Meeting 23feb notes:
====================

- What's new on home page. We only need:
    - Some automated counter for new entities (X new photographs and Y new species last month)
    - A free block of text to enter a narrative

 - Journals/litterature info: only from database, no need to import from website
 - Display: last updated: done for taxonomic models, what about others
 

Data issues to solve on/before launch
=====================================

- Willy should set a representative picture for each family.
- As we decided to ignore them, Willy needs to manually check (and enter if necessary) the families from the website 
that don't appear in the Access database (list is given my website_import.py script, but as of Feb. 16, it is: Acrolepiidae, 
Agonoxenidae, Amphisbatidae, Arctiidae, Chimabachidae, Depressariidaeare, Eriocraniidaeare, Ethmiidae, Lemoniidae, Lymantriidae, 
Nolidaeare, Thaumetopoeidae)

Customize Bootstrap (colors, ...)
=================================

- Unfortunately Bootstrap 4 final does not allow simple customisation via _custom.scss anymore (needs package managers and so on).
- We therefore currently use an online tool for this: https://pikock.github.io/bootstrap-magic/
- To update: 
    - import custom-variables-bootstrap.scss in Bootstrap Magic
    - change variables using the editor
    - download SCSS file and replace custom-variable-bootstrap.scss
    - download CSS and replace bootstrap.min.css
