#!/bin/bash -xe

ICMS_WEB_PORT="${ICMS_WEB_PORT:-8080}"
ICMS_DEBUG="${ICMS_DEBUG:-False}"
ICMS_MIGRATE="${ICMS_MIGRATE:-True}"
ICMS_NUM_WORKERS="${ICMS_NUM_WORKERS:-3}"

npm run deploy

if [ "${ICMS_MIGRATE}" = 'True' ]; then
  echo "Running migrations"
  python manage.py migrate --noinput
  python manage.py loaddata --app web web/fixtures/web/*.json
fi

if [ "$ICMS_DEBUG" = 'False' ]; then
  python manage.py collectstatic --noinput --traceback
fi

gunicorn config.wsgi \
         --name icms \
         --workers "$ICMS_NUM_WORKERS" \
         --bind 0:"$ICMS_WEB_PORT"