# Use the official Debian-hosted Python image
FROM python:3.8-slim-buster

# Tell pipenv where the shell is. 
# This allows us to use "pipenv shell" as a container entry point.
ENV PYENV_SHELL=/bin/bash

# Ensure we have an up to date baseline, install dependencies 
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app

WORKDIR /app

# Add Pipfile, Pipfile.lock
ADD Pipfile Pipfile.lock /app/

RUN pipenv sync

# Source code
ADD . /app

# Entry point
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]