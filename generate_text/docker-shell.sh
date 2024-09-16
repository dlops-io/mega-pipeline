#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

BUILD="False" 

# Define some environment variables
# Use this if you are planning to build the container
export IMAGE_NAME="mega-pipeline-generate-text"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
 
# export PERSISTENT_DIR=$(pwd)/../persistent-folder/
# export GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json

# If you want to build the image based on the Dockerfile, uncomment this
 
if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    docker build -t $IMAGE_NAME -f Dockerfile .

    # Run the container
    docker run --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app -v "$SECRETS_DIR":/secrets $IMAGE_NAME
fi

if [ "$BUILD" != "True" ]; then 
    echo "Using prebuilt image..."
    # Run the container
    docker run --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app -v "$SECRETS_DIR":/secrets  dlops/$IMAGE_NAME
fi
