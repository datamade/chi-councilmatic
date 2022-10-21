"""
Django settings for councilmatic project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

import dj_database_url

from .settings_jurisdiction import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False if os.getenv('DJANGO_DEBUG', True) == 'False' else True
allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', [])
ALLOWED_HOSTS = allowed_hosts.split(',') if allowed_hosts else []

if DEBUG:
    # Add dynamically generated Docker IP
    # Don't do this in production!
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1']

DATABASES = {}

DATABASES['default'] = dj_database_url.parse(
    os.getenv('DATABASE_URL', 'postgis://postgres:postgres@postgres:5432/chi_councilmatic'),
    conn_max_age=600,
    engine='django.contrib.gis.db.backends.postgis',
    ssl_require=True if os.getenv('POSTGRES_REQUIRE_SSL') else False
)

HAYSTACK_CONNECTIONS = {}
HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'URL': os.getenv('HAYSTACK_URL', 'http://elasticsearch:9200'),
        'INDEX_NAME': 'chicago',
        'SILENTLY_FAIL': False,
        'BATCH_SIZE': 10,
    }

cache_backend = 'dummy.DummyCache' if DEBUG is True else 'db.DatabaseCache'
CACHES = {
    'default': {
        'BACKEND': f'django.core.cache.backends.{cache_backend}',
        'LOCATION': 'site_cache',
    }
}


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'chicago',
    'councilmatic_core',
    'opencivicdata.core',
    'opencivicdata.legislative',
    'notifications',
    'django_rq',
    'password_reset',
    'adv_cache_tag',
)

try:
    INSTALLED_APPS += EXTRA_APPS
except NameError:
    pass

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'councilmatic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'councilmatic_core.views.city_context',
            ],
        },
    },
]



WSGI_APPLICATION = 'councilmatic.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_ETAGS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Preserve default loggers
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    }
}
