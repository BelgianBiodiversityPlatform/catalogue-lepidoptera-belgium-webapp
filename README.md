This repository contains the source code of the [Atlas of Lepidoptera of Belgium](http://projects.biodiversity.be/lepidoptera).

Deployment / Installation
=========================

A. Configuration
----------------

1) Get/clone the code
2) Create a (or get a backup of a) PostgreSQL database
3) Duplicate settings_local.template.py to settings_local.py and configure the previously created database
4) $ python manage.py migrate
5) $ python manage.py denorm_init
6) $ python manage.py createsuperuser (if needed)
7) (in production:) $ python manage.py collectstatic
8) (in production:) run wsgi server

Tip: Sparql to get Wikidata info on a family:
=============================================

SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label "Eriocraniidae"@en.
  ?item wdt:P105 wd:Q35409.
}

?item wdt:P105 wd:Q35409. => taxon rank is family

Tip: Customize Bootstrap (colors, ...):
=======================================

- Customize variables in static/lepidoptera/bootstrap-custom/scss/custom.scss (requires an installed version of Bootstrap 4.1)
- Compile it to static/lepidoptera/bootstrap-custom/scss/custom.css