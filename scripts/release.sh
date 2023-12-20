#!/bin/bash

if [ -n "${PRODUCTION}" ]; then
    echo "PRODUCTION is set, running setup management commands"

    python manage.py migrate --noinput
    python manage.py import_shapes data/final/chicago_shapes.geojson
    python manage.py populate_person_statistics
    python manage.py collectstatic --noinput
    python manage.py createcachetable
    python manage.py clear_cache

else
    echo "PRODUCTION is not set, skipping setup management commands"
fi
