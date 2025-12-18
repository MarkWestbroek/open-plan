#!/bin/sh
#
# Generate the API schema from the code into the output file.
#
# Run this script from the root of the repository:
#
#   ./bin/generate_api_schema.sh
#

src/manage.py spectacular \
    --validate \
    --fail-on-warn \
    --lang=nl \
    --urlconf openplan.plannen.api.urls \
    --file src/plan-openapi.yaml \
    --custom-settings openplan.plannen.api.urls.custom_settings