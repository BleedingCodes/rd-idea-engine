# DISCLAIMER — R&D Idea Engine

**MainbyteLabs | mr.mainbytelabs@gmail.com | github.com/MR-MainbyteLabs**

Read this before choosing which version to run.

---

## Third-Party Cost Notice

Two of the three versions in this package connect to external AI APIs owned and operated by third parties. MainbyteLabs does not charge you to use this tool. However, the AI providers do charge for usage.

| Version | Provider | Cost | Account Required |
|---|---|---|---|
| Option A — OpenAI | OpenAI (openai.com) | ~$0.01–$0.05 per run | Yes — openai.com |
| Option B — CLI | Anthropic (anthropic.com) | ~$0.01–$0.03 per run | Yes — console.anthropic.com |
| Option C — Ollama | None | Free | No |

- MainbyteLabs has no visibility into your usage
- MainbyteLabs receives no portion of what you pay any third party
- You are responsible for your own account, billing, and spend limits
- Set usage limits in your provider's dashboard to control costs

---

## Differences Between the Three Versions

### Option A — OpenAI Browser App

**How it runs:** Browser app served by a local proxy. Your OpenAI API key is set as an environment variable — it never touches the browser.

**What you need:** Python, an OpenAI account with billing enabled, an OpenAI API key.

**Best for:** Anyone who already has an OpenAI account or prefers GPT-4o over other models.

**Limitations:** Requires OpenAI account and payment method. Output quality depends on GPT-4o. Web search in Research Mode uses OpenAI's built-in search tool.

**Cost:** Approximately $0.01–$0.05 per full run depending on idea count and model used.

---

### Option B — Python CLI

**How it runs:** Terminal only. No browser, no UI. You run a Python script, answer prompts, and output is saved to a Markdown file.

**What you need:** Python, an Anthropic account with billing enabled, an Anthropic API key.

**Best for:** Anyone who prefers terminal workflows, wants to automate runs, or wants to pipe output into other tools.

**Limitations:** No visual UI. Output is plain text / Markdown. Less interactive than the browser versions.

**Cost:** Approximately $0.01–$0.03 per full run.

---

### Option C — Ollama Local

**How it runs:** Browser app served by a local proxy. All AI processing happens on your machine using a locally running model via Ollama. No internet connection required after setup.

**What you need:** Python, Ollama installed, a compatible local model pulled (llama3 or mistral recommended).

**Best for:** Anyone who wants zero third-party cost, full privacy, or offline use.

**Limitations:** Output quality is lower than GPT-4o or Claude. Research Mode (web search) is not available — Paste Mode only. Local models may produce less structured JSON requiring more retries. Requires a machine with enough RAM to run the model (8GB minimum, 16GB recommended).

**Cost:** Free. Electricity only.

---

## Which Should You Use

| If you want... | Use |
|---|---|
| Best output quality | Option A or B |
| No cost ever | Option C |
| Browser UI | Option A or C |
| Terminal workflow | Option B |
| Web research (Research Mode) | Option A or B |
| Full privacy, offline | Option C |
| Already have OpenAI account | Option A |
| Already have Anthropic account | Option B |

---

## Security Note — API Keys

All three versions that use API keys follow the same pattern: the key is set as an environment variable in your terminal and injected by a local proxy server. The key never appears in the browser, in any file, or in any log. Closing the terminal session clears the key from memory.

Never paste your API key directly into `app.html` or share it with anyone.

---

*MainbyteLabs Technical Analytics*
*R&D Idea Engine | github.com/MR-MainbyteLabs*
