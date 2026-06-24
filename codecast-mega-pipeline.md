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

## 4. The sample Dockerfile (~4 min)

Open the Dockerfile. Hit highlights — don't read line by line:

- `FROM python:3.12-slim-bookworm` — slim base image.
- `pip install uv` → `uv sync` — "uv is a fast Python package manager; it builds the venv from the lockfile."
- `useradd app` + `USER app` — "we don't run as root inside the container — basic hygiene."
- `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` — "the magic line: the Google client reads this env var automatically, finds the JSON, authenticates. No code change needed."
- `COPY . ./` + the venv-activating `CMD` — "you land in a shell with the environment ready."

**Rashmi:** *"How does the container actually find the credentials?"*
> "That one `GOOGLE_APPLICATION_CREDENTIALS` env var. `google.cloud.storage` checks it on startup. Point it at the JSON, you're authenticated transparently."

---

## 5. ⭐ DEEP DIVE — transcribe_audio, end to end (~5 min)

> "We'll do **this one in full**. Everything you learn here — the build, the run, the three steps — is the *exact same pattern* for the other four. Learn it once, repeat it four times."

**Build & run:**
```bash
cd transcribe_audio
docker build -t transcribe_audio .
docker run --rm -ti -v "$(pwd)":/app transcribe_audio
```
> "`-v "$(pwd)":/app` mounts my current folder into the container — my code *and* my `secrets/` go in. `--rm` cleans up on exit. `-ti` gives me an interactive terminal. And now — notice the prompt changed — I'm *inside* the container."

**Set the group name first** (show it in `cli.py`):
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

## 6. BRISK — generate_text: same pattern, one new thing (~2 min)

> "Watch — *exact same shape*. Build, run, three steps."

```bash
cd ../generate_text
docker build -t generate_text .
docker run --rm -ti -v "$(pwd)":/app generate_text
# inside:
python cli.py --download     # reads text_prompts/  (the transcript we just made)
python cli.py --generate     # ← the ONE new thing: calls an LLM to expand it
python cli.py --upload       # writes text_paragraphs/
```

> "The only real difference is `--generate`: instead of a Google audio API, this one hands the transcript to an **LLM** and asks it to expand my rough transcript into a proper formaggio.me article. Same download/upload bookends. Same bucket hand-off."

**Rashmi:** *"So once you know one, you basically know them all?"*
> "That's the whole point of doing the first one slowly. The pattern *is* the lesson."

---

## 7. SPEED ROUND — the last three (~3 min)

> "Now I'll go fast, because you already know the pattern. I'm just showing you what's *unique* about each."

**Synthesize Audio — English** (`synthesis_audio_en/`) — *needs `ffmpeg` in its Dockerfile for audio*:
```bash
python cli.py --download
python cli.py --synthesis    # Text-to-Speech → English audio of the article
```

**Translate Text** (`translate_text/`):
```bash
python cli.py --download
python cli.py --translate    # Google Translate → French
python cli.py --upload       # writes text_translated/
```

**Synthesize Audio — French** (`synthesis_audio/`):
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

| Step | Folder | Build & run | Inside container |
|---|---|---|---|
| 📝 Transcribe | `transcribe_audio` | `docker build -t transcribe_audio .`<br>`docker run --rm -ti -v "$(pwd)":/app transcribe_audio` | `--download` → `--transcribe` → `--upload` |
| 🗒️ Generate | `generate_text` | same pattern | `--download` → `--generate` → `--upload` |
| 🔊 Synth EN | `synthesis_audio_en` | same | `--download` → `--synthesis` |
| 🇫🇷 Translate | `translate_text` | same | `--download` → `--translate` → `--upload` |
| 🔊 Synth FR | `synthesis_audio` | same | `--download` → `--synthesis` |

**Say out loud, every time:**
1. Set your **group name** before each run.
2. **Windows:** use Git BASH, quote `"$(pwd)"`, prefix with `winpty` if you see "the input device is not a TTY."

**Pacing:** deep on #1, brisk on #2, speed-round #3–5. Total ≈ 25–30 min.
