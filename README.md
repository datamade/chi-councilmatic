# Chicago Councilmatic

Keep track of what Chicago City Council is doing.

## Setup

**Install OS level dependencies:**

* Python 3.4
* PostgreSQL 9.4 +

**Install app requirements**

We recommend using [virtualenv](https://virtualenv.readthedocs.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up,

```bash
mkvirtualenv chi-councilmatic
git clone https://github.com/datamade/chi-councilmatic.git
cd chi-councilmatic
pip install -r requirements.txt
```

Afterwards, whenever you want to use this virtual environment to work on chi-councilmatic, run `workon chi-councilmatic`

**OPTIONAL: install django-councilmatic locally**
If you plan on making changes to core councilmatic features (as opposed to Chicago-specific stuff), you'll want to install django-councilmatic locally instead of installing from pypi.

```bash
cd ..
git clone https://github.com/datamade/django-councilmatic.git
cd django-councilmatic
pip install -e .
pip install -r tests/requirements.txt
cd ../chi-councilmatic
```

**Create your settings file**

```bash
cp councilmatic/settings_deployment.py.example councilmatic/settings_deployment.py
```

Then edit `councilmatic/settings_deployment.py`:
- `DATABASES['default']['USER']` should be your username
- if you're setting up councilmatic for local development, use a dummy cache by setting `CACHES['default']['BACKEND']` to `'django.core.cache.backends.dummy.DummyCache'`. if you're deploying, leave it as is

**Setup your database**

Before we can run the website, we need to create a database.

```bash
createdb chi_councilmatic
psql -d chi_councilmatic -c "create extension postgis"
```

Then, run migrations

```bash
python manage.py migrate
```

Create an admin user - set a username & password when prompted

```bash
python manage.py createsuperuser
```

## Importing data

Chicago Councilmatic runs off a database populated by lightly extended [Open Civic Data models](https://github.com/opencivicdata/python-opencivicdata/). DataMade maintains a scraper to fill this database with information from Legistar. To reproduce it locally, first clone the scraper repo and install the requirements:

```bash
cd ..
git clone https://github.com/opencivicdata/scrapers-us-municipal.git
cd scrapers-us-municipal
pip install -r requirements.txt
```

Next, create a settings file for `pupa` –

```bash
touch pupa_settings.py
```

– and add the following settings:

```python
OCD_CITY_COUNCIL_NAME = ''
CITY_COUNCIL_NAME = ''
STATIC_PATH = ''

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'opencivicdata.core.apps.BaseConfig',
    'opencivicdata.legislative.apps.BaseConfig',
    'pupa',
    'councilmatic_core'
)

# Change this if you called your database something different
DATABASE_URL = 'postgres:///chi_councilmatic'
```

Initialize the database, then import the most recent data from Chicago (where most recent == from the last three days).

```bash
pupa dbinit us && pupa update chicago
```

There are tens of thousands of bills and hundreds of events in Chicago legislative history. If you'd like import everything, it'll take about 5 hours, then run:

```bash
pupa update chicago bills window=0 && pupa update chicago events window=0
```

Finally, make sure to load shapes into the database so that Posts can be associated with their corresponding boundaries:

```bash
python manage.py import_shapes data/final/shapes/chicago_shapes.json
```

## Setup CSS, Images, and other static resources
```bash
python manage.py collectstatic
```

## Running Chicago Councilmatic locally

``` bash
python manage.py runserver
```

navigate to http://localhost:8000/

## Setup Search and Redis

```bash
docker-compose up
```

**Index the database**
```bash
# back in the chi-councilmatic directory:
python manage.py rebuild_index
```

For the email notifications to work you need to also be runing
a worker
```bash
python manage.py rqworker
```

## Testing

This app provides a basic set of tests that hit all endpoints for the bills, people, events, and organizations in your local database and ensure that nothing breaks. To run them, add some data to your database, as described in [Importing data](#importing-data), then run `pytest`.

```bash
pytest -sv
```

## Team

* David Moore - project manager
* Forest Gregg - Open Civic Data (OCD) and Legistar scraping
* Cathy Deng - data models and loading
* Derek Eder - front end
* Eric van Zanten - search and dev ops

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/chi-councilmatic/issues

## Copyright

Copyright (c) 2015-17 Participatory Politics Foundation and DataMade. Released under the [MIT License](https://github.com/datamade/chi-councilmatic/blob/master/LICENSE).
