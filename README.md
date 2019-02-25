This repository contains the source code of the [Atlas of Lepidoptera of Belgium](http://projects.biodiversity.be/lepidoptera).

![website screenshot](https://raw.githubusercontent.com/BelgianBiodiversityPlatform/catalogue-lepidoptera-belgium-webapp/master/website_screenshot.jpg)


Deployment / Installation
=========================

A. Initial deployment
---------------------

1) Get/clone the code
2) pip install -r requirements.txt
3) Create a (or get a backup of an existing) PostgreSQL database
4) Duplicate settings_local.template.py to settings_local.py and configure the previously created database
5) $ python manage.py migrate
6) $ python manage.py denorm_init
7) $ python manage.py createsuperuser (if needed)
8) (in production:) $ python manage.py collectstatic
9) (in production:) run wsgi server

B. Upgrade
----------

1) Pull the code.
2) $ pip install -r requirements.txt
3) $ python manage.py denorm_drop
4) $ python manage.py denorm_init
5) $ python manage.py migrate
6) $ python manage.py collectstatic
7) restart app server


Customize Bootstrap (colors, ...):
==================================

- Customize variables in static/lepidoptera/bootstrap-custom/scss/custom.scss (requires an installed version of Bootstrap 4.1)
- Compile it to static/lepidoptera/bootstrap-custom/scss/custom.css
