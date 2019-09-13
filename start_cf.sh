#!/bin/bash -xe

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn config.wsgi \
         --name icms \
         --workers "$ICMS_NUM_WORKERS" \
         --bind 0:"$ICMS_WEB_PORT"