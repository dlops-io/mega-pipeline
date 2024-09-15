#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="mega-pipeline-transcribe-audio"
export BASE_DIR=$(pwd)
# export SECRETS_DIR=$(pwd)/../secrets/
# export PERSISTENT_DIR=$(pwd)/../persistent-folder/
# export GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
--mount type=bind,source="$BASE_DIR",target=/app $IMAGE_NAME