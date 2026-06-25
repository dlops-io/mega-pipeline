# 🎙️ Codecast — Mega Pipeline (formaggio.me content engine)

**Branch:** `main` (the simple, "training-wheels" version — shared bucket, shared service-account key, sample Dockerfile)
**Format:** Pavlos drives, Rashmi helps / asks questions.
**Audience:** Students do this live in class; this codecast is the reference anyone can follow afterward, on their own.
**Style:** Start simple — even a little tedious — on purpose. Do one container in full depth; the rest follow the same pattern.

---

## 0. Cold open — the vision (~2.5 min)

> **Say (with energy):**
> "Let me tell you about **formaggio.me**. It's the app I'm building, and here's the thing — it is *not* going to be just another chatbot. We'll build the chatbot, sure, that comes later as we go. But formaggio.me is a *destination*. A place about cheese. Somewhere people come to learn it, talk about it, fall in love with it — connect with cheesemakers, with sellers, with a newsletter, with *me* actually making my own cheese."
>
> "And to pull people in, you need content. Real content, at scale, in every language. So I did the most natural thing in the world — I recorded a podcast. About **halloumi**. Which is, hands down, the best cheese in the world... okay, *one* of the best." *(grin)*
>
> "Now I've got this one rough English recording. But formaggio.me needs it transcribed, expanded into a real article, translated for cheese lovers in France, and turned back into audio so it can go out as a podcast in *two* languages. By hand? Forget it. So we build a machine that does it for me — and that machine is what we're building today."

Show `mega-pipeline-flow.png`. Trace it:

> "🎙️ my halloumi recording → 📝 transcribe it → 🗒️ let an LLM expand it into a proper piece → 🇫🇷 translate it → 🔊 synthesize it back into audio. Five components, five little containers, each doing one job — the **content engine behind formaggio.me**."

**The AC215 how-we-work note:**

> "And here's how we do it in AC215: we follow **best practices for MLOps and DevOps**. That means we **containerize every single step** — every one of these five gets its own container. Now, I'll be honest with you up front: today this is going to feel a little **tedious**. Maybe even redundant. And that's *fine* — that's on purpose. The next tutorial gets into the more proper, streamlined workflows. But the goal of this course is to learn, step by step, *how things are actually done* — and to build them up that way ourselves."
>
> "My style is to always **start simple** — sometimes a little tedious — because when you do it the slow way first, you *understand* it. You internalize *why* each piece is there. So when we speed it up later, you're not cargo-culting a workflow you don't get — you actually know what it's doing and why."

**Rashmi:** *"So this whole pipeline is feeding formaggio.me — it's not just a demo?"*
> "Exactly. Every blog post, every translated podcast, every newsletter blurb about a new cheese — this is the thing that produces it. Today it's halloumi. Tomorrow it's running for every cheese I cover."

**Rashmi:** *"Why five separate containers instead of one script?"*
> "Because that's how real products are built — independent services, each doing one job, that you can develop, swap, and scale on their own. And like I said: simple and explicit first, so we understand it. We're building formaggio.me the way you'd build a real system, not a toy."

---

## 1. The teams + leaderboard hook (~1 min)

Open **[ac215-mega-pipeline.dlops.io](http://ac215-mega-pipeline.dlops.io/)** on screen.

> "You work in groups, and every team's progress is live here. The moment a component runs successfully under your group name, it lights up for the whole class."

**Rashmi:** *"So everyone sees our progress in real time?"*
> "Yes — which is why the **group name** matters. Set it wrong and your work shows up under the wrong team, or overwrites someone else's. We'll see exactly where to set it."

---

## 2. How the components talk — the bucket as message bus (~3 min)

> "In production, microservices call each other through APIs. We haven't covered APIs yet, so we simplify: each component **writes its output to shared storage**, and the next one **reads it as input**. The storage is a Google Cloud Storage bucket — a shared online folder."

Show the prefixes (and `mega-pipeline-bucket.png`):

```
input_audios/     ← raw audio (start)
text_prompts/     ← transcripts
text_paragraphs/  ← LLM-expanded text
text_translated/  ← translations
text_audios/      ← synthesized clips
output_audios/    ← final French audio
```

**Rashmi:** *"So no component talks to another directly?"*
> "Right — the bucket is the hand-off. Transcribe writes `text_prompts/`, Generate reads `text_prompts/` and writes `text_paragraphs/`, and so on down the chain."

---

## 3. Credentials — the shared service-account JSON (~3 min)

> "A bucket won't let you read or write unless you're **authenticated** (who you are) and **authorized** (allowed to). You don't authenticate as *yourself* — you authenticate your *app*, using a **service account**: an identity for code."

Walk it:
- Download `mega-pipeline.json` from **Canvas** (HarvardKey if prompted).
- Drop it in `<app_folder>/secrets/` inside each component folder.
- "🔑 Never put this in GitHub. There's already a `.gitignore` entry so it won't get pushed by accident. Later in the course we move secrets outside the repo entirely — for now this is enough."

**Rashmi:** *"Wait — we all share one key?"*
> "For this first pass, yes — it keeps the focus on the pipeline, not on IAM. Later you'll each create and own your own service account."

---

## 4. ⭐ Build the container — from scratch, as we go (~6 min)

> "Here's the thing — there is **no Dockerfile** in this folder. *We* write it. This is the heart of the tutorial, so we go slow and build it up piece by piece. I'm not going to paste a finished file — I want you to feel *why* each line is there. We add nothing we don't need."

### a) Scaffold the Python project
> "First, a `pyproject.toml` to declare our dependencies. `uv` scaffolds a bare one for us:"
```bash
uv init --bare
```
> "`--bare` means *just* the `pyproject.toml` — no sample `main.py`, no git init. Our code already lives here; we only want the dependency file. We'll add the actual packages in a minute."

### b) Write the Dockerfile, line by line
> "Now a new file called `Dockerfile`. I'll build it up and say what each block buys us."

```dockerfile
# Start from a small official Python image
FROM python:3.12-slim-bookworm
```
> "Slim Debian + Python 3.12. Small, official, predictable."

```dockerfile
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```
> "Three env vars. The first two tell `uv` where to put the virtual environment. The **third is the magic one** — the Google client library reads `GOOGLE_APPLICATION_CREDENTIALS` on startup, finds our JSON key, and authenticates. No auth code anywhere. Just point at the file."

**Rashmi:** *"What exactly is `UV_LINK_MODE=copy` — what does that one do?"*
> "By default `uv` installs packages by **hardlinking** them from its download cache into the venv — a hardlink is a second name for the same bytes on disk, so it's instant and uses no extra space. *But* hardlinks only work inside a single filesystem, and in Docker the cache and the venv often sit on different layers — different filesystems. So the hardlink fails and `uv` prints a warning. `copy` just says 'skip the clever trick, copy the files in' — always works, clean build, no warning. Costs a sliver of disk; here that's nothing."

```dockerfile
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
```
> "OS-level packages. `build-essential` for compiling, and `ffmpeg` because this component touches audio. Notice — this is the *one* component-specific line. Generate-text won't need ffmpeg; synthesis will. **You only install what your code actually uses.**"

```dockerfile
RUN pip install --no-cache-dir --upgrade pip && pip install uv
```
> "Install `uv` itself — our fast package manager."

**Rashmi:** *"Wait — last tutorial, on the VM, we had to write `pip install uv --break-system-packages`. Why did we need that flag then, and not now?"*
> "Great catch — and the flag was never about `uv`. On the VM we were installing into the **system Python**, the one the OS uses for its own tools. Modern Linux protects that with a rule called **PEP 668**: it marks the system Python as 'externally managed' and tells pip *'don't install here, you'll clobber something the OS depends on — use a venv.'* `--break-system-packages` is the escape hatch: 'I know, do it anyway' — fine on a throwaway VM."
>
> "But here we're on the **official Python Docker image**, and those images deliberately **don't** set that marker. There's no system Python to protect — the whole container *is* our environment. So plain `pip install uv` just works. Same command, different environment — and now you know that flag was about the OS, never about uv."

*(If asked "what is PEP 668?" → "It's the OS saying 'this Python is mine — install into your own venv, not here.' It exists because pip and apt writing into the same Python used to break systems. The marker is a file called `EXTERNALLY-MANAGED`; the official Python images leave it out on purpose.")*

```dockerfile
RUN mkdir -p /app
WORKDIR /app
COPY . ./
RUN uv sync
```
> "Make and enter `/app`, copy our source in, and `uv sync` builds the virtual environment from the `pyproject.toml` we scaffolded — which is still **empty**, so right now it installs no third-party packages. That's expected; we add those once we're inside."

> 💡 *Quick reminder — `uv sync`:* reads `pyproject.toml` (and the `uv.lock` lockfile), creates the venv if needed, and installs **exactly** those dependencies into it — so the environment matches the declared packages precisely. Think of it as "make the venv match the project's dependency list."

```dockerfile
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```
> "And when the container starts, drop me into bash with the venv already activated — so I can just run `python cli.py`."

> "That's it. Minimal, and every line earns its place. *(If you get stuck, the README has a fuller sample Dockerfile to compare against — but try it yourself first.)*"

### c) ...but the packages come later — and that's deliberate
> "Notice what we did **not** do: we never added our Python packages. `pyproject.toml` is still empty. That `uv sync` we just ran built a venv with *nothing* third-party in it — and that's fine. We'll `uv add` the real packages in the next step, **once we're inside the running container**. Hold that thought."

> ⚠️ *Pre-cast check:* the `pyproject.toml` that `uv init` writes stamps a `requires-python` from your host's `uv`. Make sure it's **`>=3.12`**, not `>=3.14` — the image is Python 3.12, and a mismatch makes `uv sync` fail at build.

**Rashmi:** *"How does the container actually find the credentials — we never wrote login code?"*
> "That one `GOOGLE_APPLICATION_CREDENTIALS` env var. `google.cloud.storage` checks it on startup, finds the JSON in `secrets/`, done. Authentication with zero auth code — that's the whole trick."

**Rashmi:** *"Why build the Dockerfile by hand instead of just giving us one?"*
> "Because next tutorial I *will* give you one — and you'd have no idea what's in it. Build it once yourself and you'll read any Dockerfile for the rest of your life. Tedious now, fluent later."

---

## 5. DEEP DIVE — transcribe_audio: build, add deps, run (~6 min)

> "We've written the Dockerfile and scaffolded an *empty* `pyproject.toml`. Now we **build the image**, **go inside**, **add our packages**, and **run** the pipeline. Everything from here is the *exact same pattern* for the other four. Learn it once, repeat it four times."

**Build the image, then run into it:**
```bash
docker build -t transcribe_audio .
docker run --rm -ti -v "$(pwd)":/app transcribe_audio
```
> "`-v "$(pwd)":/app` mounts my current folder into the container — my code *and* my `secrets/` go in. `--rm` cleans up on exit. `-ti` gives me an interactive terminal. And now — notice the prompt changed — I'm *inside* the container."

**Now add the packages — inside the container:**
```bash
uv add google-cloud-storage google-cloud-speech ffmpeg-python
```
> "*This* is where the deps go in. I open `cli.py`, see it imports storage, speech, ffmpeg — and `uv add` exactly those, nothing more. This writes them into `pyproject.toml` (which lives on my host through the mount, so it persists) **and** installs them into the venv right now, so I can run the code this second."

**Rashmi:** *"Why add them in here and not in the Dockerfile?"*
> "Two reasons. One, it's the natural dev loop — you discover a dependency, you add it, you keep going, all inside the container where `uv` already lives. Two — honest heads-up — because we used `--rm`, the venv is *ephemeral*: when I exit, the installed packages vanish. Only `pyproject.toml` survived, on my host. So once it works, I **rebuild the image** — now `uv sync` bakes the deps in permanently and I never `uv add` again. Add-inside to discover; rebuild to make it stick."

**Rashmi:** *"Couldn't we just `uv add` on our laptop — the host — instead, before building?"*
> "You absolutely can, and it's actually a bit cleaner. If I run `uv add` on the host *right after* `uv init`, it writes the packages into `pyproject.toml` and `uv.lock` **before** I build. Then when I build, `uv sync` bakes them straight into the image — no ephemeral venv, no rebuild dance. One and done."
>
> "So why am I doing it inside the container instead? Two reasons. First, it matches your component README, so when you follow along the steps line up. Second — and this is the real one — it only works on the host **if you have `uv` installed on your laptop**. Inside the container, `uv` is *guaranteed* to be there because our Dockerfile installed it. Doing it inside means the container is the single source of truth — your laptop needs nothing but Docker. That's the whole spirit of containerizing: the environment travels *with* the project, not with your machine."
>
> *(Caveat to mention: we already used `uv init` on the host, which does need host-side `uv` — so for this tutorial you do have it. The 'laptop needs nothing but Docker' ideal is where we're heading, not quite where we are today.)*

**Set the group name** (show it in `cli.py`):
> "Before anything runs: this is where the group name lives. If it's wrong, my halloumi transcript lands under the wrong team. Set it. Always."

**Run the three steps:**
```bash
python cli.py --download     # pull raw halloumi audio from the bucket
python cli.py --transcribe   # Google Speech-to-Text turns it into text
python cli.py --upload       # write the transcript to text_prompts/<group>/
```
> "Three verbs: pull inputs, do the work, push outputs. That's the shape of every component."

Watch the **leaderboard** light up.

**Rashmi:** *"What if I forgot to set the group name?"*
> "Your output lands in the wrong place — wrong team on the leaderboard, or you clobber someone. Check it before every run."

---

## 6. BRISK — generate_text: same pattern, one new thing (~3 min)

> "Same recipe — but this folder *also* has no Dockerfile, so we build one again. Watch how little changes."

```bash
cd ../generate_text
uv init --bare                                    # scaffold (empty) pyproject.toml
# write a Dockerfile — IDENTICAL to transcribe's, except:
#   apt install build-essential   ← NO ffmpeg this time (no audio here)
docker build -t generate_text .
docker run --rm -ti -v "$(pwd)":/app generate_text
# inside the container:
uv add google-cloud-storage google-genai          # ← packages this cli.py imports
python cli.py --download     # reads text_prompts/  (the transcript we just made)
python cli.py --generate     # ← the ONE new thing: calls an LLM to expand it
python cli.py --upload       # writes text_paragraphs/
```

> "Same dance: scaffold empty, build, go inside, `uv add` what *this* `cli.py` imports, run. Two differences from transcribe, both tiny: drop `ffmpeg` from the apt line because there's no audio here, and `uv add` the genai package instead of speech. Everything else — the Dockerfile shape, the build, the run, the three verbs — is *identical*. And `--generate` is the one new step: it hands the transcript to an **LLM** to expand my rough notes into a proper formaggio.me article. Same bucket hand-off."

**Rashmi:** *"So once you know one, you basically know them all?"*
> "That's the whole point of doing the first one slowly. The pattern *is* the lesson."

---

## 7. SPEED ROUND — the last three (~3 min)

> "Now I'll go fast, because you already know the recipe: `uv init --bare` → write the same Dockerfile (add `ffmpeg` only if it touches audio) → build → go inside → `uv add` whatever that `cli.py` imports → run. I'll just call out what's *unique* about each."

**Synthesize Audio — English** (`synthesis_audio_en/`) — *audio → keep `ffmpeg`; `uv add` texttospeech*:
```bash
python cli.py --download
python cli.py --synthesis    # Text-to-Speech → English audio of the article
```

**Translate Text** (`translate_text/`) — *no audio → drop `ffmpeg`; `uv add` translate*:
```bash
python cli.py --download
python cli.py --translate    # Google Translate → French
python cli.py --upload       # writes text_translated/
```

**Synthesize Audio — French** (`synthesis_audio/`) — *audio again → `ffmpeg` + texttospeech*:
```bash
python cli.py --download
python cli.py --synthesis    # Text-to-Speech → French audio
```

> **Payoff:** play the final French halloumi audio. "There it is — one rough English recording, now a polished bilingual podcast, ready for formaggio.me. *That's* the content engine."

---

## 8. Close (~2 min)

> "So today you built the **content engine** that turns one halloumi recording into a bilingual podcast for formaggio.me — and that's just *one* part of the app. The chatbot, the newsletter, the cheesemaker connections — those come as we go."
>
> "And notice what we did: we did it the **simple, explicit, slightly tedious way** — five containers, by hand, step by step. Next tutorial we make it *proper* — streamlined workflows, your own infrastructure. But now, when we speed it up, you'll know exactly what every piece is doing and *why*. That's the whole idea of this course."

---

## 📋 Driver cheat-sheet (keep visible)

**The recipe — same for every component:**
```bash
uv init --bare                          # 1. scaffold an (empty) pyproject.toml   [on host]
#   2. write Dockerfile (same shape; ffmpeg only if it touches audio)
docker build -t <name> .                # 3. build image
docker run --rm -ti -v "$(pwd)":/app <name>   # 4. run → drops you INSIDE the container
uv add <packages this cli.py imports>   # 5. INSIDE: declare + install deps
python cli.py ...                       # 6. INSIDE: run the steps
#   ↳ to bake deps in permanently: exit & rebuild (uv sync picks them up)
```
> Alt order: `uv add` on the **host** right after step 1 (before build) → deps baked at build time, no rebuild needed. README uses the inside-container order above.

| Step | Folder | Audio? (ffmpeg) | `uv add` | Inside container |
|---|---|---|---|---|
| 📝 Transcribe | `transcribe_audio` | ✅ yes | `google-cloud-storage google-cloud-speech ffmpeg-python` | `--download` → `--transcribe` → `--upload` |
| 🗒️ Generate | `generate_text` | ❌ no | `google-cloud-storage google-genai` | `--download` → `--generate` → `--upload` |
| 🔊 Synth EN | `synthesis_audio_en` | ✅ yes | `google-cloud-storage google-cloud-texttospeech` | `--download` → `--synthesis` |
| 🇫🇷 Translate | `translate_text` | ❌ no | `google-cloud-storage google-cloud-translate` | `--download` → `--translate` → `--upload` |
| 🔊 Synth FR | `synthesis_audio` | ✅ yes | `google-cloud-storage google-cloud-texttospeech` | `--download` → `--synthesis` |

> ✅ These `uv add` lists are verified against each `cli.py`'s actual imports. (`translate_v2` ships in `google-cloud-translate`.)

**Say out loud, every time:**
1. Set your **group name** before each run.
2. **Windows:** use Git BASH, quote `"$(pwd)"`, prefix with `winpty` if you see "the input device is not a TTY."

**Pacing:** deep build on #1, brisk on #2, speed-round #3–5. Total ≈ 28–33 min.
