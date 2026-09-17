# R&D Idea Engine

**MainbyteLabs | mr.mainbytelabs@gmail.com | github.com/MR-MainbyteLabs**

Execution-focused R&D research and stress-test tool. Point it at any company or product, generate improvement ideas from publicly available information, select the ones worth pursuing, and run them through an aggressive stress test before committing any time to them.

---

## ⚠️ Testing Status

This tool has three options (A, B, C). **Only Option C (Ollama — Local) has been tested.**

Testing was carried out to the point of input submission and processing initiation.
Output generation has not been verified. Options A (OpenAI browser) and B (Anthropic CLI)
are untested.

Use at your own risk. Feedback and test reports welcome — open an issue if you run it
further than I did.

## Package Structure

```
rd-idea-engine/
├── README.md                  ← This file
├── DISCLAIMER.md              ← Read before choosing a version
│
├── option-a-openai/           ← Browser app — OpenAI API
│   ├── app.html
│   ├── proxy.py
│   ├── README.md
│   └── START.md
│
├── option-b-cli/              ← Terminal CLI — Anthropic API
│   ├── cli.py
│   ├── requirements.txt
│   ├── README.md
│   └── START.md
│
└── option-c-ollama/           ← Browser app — fully local, no cost
    ├── app.html
    ├── proxy.py
    ├── README.md
    └── START.md
```

---

## Start Here

**Read `DISCLAIMER.md` first.** It explains the differences between all three versions, which require third-party accounts, what each costs, and which to choose based on your situation.

Then go into the folder for your chosen version and follow its `START.md`.

---

## What the Tool Does

**Phase 1 — Research**
Pulls publicly available information on a target company or product (Research Mode), or accepts research you paste in yourself (Paste Mode).

**Phase 2 — Idea Generation**
Generates 8–15 distinct R&D improvement ideas scoped to focus areas you select. Each idea includes difficulty, time estimate, scope risk, and smallest working version.

**Phase 3 — Stress Test**
Evaluates selected ideas with BUILD NOW / DELAY / DROP verdicts, scores, friction ratings, hidden complexity analysis, and ranked output.

---

## Built By

MainbyteLabs | Philadelphia, PA
github.com/MR-MainbyteLabs | mr.mainbytelabs@gmail.com

Origin
This tool was converted from the Guided Build Framework (github.com/BleedingCodes/guided-build-framework) — a prompt-based system for idea generation and execution-focused evaluation. The framework defined the evaluation logic and stress test criteria. This repo is the full implementation: browser UI, local proxy, CLI, and three deployment options built from that foundation.
