#!/bin/bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py import_shapes data/final/shapes/chicago_shapes.json
python manage.py collectstatic --noinput