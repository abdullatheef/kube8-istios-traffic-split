#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build images with absolute paths
cd "$SCRIPT_DIR/../backend/to_do_backend/" && docker build -f CeleryDockerfile -t my-celery-image .
cd "$SCRIPT_DIR/../backend/to_do_backend/" && docker build -t my-django-image .
cd "$SCRIPT_DIR/../frontend/" && docker build -t my-nginx-image .
