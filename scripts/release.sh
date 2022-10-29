#!/bin/bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py import_shapes data/final/shapes/chicago_shapes.json
python manage.py collectstatic --noinput
python manage.py createcachetable
python manage.py clear_cache