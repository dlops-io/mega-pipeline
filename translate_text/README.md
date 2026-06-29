# Translate Text

🗒️ → 🇫🇷

In this container, you will implement the following:
- Read the text from the GCS bucket `mega-pipeline-bucket` and folder `text_paragraphs`
- Use the **Google Cloud Translate API** (via the `google-cloud-translate` client library) to translate the text from English to French (or any other language). This is a managed GCP service — it authenticates the same way as the Speech-to-Text and Text-to-Speech components, using the service-account JSON in `secrets/mega-pipeline.json`.
- Save the translated text as a text file in bucket `mega-pipeline-bucket` and folder `text_translated` (use the same file name)


## Project Setup

* Create a folder `translate_text` or clone this repo

## GCP Credentials File
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `translate_text`
<a href="https://canvas.harvard.edu/files/23163432/download?download_frd=1" download>mega-pipeline.json</a>

## Create pyproject.toml
Inside the `translate_text` folder, scaffold a minimal `pyproject.toml` with:
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
* Inside the `translate_text` folder
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
* Build your docker image and give your image the name `translate_text`

* You should be able to run your docker image by using:
```bash
docker run --rm -ti -v "$(pwd):/app" translate_text
```
* The `-v "$(pwd):/app"` option mounts your current working directory into the `/app` directory inside the container as a volume. This helps us during app development, so when you change a source code file using VSCode from your host machine, the files are automatically changed inside the container.

## Python packages required
* `uv add` the following:
  - `google-cloud-storage`
  - `google-cloud-translate`

* Run these commands **inside the container**. They update `pyproject.toml` on your host (via the volume mount). After exiting the container, re-build the image so the dependencies are baked in for future runs.

## CLI to interact with your code
* Use the given Python file [`cli.py`](https://github.com/dlops-io/mega-pipeline/blob/main/translate_text/cli.py)
* Assign your group-number to the `group_name` variable in `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-t] [-u]

Translate English to French

options:
  -h, --help       show this help message and exit
  -d, --download   Download text paragraphs from GCS bucket
  -t, --translate  Translate text
  -u, --upload     Upload translated text to GCS bucket
```

## Testing your code locally
* Inside your docker shell, make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from the GCS bucket
* `python cli.py -t` - Should translate text from English to French and save it locally
* `python cli.py -u` - Should upload the French translated text to the remote GCS bucket
* Verify that your uploaded data shows up in the [Mega Pipeline App](https://ac215-mega-pipeline.dlops.io/)

## OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag translate_text <USER NAME>/translate_text`
* Push to Docker Hub: `docker push <USER NAME>/translate_text`
