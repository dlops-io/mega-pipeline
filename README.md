# Mega Pipeline App

🎙️ → 📝 → 🗒️ → [🔊🇫🇷] → 🔊

The goal of this tutorial is to build an **AI-assisted podcast generator** that works across multiple languages. Starting from a **recorded** draft, we'll **transcribe** it, enrich it with an LLM, **translate** it, and **synthesize** the result back into audio.

The key idea is to **simulate a microservice architecture**, where each component runs as its own containerized service. The full pipeline is shown below.

1. Pavlos recorded a draft podcast in English, which serves as our starting point.
2. The audio file is transcribed using the **Google Cloud Speech-to-Text API**.
3. The resulting text is sent to an LLM to generate an expanded version of the podcast.
4. The generated text is synthesized into audio with **Google Cloud Text-to-Speech**.
5. The text is also translated into French (or another language) using the **Google Cloud Translate API**.
6. The translated text is synthesized into audio again with Google Cloud Text-to-Speech.
7. **Bonus step**: The translated text can also be synthesized with ElevenLabs to recreate Pavlos' voice.

The pipeline flow is illustrated below:
<img src="mega-pipeline-flow.png" width="800">

---

## Prerequisites

Complete **[Tutorial 0 - Setup & Installs](https://github.com/dlops-io/ac215-setup)** first. It covers everything this tutorial assumes: a GCP account + project, VS Code, Git, Docker Desktop, and `uv`.

> Unlike Tutorial 0, you **will** need GCP credentials for this tutorial — every component reads from and writes to a GCS bucket, and most also call a Google Cloud AI API. In this branch you create that service account yourself; see **Service Account & Secrets** below.

---

## Get the Code

**Starting fresh?** Clone the branch directly:

```bash
git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git
cd mega-pipeline
```

**Already have the repo from the last tutorial?** You're on `main` — switch branches instead of re-cloning:

```bash
cd mega-pipeline
git fetch origin                      # get the branches you don't have yet
git checkout flexible-workflow        # switch to this tutorial's branch
git branch                            # confirm: * flexible-workflow
```

> If `git checkout` refuses with *"Your local changes would be overwritten"*, that's your edits to `cli.py` from last time. Either stash them (`git stash`) or throw them away (`git checkout -- .`) — you don't need them here, since this branch has its own `cli.py`.

Your `secrets/` folder and any downloaded audio stay put — they're ignored by Git, so switching branches doesn't touch them.

Each of the five components lives in its own subfolder here (`transcribe_audio/`, `generate_text/`, ...) — you'll `cd` into each one as you build and run it.

---

## Where We Are, Where We're Going

You've already built this pipeline once, with most of the scaffolding handed to you — a shared bucket, a shared service account, a ready-made Docker setup. That was enough to see the pieces fit together.

This branch is the **same pipeline, built the way a real team would build it**. Concretely, that means:

* 🪣 **Your own GCS bucket.** Each team provisions and owns its storage.
* 🔐 **Your own service account.** You create a Service Account in GCP, grant it the right IAM roles, download its JSON key, and manage it as a secret.
* 🐳 **A real Dockerfile per component — already written for you.** You no longer author it from scratch; you read it, understand it, and change it when your component needs something new.
* 🛠️ **A `docker-shell.sh` script per component.** The `docker build` and `docker run` commands now have to juggle multiple architectures, mounted volumes, environment variables, and secrets. Wrapping that logic in a script keeps the workflow sane and consistent across Mac/Linux/Windows.

### Two ways to work — and we support both

Once a Docker image exists for a component, a team can either **build it locally** or **pull a prebuilt copy** from a registry. There is no single "right" workflow:

* **Early in development** — devs pull the `Dockerfile` and `uv.lock` from GitHub and build images locally. Anyone can edit the Dockerfile or add dependencies and submit a PR.
* **Later in development** — a senior dev publishes prebuilt images to DockerHub. Most devs just pull and run; rebuilding is rare.

Each component's `docker-shell.sh` supports both modes: pass `dev` to build locally, `prod` to build multi-arch and push to a registry, `run` to pull and run from the registry, or no argument to build-and-run locally. That's the **flexible workflow** in the branch name.

> ℹ️ The `docker-shell.sh` files default to pushing under the `dlops` DockerHub org. If your team publishes its own images, update `DOCKER_USERNAME` inside each component's script.

---

## What You'll Learn

By completing this tutorial, you'll gain hands-on experience with:

- **Owning your own cloud resources** — bucket, service account, IAM roles.
- **Managing secrets safely** — keep them out of Git, mount them into containers at runtime.
- **Reading and modifying real Dockerfiles** for AI/ML workflows.
- **Encapsulating build/run logic in a script** so the workflow is repeatable across machines.
- **Working across two delivery modes** — build it yourself vs. pull a prebuilt image.
- **Calling managed Google Cloud AI APIs** (Speech-to-Text, Translate, Text-to-Speech) from inside your containers.

---

## The Five Components

Each component has its own folder, its own container, and its own README. Work through them **in this order** — each one reads from the bucket what the previous one wrote:

* 📝 Task A — [transcribe_audio](./transcribe_audio)
* 🗒️ Task B — [generate_text](./generate_text)
* 🔊 Task C — [synthesis_audio_en](./synthesis_audio_en)
* 🇫🇷 Task D — [translate_text](./translate_text)
* 🔊 Task E — [synthesis_audio](./synthesis_audio)

By the end, every team will have built a complete pipeline that mirrors a **real-world microservice architecture**: multiple independent services, each containerized, working together to form a larger application.

### Recommended folder layout

```text
<your-workspace>/
├── mega-pipeline/          ← this repo
│   ├── transcribe_audio/
│   ├── generate_text/
│   ├── synthesis_audio_en/
│   ├── translate_text/
│   └── synthesis_audio/
└── secrets/                ← lives OUTSIDE the repo, mounted into containers at runtime
    └── mega-pipeline.json  ← your Service Account JSON key
```

The `docker-shell.sh` in each component mounts `../../secrets/` into the container at `/secrets`, so secrets stay one level above the repo and never get committed.

---

## ⚠️ Configure each `cli.py` before you run it

Near the top of every component's `cli.py` there are three values you need to set for your team:

```python
gcp_project = ""          # ← your team's GCP project id
bucket_name = ""   # ← your team's own bucket
group_name = ""                        # ← your group, e.g. "group-01"
```

* **`gcp_project` and `bucket_name`** still point at the shared class resources from the earlier tutorial. Since this branch has you provision your own, **change both to your team's project and bucket**.
* **`group_name`** scopes your outputs to `…/<group_name>/…` inside that bucket. The CLIs `assert` that it has been changed from the default — if you forget, the script stops before doing anything.

---

## Connecting the Pipeline Components

In a production pipeline, containerized services talk to each other through APIs, sending requests and responses directly between microservices.

Since we haven't covered APIs yet, we'll simplify. Instead of calling one another directly, components will **communicate indirectly by writing their outputs to storage**, which the next stage will then read as input.

In this tutorial, rather than using your local disk, components will write to and read from **your team's own Google Cloud Storage (GCS) bucket**. The bucket acts like a common drive for transcripts, generated text, and synthesized audio — but each team owns its own, and each team's outputs are scoped under its `group_name` prefix.

This setup gives you practical hands-on experience now, while preparing you for the **API-driven systems** we'll tackle later.

### GCS Bucket Details

In Google Cloud, a **bucket** is an online folder where files can be stored and retrieved. Each team creates its own bucket inside the team's GCP project. The components read and write to it using the prefixes below:

* `input_audios/` — raw audio files (starting point).
* `text_prompts/` — transcripts generated from speech-to-text.
* `text_paragraphs/` — expanded text generated by the LLM.
* `text_translated/` — translated versions of the text.
* `text_audios/` — synthesized English audio clips for each paragraph.
* `output_audios/` — final audio outputs in French (or another language).
* `output_audios_pp/` — bonus: audio outputs synthesized with ElevenLabs in Pavlos' voice.

![Mega pipeline bucket](mega-pipeline-bucket.png)

Want to learn more about GCS?

- [Google Cloud Storage](https://www.youtube.com/watch?v=VDBhvexAj8I)
- [Google Cloud Storage Overview](https://cloud.google.com/storage)

---

## Service Account & Secrets

Buckets won't let you read or write anything unless you are both **authenticated** (proving who you are) and **authorized** (having the right permissions). For server-to-server work like this, the standard pattern is a **Service Account** — an identity for your *code*, not for you.

In the earlier version of this tutorial we handed you a shared JSON key. In this branch **each team creates and owns its own Service Account**, following the steps covered in lecture:

1. In the GCP console, go to **IAM & Admin → Service accounts**.
2. Create a new service account (e.g. `mega-pipeline-sa`).
3. Grant it these roles on your project:
   - **Storage Admin** (`roles/storage.admin`) — read/write your bucket. All five components need this.
   - **Agent Platform User** (`roles/aiplatform.user`) — `generate_text` calls Gemini through **Vertex AI**. ⚠️ Search the role picker for **"Agent Platform User"** — Google renamed these titles, so searching "Vertex AI User" finds nothing.
   - **Cloud Speech Client** (`roles/speech.client`) — `transcribe_audio`.
   - **Cloud Translation API User** (`roles/cloudtranslate.user`) — `translate_text`.
4. Under **Keys → Add Key → Create new key**, download a **JSON** key.
5. Save it as `mega-pipeline.json` in a `secrets/` folder that sits **one level above this repo** (see folder layout above).

> **Text-to-Speech needs no role** — it defines no service-specific role at all, so enabling the API is enough. Don't go hunting for a "Cloud Text-to-Speech User"; it doesn't exist. The two synthesis components write their audio straight into your bucket, which **Storage Admin** already covers.

> Make sure the corresponding APIs are **enabled** in your GCP project: Cloud Storage, **Vertex AI**, Speech-to-Text, Cloud Translation, and Text-to-Speech. Enabling the API and granting the role are two separate steps.

**To enable them** — in the console, go to **APIs & Services → Library**, search each name, and click **Enable**. Or do all five at once:

```bash
gcloud config set project <your-project-id>
gcloud services enable \
  storage.googleapis.com \
  aiplatform.googleapis.com \
  speech.googleapis.com \
  texttospeech.googleapis.com \
  translate.googleapis.com
```

The provided `docker-shell.sh` mounts that `secrets/` folder into the container at `/secrets` and sets `GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json`, so the calls to `google.cloud.storage` inside `cli.py` authenticate transparently.

🔑 **Never commit `secrets/` to Git.** Keeping the folder outside the repo (as this branch does) is the canonical way to make that mistake impossible.

---

## How to Run a Component

Every component is driven through its `docker-shell.sh`. From inside a component folder (e.g. `transcribe_audio/`):

```bash
./docker-shell.sh          # build the image locally and run it (default)
./docker-shell.sh dev      # only build the local image
./docker-shell.sh run      # run from a prebuilt image (falls back to DockerHub)
./docker-shell.sh prod     # build multi-arch (amd64 + arm64) and push to DockerHub
```

The default mode drops you into a shell **inside** the container with the `uv` virtual environment already activated and `/secrets` mounted. From there you run the CLI commands listed below.

If `docker-shell.sh` isn't executable yet:

```bash
chmod +x docker-shell.sh
```

> 🪟 **On Windows**, run from Git BASH and prefix with `winpty` if you see "the input device is not a TTY." (see notes at the bottom of this file).

---

## Quick Reference — Running Each Component

Inside each component's container, drive it through `cli.py`. The flags (`--download`, `--transcribe`, `--generate`, `--translate`, `--synthesis`, `--upload`) follow the same pattern: pull inputs from your bucket, run the step, push outputs back.

**Transcribe Audio**

```bash
python cli.py --download
python cli.py --transcribe
python cli.py --upload
```

**Generate Text**

```bash
python cli.py --download
python cli.py --generate
python cli.py --upload
```

**Synthesize Audio (English)**

```bash
python cli.py --download
python cli.py --synthesis
```

> Note: synthesis writes audio directly to GCS — no separate `--upload` step needed.

**Translate Text**

```bash
python cli.py --download
python cli.py --translate
python cli.py --upload
```

**Synthesize Audio (Translated)**

```bash
python cli.py --download
python cli.py --synthesis
```

> Note: synthesis writes audio directly to GCS — no separate `--upload` step needed.

---

## Appendix

### Sample Code: Read/Write to a GCS Bucket

* Download from bucket

```python
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

```python
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

Each component ships with its own Dockerfile — see [`transcribe_audio/Dockerfile`](./transcribe_audio/Dockerfile) for the canonical example. The other components follow the same shape; the only difference is the extra OS packages they need (e.g. `ffmpeg` for audio). All of them build on **Python 3.14** and install dependencies from the component's `pyproject.toml` / `uv.lock` with `uv sync`.

```dockerfile
# Use the official Debian-hosted Python image
FROM python:3.14-slim-bookworm

ARG DEBIAN_PACKAGES="build-essential"

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Tell uv to copy packages from the wheel into the site-packages
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv

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

> Note that unlike the earlier tutorial, this Dockerfile does **not** bake `GOOGLE_APPLICATION_CREDENTIALS` in. The credentials path is passed at runtime by `docker-shell.sh`, which mounts your `secrets/` folder at `/secrets`.

### Notes for running on Windows

> Docker Desktop installation is covered in [Tutorial 0](https://github.com/dlops-io/ac215-setup). These are the gotchas that show up *after* install:

* Run docker commands from **Git BASH** (Windows `cmd` and PowerShell quote arguments differently and will mangle the volume-mount syntax).
* **Always quote `$(pwd)`** — Windows paths often contain spaces (e.g. `C:\Users\First Last\...`), and without quotes the shell splits the path mid-argument.
* If you see `the input device is not a TTY`, prefix the command with `winpty`. Git BASH on Windows doesn't expose a real TTY to Docker, and `winpty` is the shim that fixes it.

## Solutions

Solutions to this tutorial will be posted here after the assignment deadline.
