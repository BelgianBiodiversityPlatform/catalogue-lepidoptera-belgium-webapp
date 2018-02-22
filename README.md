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
5) $ python manage.py createsuperuser)
6) (in production:) $ python manage.py collectstatic
7) (in production:) $ run wsgi server

B. data populate
----------------
    
1) Import (converted) Access DB:

    $ psql -d <DATABASE_NAME> -f initial_data/access/converted/CatLepBelgium_be.sql
    
$ python manage.py access_import
$ python manage.py website_import initial_data/website_extract_andre/LepidopteraAtlas/LAFamilies.csv
    
To discuss with team
====================

- Show the page fragment mechanism/markdown and ask if ok
- Family overview on home page: vernacular name always id Dutch? Or current language with Dutch fallback? Something else?
- On home page: what's new... Should it be a simple block of text :(
- Show dynamic counters in footer
- Ask if all taxonomic models should be "orderable" (prev/next)?
- Ask if the species presence in a province should be markable as unknown
- Show reconciliation (website script) so they have a better idea of how all that works.

To ask very soon to Willy:
==========================

- In Access DB, we have duplicates speciesNumber for (2 records for each):
450010011
450010020
300010151
250110250
450010010
901040010
601210010

- In website_import, we don't import the Family description if there's already something in the text field. IS it correct? 
Or maybe we can import in all case if data is better on website than in Access?


Data issues to solve on/before launch
=====================================

- Willy should set a representative picture for each family.
- As we decided to ignore them, Willy needs to manually check (and enter if necessary) the families from the website 
that don't appear in the Access database (list is given my website_import.py script, but as of Feb. 16, it is: Acrolepiidae, 
Agonoxenidae, Amphisbatidae, Arctiidae, Chimabachidae, Depressariidaeare, Eriocraniidaeare, Ethmiidae, Lemoniidae, Lymantriidae, 
Nolidaeare, Thaumetopoeidae)
- I decided to drop (not import from access the species and genus "UNKNOWN"). Confirm it's fine...

