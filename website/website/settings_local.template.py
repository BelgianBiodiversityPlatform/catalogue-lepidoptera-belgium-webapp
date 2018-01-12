# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'belgium_lepidoptera',
        'HOST': 'localhost',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXXXXX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []