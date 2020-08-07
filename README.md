# 👀 Chicago Councilmatic

Keep track of what the Chicago City Council is doing.

## Setup

These days, we run apps in containers for local development. Prefer to run the
app locally? See the [legacy setup instructions](https://github.com/datamade/chi-councilmatic/blob/2e56e03cd689495899d8675ee97a65f672274cb9/README.md#setup).

### Install OS level dependencies:

* [Docker](https://www.docker.com/get-started)

### Run the application

```bash
docker-compose up -d app
```

Note that you can omit the `-d` flag to follow the application and service logs.
If you prefer a quieter environment, you can view one log stream at a time with
`docker-compose logs -f SERVICE_NAME`, where `SERVICE_NAME` is the name of one
of the services defined in `docker-compose.yml`, e.g., `app`, `postgres`, etc.

When the command exits (`-d`) or your logs indicate that your app is up and
running, move on to the next step.

### Load in the data

Chicago Councilmatic needs to data work properly.

The `docker-compose.yml` file contains a service to scrape Legistar web API and
populate your database with standardized data on the council and its members,
legislation, and events. The default command scrapes all committees and people,
and any events and legislation updated in the last 30 days or scheduled for a
future date.

To import data, simply run:

```bash
docker-compose run --rm scrapers
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

* David Moore - project manager
* Forest Gregg - Open Civic Data (OCD) and Legistar scraping
* Cathy Deng - data models and loading
* Derek Eder - front end
* Eric van Zanten - search and dev ops

### Maintenance

Chicago Councilmatic is maintained by [the DataMade team](https://datamade.us/team/).

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/chi-councilmatic/issues

## Copyright

Copyright (c) 2015-2020 Participatory Politics Foundation and DataMade. Released
under the [MIT License](https://github.com/datamade/chi-councilmatic/blob/master/LICENSE).
