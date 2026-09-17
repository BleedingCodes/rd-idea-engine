# Option C — Ollama Local

Browser-based R&D Idea Engine running entirely on your machine via Ollama.
No API key. No third-party account. No cost. No internet required after setup.

**Provider:** None — fully local
**Interface:** Browser app at http://localhost:5050/
**Research Mode:** Not available — Paste Mode only
**Requires:** Python, Ollama, a pulled local model (llama3 or mistral)

Read `DISCLAIMER.md` in the root folder before using.
Read `START.md` in this folder to run the tool.

---

## Files

| File | Purpose |
|---|---|
| `app.html` | The tool UI |
| `proxy.py` | Local server — routes browser requests to Ollama |
| `START.md` | How to run |
| `README.md` | This file |

---

## Limitations vs Cloud Versions

- Paste Mode only — no web search
- Lower output quality than GPT-4o or Claude
- Slower inference, especially on CPU
- Occasional JSON parse errors — retry if they occur
- Idea count capped at 10 for reliability

---

*MainbyteLabs | mr.mainbytelabs@gmail.com*
