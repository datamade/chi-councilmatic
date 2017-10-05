import os
import types
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('APPLICATION_CONFIG'):
    filename = os.environ['APPLICATION_CONFIG']
else:
    filename = os.path.join(BASE_DIR, 'settings_deployment.py')

config = types.ModuleType('config')
config.__file__  = filename

with open(filename, 'rb') as config_file:
    exec(compile(config_file.read(), filename, 'exec'), config.__dict__)


def getSettingValue(setting, required=True):
    try:
        return getattr(config, setting)
    except AttributeError:
        if required:
            raise ImproperlyConfigured('Expected setting {}" in settings_deployment'.format(setting))
        pass

from .settings_jurisdiction import *

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    '.datamade.us',
    '.councilmatic.org'
]

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
    'notifications',
    'django_rq',
    'password_reset',
    'adv_cache_tag',
)

try:
    INSTALLED_APPS += config.EXTRA_APPS
except AttributeError:
    pass

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_ETAGS = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Uncomment for HTTPS sites
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# os.environ['HTTPS'] = "on"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# os.environ['wsgi.url_scheme'] = 'https'

# All the secret & dynamic stuff ...

SECRET_KEY = getSettingValue('SECRET_KEY')
DEBUG = getSettingValue('DEBUG')
DATABASES = getSettingValue('DATABASES')
HAYSTACK_CONNECTIONS = getSettingValue('HAYSTACK_CONNECTIONS')
CACHES = getSettingValue('CACHES')
FLUSH_KEY = getSettingValue('FLUSH_KEY')
DISQUS_SHORTNAME = getSettingValue('DISQUS_SHORTNAME')
ANALYTICS_TRACKING_CODE = getSettingValue('ANALYTICS_TRACKING_CODE')
HEADSHOT_PATH = getSettingValue('HEADSHOT_PATH')

RQ_QUEUES = getSettingValue('RQ_QUEUES')

#RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers
RQ_SHOW_ADMIN_LINK = getSettingValue('RQ_SHOW_ADMIN_LINK')

EMAIL_HOST = getSettingValue('EMAIL_HOST')
EMAIL_PORT = getSettingValue('EMAIL_PORT')
EMAIL_USE_TLS = getSettingValue('EMAIL_USE_TLS')
EMAIL_HOST_USER = getSettingValue('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=getSettingValue('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL=getSettingValue('DEFAULT_FROM_EMAIL')

LOGGING=getSettingValue('LOGGING')
