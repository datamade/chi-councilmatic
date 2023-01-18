# 👀 Chicago Councilmatic

Chicago Councilmatic tracks all things related to Chicago City Council: the legislation introduced and passed, its various committees and the meetings they hold, and the aldermen themselves.

You can search and browse legislation from 2011 onwards. Some interesting searches include:

- changes in how properties are zoned
- what the City is paying out in settlements
- committee appointments
- celebrating birthdays?!

Chicago Councilmatic is a free and easy way to access official Chicago City Council information.

## Production data and SQLite archive

If you'd like to explore the data for Chicago Councilmatic yourself, we make a SQLite database using [Datasette](https://datasette.io/) available here: https://puddle.bunkum.us/chicago_council. This data is updated nightly.

The data updates for the production instance of this site is done with GitHub actions in the https://github.com/datamade/chicago-council-scrapers repository. Data is also updated nightly.

## Setup

These days, we run apps in containers for local development. Prefer to run the
app locally? See the [legacy setup instructions](https://github.com/datamade/chi-councilmatic/blob/2e56e03cd689495899d8675ee97a65f672274cb9/README.md#setup).

### Install OS level dependencies:

- [Docker](https://www.docker.com/get-started)

### Run the application

```bash
docker-compose up
```

### Load in the data

Chicago Councilmatic needs to data work properly and the database is quite large (several GB). You can either restore from another database (faster) or scrape the data yourself.

#### Option 1: Import data from production

If you have existing data, bring down your existing data & volumes

```bash
docker-compose down --volumes
```

spin up just the postgres container. this will initialize your database

```bash
docker-compose up postgres
```

in a new terminal window, shell into the postgres container

```bash
docker exec -it CONTAINER_ID /bin/bash
psql -d postgres -U postgres
```

in the PSQL interpreter, delete the old database

```sql
DROP DATABASE chi_councilmatic;
```

then, exit out of PSQL and the container. while the postgres container is still running, run the `heroku pg:pull` command to restore the production data to your local database. This will take about an hour.

```bash
PGUSER=postgres PGPASSWORD=postgres PGHOST=127.0.0.1 PGPORT=32001 heroku pg:pull DATABASE_URL chi_councilmatic --app chi-councilmatic-production
```

#### Option 2: Scrape directly from the source

The `docker-compose-scrape.yml` file contains a service to scrape Legistar web API and
populate your database with standardized data on the council and its members,
legislation, and events. The default command scrapes all committees and people,
and any events and legislation updated in the last 30 days or scheduled for a
future date.

To import data:

```bash
docker-compose -f docker-compose-scrape.yml up
```

This may take a few minutes to an hour, depending on the volume of recent
updates! Once it's finished, head over to http://localhost:8000 to view your
shiny new app!

### Optional: Update the search index

If you wish to use search in your local install, add your shiny new data to your
search index with the `rebuild_index` command from Haystack.

```bash
docker-compose run --rm app python manage.py update_index --batch-size=100
```

### Set-up pre-commit

Pre-commit hooks are scripts that run on your local machine before every commit.

We use the [pre-commit](https://pre-commit.com/) framework to run code linters and formatters that keep our codebase clean.

To set up Pre-Commit, install the Python package on your local machine using

```bash
python -m pip install pre-commit
```

If you'd rather not install pre-commit globally, create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) in this repo before running the above command.

Then, run

```bash
pre-commit install
```

to set up the git hooks.

Since hooks are run locally, you can modify which scripts are run before each commit by modifying `.pre-commit-config.yaml`.

## Testing

This app provides a basic set of tests that hit all endpoints for the bills,
people, events, and organizations in your local database and ensure that nothing
breaks. To run them, add some data to your database, as described in
[Load in the data](#load-in-the-data), then run `pytest` via `docker-compose`.

```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

## Team

### Original project team

- David Moore - project manager
- Forest Gregg - Open Civic Data (OCD) and Legistar scraping
- Cathy Deng - data models and loading
- Derek Eder - front end
- Eric van Zanten - search and dev ops

### Maintenance

Chicago Councilmatic is maintained by [the DataMade team](https://datamade.us/team/).

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/chi-councilmatic/issues

## Copyright

Copyright (c) 2015-2020 Participatory Politics Foundation and DataMade. Released
under the [MIT License](https://github.com/datamade/chi-councilmatic/blob/master/LICENSE).
