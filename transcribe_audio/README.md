# Transcribe Audio

🎙️ &rightarrow; 📝 

In this container you will implement the following:
* Read audio files from the GCS bucket `mega-pipeline-bucket` and folder `input_audios`
* Use the Google Cloud Speech to Text API
* Save the transcribed text as text file in bucket `mega-pipeline-bucket` and folder `text_prompts` (use the same file name and change extension to .txt)


### Project Setup

* Create a folder `transcribe_audio` or clone this repo

### GCP Credentials File
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `transcribe_audio`
<a href="https://static.us.edusercontent.com/files/fo4cDM3adnwMlJVUXZXtzcH2" download>mega-pipeline.json</a>

### Create Pipfile & Pipfile.lock files
* Inside the `transcribe_audio` folder create:
* Add `Pipfile` with a the following contents:
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

* Add `Pipfile.lock` with a the following contents:
```
{
    "_meta": {
        "hash": {
            "sha256": "7f7606f08e0544d8d012ef4d097dabdd6df6843a28793eb6551245d4b2db4242"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.8"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {},
    "develop": {}
}
```

### Create Dockerfile
* Inside the `transcribe_audio` folder
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
apt-get install -y --no-install-recommends build-essential ffmpeg
```

* Install pipenv
```
pip install --no-cache-dir --upgrade pip
pip install pipenv
```

* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app/` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`

* Example dockerfile can be found [here](https://github.com/dlops-io/mega-pipeline#sample-dockerfile)

### Docker Build & Run
* Build your docker image and give your image the name `transcribe_audio`

* You should be able to run your docker image by using:
```
docker run --rm -ti -v "$(pwd)":/app transcribe_audio
```

* The `-v "(pwd)":/app` option is to mount your current working directory into the `/app` directory inside the container as a volume. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `google-cloud-speech`
  - `ffmpeg-python`

* If you exit your container at this point, in order to get the latest environment from the pipenv file. Make sure to re-build your docker image again

### CLI to interact with your code
* Use the given python file [`cli.py`](https://github.com/dlops-io/mega-pipeline/blob/main/transcribe_audio/cli.py)
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

### Testing your code locally
* Inside your docker shell make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from GCS bucket
* `python cli.py -t` - Should transcribe audio to text and save it locally
* `python cli.py -u` - Should upload the transcribed text to the remote GCS bucket
* Verify that your uploaded data shows up in the [Mega Pipeline App](https://ai5-mega-pipeline.dlops.io/)

### OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag transcribe_audio <USER NAME>/transcribe_audio`
* Push to Docker Hub: `docker push <USER NAME>/transcribe_audio`

