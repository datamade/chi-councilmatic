#!/bin/sh
set -e

pip install -e /postgres-fts-backend

if [ "$DJANGO_MANAGEPY_MIGRATE" = "True" ]; then
    python manage.py migrate --noinput
fi

exec "$@"
