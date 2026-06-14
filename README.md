# Mega Pipeline App

🎙️ → 📝 → 🗒️ → [🔊🇫🇷] → 🔊  

The goal of this tutorial is to build an **AI-assisted podcast generator** that works across multiple languages. Starting from a **recorded** draft, we’ll **transcribe** it, enrich it with an LLM, **translate** it, and **synthesize** the result back into audio.

The key idea is to **simulate a microservice architecture**, where each component runs as its own containerized service. The full pipeline is shown below.

1. Pavlos recorded a draft podcast in English, which serves as our starting point.  
2. The audio file is transcribed using the **Google Cloud Speech-to-Text API**.  
3. The resulting text is sent to an LLM to generate an expanded version of the podcast.  
4. The generated text is synthesized into audio with **Google Cloud Text-to-Speech**.  
5. The text is also translated into French (or another language) using **Google Translation** services.  
6. The translated text is synthesized into audio again with Google Cloud Text-to-Speech.  
7. **Bonus step**: The translated text can also be synthesized with ElevenLabs to recreate Pavlos’ voice.  

The pipeline flow is illustrated below:  
<img src="mega-pipeline-flow.png" width="800">

---

## 👥 You'll work in teams — and there's a leaderboard 🏆

This tutorial is done in **groups**: each team will build the entire pipeline end to end, containerizing and connecting every component (not just one piece).

And to make things a little more interesting, every team's progress is published live on a public leaderboard at **[ac215-mega-pipeline.dlops.io](http://ac215-mega-pipeline.dlops.io/)**. The moment a component runs successfully under your group name, it lights up for the whole class to see — so you can watch your pipeline come together stage by stage and see how your team is doing relative to the rest of the class.

> ⚠️ Make sure to **SET YOUR GROUP NAME** correctly in each component (see the note further down). Otherwise, your work won't show up under your team — or worse, it might overwrite someone else's. ⚠️

---

## What You’ll Learn
By completing this tutorial, you’ll gain experience with:
- **Containerizing AI/ML workflows** step by step.  
- **Using shared cloud storage (GCS)** to connect independent services.  
- **Securing applications** with service account authentication.  
- **Calling managed Google Cloud AI APIs** (Speech-to-Text for transcription, Translate for cross-language conversion, and Text-to-Speech for audio synthesis) from inside your containers.  

---

## The Five Components

Each component has its own folder, its own container, and its own step-by-step `README`. Click through to follow along:

- 📝 Task A — [transcribe_audio](https://github.com/dlops-io/mega-pipeline/tree/main/transcribe_audio)  
- 🗒️ Task B — [generate_text](https://github.com/dlops-io/mega-pipeline/tree/main/generate_text)  
- 🔊 Task C — [synthesis_audio_en](https://github.com/dlops-io/mega-pipeline/tree/main/synthesis_audio_en)  
- 🇫🇷 Task D — [translate_text](https://github.com/dlops-io/mega-pipeline/tree/main/translate_text)  
- 🔊 Task E — [synthesis_audio](https://github.com/dlops-io/mega-pipeline/tree/main/synthesis_audio)  

By the end, every team will have built a complete pipeline that mirrors a **real-world microservice architecture**: multiple independent services (each containerized), working together to form a larger application.

---

⚠️ **IMPORTANT NOTE** ⚠️

When building your containers, make sure you `update the group name` inside your configuration. This is how we track your progress and display it correctly on the leaderboard.  

If you don’t change the group name, your work may overwrite someone else’s, or it won’t be visible under your team. So please double-check before you push or run your containerized tasks!

---

## Connecting the Pipeline Components
In a production pipeline, containerized services talk to each other through APIs, sending requests and responses directly between microservices.

Since we haven’t covered APIs yet, we’ll simplify. Instead of calling one another directly, components will **communicate indirectly by writing their outputs to storage**, which the next stage will then read as input.

In this tutorial, rather than just using your local disk, components will write to and read from a **Google Cloud Storage (GCS)** bucket. This shared bucket acts like a common drive for transcripts, generated text, and synthesized audio.

This setup gives you a practical hands-on experience now, while preparing you for the **API-driven systems** we’ll tackle later.

---

### GCS Bucket Details
In Google Cloud, a **bucket** is like a shared online folder where files can be stored and retrieved. Instead of saving outputs locally, our pipeline components will write and read to this shared bucket so all stages can communicate easily.

- `input_audios/` — raw audio files (starting point).  
- `text_prompts/` — transcripts generated from speech-to-text.  
- `text_paragraphs/` — expanded text generated by the LLM.  
- `text_translated/` — translated versions of the text.  
- `text_audios/` — synthesized English audio clips for each paragraph.  
- `output_audios/` — final synthesized audio outputs in the target language.  
- `output_audios_pp/` — bonus: audio outputs synthesized with ElevenLabs in Pavlos’ voice.  

![Mega pipeline bucket](mega-pipeline-bucket.png)

Want to learn more about GCS?
- [Google Cloud Storage](https://www.youtube.com/watch?v=VDBhvexAj8I)
- [Google Cloud Storage Overview](https://cloud.google.com/storage) 

## GCP Credentials File

The last piece we need in order to access the GCP bucket is authentication.
Buckets won’t let you read or write anything unless you are both authenticated (proving who you are) and authorized (having the right permissions).

In this course, you don’t need to authenticate yourself as a person. Instead, you’ll authenticate your app so it can talk to GCP securely. The way we do this is by using a Service Account—part of IAM in GCP.

To keep it simple, you’ll use a JSON credentials file that represents this Service Account. **We’ve uploaded this file to the course Canvas site for you** — download it from the link below and place it inside `<app_folder>/secrets/` in each component folder you build:

<a href="https://canvas.harvard.edu/files/23163432/download?download_frd=1" download>mega-pipeline.json</a> *(on Canvas — sign in with your Harvard Key if prompted)*

Later in the course, we’ll revisit authentication in more depth, but for now, this file is all you need to let your containerized apps talk to the GCP bucket.

### 🔑 Important Note on Secrets

We do not want to put this JSON file in GitHub — it is a secret, after all.
Make sure the secrets/ folder containing the file is not part of your repo. For this tutorial, we’ve already added a .gitignore entry so the file won’t be pushed accidentally. The canonical (best) way to handle this is to keep your secrets folder outside the repo entirely. That’s what we’ll be moving toward later in the course.

## Running the Pipeline Components

Once you’re inside each component’s container, you’ll drive it through `cli.py`. The commands for each stage are listed below — the flag names (`--download`, `--transcribe`, `--generate`, `--translate`, `--synthesis`, `--upload`) should make the intent obvious: pull inputs from the bucket, run the component, push outputs back.

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


### Sample Dockerfile
```dockerfile
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
> Docker Desktop installation is covered in [Tutorial 0](https://github.com/dlops-io/ac215-setup). These are the gotchas that show up *after* install:

* Run docker commands from **Git BASH** (Windows `cmd` and PowerShell quote arguments differently and will mangle the volume-mount syntax below).
* **Always quote `$(pwd)`** — Windows paths often contain spaces (e.g. `C:\Users\First Last\...`), and without quotes the shell splits the path mid-argument.
* If you see `the input device is not a TTY.`, prefix the command with `winpty`. Git BASH on Windows doesn't expose a real TTY to Docker, and `winpty` is the shim that fixes it.
* Putting it all together, the run command from earlier becomes:
  ```bash
  winpty docker run --rm -ti -v "$(pwd)":/app generate_text
  ```

## Solutions
Solutions to this tutorial will be posted here after the assignment deadline.
