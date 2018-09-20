# Take inspiration to create your own settings file. This example is well suited for development.

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'belgium_lepidoptera',
        'HOST': 'localhost',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SOMETHING_RANDOM_AND_SECRET'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# A few specific for django-debug-toolbar, if you use it during development.

INSTALLED_APPS.extend([
    'debug_toolbar',
])

MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware'
])

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

INTERNAL_IPS = ['127.0.0.1']