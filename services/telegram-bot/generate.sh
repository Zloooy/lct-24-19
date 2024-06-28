#/usr/bin/bash

mkdir -p api

openapi-python-client generate --path ../backend/openapi.yaml --output-path api/backend
openapi-python-client generate --path ../researcher/openapi.yaml --output-path api/researcher


# openapi-generator generate -g python -i ../backend/openapi.yaml -o api/backend
# openapi-generator generate -g python -i ../researcher/openapi.yaml -o api/researcher