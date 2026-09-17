# START — Option A: OpenAI Browser App

---

## What You Need

- Python 3.11+
- An OpenAI API key — get one at platform.openai.com
- Files in this folder: `app.html`, `proxy.py`

---

## Get an OpenAI API Key

1. Go to **platform.openai.com**
2. Sign in or create an account
3. Click **API Keys** in the left sidebar
4. Click **Create new secret key**
5. Name it — e.g. `rd-idea-engine`
6. Copy immediately — shown once only, starts with `sk-`

**Cost notice:**
This tool connects to OpenAI's API — a paid third-party service. MainbyteLabs does not charge you. OpenAI does. You are responsible for your own account and billing. Add a payment method at platform.openai.com under **Billing** before your key will work. Each full run costs approximately $0.01–$0.05. Set a spend limit under **Billing → Usage Limits**.

---

## One-Time Setup

```
pip install flask flask-cors requests
```

---

## Every Time You Run

### Step 1 — Set your key

**Linux / Mac:**
```
export OPENAI_API_KEY=your_key_here
```
**Windows CMD:**
```
set OPENAI_API_KEY=your_key_here
```
**Windows PowerShell:**
```
$env:OPENAI_API_KEY="your_key_here"
```

### Step 2 — Start the proxy
```
python proxy.py
```

Expected output:
```
  MainbyteLabs R&D Idea Engine — Option A (OpenAI)
  Open in browser: http://localhost:5050/
  API key: set ✓
```

### Step 3 — Open the tool

Go to: `http://localhost:5050/`

Do NOT open `app.html` by double-clicking it.

### Step 4 — Verify
```
http://localhost:5050/health
```
Must show `"api_key_set": true` before running.

---

## Stop the Proxy

Press `Ctrl + C` in the terminal.

---

*MainbyteLabs | mr.mainbytelabs@gmail.com*
