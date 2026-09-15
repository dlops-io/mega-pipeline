# Translate Text

🗒️ → 🇫🇷

In this container, you will implement the following:

* Read the text from your GCS bucket, folder `text_paragraphs`
* Use the **Google Cloud Translate API** (via the `google-cloud-translate` client library) to translate the text from English to French (or any other language). This is a managed GCP service — it authenticates the same way as the Speech-to-Text and Text-to-Speech components, using your service-account JSON.
* Save the translated text as a text file in your bucket, folder `text_translated` (use the same file name)

---

## Project Setup

`cd` into the `translate_text` folder (you already have it from cloning the [mega-pipeline](https://github.com/dlops-io/mega-pipeline/tree/flexible-workflow) repo).

Unlike the earlier version of this tutorial, **you do not write the container tooling here** — it ships with the repo:

| File | What it is |
| --- | --- |
| `Dockerfile` | Python 3.14 image, installs deps with `uv sync`, runs as a non-root `app` user |
| `docker-shell.sh` | Wraps `docker build` / `docker run`; mounts your code and your secrets |
| `pyproject.toml` | Declares this component's Python dependencies |
| `uv.lock` | Pins the exact resolved versions so every teammate gets the same environment |

Read all four before you run anything — you'll be modifying them later in the course.

---

## Before You Run: Credentials and Configuration

### 1. Service Account key

This component needs a GCP service account key at `secrets/mega-pipeline.json`, **one level above the repo**. If you haven't created one yet, follow [Service Account & Secrets](https://github.com/dlops-io/mega-pipeline/tree/flexible-workflow#service-account--secrets) in the root README.

```text
<your-workspace>/
├── mega-pipeline/
│   └── translate_text/   ← you are here
└── secrets/
    └── mega-pipeline.json
```

`docker-shell.sh` mounts that folder into the container at `/secrets` and sets `GOOGLE_APPLICATION_CREDENTIALS` for you.

> Your service account needs the **Cloud Translation API User** role, and the **Cloud Translation API** must be enabled in your project.

### 2. Edit `cli.py`

Near the top of `cli.py`:

```python
gcp_project = "ac215-project"          # ← your team's GCP project id
bucket_name = "mega-pipeline-bucket"   # ← your team's own bucket
group_name = ""                        # ← your group, e.g. "group-01"
```

Set all three for your team. `cli.py` `assert`s that `group_name` has been changed — leave it empty and the script stops immediately with `AssertionError: Update group name`.

---

## Build & Run

You don't write the Dockerfile — you run it, through `docker-shell.sh`:

```bash
./docker-shell.sh          # build the image locally and run it (default)
./docker-shell.sh dev      # only build the local image
./docker-shell.sh run      # run from a prebuilt image (falls back to DockerHub)
./docker-shell.sh prod     # build multi-arch (amd64 + arm64) and push to DockerHub
```

The default mode drops you into a shell **inside** the container, with the `uv` virtual environment already activated, your source folder mounted at `/app`, and your secrets at `/secrets`. Because `/app` is a bind mount, edits you make in VS Code on your host show up instantly inside the container.

If the script isn't executable yet: `chmod +x docker-shell.sh`

> The image is named `mega-pipeline-translate-text`. To publish under your own DockerHub org rather than `dlops`, change `DOCKER_USERNAME` at the top of `docker-shell.sh`.

---

## Python packages

Already declared in `pyproject.toml` and pinned in `uv.lock`:

- `google-cloud-storage`
- `google-cloud-translate`

To add a dependency, run `uv add <package>` **inside the container**. It updates `pyproject.toml` and `uv.lock` on your host through the volume mount — commit both, then rebuild (`./docker-shell.sh dev`) so the dependency is baked into the image.

---

## Translating into a different language

`cli.py` calls the API with an explicit source and target language:

```python
result = translate_client.translate(
    input_text,
    source_language="en",
    target_language="fr",
    format_="text",
)
```

Change `target_language` to any [supported language code](https://cloud.google.com/translate/docs/languages) (`es`, `de`, `el`, ...) to translate somewhere other than French.

---

## CLI to interact with your code

The CLI has the following command line argument options:

```console
$ python cli.py --help
usage: cli.py [-h] [-d] [-t] [-u]

Translate English to French

options:
  -h, --help       show this help message and exit
  -d, --download   Download text paragraphs from GCS bucket
  -t, --translate  Translate text
  -u, --upload     Upload translated text to GCS bucket
```

## Testing your code

Inside your docker shell, run the steps in order:

```bash
python cli.py -d   # download the generated paragraphs from your GCS bucket
python cli.py -t   # translate English → French, saved locally
python cli.py -u   # upload the translated text back to your bucket
```

Then verify in the GCP console that `text_translated/<group_name>/` in your bucket contains the new `.txt` files. That's the input `synthesis_audio` will pick up next.

---

## OPTIONAL: Publish the container

`./docker-shell.sh prod` builds for `linux/amd64` + `linux/arm64` and pushes in one step. It expects you to be logged in first:

```bash
docker login -u <USER NAME> -p <ACCESS TOKEN>
```

Create an access token under [DockerHub → Security](https://hub.docker.com/settings/security).
