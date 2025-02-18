#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="mega-pipeline-translate-text"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
 
# Default values
DOCKER_USERNAME="dlops"
BUILD_MODE="dev-run"  # Default mode

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  prod      Build production docker image and push to registry"
    echo "  dev       Build development docker image locally"
    echo "  run       Run the container (uses registry image if local not found)"
    echo "  No args   Build development image and run container (default)"
    exit 1
}

# Parse command line arguments
if [ $# -gt 0 ]; then
    case "$1" in
        prod)
            BUILD_MODE="prod"
            ;;
        dev)
            BUILD_MODE="dev"
            ;;
        run)
            BUILD_MODE="run"
            ;;
        -h|--help)
            usage
            ;;
        *)
            usage
            ;;
    esac
fi

echo "Docker Username: $DOCKER_USERNAME, Build Mode: $BUILD_MODE"

# Production build
if [ "$BUILD_MODE" == "prod" ]; then 
    echo "Building production image..."

    # Check if multi-arch builder exists and remove it if it does
    if docker buildx inspect multi-arch >/dev/null 2>&1; then
        echo "Removing existing multi-arch builder..."
        docker buildx rm multi-arch
    fi

    # Setup multi architecture build
    echo "Creating new multi-arch builder..."
    docker buildx create --driver-opt network=host --use --name multi-arch

    # Build for multiple architectures
    echo "Building multi-arch image..."
    docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_USERNAME/$IMAGE_NAME -f Dockerfile .

    # Push
    echo "Pushing multi-arch image to registry..."
    docker buildx build --platform linux/amd64,linux/arm64 --push -t $DOCKER_USERNAME/$IMAGE_NAME -f Dockerfile .

    echo "Production build complete and pushed to registry"

# Development build
elif [ "$BUILD_MODE" == "dev" ] || [ "$BUILD_MODE" == "dev-run" ]; then
    echo "Building development image locally..."

    # Build the image based on the Dockerfile
    docker build -t $IMAGE_NAME -f Dockerfile .
fi

# Run container (either after dev build or standalone)
if [ "$BUILD_MODE" == "run" ] || [ "$BUILD_MODE" == "dev-run" ]; then
    echo "Run Docker container..."

    # Check if local image exists
    if docker image inspect $IMAGE_NAME >/dev/null 2>&1; then
        echo "Using local image..."
        CONTAINER_IMAGE=$IMAGE_NAME
    else
        echo "Local image not found, using image from registry..."
        CONTAINER_IMAGE=$DOCKER_USERNAME/$IMAGE_NAME
    fi

    # Run Container
    docker run --rm --name $IMAGE_NAME -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    $CONTAINER_IMAGE
fi
