#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

BUILD="True" 

# Define some environment variables
export IMAGE_NAME="test-cloud-run"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
export GCP_PROJECT="ac215-project" 
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/mega-pipeline.json"


echo "Building image..."
# docker manifest push dlops/$IMAGE_NAME:latest
docker buildx build --platform linux/amd64 -t dlops/$IMAGE_NAME:latest --push .

# Run the container with no auth
# docker run  dlops/test-cloud-run pipenv shell python cli.py --help
# docker run --rm --name $IMAGE_NAME -ti \
# -v "$BASE_DIR":/app \
# dlops/$IMAGE_NAME

# Run the container with auth using secrest file
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
dlops/$IMAGE_NAME
