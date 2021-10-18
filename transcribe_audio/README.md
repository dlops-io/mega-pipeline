# Transcribe Audio
---
🎙️ &rightarrow; 📝 

In this container you will implement the following:
* Read audio files from the GCS bucket `mega-pipeline-bucket` and folder `input_audios`
* Use the Google Cloud Speech to Text API
* Save the transcribed text as text file in bucket `mega-pipeline-bucket` and folder `text_prompts` (use the same file name and change extension to .txt)

### GCP Credentials File
* Download the `mega-pipeline.json` from Ed and save it inside the `secrets` folder

### Create Dockerfile
* Create a `Dockerfile` and base it from `python:3.8-slim-buster` the official Debian-hosted Python 3.8 image
* Set the following environment variables:
```
ENV PYENV_SHELL=/bin/bash
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```

* Ensure we have an up to date baseline, install dependencies by running
```
apt-get update
apt-get upgrade -y
apt-get install -y --no-install-recommends build-essential git ffmpeg
```

* Install pipenv
* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`


### Docker Build & Run
* You should be able to build your docker image by using:
```
docker build -t transcribe_audio -f Dockerfile .
```
* You should be able to run your docker image by using:
```
docker run --rm -ti --mount type=bind,source=$BASE_DIR,target=/app transcribe_audio
```

### CLI to interact with your code
* Add a python file `cli.py`

### Push Container to Docker Hub
