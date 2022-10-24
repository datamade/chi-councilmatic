#!/bin/sh
set -e

if [ "$DJANGO_MANAGEPY_MIGRATE" = "True" ]; then
    python manage.py migrate --noinput
fi

exec "$@"
