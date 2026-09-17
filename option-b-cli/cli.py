"""
MainbyteLabs R&D Idea Engine — Option B: CLI
Terminal-based version. No browser required.
Output saved to a Markdown file.

Usage:
    python cli.py

Requires:
    pip install -r requirements.txt

Set your key before running:
    Linux/Mac:   export ANTHROPIC_API_KEY=your_key_here
    Windows CMD: set ANTHROPIC_API_KEY=your_key_here
"""

import os
import json
import sys
import datetime
import anthropic

FOCUS_OPTIONS = [
    ("performance",   "Performance"),
    ("efficiency",    "Efficiency"),
    ("features",      "Features"),
    ("cost",          "Cost Reduction"),
    ("reliability",   "Reliability"),
    ("software",      "Software / Firmware"),
    ("integration",   "Integration"),
    ("manufacturing", "Manufacturing"),
    ("safety",        "Safety"),
    ("ux",            "UX / Interfaces"),
]


def check_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("\n  ERROR: ANTHROPIC_API_KEY is not set.")
        print("  Set it before running:")
        print("    Linux/Mac:   export ANTHROPIC_API_KEY=your_key_here")
        print("    Windows CMD: set ANTHROPIC_API_KEY=your_key_here\n")
        sys.exit(1)
    return key


def separator(char="─", width=60):
    print(char * width)


def header():
    separator("═")
    print("  MainbyteLabs R&D Idea Engine — CLI")
    print("  github.com/MR-MainbyteLabs")
    separator("═")
    print()


def pick_focus_areas() -> list[str]:
    print("Focus Areas — enter numbers separated by commas, or press Enter for default (1,2,3):\n")
    for i, (tag, label) in enumerate(FOCUS_OPTIONS, 1):
        print(f"  {i:2}. {label}")
    print()
    raw = input("  Selection: ").strip()
    if not raw:
        selected = ["performance", "efficiency", "features"]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in raw.split(",")]
            selected = [FOCUS_OPTIONS[i][0] for i in indices if 0 <= i < len(FOCUS_OPTIONS)]
        except (ValueError, IndexError):
            print("  Invalid input — using default (performance, efficiency, features)")
            selected = ["performance", "efficiency", "features"]
    labels = [label for tag, label in FOCUS_OPTIONS if tag in selected]
    print(f"\n  Selected: {', '.join(labels)}\n")
    return selected


def pick_idea_count() -> int:
    raw = input("  Number of ideas to generate [8/12/15, default 12]: ").strip()
    if raw in ("8", "12", "15"):
        return int(raw)
    return 12


def pick_input_mode() -> tuple[str, str, str]:
    print("Input Mode:")
    print("  1. Research Mode — searches publicly available information")
    print("  2. Paste Mode    — paste your own research\n")
    mode = input("  Select [1/2, default 1]: ").strip()

    if mode == "2":
        print("\n  Paste your research below.")
        print("  When done, type END on a new line and press Enter:\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        research = "\n".join(lines)
        target = input("\n  Product / company name: ").strip() or "the product"
        return "paste", target, research
    else:
        target = input("\n  Company / product name: ").strip()
        if not target:
            print("  No target entered. Exiting.")
            sys.exit(0)
        return "research", target, ""


def call_claude(client: anthropic.Anthropic, system: str, user: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return response.content[0].text


def research_target(client: anthropic.Anthropic, target: str) -> str:
    print(f"\n  Researching {target}...")
    # Use web search via tool use
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{
            "role": "user",
            "content": f'Research "{target}" thoroughly. Find: product specifications, known limitations, competitor products, recent news, pricing, market positioning. Public information only. Summarize in detail.'
        }]
    )
    return "".join(b.text for b in response.content if getattr(b, "type", "") == "text")


def generate_ideas(client: anthropic.Anthropic, target: str, research: str, focus: list[str], count: int) -> list[dict]:
    print(f"  Generating {count} ideas...")
    system = f"""You are a ruthless R&D strategist. Generate exactly {count} distinct, actionable R&D improvement ideas.
Focus areas: {', '.join(focus)}.
CRITICAL: Return ONLY a valid JSON array. No markdown, no preamble. Start with [ end with ].
Each idea: {{"title":"","domain":"","description":"","difficulty":1,"dependencies":"","estimated_time":"","visible_result":"","smallest_version":"","why_interesting":"","scope_risk":"low|medium|high","connects_to":""}}"""
    raw = call_claude(client, system, f"Target: {target}\n\nResearch:\n{research}\n\nGenerate {count} ideas. JSON array only.")
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned[cleaned.index("["):cleaned.rindex("]") + 1])


def display_ideas(ideas: list[dict]) -> list[int]:
    print()
    separator()
    print(f"  {len(ideas)} Ideas Generated")
    separator()
    for i, idea in enumerate(ideas, 1):
        risk_sym = {"low": "●", "medium": "◆", "high": "▲"}.get(idea.get("scope_risk", ""), "●")
        print(f"\n  [{i:02}] {idea['title']}")
        print(f"       Domain: {idea.get('domain','')}  |  Difficulty: {idea.get('difficulty','')}/5  |  {risk_sym} {idea.get('scope_risk','')} scope risk")
        print(f"       {idea.get('description','')[:120]}...")
        print(f"       Time: {idea.get('estimated_time','')}  |  MVP: {idea.get('smallest_version','')[:80]}")

    print()
    separator()
    raw = input("  Select ideas to stress test (e.g. 1,3,5) or press Enter for all: ").strip()
    if not raw:
        return list(range(len(ideas)))
    try:
        return [int(x.strip()) - 1 for x in raw.split(",") if x.strip().isdigit()]
    except ValueError:
        return list(range(len(ideas)))


def stress_test(client: anthropic.Anthropic, target: str, ideas: list[dict]) -> dict:
    print(f"\n  Running stress test on {len(ideas)} ideas...")
    system = """You are a ruthless execution-focused technical evaluator. Stress test each R&D idea. Be specific. No flattery.
CRITICAL: Return ONLY valid JSON. No markdown.
Structure: {"summary":"","evaluations":[{"title":"","verdict":"BUILD NOW|DELAY|DROP","reality_check":"","motivation_collapse":"","hidden_complexity":"","value_analysis":"","scope_classification":"TOO BIG|TOO SMALL|MISCOPED|VALID","simplified_versions":{"two_to_five_hours":"","one_day":"","mvp":""},"execution_risks":[],"scores":{"execution_likelihood":1,"learning_value":1,"reusability":1,"clarity":1,"visible_progress":1,"scope_control":1,"setup_friction":1,"debugging_friction":1,"maintenance_friction":1},"final_score":0,"execution_plan":{"hour_1":"","first_file":"","done_means":"","do_not_add":"","stall_risk":""}}],"ranking":[{"rank":1,"title":"","verdict":"","main_risk":""}]}"""
    raw = call_claude(client, system, f"Target: {target}\n\nIdeas:\n{json.dumps(ideas, indent=2)}\n\nReturn JSON only.")
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned[cleaned.index("{"):cleaned.rindex("}") + 1])


def save_output(target: str, ideas: list[dict], selected: list[dict], results: dict) -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(" ", "_").replace("/", "-")[:30]
    filename = f"rd_output_{safe_target}_{ts}.md"

    lines = [
        f"# R&D Idea Engine — Output Report",
        f"**Target:** {target}",
        f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Generated by:** MainbyteLabs R&D Idea Engine (CLI)",
        "",
        "---",
        "",
        f"## Generated Ideas ({len(ideas)} total)",
        "",
    ]

    for i, idea in enumerate(ideas, 1):
        lines += [
            f"### [{i:02}] {idea['title']}",
            f"**Domain:** {idea.get('domain','')} | **Difficulty:** {idea.get('difficulty','')}/5 | **Scope Risk:** {idea.get('scope_risk','')}",
            "",
            idea.get("description", ""),
            "",
            f"- **Time Estimate:** {idea.get('estimated_time','')}",
            f"- **Visible Result:** {idea.get('visible_result','')}",
            f"- **Smallest Version:** {idea.get('smallest_version','')}",
            f"- **Why Interesting:** {idea.get('why_interesting','')}",
            "",
        ]

    lines += ["---", "", "## Stress Test Results", ""]

    if results.get("summary"):
        lines += [f"**Summary:** {results['summary']}", ""]

    for ev in results.get("evaluations", []):
        s = ev.get("scores", {})
        exec_total = sum(s.get(k, 0) for k in ["execution_likelihood","learning_value","reusability","clarity","visible_progress","scope_control"])
        friction_total = sum(s.get(k, 0) for k in ["setup_friction","debugging_friction","maintenance_friction"])
        lines += [
            f"### {ev['title']}",
            f"**Verdict:** {ev.get('verdict','')} | **Scope:** {ev.get('scope_classification','')} | **Final Score:** {ev.get('final_score','—')}",
            "",
            f"**Reality Check:** {ev.get('reality_check','')}",
            "",
            f"**Motivation Collapse Point:** {ev.get('motivation_collapse','')}",
            "",
            f"**Hidden Complexity:** {ev.get('hidden_complexity','')}",
            "",
            f"**Value Analysis:** {ev.get('value_analysis','')}",
            "",
        ]
        sv = ev.get("simplified_versions", {})
        if sv:
            lines += [
                "**Simplified Versions:**",
                f"- 2–5 hrs: {sv.get('two_to_five_hours','')}",
                f"- 1 day: {sv.get('one_day','')}",
                f"- MVP: {sv.get('mvp','')}",
                "",
            ]
        if ev.get("execution_risks"):
            lines += ["**Execution Risks:**"] + [f"- {r}" for r in ev["execution_risks"]] + [""]
        ep = ev.get("execution_plan", {})
        if ep:
            lines += [
                "**Execution Plan:**",
                f"- Hour 1: {ep.get('hour_1','')}",
                f"- First File: {ep.get('first_file','')}",
                f"- Done Means: {ep.get('done_means','')}",
                f"- Do NOT Add: {ep.get('do_not_add','')}",
                f"- Stall Risk: {ep.get('stall_risk','')}",
                "",
            ]
        lines.append("")

    lines += ["---", "", "## Final Rankings", ""]
    for r in results.get("ranking", []):
        lines.append(f"{r['rank']}. **{r['title']}** — {r['verdict']} — {r['main_risk']}")

    lines += ["", "---", "*MainbyteLabs R&D Idea Engine | github.com/MR-MainbyteLabs*"]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename


def display_results(results: dict):
    print()
    separator()
    print("  Stress Test Results")
    separator()
    if results.get("summary"):
        print(f"\n  {results['summary']}\n")
    for ev in results.get("evaluations", []):
        verdict_sym = {"BUILD NOW": "✓", "DELAY": "◆", "DROP": "✗"}.get(ev.get("verdict",""), "◆")
        print(f"\n  {verdict_sym} {ev['title']} — {ev.get('verdict','')} (Score: {ev.get('final_score','—')})")
        print(f"     Scope: {ev.get('scope_classification','')}")
        print(f"     Collapse: {ev.get('motivation_collapse','')[:100]}")
    print()
    separator()
    print("  Rankings")
    separator()
    for r in results.get("ranking", []):
        print(f"  {r['rank']}. {r['title']} — {r['verdict']} — {r['main_risk']}")


def main():
    header()
    check_api_key()
    client = anthropic.Anthropic()

    mode, target, paste_research = pick_input_mode()
    focus = pick_focus_areas()
    count = pick_idea_count()

    print()
    separator()
    print(f"  Target: {target}")
    print(f"  Mode: {'Research' if mode=='research' else 'Paste'}")
    print(f"  Focus: {', '.join(focus)}")
    print(f"  Ideas: {count}")
    separator()
    print()

    if mode == "research":
        research = research_target(client, target)
    else:
        research = paste_research

    ideas = generate_ideas(client, target, research, focus, count)
    selected_indices = display_ideas(ideas)
    selected_ideas = [ideas[i] for i in selected_indices if 0 <= i < len(ideas)]

    if not selected_ideas:
        print("  No ideas selected. Exiting.")
        sys.exit(0)

    results = stress_test(client, target, selected_ideas)
    display_results(results)

    filename = save_output(target, ideas, selected_ideas, results)
    print(f"\n  Output saved to: {filename}\n")
    separator("═")


if __name__ == "__main__":
    main()
