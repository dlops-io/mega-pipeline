# Synthesize Audio (Translated)

🇫🇷 → 🔊

In this container, you will implement the following:
- Read the translated text from the GCS bucket `mega-pipeline-bucket` and folder `text_translated`
- Use the **Cloud Text-to-Speech API** to generate an audio file in French (or any other language)
- The audio is written **directly to GCS** — no local file is created. The output is saved in bucket `mega-pipeline-bucket` and folder `output_audios` (same file name, `.mp3` extension)


## Project Setup

* Create a folder `synthesis_audio` or clone this repo

## GCP Credentials File
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `synthesis_audio`
<a href="https://canvas.harvard.edu/files/23163432/download?download_frd=1" download>mega-pipeline.json</a>

## Create pyproject.toml
Inside the `synthesis_audio` folder, scaffold a minimal `pyproject.toml` with:
```bash
uv init --bare
```
The `--bare` flag gives you just the `pyproject.toml` (no sample `main.py`, no README, no git init) — exactly what we want, since the source code already lives here. You'll add the specific dependencies further down with `uv add`.

> **Don't have `uv` installed?** Run the following to install it first:
> ```bash
> # macOS / Linux
> curl -LsSf https://astral.sh/uv/install.sh | sh
>
> # Windows (PowerShell)
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> ```
> Then restart your terminal and re-run `uv init --bare`. Alternatively, you can install via pip: `pip install uv`.

## Create Dockerfile
* Inside the `synthesis_audio` folder
* Create a `Dockerfile` and base it from `python:3.12-slim-bookworm` — the official Debian-hosted Python 3.12 image

* Declare the system packages you need as a build arg:
```dockerfile
ARG DEBIAN_PACKAGES="build-essential"
```

* Set the following environment variables:
```dockerfile
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```

* Update the system, install dependencies, install uv, and create a non-root `app` user — all in one `RUN` layer to keep the image small:
```dockerfile
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app
```

> **Why a non-root user?** Running containers as root is a security risk. The `app` user owns `/app` so the container process never needs root privileges.

* Switch to the non-root user and set the working directory:
```dockerfile
USER app
WORKDIR /app
```

* Copy source files (preserving `app` ownership) and install Python dependencies:
```dockerfile
COPY --chown=app:app . ./
RUN uv sync
```

* Add the entry point and default command to drop into the virtual environment shell:
```dockerfile
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```

* Example dockerfile can be found [here](https://github.com/dlops-io/mega-pipeline#sample-dockerfile)

## Docker Build & Run
* Build your docker image and give your image the name `synthesis_audio`

* You should be able to run your docker image by using:
```bash
docker run --rm -ti -v "$(pwd):/app" synthesis_audio
```
* The `-v "$(pwd):/app"` option mounts your current working directory into the `/app` directory inside the container as a volume. This helps us during app development, so when you change a source code file using VSCode from your host machine, the files are automatically changed inside the container.

## Python packages required
* `uv add` the following:
  - `google-cloud-storage`
  - `google-cloud-texttospeech`

* Run these commands **inside the container**. They update `pyproject.toml` on your host (via the volume mount). After exiting the container, re-build the image so the dependencies are baked in for future runs.

## CLI to interact with your code
* Use the given Python file [`cli.py`](https://github.com/dlops-io/mega-pipeline/blob/main/synthesis_audio/cli.py)
* Assign your group-number to the `group_name` variable in `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-s]

Synthesis audio from text

options:
  -h, --help       show this help message and exit
  -d, --download   Download translated text from GCS bucket
  -s, --synthesis  Synthesis audio
```

## Testing your code locally
* Inside your docker shell, make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from GCS bucket
* `python cli.py -s` - Should synthesize audio from text and write it **directly to GCS** (no `--upload` step needed)
* Verify that your uploaded data shows up in the [Mega Pipeline App](http://ac215-mega-pipeline.dlops.io/)

## OPTIONAL: Synthesize with ElevenLabs (Pavlos' voice)

`cli_11.py` uses the [ElevenLabs API](https://elevenlabs.io/) to synthesize the translated text in **Pavlos' voice** instead of a standard Google TTS voice. The output is saved to `output_audios_pp/` in the GCS bucket.

**Setup:**

1. Create an account at [elevenlabs.io](https://elevenlabs.io/) and generate an API key
2. Create a file `secrets/11lab_api_key.txt` with the following content:
```
XI_API_KEY=your_api_key_here
```

3. Add `requests` to your Python packages (needed by `cli_11.py`):
```bash
uv add requests
```

**Running:**
```bash
python cli_11.py --download
python cli_11.py --synthesis
python cli_11.py --upload
```

> Note: unlike `cli.py`, `cli_11.py` saves audio **locally first** then uploads to GCS via `--upload`.

## OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag synthesis_audio <USER NAME>/synthesis_audio`
* Push to Docker Hub: `docker push <USER NAME>/synthesis_audio`
