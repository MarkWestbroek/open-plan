#!/bin/bash

set -e

LOGLEVEL=${CELERY_LOGLEVEL:-INFO}

export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openplan-scheduler}"

mkdir -p celerybeat

echo "Starting celery beat"
exec celery beat \
    --app openplan \
    -l $LOGLEVEL \
    --workdir src \
    -s ../celerybeat/beat
