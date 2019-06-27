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

There are tens of thousands of bills and hundreds of events in Chicago legislative history. If you'd like import everything, set aside about an hour, then run:

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

## Setup Search

**Install Open JDK or update Java**

On Ubuntu:

``` bash
$ sudo apt-get update
$ sudo apt-get install openjdk-7-jre-headless
```

On OS X:

1. Download latest Java from
[http://java.com/en/download/mac_download.jsp?locale=en](http://java.com/en/download/mac_download.jsp?locale=en)
2. Follow normal install procedure
3. Change system Java to use the version you just installed:

    ``` bash
    sudo mv /usr/bin/java /usr/bin/java16
    sudo ln -s /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java /usr/bin/java
    ```

**Download & setup Solr**

``` bash
wget http://mirror.sdunix.com/apache/lucene/solr/4.10.4/solr-4.10.4.tgz
tar -xvf solr-4.10.4.tgz
sudo cp -R solr-4.10.4/example /opt/solr

# Copy schema.xml for this app to solr directory
sudo cp solr_scripts/schema.xml /opt/solr/example/solr/collection1/conf/schema.xml
```

**Run Solr**
```bash
# Next, start the java application that runs solr
# Do this in another terminal window & keep it running
# If you see error output, somethings wrong
cd /opt/solr/example
sudo java -jar start.jar
```

**Index the database**
```bash
# back in the chi-councilmatic directory:
python manage.py rebuild_index
```

**OPTIONAL: Install and configure Jetty for Solr**

Just running Solr as described above is probably OK in a development setting.
To deploy Solr in production, you'll want to use something like Jetty. Here's
how you'd do that on Ubuntu:

``` bash
sudo apt-get install jetty

# Backup stock init.d script
sudo mv /etc/init.d/jetty ~/jetty.orig

# Get init.d script suggested by Solr docs
sudo cp solr_scripts/jetty.sh /etc/init.d/jetty
sudo chown root.root /etc/init.d/jetty
sudo chmod 755 /etc/init.d/jetty

# Add Solr specific configs to /etc/default/jetty
sudo cp solr_scripts/jetty.conf /etc/default/jetty

# Change ownership of the Solr directory so Jetty can get at it
sudo chown -R jetty.jetty /opt/solr

# Start up Solr
sudo service jetty start

# Solr should now be running on port 8983
```

**Regenerate Solr schema**

While developing, if you need to make changes to the fields that are getting
indexed or how they are getting indexed, you'll need to regenerate the
schema.xml file that Solr uses to make it's magic. Here's how that works:

```
python manage.py build_solr_schema > solr_scripts/schema.xml
cp solr_scripts/schema.xml /opt/solr/solr/collection1/conf/schema.xml
```

In order for Solr to use the new schema file, you'll need to restart it.

**Using Solr for more than one Councilmatic on the same server**

If you intend to run more than one instance of Councilmatic on the same server,
you'll need to take a look at [this README](solr_scripts/README.md) to make sure you're
configuring things properly.

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
