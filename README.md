Data sources
============

- Taxonomic data comes from the access database
- Other data (distribution, ...) should be extracted from http://www.phegea.org/Checklists/Lepidoptera/Lepmain.htm
(an extracted version is in initial_data/previous_website_12jan2018, but it's better to use the data online, in case of 
updates)
- Finally, other data (pictures, ...) may be provided by the curators.


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
    
1) Import (converted) Access DB:

    $ psql -d <DATABASE_NAME> -f initial_data/access/converted/CatLepBelgium_be.sql
    
$ python manage.py access_import
$ python manage.py website_import initial_data/website_extract_andre/LepidopteraAtlas/LAFamilies.csv initial_data/website_extract_andre/LepidopteraAtlas/LASpecies.csv

 or needed before, in config?)
$ python manage.py denorm_rebuild (after all data populate)
    
To discuss with team
====================

- Show the page fragment mechanism/markdown and ask if ok
- On home page: what's new... Should it be a simple block of text :(
- Show dynamic counters in footer
- Ask if all taxonomic models should be "orderable" (prev/next)?
- Ask if the species presence in a province should be markable as unknown
- Show reconciliation (website script) so they have a better idea of how all that works.
- Show validation in admin
- In website_import, we don't import the Family description if there's already something in the text field. IS it correct? 
Or maybe we can import in all case if data is better on website than in Access?
- Word document: what is "families by thumbnails" on start page?

Meeting 23feb notes:
====================

- Species code should be editable (unique I guess), since it's used as a key in other databases
- What's new on home page. We only need:
    - Some automated counter for new entities (X new photographs and Y new species last month)
    - A free block of text to enter a narrative
 - Family descriptions: we can overwrite what's in the database from what's in the website.
 - Imago: it's on species page, there's no need for  global image gallery
 - We need to import/show hosts plants from Access
 - Journals/litterature info: only from database, no need to import from website
 - I Copied 6000 pictures, to be linked with species according to Theo's naming logic
 - Display: last updated only for important models (use Django's history), and display in a way that make clear that the model has been updated, not the page  
 

Data issues to solve on/before launch
=====================================

- Willy should set a representative picture for each family.
- As we decided to ignore them, Willy needs to manually check (and enter if necessary) the families from the website 
that don't appear in the Access database (list is given my website_import.py script, but as of Feb. 16, it is: Acrolepiidae, 
Agonoxenidae, Amphisbatidae, Arctiidae, Chimabachidae, Depressariidaeare, Eriocraniidaeare, Ethmiidae, Lemoniidae, Lymantriidae, 
Nolidaeare, Thaumetopoeidae)
- I decided to drop (not import from access the species and genus "UNKNOWN"). Confirm it's fine...

