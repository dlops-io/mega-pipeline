#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

BUILD="True" 

# Define some environment variables
# Use this if you are planning to build the container
export IMAGE_NAME="mega-pipeline-synthesis-audio"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
 
# export PERSISTENT_DIR=$(pwd)/../persistent-folder/


 
if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    #docker build -t $IMAGE_NAME -f Dockerfile .
    # docker buildx build --platform linux/amd64 -t dlops/$IMAGE_NAME:amd64 --push .
    # docker buildx build --platform linux/arm64 -t dlops/$IMAGE_NAME:arm64 --push .
    # docker manifest create dlops/$IMAGE_NAME:latest \
    #     dlops/$IMAGE_NAME:amd64 \
    #     dlops/$IMAGE_NAME:arm64

    # docker manifest push dlops/$IMAGE_NAME:latest

    # docker manifest push dlops/$IMAGE_NAME:latest
    docker buildx build --platform linux/amd64 -t dlops/$IMAGE_NAME:latest --push .

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
