from django.conf import settings

import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
	    'default': {
	        'ENGINE': 'django.contrib.gis.db.backends.postgis',
	        'NAME': 'chicago_councilmatic',
	        'USER': '',
	        'PASSWORD': '',
	        'PORT': 5432,
	    }
	}
