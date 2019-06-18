import os

from .test_config_jurisdiction import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'super secret key'
OCD_CITY_COUNCIL_NAME = 'Chicago City Council'

INSTALLED_APPS = (
    'chicago',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'debug_toolbar',
    'haystack',
    'councilmatic_core',
    'opencivicdata.core',
    'opencivicdata.legislative',
    'adv_cache_tag',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'councilmatic.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'chicago_councilmatic',
        'USER': '',
        'PASSWORD': '',
        'PORT': 5432,
    }
}

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

STATIC_PATH = ''
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

HAYSTACK_CONNECTIONS = {
    'default': {},
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

USING_NOTIFICATIONS = False
