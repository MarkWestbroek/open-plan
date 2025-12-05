#!/bin/bash
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openplan-flower}"

exec celery flower --app openplan --workdir src
