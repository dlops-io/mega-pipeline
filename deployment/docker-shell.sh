#!/bin/bash

# set -e

# Read the settings file
source ./env.dev

#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .


docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
--mount type=bind,source="$(pwd)",target=/app \
--mount type=bind,source="$(pwd)/../secrets/",target=/secrets \
--mount type=bind,source="$HOME/.ssh",target=/home/app/.ssh \
--mount type=bind,source="$(pwd)/../api-service",target=/api-service \
--mount type=bind,source="$(pwd)/../frontend",target=/frontend \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE $IMAGE_NAME

