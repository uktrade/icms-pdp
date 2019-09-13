#!/bin/bash -xe

ICMS_WEB_PORT="${ICMS_WEB_PORT:-8080}"
ICMS_DEBUG="${ICMS_DEBUG:-False}"
ICMS_MIGRATE="${ICMS_MIGRATE:-True}"
ICMS_NUM_WORKERS="${ICMS_NUM_WORKERS:-3}"

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn config.wsgi \
         --name icms \
         --workers "$ICMS_NUM_WORKERS" \
         --bind 0:"$ICMS_WEB_PORT"