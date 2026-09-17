# START — Option B: CLI

---

## What You Need

- Python 3.11+
- An Anthropic API key — get one at console.anthropic.com

---

## Get an Anthropic API Key

1. Go to **console.anthropic.com**
2. Sign in or create an account
3. Click **API Keys** → **Create Key**
4. Name it — e.g. `rd-idea-engine`
5. Copy immediately — starts with `sk-ant-`, shown once only

**Cost notice:**
This tool connects to Anthropic's API — a paid third-party service. MainbyteLabs does not charge you. Anthropic does. Add a payment method at console.anthropic.com under **Billing**. Each full run costs approximately $0.01–$0.03. Set a spend limit under **Billing → Usage Limits**.

---

## One-Time Setup

```
pip install -r requirements.txt
```

---

## Every Time You Run

### Step 1 — Set your key

**Linux / Mac:**
```
export ANTHROPIC_API_KEY=your_key_here
```
**Windows CMD:**
```
set ANTHROPIC_API_KEY=your_key_here
```

### Step 2 — Run

```
python cli.py
```

The tool walks you through input mode, focus areas, idea count, idea selection, and stress test interactively. Output is saved as a Markdown file in the same folder.

---

## Output

Each run saves a file named:
```
rd_output_CompanyName_YYYYMMDD_HHMMSS.md
```

Open it in any Markdown viewer, text editor, or paste it into Notion/Obsidian.

---

*MainbyteLabs | mr.mainbytelabs@gmail.com*
