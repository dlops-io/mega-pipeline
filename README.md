# Mega Pipeline App

🎙️ &rightarrow; 📝 &rightarrow; 🗒️ &rightarrow;  [🔊🇫🇷] &rightarrow; 🔊

The goal of this tutorial is to build an AI-assisted podcast generator that works across multiple languages. Starting from a recorded draft, we transcribe it, expand it with an LLM, translate it, and synthesize the result into audio.

The key idea is to simulate a microservice architecture, where each of these components runs as its own containerized service. The full pipeline is shown below.

* Pavlos recorded a draft podcast in English, which will serve as our starting point for the pipeline.
* The audio file is transcribed using the Google Cloud Speech-to-Text API.
* The resulting text is used as a prompt to an LLM to generate an expanded version of the podcast.
* The generated text is synthesized into audio using the Google Cloud Text-to-Speech API.
* The text is also translated into French (or another language) using Google Translation services.
* The translated text is then converted back to audio using the Google Cloud Text-to-Speech API.
* **Bonus step**: The translated text can be synthesized into audio using ElevenLabs, recreating the voice in Pavlos’ style.

The pipeline flow is illustrated below:
<img src="mega-pipeline-flow.png"  width="800">

## Group Tasks for the Mega Pipeline
Each team will be responsible for building all stages of the pipeline, end to end. This means you won’t just work on one piece—you’ll containerize and connect every component.

All components and their step-by-step instructions are listed below, so you can follow along to build the full pipeline.

* 📝Task A [transcribe_audio](https://github.com/dlops-io/mega-pipeline/tree/main/transcribe_audio)
* 🗒️Task B [generate_text](https://github.com/dlops-io/mega-pipeline/tree/main/generate_text)
* 🔊Task C [synthesis_audio_en](https://github.com/dlops-io/mega-pipeline/tree/main/synthesis_audio_en)
* 🇫🇷Task D [translate_text](https://github.com/dlops-io/mega-pipeline/tree/main/translate_text)
* 🔊Task E [synthesis_audio](https://github.com/dlops-io/mega-pipeline/tree/main/synthesis_audio)

By the end, every team will have built a complete pipeline that mirrors a real-world microservice architecture: multiple independent services, each containerized, working together to form a larger application.

The overall progress of this mega pipeline can be viewed [here](http://ac215-mega-pipeline.dlops.io/).

## Connecting the Pipeline Components

In a real-world production pipeline, containerized services communicate through APIs, passing requests and responses directly between microservices.

Since we haven’t covered APIs yet in this course, we’ll simplify things for now. Instead of calling each other, components will communicate indirectly by writing their outputs to disk, which the next stage will then read as input.

Because this tutorial runs locally on your machine, file-based communication is the simplest way to connect the pieces. In production, however, each container would typically run on its own VM in the cloud and exchange data via APIs. To prepare for that, we adopt the same principle of a shared storage layer. For now, the components will still communicate by writing their outputs to a Google Cloud Storage (GCS) bucket, which serves as the shared drive for transcripts, generated text, and synthesized audio.

This setup is a stepping stone: it gives you hands-on practice with the full pipeline now, while preparing you for the more advanced, API-driven systems we’ll tackle later in the course.

## GCS Bucket Details:
Before diving into the bucket layout, let’s connect the dots.
In Google Cloud, a bucket is like a shared online folder where we can store and retrieve files. Instead of saving outputs locally, our pipeline components will read from and write to this shared bucket, making it easy for all stages of the pipeline to communicate. You’ll access these buckets through the Google Cloud Storage (GCS) client, which lets you upload, download, and list files programmatically from inside your containers.

* **input_audios** - Bucket where we store the input audio files.
* **text_prompts** - Bucket where we store the text prompts that was synthesized by audio to text.
* **text_paragraphs** - Bucket where we store the generated text from GPT2.
* **text_translated** - Bucket where we store the translated text.
* **text_audios** - Bucket where we store the audio of the paragraph of text.
* **output_audios** - Bucket where we store the final French audio files.
* **output_audios_pp** - Bucket where we store the French audio files (Pavlos voice).

![Mega pipeline bucket](mega-pipeline-bucket.png)


## GCP Credentials File:
Download the json file and place inside <app_folder>/secrets:
<a href="https://canvas.harvard.edu/files/21857112/download?download_frd=1" download>mega-pipeline.json</a>



### Resulting CLI options for each container

**Transcribe Audio**
```
python cli.py --download
python cli.py --transcribe
python cli.py --upload
```

**Generate Text**
```
python cli.py --download
python cli.py --generate
python cli.py --upload
```

**Synthesis Audio English**
```
python cli.py --download
python cli.py --synthesis
```

**Translate Text**
```
python cli.py --download
python cli.py --translate
python cli.py --upload
```

**Synthesis Audio**
```
python cli.py --download
python cli.py --synthesis
```


### Sample Code to Read/Write to GCS Bucket

* Download from bucket
```
from google.cloud import storage

# Initiate Storage client
storage_client = storage.Client(project=gcp_project)

# Get reference to bucket
bucket = storage_client.bucket(bucket_name)

# Find all content in a bucket
blobs = bucket.list_blobs(prefix="input_audios/")
for blob in blobs:
    print(blob.name)
    if not blob.name.endswith("/"):
        blob.download_to_filename(blob.name)

```

* Upload to bucket
```
from google.cloud import storage

# Initiate Storage client
storage_client = storage.Client(project=gcp_project)

# Get reference to bucket
bucket = storage_client.bucket(bucket_name)

# Destination path in GCS 
destination_blob_name = "input_audios/test.mp3"
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename("Path to test.mp3 on local computer")

```

### Sample Dockerfile
```
# Use the official Debian-hosted Python image
FROM python:3.12-slim-bookworm

ARG DEBIAN_PACKAGES="build-essential curl"

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Tell uv to copy packages from the wheel into the site-packages
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv

# This is done for the tutorial only
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json

# Ensure we have an up to date baseline, install dependencies and
# create a user so we don't run the app as root
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app

# Switch to the new user
USER app
WORKDIR /app

# Copy the source code
COPY --chown=app:app . ./

RUN uv sync

# Entry point
ENTRYPOINT ["/bin/bash"]
# Get into the uv virtual environment shell
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```

### Some notes for running on Windows
* Docker Win10 installation - needs WSL2 or Hyper-V enabled: https://docs.docker.com/desktop/windows/install/
* Use `Git` BASH to run (which is like a smaller `Cygwin`)
* Needed to add pwd in quotes in order to escape the spaces that common in windows directory structures
* Need to prefix docker run with `winpty` otherwise I get a "the input device is not a TTY." error
* `winpty docker run --rm -ti --mount type=bind,source="$(pwd)",target=/app generate_text`

## Solutions
Solutions to this tutorial can be found [here]()
