# START — Option C: Ollama (Local, Free)

---

## What You Need

- Python 3.11+
- Ollama installed on your machine
- A local model pulled (llama3 or mistral recommended)
- Files in this folder: `app.html`, `proxy.py`

**No API key. No third-party account. No cost.**

---

## One-Time Setup

### Step 1 — Install Ollama

Go to **ollama.com** and download the installer for your OS. Install it.

### Step 2 — Pull a model

Open a terminal and run:

```
ollama pull llama3
```

This downloads the model to your machine (~4GB). Do this once. Takes a few minutes depending on your connection.

Alternatives if llama3 is too large for your machine:
```
ollama pull mistral      (smaller, still capable)
ollama pull gemma:2b     (very small, lower quality)
```

### Step 3 — Install Python dependencies

```
pip install flask flask-cors requests
```

---

## Every Time You Run

### Step 1 — Start Ollama

```
ollama serve
```

Leave this terminal open.

### Step 2 — Start the proxy

Open a second terminal in this folder and run:

```
python proxy.py
```

Expected output:
```
  MainbyteLabs R&D Idea Engine — Option C (Ollama)
  Open in browser: http://localhost:5050/
  Ollama: running ✓
  Models: llama3
```

If you see `WARNING: Ollama is not running` — go back to Step 1.

### Step 3 — Open the tool

Go to: `http://localhost:5050/`

Do NOT open `app.html` by double-clicking it.

### Step 4 — Verify

```
http://localhost:5050/health
```

Must show `"ollama_running": true` and your model listed under `available_models`.

---

## Important Differences from Cloud Versions

- **Paste Mode only** — local models cannot search the web
- **Idea count capped at 10** — higher counts cause JSON parse errors with local models
- **Slower** — local inference is slower than cloud APIs, especially on CPU
- **Lower output quality** — local models produce less precise, less structured output than GPT-4o or Claude
- **Retry on parse errors** — local models occasionally produce malformed JSON; retry once if this happens

---

## System Requirements

| RAM | Recommended Model |
|---|---|
| 8GB | mistral or gemma:2b |
| 16GB | llama3 |
| 32GB+ | llama3 or larger models |

Running on CPU is slow but works. A GPU significantly speeds up inference.

---

## Stop Everything

- Press `Ctrl + C` in the proxy terminal
- Press `Ctrl + C` in the ollama serve terminal

---

*MainbyteLabs | mr.mainbytelabs@gmail.com*
