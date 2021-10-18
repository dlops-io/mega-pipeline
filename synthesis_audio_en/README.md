# Synthesis Audio

🗒️  &rightarrow; 🔊

In this container you will implement the following:
* Read the paragraphs of text from the GCS bucket `mega-pipeline-bucket` and folder `text_paragraphs`
* Use Cloud Text-to-Speech API to generate an audio file in English
* Save the audio mp3 file in bucket `mega-pipeline-bucket` and folder `text_audios` (use the same file name and change extension to .mp3)


### Prerequisites for Development
* Have Docker Desktop installed
* Check that your Docker is running with the following command
`docker run hello-world`
### Install VSCode  
Follow the [instructions](https://code.visualstudio.com/download) for your operating system.  
If you already have a preferred text editor, skip this step.  

### Project Setup

* Create a folder `synthesis_audio_en`

### GCP Credentials File
* Download the `mega-pipeline.json` from Ed and save it inside a folder called `secrets` inside `synthesis_audio_en`

### Create Pipfile & Pipfile.lock files
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
apt-get install -y --no-install-recommends build-essential
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
docker build -t synthesis_audio_en -f Dockerfile .
```
* You should be able to run your docker image by using:
```
docker run --rm -ti --mount type=bind,source=$(pwd),target=/app synthesis_audio_en
```
* The `--mount type=bind,source=$(pwd)` option is to mount your current working directory into the `/app` directory inside the container. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `google-cloud-texttospeech`

### CLI to interact with your code
* Add a python file `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-s] [-u]

Synthesis audio from text

optional arguments:
  -h, --help       show this help message and exit
  -d, --download   Download paragraph of text from GCS bucket
  -s, --synthesis  Synthesis audio
  -u, --upload     Upload audio file to GCS bucket

```

* Requirements for `cli.py`
Use the following values:
```
gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_paragraphs = "text_paragraphs"
text_audios = "text_audios"
```

* `text_paragraphs` - Bucket where we store the generated text from GPT2
* `text_audios` - Bucket where we store the audio of the paragraph of text

* -d, --download    Download text prompts from GCS bucket
Write a function to download all text paragraphs from the bucket `text_paragraphs` and store them locally in a folder `text_paragraphs`

* -s, --synthesis  Synthesis audio
Write a function to synthesis audio from text and store in a local folder `text_audios`

* Example code to synthesis an audio.mp3 file from text:
```
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

input_text = "Hello, welcome to AC215"

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=input_text)

# Build the voice request
language_code = "en-US"
voice = texttospeech.VoiceSelectionParams(
    language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Save the audio file
audio_file = "audio.mp3"
with open(audio_file, "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
```

* -u, --upload      Upload paragraph text to GCS bucket
Write a function to upload the files in `text_audios` to the bucket `text_audios` in GCS

### Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag synthesis_audio_en <USER NAME>/synthesis_audio_en`
* Push to Docker Hub: `docker push <USER NAME>/synthesis_audio_en`