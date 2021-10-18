# Transcribe Audio

🎙️ &rightarrow; 📝 

In this container you will implement the following:
* Read audio files from the GCS bucket `mega-pipeline-bucket` and folder `input_audios`
* Use the Google Cloud Speech to Text API
* Save the transcribed text as text file in bucket `mega-pipeline-bucket` and folder `text_prompts` (use the same file name and change extension to .txt)

### Prerequisites for Development
* Have Docker Desktop installed
* Check that your Docker is running with the following command
`docker run hello-world`
### Install VSCode  
Follow the [instructions](https://code.visualstudio.com/download) for your operating system.  
If you already have a preferred text editor, skip this step.  

### Project Setup

* Create a folder `transcribe_audio`

### GCP Credentials File
* Download the `mega-pipeline.json` from Ed and save it inside a folder called `secrets` inside `transcribe_audio`

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
docker run --rm -ti --mount type=bind,source=$(pwd),target=/app transcribe_audio
```
* The `--mount type=bind,source=$(pwd)` option is to mount your current working directory into the `/app` directory inside the container. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### CLI to interact with your code
* Add a python file `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-t] [-u]

Transcribe audio file to text

optional arguments:
  -h, --help        show this help message and exit
  -d, --download    Download audio files from GCS bucket
  -t, --transcribe  Transcribe audio files to text
  -u, --upload      Upload transcribed text to GCS bucket
```

### Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag transcribe_audio <USER NAME>/transcribe_audio`
* Push to Docker Hub: `docker push <USER NAME>/transcribe_audio`

