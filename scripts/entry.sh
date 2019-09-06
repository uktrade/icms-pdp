#!/bin/sh -e
ICMS_WEB_PORT="${ICMS_WEB_PORT:-8080}"
ICMS_DEBUG="${ICMS_DEBUG:-False}"
ICMS_MIGRATE="${ICMS_MIGRATE:-True}"
ICMS_NUM_WORKERS="${ICMS_NUM_WORKERS:-3}"

#while true; do sleep 10000; done
#sleep infinity

echo "ICMS running now with debug $ICMS_DEBUG"

pip install pipenv

if [ "${ICMS_MIGRATE}" = 'True' ]; then
  echo "Running migrations"
  pipenv run python manage.py migrate
  pipenv run python manage.py loaddata --app web web/fixtures/web/*.json
fi

# Run webpack which bundles javascript in production mode
npm run deploy

if [ "$ICMS_DEBUG" = 'False' ]; then
  pipenv run python manage.py collectstatic --noinput --traceback
fi


if [ "$ICMS_DEBUG" = 'True' ]; then
  pipenv run python manage.py runserver 0:"$ICMS_WEB_PORT"
else
  gunicorn config.wsgi \
           --name icms \
           --workers "$ICMS_NUM_WORKERS" \
           --bind 0:"$ICMS_WEB_PORT"
fi
