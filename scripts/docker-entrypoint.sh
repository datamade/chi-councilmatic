#!/bin/sh
set -e

if [ "$DJANGO_MANAGEPY_MIGRATE" = "True" ]; then
    python manage.py migrate --noinput
    python manage.py import_shapes data/final/shapes/chicago_shapes.json
    python manage.py collectstatic
fi

exec "$@"
