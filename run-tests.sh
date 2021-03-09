#!/bin/bash

set -e

export DJANGO_SETTINGS_MODULE=config.settings.test
export ICMS_DEBUG=False

#docker-compose run --rm web pytest --tb=short --cov=web --cov=config --cov-report xml:test-reports/cov.xml --dist=loadfile --tx=4*popen "$@"
docker-compose run --rm web pytest --tb=short --cov=web --cov=config --cov-report html:test-reports/cov.html --dist=loadfile --tx=4*popen "$@"
