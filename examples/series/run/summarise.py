#!/usr/bin/env python3
"""Collect the measured numbers and put each next to the slide it replaces.

  python3 run/summarise.py                 # writes examples/series/results/SUMMARY.md
  python3 run/summarise.py --results DIR   # another results root
  python3 run/summarise.py --mapping       # print the slide mapping table (for the README)

For each talk it reads the newest results/<talk>/<timestamp>/summary.json
(written by the runners) and fills the MAPPING below. Rows without results
say so; rows marked "manual" need a recording or a screenshot, not a run.
"""
import argparse
import json
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent


def g(data, *path, default=None):
    for key in path:
        if isinstance(data, dict) and key in data:
            data = data[key]
        elif isinstance(data, list) and isinstance(key, int) and -len(data) <= key < len(data):
            data = data[key]
        else:
            return default
    return data


def tok(value):
    if not isinstance(value, (int, float)):
        return "n/a"
    return f"{value / 1000:.1f}k" if value >= 1000 else f"{int(value)}"


def usd(value, places=2):
    return f"${value:.{places}f}" if isinstance(value, (int, float)) else "n/a"


# ── formatters: summary.json of one talk -> the text for the slide ──────────

def t03_s22(s):
    parts = []
    for key in ("A", "B"):
        e = g(s, "setups", key) or {}
        if e:
            parts.append(f"{key} ({e.get('label')}): {usd(e.get('cost_usd'))} total, {e.get('accepted')}/{e.get('runs')} accepted, "
                         f"{usd(e.get('cost_per_accepted_usd'), 3)} per accepted, {e.get('mean_turns')} turns, "
                         f"~{e.get('mean_diff_lines')} diff lines")
    return "; ".join(parts) or None


def t04_s8(s):
    inline, sub = g(s, "survey", "inline"), g(s, "survey", "subagents")
    if not inline and not sub:
        return None
    out = []
    if inline:
        out.append(f"inline: {inline.get('file_reads')} reads, ~{tok(inline.get('tokens_into_lead_est'))} tool output stayed in the lead "
                   f"(lead context at end {tok(inline.get('lead_context_final'))})")
    if sub:
        out.append(f"delegated: ~{tok(sub.get('subagent_return_tokens_est'))} returned to the lead from "
                   f"{len(sub.get('subagents') or [])} subagents (lead context at end {tok(sub.get('lead_context_final'))})")
    return "; ".join(out)


def _biggest_agent(s):
    agents = g(s, "survey", "subagents", "subagents") or []
    agents = [a for a in agents if isinstance(a.get("total_tokens_final_request"), (int, float))]
    return max(agents, key=lambda a: a["total_tokens_final_request"]) if agents else None


def t04_s11(s):
    a = _biggest_agent(s)
    if not a:
        return None
    return (f"{a.get('total_tool_use_count')} tool uses, {tok(a.get('total_tokens_final_request'))} tokens in its window "
            f"(final request) -> ~{tok(a.get('returned_tokens_est'))} tokens back")


def t04_s17(s):
    agents = g(s, "survey", "subagents", "subagents") or []
    if not agents:
        return None
    lines = [f"{a.get('subagent_type') or 'Agent'}({a.get('description')}) Done ({a.get('total_tool_use_count')} tool uses · "
             f"{tok(a.get('total_tokens_final_request'))} tokens · {round((a.get('total_duration_ms') or 0) / 1000)}s)"
             for a in agents]
    total = sum(a.get("total_tokens_final_request") or 0 for a in agents)
    return " / ".join(lines) + f"; {tok(total)} tokens stayed out of the lead"


def t04_s12_14(s):
    inline, sub = g(s, "survey", "inline"), g(s, "survey", "subagents")
    if not (inline and sub):
        return None
    ratio = (sub.get("total_tokens") or 0) / (inline.get("total_tokens") or 1)
    return (f"wall-clock {inline.get('duration_s')}s inline vs {sub.get('duration_s')}s fanned out; "
            f"total tokens {tok(inline.get('total_tokens'))} vs {tok(sub.get('total_tokens'))} ({ratio:.1f}x); "
            f"cost {usd(inline.get('cost_usd'), 3)} vs {usd(sub.get('cost_usd'), 3)}")


def t04_s31(s):
    cache = g(s, "cache") or []
    if len(cache) < 2:
        return None
    c1, c2 = cache[0], cache[1]
    return (f"call 1: cache_creation {tok(g(c1, 'first_call', 'cache_creation_tokens'))}, cache_read {tok(g(c1, 'first_call', 'cache_read_tokens'))}; "
            f"call 2 (+{c2.get('started_after_s')}s): cache_creation {tok(g(c2, 'first_call', 'cache_creation_tokens'))}, "
            f"cache_read {tok(g(c2, 'first_call', 'cache_read_tokens'))}")


def t04_s32(s):
    cache = g(s, "cache") or []
    if not cache:
        return None
    return "; ".join(f"{c.get('label')}: {c.get('cache_hit_pct')}% of input from cache, {usd(c.get('cost_usd'), 4)}" for c in cache)


def t04_s34(s):
    agents = g(s, "survey", "subagents", "subagents") or []
    if not agents:
        return None
    return "first call per subagent: " + "; ".join(
        f"{a.get('description') or a.get('tool_use_id')}: write {tok(a.get('first_call_cache_creation'))} / read {tok(a.get('first_call_cache_read'))}"
        for a in agents)


def t05_s6(s):
    bill = g(s, "bill") or {}
    if not bill:
        return None
    shares = bill.get("shares_pct") or {}
    return (f"cached prefix {shares.get('cached prefix')}% · file reads x{bill.get('file_reads')} {shares.get('file reads')}% · "
            f"re-reads x{bill.get('re_reads')} {shares.get('re-reads')}% · other tool output {shares.get('other tool results')}% · "
            f"thinking + answer {shares.get('thinking + answer')}% ({bill.get('api_calls')} calls, weighted estimate)")


def t05_s17(s):
    overhead = g(s, "overhead") or {}
    if not overhead:
        return None
    return " · ".join(f"{name} {tok(value)}" for name, value in overhead.items())


def t05_s25(s):
    out = []
    for variant in ("bloated", "lean"):
        v = g(s, "variants", variant) or {}
        if v.get("runs"):
            out.append(f"{variant}: {v.get('turns')} turns, {tok(v.get('total_tokens'))} tokens, "
                       f"CLAUDE.md {tok(v.get('claude_md_tokens_per_turn'))}/turn, {v.get('outcome')}")
    return "; ".join(out) or None


def t06_s13(s):
    m = g(s, "merge")
    if not m or m.get("pair") != "overlap":  # PAIR=clean is the control; see its summary.md
        return None
    files = ", ".join(m.get("conflicted_files") or [])
    return (f"PAIR={m.get('pair')}: merge {m.get('first')} {m.get('first_merge')}, {m.get('second')} {m.get('second_merge')}"
            + (f" in {files}" if files else "") + f"; agents ran in parallel for {m.get('parallel_wall_s')}s")


def t06_s30(s):
    p = g(s, "mcp_vs_cli") or {}
    if not p:
        return None
    mcp, cli = p.get("mcp", {}), p.get("cli", {})
    return (f"before first call {tok(mcp.get('context_total_tokens'))} vs {tok(cli.get('context_total_tokens'))} "
            f"(MCP schemas {tok(mcp.get('mcp_tool_tokens'))}); whole task {tok(mcp.get('total_tokens'))} vs {tok(cli.get('total_tokens'))}; "
            f"{mcp.get('duration_s')}s vs {cli.get('duration_s')}s; right: {mcp.get('correct')} vs {cli.get('correct')} (MCP vs CLI)")


def t07_variants(s):
    variants = g(s, "variants") or {}
    if not variants:
        return None
    return "; ".join(f"{name}: {v.get('passes')}/{v.get('runs')} runs pass, pass@{v.get('k')} {v.get('pass_at_k_tasks')}/{v.get('tasks')} tasks, "
                     f"pass^{v.get('k')} {v.get('pass_hat_k_tasks')}/{v.get('tasks')}, {usd(v.get('cost_per_pass_usd'), 3)}/pass"
                     for name, v in variants.items())


def t07_s5(s):
    cells = g(s, "cells") or {}
    if not cells:
        return None
    variant = sorted({c["variant"] for c in cells.values()})[-1]
    rows = [c for c in cells.values() if c["variant"] == variant]
    passed = sum(1 for c in rows if c["passes"] == c["k"])
    return (f"{variant}: " + ", ".join(f"{c['task']} {'pass' if c['passes'] == c['k'] else f'{c['passes']}/{c['k']}'}" for c in sorted(rows, key=lambda c: c['task']))
            + f" -> {passed}/{len(rows)} pass every run")


def t07_s8(s):
    ex = g(s, "example_trace")
    if not ex:
        return None
    steps = ex.get("steps") or []
    return f"{ex.get('task')}: {len(steps)} lead turns; " + " | ".join(
        f"t{st['turn']} " + (", ".join(f"{t['tool']} {t['target'].split('/')[-1]}" for t in st["tools"]) or "answer") for st in steps[:6])


def t07_s9(s):
    w = g(s, "waste") or {}
    if not w:
        return None
    wasted = w.get("re-read", 0) + w.get("repeat", 0) + w.get("blind retry", 0)
    return (f"{wasted} of {w.get('turns', 0)} lead turns over {w.get('runs', 0)} runs repeated work "
            f"(re-reads {w.get('re-read', 0)}, repeats {w.get('repeat', 0)}, blind retries {w.get('blind retry', 0)})")


# ── the mapping ─────────────────────────────────────────────────────────────
# kind: auto (a runner fills it), partial (a runner gives the numbers, a human
# edits the visual), manual (needs a recording or data the kit cannot produce).

MAPPING = [
    dict(talk="03", deck="agentic-engineering-v2.html (source: scripts/build_first_three_v2.py)", slide=22,
         title="Measure the cost per accepted task", illustrative="A $6, 6/10 accepted, $1/accepted, 40 min review; B $10, 10/10, $1, 15 min",
         runner="talk03.sh", field="setups.{A,B}.{cost_usd,accepted,runs,cost_per_accepted_usd}", kind="partial", fmt=t03_s22,
         note="Review time is not measured; time your own review of each diff (diff.patch per run)."),
    dict(talk="03", deck="agentic-engineering-v2.html", slide=24, title="Problem 6 · one agent carries too much",
         illustrative="animation: 80k tokens in the worker, 200 back", runner="talk04.sh", field="survey.inline.lead_context_final, survey.subagents.subagent_return_tokens_est",
         kind="partial", fmt=t04_s8, source_talk="04", note="Numbers from the talk 04 survey; the Remotion animation needs re-rendering by hand."),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=7, title="A subagent works in its own window",
         illustrative="animation token counts", runner="talk04.sh", field="survey.subagents.subagents[*]", kind="partial", fmt=t04_s11,
         note="Animation: re-render in remotion/ with the measured counts, or say they are from our run."),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=8, title="Where fifteen file reads end up",
         illustrative="15 reads, 45,000 tokens stay in the lead vs 200 reach it", runner="talk04.sh",
         field="survey.inline.{file_reads,tokens_into_lead_est}, survey.subagents.subagent_return_tokens_est", kind="auto", fmt=t04_s8),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=11, title="Many turns collapse into one block",
         illustrative="30 turns, 41,700 tokens -> ~300 tokens", runner="talk04.sh",
         field="survey.subagents.subagents[max].{total_tool_use_count,total_tokens_final_request,returned_tokens_est}", kind="auto", fmt=t04_s11),
    dict(talk="04", deck="subagents-prompt-caching.html", slide="12, 14", title="Fan out to cut the waiting / 15x tokens",
         illustrative="diagram; 1x / 4x / 15x (Anthropic research system)", runner="talk04.sh",
         field="survey.{inline,subagents}.{duration_s,total_tokens,cost_usd}", kind="partial", fmt=t04_s12_14,
         note="The 15x is Anthropic's published figure; keep it and add ours as a local data point."),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=17, title="Watch subagents run in Claude Code",
         illustrative="Done (9 tool uses · 32.1k tokens · 48s) x3, 90k never reach the session", runner="talk04.sh",
         field="survey.subagents.subagents[*].{total_tool_use_count,total_tokens_final_request,total_duration_ms}", kind="auto", fmt=t04_s17),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=31, title="Read the usage fields to confirm a hit",
         illustrative="call 1 writes 48,210; call 2 reads 48,210", runner="talk04.sh",
         field="cache[0].first_call.cache_creation_tokens, cache[1].first_call.cache_read_tokens", kind="auto", fmt=t04_s31,
         note="Claude Code's prefix (system prompt, tools, CLAUDE.md), not the slide's big_document; say so."),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=32, title="Caching you only see on the usage screen",
         illustrative="docs example: $0.55, 91% of input from cache", runner="talk04.sh", field="cache[*].cache_hit_pct",
         kind="partial", fmt=t04_s32, note="For the /usage screen itself, screenshot it after the run (interactive only)."),
    dict(talk="04", deck="subagents-prompt-caching.html", slide=34, title="Subagents with the same prefix share a cache",
         illustrative="20k prefix: 80k without caching vs 31k with", runner="talk04.sh",
         field="survey.subagents.subagents[*].first_call_cache_{creation,read}", kind="partial", fmt=t04_s34,
         note="Shows whether Claude Code's parallel Explore subagents actually shared a prefix; the slide's arithmetic stays."),
    dict(talk="05", deck="cost-and-context.html", slide=6, title="Where one session's tokens go",
         illustrative="cached prefix 7 · file reads x12 42 · re-reads x4 20 · thinking + answer 31", runner="talk05.sh",
         field="bill.{shares_pct,file_reads,re_reads}", kind="auto", fmt=t05_s6,
         note="Totals are Claude Code's; the split per line is estimated from transcript sizes (see analyze.py)."),
    dict(talk="05", deck="cost-and-context.html", slide=17, title="The overhead you pay before you type",
         illustrative="system prompt 4,200 · memory 960 · MCP names 120 · skills 450 · CLAUDE.md 2,120 (docs)", runner="talk05.sh",
         field="overhead (from /context context_usage.categories)", kind="auto", fmt=t05_s17),
    dict(talk="05", deck="cost-and-context.html", slide=24, title="Same task, two CLAUDE.md files (live)",
         illustrative="turns / total tokens / outcome counters", runner="talk05.sh", field="variants.{bloated,lean}", kind="auto", fmt=t05_s25,
         note="Rehearsal baseline; the live run on stage produces its own numbers."),
    dict(talk="05", deck="cost-and-context.html", slide=25, title="Fallback: the rehearsal run",
         illustrative="8 cells 'fill in'", runner="talk05.sh",
         field="variants.{bloated,lean}.{turns,total_tokens,claude_md_tokens_per_turn,outcome}", kind="auto", fmt=t05_s25),
    dict(talk="06", deck="orchestrating-agents.html", slide=5, title="Herdr: every agent in one terminal",
         illustrative="pane list is a mock-up", runner="manual", field="-", kind="manual", fmt=None,
         note="Screenshot a real Herdr workspace; outside the kit."),
    dict(talk="06", deck="orchestrating-agents.html", slide=9, title="Fallback: the Symphony run",
         illustrative="'Screen recording goes here'", runner="record.sh 06-s9", field="-", kind="manual", fmt=None,
         note="Symphony drives Codex from Linear; record the terminal with record.sh and the board with Cmd+Shift+5."),
    dict(talk="06", deck="orchestrating-agents.html", slide=13, title="Failure mode 2: merge conflicts between agents",
         illustrative="diagram: auth.ts edited in two worktrees", runner="talk06.sh", field="merge.{first_merge,second_merge,conflicted_files}",
         kind="auto", fmt=t06_s13, note="Swap auth.ts for the real file (invoicing/export.py) and show merge-conflict.diff."),
    dict(talk="06", deck="orchestrating-agents.html", slide=14, title="Failure mode 3: review bottlenecks",
         illustrative="12 PRs opened a day, 4 reviewed -> 40 waiting by Friday", runner="manual", field="-", kind="manual", fmt=None,
         note="Needs your team's PR data (gh pr list --state all --json createdAt,mergedAt); not a single-run measurement."),
    dict(talk="06", deck="orchestrating-agents.html", slide=23, title="Fallback: the skill demo",
         illustrative="'Screen recording goes here'", runner="record.sh 06-s23", field="-", kind="manual", fmt=None,
         note="record.sh opens a fresh repo with demo-skill/backlog-issue/SKILL.md ready to paste."),
    dict(talk="06", deck="orchestrating-agents.html", slide=30, title="Measure one tool both ways",
         illustrative="8 cells 'your number'", runner="talk06.sh", field="mcp_vs_cli.{mcp,cli}.{context_total_tokens,total_tokens,duration_s,correct}",
         kind="auto", fmt=t06_s30),
    dict(talk="07", deck="measuring-what-works.html", slide=4, title="Why vibes don't scale",
         illustrative="A 6/10, B 9/10", runner="talk07.sh", field="variants.*.{passes,runs}", kind="partial", fmt=t07_variants,
         note="Optional: replace with our two variants' pass counts."),
    dict(talk="07", deck="measuring-what-works.html", slide=5, title="Start with a task-completion suite",
         illustrative="6 tasks from last month, 4/6 pass", runner="talk07.sh", field="cells[*].{task,passes,k}", kind="auto", fmt=t07_s5),
    dict(talk="07", deck="measuring-what-works.html", slide=8, title="A trace is the whole transcript",
         illustrative="t1-t6 auth.ts session", runner="talk07.sh", field="example_trace.steps", kind="auto", fmt=t07_s8),
    dict(talk="07", deck="measuring-what-works.html", slide=9, title="Read traces for wasted turns",
         illustrative="3 of 6 turns repeat earlier work", runner="talk07.sh", field="waste.{re-read,repeat,blind retry,turns}", kind="auto", fmt=t07_s9),
    dict(talk="07", deck="measuring-what-works.html", slide=11, title="Anatomy of an agent trace",
         illustrative="Elastic example: 8,214 input, 1,102 output, 412 ms / 96 ms tools", runner="manual", field="-", kind="manual", fmt=None,
         note="OTel spans need CLAUDE_CODE_ENABLE_TELEMETRY=1 + CLAUDE_CODE_ENHANCED_TELEMETRY_BETA and a collector; per-call tokens are in any transcript (analyze.py trace)."),
    dict(talk="07", deck="measuring-what-works.html", slide="17-18", title="Live: score two variants / Fallback: the recorded eval run",
         illustrative="task 1-4 x variant A/B '…'", runner="talk07.sh + record.sh 07-s18", field="cells, variants", kind="auto", fmt=t07_variants,
         note="The per-task sheet is in results/talk07/<ts>/summary.md; the screenshot slot needs record.sh 07-s18."),
    dict(talk="07", deck="measuring-what-works.html", slide=20, title="No model wins on cost, intelligence and taste",
         illustrative="A/B/C placement", runner="talk07.sh VARIANT=models", field="variants.*.{pass_rate,cost_per_pass_usd}", kind="partial", fmt=t07_variants,
         note="Two models on our six tasks give cost and pass-rate positions; taste is not measured."),
    dict(talk="07", deck="measuring-what-works.html", slide=28, title="Fallback: the recorded local run",
         illustrative="recording slot", runner="record.sh 07-s28", field="-", kind="manual", fmt=None,
         note="Ollama and the model weights are outside the kit."),
    dict(talk="07", deck="measuring-what-works.html", slide=33, title="Fallback: the recorded dictation",
         illustrative="recording slot", runner="record.sh 07-s33", field="-", kind="manual", fmt=None,
         note="Terminal capture shows text only; use a screen recording with audio."),
    dict(talk="08", deck="claude-design.html", slide=18, title="Fallback: the same run, frame by frame",
         illustrative="five drawn stand-in frames", runner="manual", field="-", kind="manual", fmt=None,
         note="Claude Design is a web app: screen-record or screenshot the five steps (Cmd+Shift+5)."),
]


def talk_runs(results: Path, talk: str):
    """(summary, run_dir) for every run of a talk, newest first."""
    runs = sorted((p for p in (results / f"talk{talk}").glob("*") if (p / "summary.json").is_file()),
                  key=lambda p: p.name, reverse=True)
    out = []
    for run in runs:
        try:
            out.append((json.loads((run / "summary.json").read_text()), run))
        except ValueError:
            continue
    return out


def first_value(fmt, runs):
    """The newest run that has data for this row (runs with --only leave gaps)."""
    for summary, run_dir in runs:
        try:
            value = fmt(summary)
        except Exception as exc:  # a malformed summary should not hide the other rows
            value = f"error reading {run_dir.name}: {exc}"
        if value is not None:
            return value, run_dir
    return None, None


def mapping_table():
    lines = ["| Talk | Slide | Title | Illustrative now | Runner | Field(s) | Kind |", "|---|---|---|---|---|---|---|"]
    for m in MAPPING:
        lines.append(f"| {m['talk']} | {m['slide']} | {m['title']} | {m['illustrative']} | `{m['runner']}` | `{m['field']}` | {m['kind']} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results", type=Path, default=SERIES / "results")
    parser.add_argument("--mapping", action="store_true", help="print the mapping table and exit")
    args = parser.parse_args(argv)
    if args.mapping:
        print(mapping_table())
        return 0
    runs = {talk: talk_runs(args.results, talk) for talk in ("03", "04", "05", "06", "07")}
    lines = ["# Measured numbers for the slides", "",
             "Generated by `run/summarise.py` from the newest run of each talk. "
             "Illustrative values are what the deck shows today.", "",
             "| Talk | Slide | Title | Illustrative now | Measured | Source |", "|---|---|---|---|---|---|"]
    filled = 0
    for m in MAPPING:
        talk_history = runs.get(m.get("source_talk", m["talk"])) or []
        if m["kind"] == "manual":
            value, source = f"manual: {m.get('note', '')}", m["runner"]
        elif not talk_history:
            value, source = f"not run yet: `run/{m['runner'].split()[0]}`", "-"
        else:
            value, run_dir = first_value(m["fmt"], talk_history)
            source = str(run_dir.relative_to(args.results)) if run_dir else "-"
            if value is None:
                value = "no data in any run yet"
            else:
                filled += 1
                if m.get("note"):
                    value += f" ({m['note']})"
        lines.append(f"| {m['talk']} | {m['slide']} | {m['title']} | {m['illustrative']} | {value.replace('|', '/')} | {source} |")
    lines += ["", f"{filled} of {sum(1 for m in MAPPING if m['kind'] != 'manual')} measurable rows filled."]
    out = args.results / "SUMMARY.md"
    args.results.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({filled} rows filled)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
