#!/usr/bin/env python3
"""Lab kit helpers: transcripts, results export, and the per-lab summaries.

Standard library only. The lab scripts call it; you rarely need it directly.

  labkit.py pair                          the pair id used on the board
  labkit.py session TRANSCRIPT            session metrics (JSON) from a stream-json transcript
  labkit.py result-text TRANSCRIPT        the final answer; exit 3 when there is no result event
  labkit.py task-prompt TASK.yaml         the prompt block of an smevals task file
  labkit.py collect LAB RESULTS_DIR       write RESULTS_DIR/export.json from runs/**
  labkit.py summary LAB RESULTS_DIR       print and save summary.md for lab1 | lab2 | lab6
  labkit.py export [--lab L] [--latest] [--sample] [--root DIR]
                                          one compact JSON line per run (the board format)
  labkit.py validate [FILE|-]             check JSON lines against RESULTS-SCHEMA.md
  labkit.py predict lean|bloated          record the pair's lab 1 prediction
  labkit.py reuse --lab6-tasks T... --model M
                                          earlier lean runs of M (labs 1-2) that lab 6 can reuse
  labkit.py sample-summary LAB            lab 2 or lab 6 summary over sample-results/

Where the numbers come from: the stream-json `result` event (total_cost_usd,
num_turns, duration_ms, usage, modelUsage). Token counts in the export are the
modelUsage totals (every model call, subagents included). Dollar figures are
Claude Code's client-side estimates at API list prices; on a Pro or Max plan the
runs use plan usage instead.
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import socket
import statistics
import sys
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent
RESULTS_ROOT = Path(os.environ.get("RESULTS_ROOT") or LAB_DIR / "results")
SAMPLE_DIR = Path(os.environ.get("SAMPLE_DIR") or LAB_DIR / "sample-results")
SCHEMA_VERSION = 1
RUN_LABS = ("lab1", "lab2", "lab5", "lab6")
RUN_KEYS = ("v", "pair", "lab", "variant", "task", "run", "passed", "turns", "input_tokens",
            "output_tokens", "cache_read_tokens", "cache_write_tokens", "cost_usd", "duration_s", "model")
PREDICTION_KEYS = ("v", "pair", "lab", "kind", "variant")
JUDGE_KEYS = ("v", "pair", "lab", "kind", "sample", "human", "judge", "author")


# ── pair id ────────────────────────────────────────────────────────────────

def pair_id():
    value = os.environ.get("PAIR", "").strip()
    if not value:
        pair_file = LAB_DIR / ".pair"
        if pair_file.is_file():
            value = pair_file.read_text(encoding="utf-8").strip()
    if not value:
        value = "h-" + hashlib.sha256(socket.gethostname().encode()).hexdigest()[:8]
    return re.sub(r"[^A-Za-z0-9_.-]", "-", value)[:40]


# ── transcripts ────────────────────────────────────────────────────────────

def load_events(path):
    path = Path(path)
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.strip()
    if stripped.startswith("{") and "\n" not in stripped:
        try:
            return [json.loads(stripped)]
        except ValueError:
            pass
    events = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
    return events


def load_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def result_event(events):
    for event in reversed(events):
        if event.get("type") == "result":
            return event
    return {}


def usage_totals(result):
    """Token totals over every model (modelUsage), falling back to the main-loop usage."""
    totals = Counter()
    for usage in (result.get("modelUsage") or {}).values():
        totals["input_tokens"] += int(usage.get("inputTokens") or 0)
        totals["output_tokens"] += int(usage.get("outputTokens") or 0)
        totals["cache_read_tokens"] += int(usage.get("cacheReadInputTokens") or 0)
        totals["cache_write_tokens"] += int(usage.get("cacheCreationInputTokens") or 0)
    if not totals and result.get("usage"):
        usage = result["usage"]
        totals["input_tokens"] = int(usage.get("input_tokens") or 0)
        totals["output_tokens"] = int(usage.get("output_tokens") or 0)
        totals["cache_read_tokens"] = int(usage.get("cache_read_input_tokens") or 0)
        totals["cache_write_tokens"] = int(usage.get("cache_creation_input_tokens") or 0)
    return {key: totals.get(key, 0) for key in
            ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens")}


def session_metrics(transcript):
    events = load_events(transcript)
    result = result_event(events)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    models = list((result.get("modelUsage") or {}).keys())
    tokens = usage_totals(result)
    tools = Counter()
    for event in events:
        if event.get("type") == "assistant" and not event.get("parent_tool_use_id"):
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tools[block.get("name")] += 1
    return {
        "transcript": str(transcript),
        "has_result": bool(result),
        "ok": bool(result) and not result.get("is_error", False),
        "subtype": result.get("subtype"),
        "terminal_reason": result.get("terminal_reason"),
        "num_turns": result.get("num_turns"),
        "duration_s": round((result.get("duration_ms") or 0) / 1000, 1),
        "cost_usd": result.get("total_cost_usd"),
        "model": init.get("model") or (models[0] if models else None),
        **tokens,
        # checker-compatible aliases
        "cache_creation_tokens": tokens["cache_write_tokens"],
        "total_tokens": sum(tokens.values()),
        "tools": dict(tools),
        "permission_denials": len(result.get("permission_denials") or []),
    }


def result_text(transcript):
    result = result_event(load_events(transcript))
    if not result:
        print("no result event: Claude Code did not finish (harness error)", file=sys.stderr)
        return 3
    print(result.get("result") or f"[{result.get('subtype')}]")
    return 0


def task_prompt(path):
    """The `prompt: |` block of a task YAML (no PyYAML needed for this layout)."""
    text = Path(path).read_text(encoding="utf-8")
    match = re.search(r"^prompt: \|\n((?:  .*\n?|\n)+)", text, re.M)
    if not match:
        raise SystemExit(f"no prompt block in {path}")
    return "\n".join(line[2:] for line in match.group(1).rstrip("\n").splitlines())


# ── schema ─────────────────────────────────────────────────────────────────

def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate(obj):
    """Return a list of problems with one export object ([] means valid)."""
    problems = []
    if not isinstance(obj, dict):
        return ["not a JSON object"]
    if obj.get("v") != SCHEMA_VERSION:
        problems.append("v must be 1")
    if not isinstance(obj.get("pair"), str) or not obj.get("pair"):
        problems.append("pair must be a non-empty string")
    kind = obj.get("kind")
    if kind == "prediction":
        expected = PREDICTION_KEYS
        if obj.get("lab") != "lab1":
            problems.append("prediction lab must be lab1")
        if obj.get("variant") not in ("lean", "bloated"):
            problems.append("prediction variant must be lean or bloated")
    elif kind == "judge":
        expected = JUDGE_KEYS
        if obj.get("lab") != "lab5":
            problems.append("judge lab must be lab5")
        if not isinstance(obj.get("sample"), str):
            problems.append("sample must be a string")
        for key in ("human", "judge"):
            if not (_is_int(obj.get(key)) and 1 <= obj[key] <= 5):
                problems.append(f"{key} must be an integer 1-5")
        if obj.get("author") not in ("human", "model"):
            problems.append("author must be human or model")
    elif kind is None:
        expected = RUN_KEYS
        if obj.get("lab") not in RUN_LABS:
            problems.append("lab must be one of " + "|".join(RUN_LABS))
        for key in ("variant", "task", "model"):
            if not isinstance(obj.get(key), str) or not obj.get(key):
                problems.append(f"{key} must be a non-empty string")
        if not _is_int(obj.get("run")) or obj.get("run", 0) < 1:
            problems.append("run must be an integer >= 1")
        if obj.get("passed") not in (True, False, None):
            problems.append("passed must be true, false or null")
        for key in ("turns", "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens"):
            if not _is_int(obj.get(key)) or obj[key] < 0:
                problems.append(f"{key} must be a non-negative integer")
        for key in ("cost_usd", "duration_s"):
            if not _is_num(obj.get(key)) or obj[key] < 0:
                problems.append(f"{key} must be a non-negative number")
    else:
        return [f"unknown kind {kind!r}"]
    extra = set(obj) - set(expected)
    missing = set(expected) - set(obj)
    if extra:
        problems.append("unexpected keys: " + ", ".join(sorted(extra)))
    if missing:
        problems.append("missing keys: " + ", ".join(sorted(missing)))
    return problems


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# ── collecting runs into export.json ───────────────────────────────────────

def run_record(run_dir, pair):
    run_dir = Path(run_dir)
    labrun = load_json(run_dir / "labrun.json", {}) or {}
    metrics = load_json(run_dir / "metrics.json", {}) or {}
    check = load_json(run_dir / "check.json")
    if check is None:
        check = load_json(run_dir / "grades" / "default" / "checker.json")
    passed = None
    if metrics.get("has_result") and isinstance(check, dict) and "score" in check:
        passed = check.get("score") == 1.0
    record = {
        "v": SCHEMA_VERSION, "pair": pair,
        "lab": labrun.get("lab", "lab1"),
        "variant": labrun.get("variant") or "unknown",
        "task": labrun.get("task") or run_dir.parts[-4],
        "run": int(labrun.get("run") or 1),
        "passed": passed,
        "turns": int(metrics.get("num_turns") or 0),
        "input_tokens": int(metrics.get("input_tokens") or 0),
        "output_tokens": int(metrics.get("output_tokens") or 0),
        "cache_read_tokens": int(metrics.get("cache_read_tokens") or 0),
        "cache_write_tokens": int(metrics.get("cache_write_tokens") or 0),
        "cost_usd": round(float(metrics.get("cost_usd") or 0.0), 6),
        "duration_s": float(metrics.get("duration_s") or 0.0),
        "model": metrics.get("model") or labrun.get("model_requested") or "unknown",
    }
    if record["variant"] == "local":
        record["cost_usd"] = 0.0  # Claude Code prices local tokens at Anthropic rates: meaningless
    return record


def collect(lab, results_dir):
    results_dir = Path(results_dir)
    pair = pair_id()
    records = [run_record(p.parent, pair) for p in sorted(results_dir.glob("runs/**/labrun.json"))]
    records.sort(key=lambda r: (r["variant"], r["task"], r["run"]))
    extra = load_json(results_dir / "reused.json", []) or []
    records += extra
    for record in records:
        problems = validate(record)
        if problems:
            print(f"warning: export record does not validate: {problems}", file=sys.stderr)
    (results_dir / "export.json").write_text(
        "[\n" + ",\n".join(compact(r) for r in records) + "\n]\n", encoding="utf-8")
    return records


def export_files(root, lab=None, latest=False):
    root = Path(root)
    files = []
    labs = [lab] if lab else sorted(p.name for p in root.glob("lab*") if p.is_dir())
    for name in labs:
        runs = sorted((root / name).glob("*/export.json"))
        files += runs[-1:] if latest else runs
    if lab in (None, "lab1") and (root / "predictions").is_dir():
        preds = sorted((root / "predictions").glob("*.json"))
        files += preds[-1:] if latest else preds
    return files


def read_export(path):
    data = load_json(path)
    if data is None:
        return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()
                if line.strip().startswith("{")]
    return data if isinstance(data, list) else [data]


def sample_lines():
    path = SAMPLE_DIR / "export.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("{")] if path.is_file() else []


def cmd_export(args):
    if args.sample:
        objs = sample_lines()
    else:
        objs = []
        for path in export_files(args.root, args.lab, args.latest):
            objs += read_export(path)
    if args.lab:
        objs = [o for o in objs if o.get("lab") == args.lab]
    bad = 0
    for obj in objs:
        problems = validate(obj)
        if problems:
            bad += 1
            print(f"invalid: {problems}: {compact(obj)}", file=sys.stderr)
            continue
        print(compact(obj))
    if not objs:
        print("no results yet (run a lab, or use --sample)", file=sys.stderr)
    return 1 if bad else 0


def cmd_validate(path):
    stream = sys.stdin if path in (None, "-") else open(path, encoding="utf-8")
    count = bad = 0
    for number, line in enumerate(stream, 1):
        line = line.strip()
        if not line:
            continue
        count += 1
        try:
            obj = json.loads(line)
        except ValueError as exc:
            bad += 1
            print(f"line {number}: not JSON ({exc})")
            continue
        problems = validate(obj)
        if problems:
            bad += 1
            print(f"line {number}: {'; '.join(problems)}")
    print(f"{count - bad}/{count} lines valid")
    return 1 if bad or not count else 0


def cmd_predict(variant):
    if variant not in ("lean", "bloated"):
        raise SystemExit("usage: predict.sh lean|bloated  (which CLAUDE.md will be cheaper per passing run?)")
    obj = {"v": SCHEMA_VERSION, "pair": pair_id(), "lab": "lab1", "kind": "prediction", "variant": variant}
    folder = RESULTS_ROOT / "predictions"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".json")
    path.write_text(compact(obj) + "\n", encoding="utf-8")
    print(f"Prediction recorded: {variant} (pair {obj['pair']}) -> {path}")
    print(compact(obj))
    return 0


def latest_prediction():
    folder = RESULTS_ROOT / "predictions"
    files = sorted(folder.glob("*.json")) if folder.is_dir() else []
    return (load_json(files[-1]) or {}).get("variant") if files else None


# ── statistics ─────────────────────────────────────────────────────────────

def wilson(passes, n, z=1.96):
    if not n:
        return (None, None)
    p = passes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(max(0.0, centre - half), 2), round(min(1.0, centre + half), 2))


def fmt_tokens(value):
    if not isinstance(value, (int, float)):
        return "n/a"
    return f"{value / 1e6:.2f}M" if value >= 1e6 else f"{value / 1000:.0f}k" if value >= 1000 else str(int(value))


def fmt_usd(value, places=3):
    return f"${value:.{places}f}" if isinstance(value, (int, float)) else "n/a"


def md_table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def total_tokens(r):
    return r["input_tokens"] + r["output_tokens"] + r["cache_read_tokens"] + r["cache_write_tokens"]


def group(records, *keys):
    out = OrderedDict()
    for r in records:
        out.setdefault(tuple(r[k] for k in keys), []).append(r)
    return out


def mean(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return statistics.mean(values) if values else None


# ── per-lab summaries ──────────────────────────────────────────────────────

def summary_lab1(records):
    runs = [r for r in records if r.get("kind") is None]
    rows = []
    per_variant = {}
    for (variant,), items in group(sorted(runs, key=lambda r: r["variant"]), "variant").items():
        graded = [r for r in items if r["passed"] is not None]
        passes = sum(1 for r in graded if r["passed"])
        cost = sum(r["cost_usd"] for r in items)
        per_variant[variant] = {"cost": cost, "passes": passes, "runs": len(items),
                                "tokens": mean(total_tokens(r) for r in items)}
        rows.append([variant, f"{passes}/{len(graded)}", f"{mean(r['turns'] for r in items):.1f}",
                     fmt_tokens(mean(total_tokens(r) for r in items)),
                     fmt_tokens(mean(r['cache_read_tokens'] for r in items)),
                     fmt_usd(mean(r["cost_usd"] for r in items)),
                     fmt_usd(cost / passes) if passes else "n/a",
                     f"{mean(r['duration_s'] for r in items):.0f}s"])
    cells = [[r["task"], r["variant"], {True: "pass", False: "FAIL", None: "no result"}[r["passed"]],
              r["turns"], fmt_tokens(total_tokens(r)), fmt_usd(r["cost_usd"])]
             for r in sorted(runs, key=lambda r: (r["task"], r["variant"]))]
    md = ["# Lab 1 · guess, then measure: lean vs bloated CLAUDE.md", "",
          md_table(["Variant", "Passed", "Turns (mean)", "Tokens (mean)", "of which cache reads",
                    "Cost/run (mean)", "Cost per pass", "Time (mean)"], rows), "",
          md_table(["Task", "Variant", "Outcome", "Turns", "Tokens", "Cost"], cells), ""]
    prediction = latest_prediction()
    if prediction and len(per_variant) == 2 and all(v["passes"] for v in per_variant.values()):
        cheaper = min(per_variant, key=lambda v: per_variant[v]["cost"] / per_variant[v]["passes"])
        verdict = "right" if cheaper == prediction else "wrong"
        md.append(f"Your prediction: **{prediction}** would be cheaper per passing run. "
                  f"Measured: **{cheaper}** was. You were {verdict}, on one run per cell, "
                  "which is exactly why lab 2 exists.")
    elif prediction:
        md.append(f"Your prediction: **{prediction}**. Not enough passing runs in both variants to call it.")
    else:
        md.append("No prediction recorded. Next time: ./predict.sh lean|bloated before ./lab1.sh.")
    md += ["", "One run per cell is an anecdote. Compare with the room on the board before you conclude anything."]
    return "\n".join(md)


def passk_rows(runs):
    rows = []
    for (variant, task), items in group(sorted(runs, key=lambda r: (r["variant"], r["task"])), "variant", "task").items():
        graded = [r for r in items if r["passed"] is not None]
        k = len(graded)
        passes = sum(1 for r in graded if r["passed"])
        p = passes / k if k else None
        lo, hi = wilson(passes, k)
        rows.append({
            "variant": variant, "task": task, "k": k, "passes": passes,
            "pass_at_k": passes > 0 if k else None, "pass_hat_k": passes == k if k else None,
            "p": p, "ci": (lo, hi),
            "est_pass_at_k": 1 - (1 - p) ** k if k else None, "est_pass_hat_k": p ** k if k else None,
            "cost_per_pass": sum(r["cost_usd"] for r in items) / passes if passes else None,
            "turns": [r["turns"] for r in items], "cost": [r["cost_usd"] for r in items],
        })
    return rows


def summary_lab2(records, title="Lab 2 · variance: pass@k and pass^k"):
    runs = [r for r in records if r.get("kind") is None]
    pairs = sorted({r["pair"] for r in runs})
    if len(pairs) > 1:
        return pooled_lab2(runs, pairs, title)
    rows = passk_rows(runs)
    table = [[r["variant"], r["task"], f"{r['passes']}/{r['k']}",
              "yes" if r["pass_at_k"] else "no", "yes" if r["pass_hat_k"] else "no",
              f"{r['ci'][0]}-{r['ci'][1]}" if r["k"] else "n/a",
              " ".join(str(t) for t in r["turns"]), " ".join(f"{c:.2f}" for c in r["cost"]),
              fmt_usd(r["cost_per_pass"])] for r in rows]
    md = [f"# {title}", "",
          md_table(["Variant", "Task", "Passes/k", "pass@k", "pass^k", "95% CI of pass rate (Wilson)",
                    "Turns per run", "Cost per run ($)", "Cost per pass"], table), "",
          "pass@k: at least one of k runs passed (could a retry loop get there?).",
          "pass^k: all k runs passed (can you rely on it unattended?).",
          "With k = 3 the interval on the pass rate is wide: 3/3 is consistent with a true rate as low as ~0.44.",
          "The board pools every pair's runs; that is where the interval gets narrow enough to mean something."]
    spread = [r for r in rows if len(set(r["turns"])) > 1]
    if spread:
        md += ["", "Same task, same setup, different paths: turns ranged "
               + "; ".join(f"{r['variant']} {min(r['turns'])}-{max(r['turns'])}" for r in spread) + "."]
    return "\n".join(md)


def pooled_lab2(runs, pairs, title):
    """The room view: every pair ran k times; pool the runs and count pairs."""
    table = []
    for (variant, task), items in group(sorted(runs, key=lambda r: (r["variant"], r["task"])), "variant", "task").items():
        graded = [r for r in items if r["passed"] is not None]
        passes = sum(1 for r in graded if r["passed"])
        p = passes / len(graded) if graded else 0.0
        lo, hi = wilson(passes, len(graded))
        per_pair = [[r["passed"] for r in graded if r["pair"] == pair] for pair in pairs]
        per_pair = [x for x in per_pair if x]
        k = round(statistics.mean(len(x) for x in per_pair)) if per_pair else 0
        at_k = sum(any(x) for x in per_pair)
        hat_k = sum(all(x) for x in per_pair)
        turns = [r["turns"] for r in items]
        table.append([variant, task, len(per_pair), k, f"{passes}/{len(graded)} = {p:.2f}", f"{lo}-{hi}",
                      f"{at_k}/{len(per_pair)}", f"{hat_k}/{len(per_pair)}",
                      f"{1 - (1 - p) ** k:.2f} / {p ** k:.2f}", f"{min(turns)}-{max(turns)}",
                      fmt_usd(sum(r["cost_usd"] for r in items) / passes) if passes else "n/a"])
    return "\n".join([f"# {title}", "",
                      md_table(["Variant", "Task", "Pairs", "k", "Pooled pass rate", "95% CI (Wilson)",
                                "Pairs with pass@k", "Pairs with pass^k", "Expected pass@k / pass^k from pooled rate",
                                "Turns (range)", "Cost per pass"], table), "",
                      "Pooled: every pair's runs together. The interval narrows with the room's sample size;",
                      "pass^k falls fast as k grows (0.7^3 = 0.34): an agent that usually works still fails",
                      "unattended batches often. Compare lean vs bloated only if the intervals separate."])


def summary_lab6(records):
    runs = [r for r in records if r.get("kind") is None]
    by_model = group(sorted(runs, key=lambda r: r["variant"]), "variant")
    rows = []
    for (variant,), items in by_model.items():
        graded = [r for r in items if r["passed"] is not None]
        passes = sum(1 for r in graded if r["passed"])
        cost = sum(r["cost_usd"] for r in items)
        lo, hi = wilson(passes, len(graded))
        rows.append([variant, ", ".join(sorted({r["model"] for r in items})), f"{passes}/{len(graded)}",
                     f"{lo}-{hi}" if graded else "n/a", fmt_usd(cost / len(items)) if items else "n/a",
                     fmt_usd(cost / passes) if passes else "n/a (no passes)",
                     f"{mean(r['turns'] for r in items):.1f}", f"{mean(r['duration_s'] for r in items):.0f}s"])
    per_task = []
    for (task,), items in group(sorted(runs, key=lambda r: r["task"]), "task").items():
        cells = []
        for (variant,), sub in group(sorted(items, key=lambda r: r["variant"]), "variant").items():
            passes = sum(1 for r in sub if r["passed"])
            cells.append(f"{variant} {passes}/{len(sub)}")
        per_task.append([task, " · ".join(cells)])
    md = ["# Lab 6 · route by the numbers: cost per accepted task", "",
          md_table(["Model", "Model id", "Accepted", "95% CI (Wilson)", "Cost per run", "Cost per ACCEPTED task",
                    "Turns (mean)", "Time (mean)"], rows), "",
          md_table(["Task", "Accepted per model"], per_task), "",
          "Cost per accepted task = total spend of that model / runs that passed the hidden tests.",
          "A cheap model that fails costs you the run AND a retry (or a review). A local model's dollar",
          "figure is not measured (exported as 0.0): Claude Code prices tokens at Anthropic rates."]
    if any(r.get("variant") == "sonnet" and r.get("_reused") for r in runs):
        md.append("Some sonnet runs were reused from your labs 1-2 (same task, lean CLAUDE.md).")
    return "\n".join(md)


SUMMARIES = {"lab1": summary_lab1, "lab2": summary_lab2, "lab6": summary_lab6}


def cmd_summary(lab, results_dir):
    results_dir = Path(results_dir)
    records = read_export(results_dir / "export.json") if (results_dir / "export.json").is_file() else []
    if lab == "lab6":
        reused_ids = {compact(r) for r in load_json(results_dir / "reused.json", []) or []}
        for r in records:
            r["_reused"] = compact({k: v for k, v in r.items() if k != "_reused"}) in reused_ids
    text = SUMMARIES[lab](records)
    (results_dir / "summary.md").write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def cmd_sample_summary(lab):
    lines = [o for o in sample_lines() if o.get("lab") == lab and o.get("kind") is None]
    print("SYNTHETIC sample data (sample-results/), not measurements. Shape only.\n")
    if lab == "lab2":
        for (pair,), items in list(group(sorted(lines, key=lambda r: r["pair"]), "pair").items())[:3]:
            print(summary_lab2(items, title=f"Lab 2 · pair {pair} (synthetic)"))
            print()
        print(summary_lab2(lines, title="Lab 2 · all synthetic pairs pooled"))
    elif lab == "lab6":
        print(summary_lab6(lines))
    elif lab == "lab1":
        print(summary_lab1(lines))
    return 0


# ── lab 6 reuse of earlier sonnet runs ─────────────────────────────────────

def cmd_reuse(tasks, model_substr, want):
    """Print JSON: earlier lean runs of a model from labs 1-2 on these tasks, at most `want` per task."""
    pool = defaultdict(list)
    for lab in ("lab1", "lab2"):
        for path in export_files(RESULTS_ROOT, lab):
            for r in read_export(path):
                if (r.get("kind") is None and r.get("variant") == "lean" and r.get("task") in tasks
                        and model_substr in (r.get("model") or "") and r.get("passed") is not None):
                    pool[r["task"]].append(r)
    out = {}
    for task in tasks:
        chosen = pool.get(task, [])[-want:]
        out[task] = [{**r, "lab": "lab6", "variant": "sonnet", "run": i + 1} for i, r in enumerate(chosen)]
    print(json.dumps(out))
    return 0


# ── CLI ────────────────────────────────────────────────────────────────────

def main(argv):
    parser = argparse.ArgumentParser(description="lab kit helpers")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("pair")
    for name in ("session", "result-text", "task-prompt"):
        sub.add_parser(name).add_argument("path")
    for name in ("collect", "summary"):
        p = sub.add_parser(name)
        p.add_argument("lab")
        p.add_argument("results_dir")
    p = sub.add_parser("export")
    p.add_argument("--lab")
    p.add_argument("--latest", action="store_true")
    p.add_argument("--sample", action="store_true")
    p.add_argument("--root", default=str(RESULTS_ROOT))
    sub.add_parser("validate").add_argument("path", nargs="?")
    sub.add_parser("predict").add_argument("variant", nargs="?", default="")
    p = sub.add_parser("reuse")
    p.add_argument("--tasks", nargs="+", required=True)
    p.add_argument("--model", default="sonnet")
    p.add_argument("--want", type=int, default=2)
    sub.add_parser("sample-summary").add_argument("lab")
    args = parser.parse_args(argv[1:])

    if args.command == "pair":
        print(pair_id())
    elif args.command == "session":
        print(json.dumps(session_metrics(args.path), indent=2, ensure_ascii=False))
    elif args.command == "result-text":
        return result_text(args.path)
    elif args.command == "task-prompt":
        print(task_prompt(args.path))
    elif args.command == "collect":
        records = collect(args.lab, args.results_dir)
        print(f"export.json: {len(records)} runs")
    elif args.command == "summary":
        return cmd_summary(args.lab, args.results_dir)
    elif args.command == "export":
        return cmd_export(args)
    elif args.command == "validate":
        return cmd_validate(args.path)
    elif args.command == "predict":
        return cmd_predict(args.variant)
    elif args.command == "reuse":
        return cmd_reuse(args.tasks, args.model, args.want)
    elif args.command == "sample-summary":
        return cmd_sample_summary(args.lab)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
