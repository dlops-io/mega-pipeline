# Generate Text

📝 → 🗒️

In this container, you will implement the following:

* Read the text prompt from your GCS bucket, folder `text_prompts`
* Use the **Gemini API** via Vertex AI to correct the transcribed text and enhance the script with additional facts that we will use later for audio synthesis
* Save the generated text as a text file in your bucket, folder `text_paragraphs` (use the same file name)

---

## Project Setup

`cd` into the `generate_text` folder (you already have it from cloning the [mega-pipeline](https://github.com/dlops-io/mega-pipeline/tree/flexible-workflow) repo).

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
│   └── generate_text/   ← you are here
└── secrets/
    └── mega-pipeline.json
```

`docker-shell.sh` mounts that folder into the container at `/secrets` and sets `GOOGLE_APPLICATION_CREDENTIALS` for you.

> This component calls Gemini through **Vertex AI**, so your service account also needs the **Vertex AI User** role, and the Vertex AI API must be enabled in your project.

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

> The image is named `mega-pipeline-generate-text`. To publish under your own DockerHub org rather than `dlops`, change `DOCKER_USERNAME` at the top of `docker-shell.sh`.

---

## Choosing the Gemini model

`cli.py` reads the model name from an environment variable and falls back to a sensible default:

```python
model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
```

To try a different model without editing code, set `GEMINI_MODEL` inside the container before running:

```bash
export GEMINI_MODEL=gemini-2.5-flash
python cli.py --generate
```

---

## Python packages

Already declared in `pyproject.toml` and pinned in `uv.lock`:

- `google-cloud-storage`
- `google-genai`

To add a dependency, run `uv add <package>` **inside the container**. It updates `pyproject.toml` and `uv.lock` on your host through the volume mount — commit both, then rebuild (`./docker-shell.sh dev`) so the dependency is baked into the image.

---

## CLI to interact with your code

The CLI has the following command line argument options:

```console
$ python cli.py --help
usage: cli.py [-h] [-d] [-g] [-u]

Generate text from prompt

options:
  -h, --help      show this help message and exit
  -d, --download  Download text prompts from GCS bucket
  -g, --generate  Generate a text paragraph
  -u, --upload    Upload paragraph text to GCS bucket
```

## Testing your code

Inside your docker shell, run the steps in order:

```bash
python cli.py -d   # download the transcribed prompts from your GCS bucket
python cli.py -g   # generate the expanded podcast text, saved locally
python cli.py -u   # upload the generated text back to your bucket
```

Then verify in the GCP console that `text_paragraphs/<group_name>/` in your bucket contains the new `.txt` files. Both `synthesis_audio_en` and `translate_text` read from there next.

---

## OPTIONAL: Publish the container

`./docker-shell.sh prod` builds for `linux/amd64` + `linux/arm64` and pushes in one step. It expects you to be logged in first:

```bash
docker login -u <USER NAME> -p <ACCESS TOKEN>
```

Create an access token under [DockerHub → Security](https://hub.docker.com/settings/security).
