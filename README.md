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
    
    