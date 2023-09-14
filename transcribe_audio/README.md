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
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `transcribe_audio`
<a href="https://static.us.edusercontent.com/files/Xdc8fhBM7b703yPPV1B5xtBN" download>mega-pipeline.json</a>

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
* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`


### Docker Build & Run
* Build your docker image and give your image the name `transcribe_audio`

* You should be able to run your docker image by using:
```
docker run --rm -ti --mount type=bind,source="$(pwd)",target=/app transcribe_audio
```
* The `--mount type=bind,source="$(pwd)",target=/app` option is to mount your current working directory into the `/app` directory inside the container. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `google-cloud-speech`
  - `ffmpeg-python`
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

* Use this as a starter template for your `cli.py`
```
"""
Module that contains the command line app.
"""
import argparse

def download():
    print("download")

def transcribe():
    print("transcribe")

def upload():
    print("upload")

def main(args=None):

    print("Args:", args)

    if args.download:
        download()
    if args.transcribe:
        transcribe()
    if args.upload:
        upload()

if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(
        description='Transcribe audio file to text')

    parser.add_argument("-d", "--download", action='store_true',
                        help="Download audio files from GCS bucket")

    parser.add_argument("-t", "--transcribe", action='store_true',
                        help="Transcribe audio files to text")

    parser.add_argument("-u", "--upload", action='store_true',
                        help="Upload transcribed text to GCS bucket")

    args = parser.parse_args()

    main(args)

```


* Requirements for `cli.py`
Use the following values:
```
gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
input_audios = "input_audios"
text_prompts = "text_prompts"
```

* `input_audios` - Bucket where we store the input audio files
* `text_prompts` - Bucket where we store the text prompts that was synthesized by audio to text

* -d, --download    Download audio files from GCS bucket
Write a function to download all audio files from the bucket `input_audios` and store them locally in a folder `input_audios`

* -t, --transcribe  Transcribe audio files to text
Write a function to transcribe the audio files to text and store them locally in a folder `text_prompts`

* Sample code to read/write to a GCS Bucket can be found [hear](https://github.com/dlops-io/mega-pipeline#sample-code-to-readwrite-to-gcs-bucket)

* Example code to transcribe an audio.mp3 file to text:
```
from tempfile import TemporaryDirectory
# Imports the Google Cloud client library
from google.cloud import speech


# Instantiates a client
client = speech.SpeechClient()

audio_path = "path to audio.mp3"

with TemporaryDirectory() as audio_dir:
    flac_path = os.path.join(audio_dir, "audio.flac")
    stream = ffmpeg.input(audio_path)
    stream = ffmpeg.output(stream, flac_path)
    ffmpeg.run(stream)

    with io.open(flac_path, "rb") as audio_file:
        content = audio_file.read()

    # Transcribe
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        language_code="en-US"
    )
    operation = client.long_running_recognize(
        config=config, audio=audio)
    response = operation.result(timeout=90)
    print(response)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
```

* -u, --upload      Upload transcribed text to GCS bucket
Write a function to upload the files in `text_prompts` to the bucket `text_prompts` in GCS

### Testing your code locally
* Inside your docker shell make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from GCS bucket
* `python cli.py -t` - Should transcribe audio to text and save it locally
* `python cli.py -u` - Should upload the transcribed text to the remote GCS bucket
* Verify that your uploaded data shows up in the [Mega Pipeline App](https://ac215-mega-pipeline.dlops.io/)

### OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag transcribe_audio <USER NAME>/transcribe_audio`
* Push to Docker Hub: `docker push <USER NAME>/transcribe_audio`

