#!/usr/bin/env python3
"""trace-report: read Claude Code stream-json transcripts for wasted work.

    traces.py [--md OUT.md] [--json OUT.json] TRANSCRIPT.jsonl...

For each transcript it prints the lead agent's turns and flags four kinds of
waste, each with the tokens it put into the context and an estimated cost:

  re-read      Read of a file already read, with no Edit/Write to it in between
  repeat       the same tool call with the same input, with no edit in between,
               after the first one succeeded
  blind retry  the same call again right after it failed, with no edit in
               between (nothing changed, so why would it pass now?)
  restated plan  assistant text that mostly repeats an earlier plan or summary
               (>= 25 words, >= 60% word overlap with an earlier message)

Attribution (an estimate, not a meter reading): tool output and text enter the
context once (cache write, 1.25x the input price) and are re-read from the cache
on every later API call (0.1x). Text the model writes also costs the output
price. When an API call did nothing but the flagged work, that call's own cost
(its whole cached context read again, plus its output) is added too, since
without the waste the call would not have happened. Tool output is sized at ~4 characters per token. Prices per million
tokens (input/output): Haiku 4.5 $1/$5, Sonnet 5 $2/$10, Opus 5.5 $4/$20.
The session total comes from Claude Code's own `total_cost_usd`.

Ported from examples/series/run/lib/analyze.py (talk 07 kit). One change: a
repeated identical call is only waste when nothing was edited in between, so
re-running the tests after a fix is not flagged.
"""
import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from labkit import load_events, load_json, result_event  # noqa: E402

CHARS_PER_TOKEN = 4
W_WRITE, W_READ = 1.25, 0.1
PRICES = {"haiku": (1.0, 5.0), "sonnet": (2.0, 10.0), "opus": (4.0, 20.0)}
EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
FLAGS = ("re-read", "repeat", "blind retry", "restated plan")


def est_tokens(text):
    return round(len(text or "") / CHARS_PER_TOKEN)


def prices(model):
    for key, value in PRICES.items():
        if key in (model or ""):
            return value
    return PRICES["sonnet"]


def content_text(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif "content" in block:
                parts.append(content_text(block["content"]))
    return "\n".join(parts)


def short_path(value):
    for marker in ("/repo/",):
        if marker in value:
            return value.rsplit(marker, 1)[1]
    return value


def tool_target(tool):
    data = tool.get("input") or {}
    for key in ("file_path", "path", "pattern", "command", "description", "query"):
        if data.get(key):
            value = short_path(str(data[key]).replace("\n", " "))
            return value if len(value) <= 60 else value[:57] + "..."
    return ""


def words(text):
    return re.findall(r"[a-z0-9]+", (text or "").lower())


def lead_calls(events):
    """Lead-thread API calls in order (events sharing message.id are one call)."""
    calls, index = [], {}
    for event in events:
        if event.get("type") != "assistant" or event.get("parent_tool_use_id"):
            continue
        message = event.get("message") or {}
        key = message.get("id") or f"anon-{len(calls)}"
        if key not in index:
            index[key] = len(calls)
            calls.append({"usage": {}, "tools": [], "text": ""})
        call = calls[index[key]]
        for field, value in (message.get("usage") or {}).items():
            if isinstance(value, (int, float)):
                call["usage"][field] = max(call["usage"].get(field, 0), value)
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                call["tools"].append({"id": block.get("id"), "name": block.get("name"),
                                      "input": block.get("input") or {}})
            elif block.get("type") == "text":
                call["text"] += block.get("text", "")
    return calls


def tool_results(events):
    out = {}
    for event in events:
        if event.get("type") != "user":
            continue
        content = (event.get("message") or {}).get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    text = content_text(block.get("content"))
                    out[block.get("tool_use_id")] = {"tokens": est_tokens(text),
                                                     "error": bool(block.get("is_error"))}
    return out


def analyse(path):
    events = load_events(path)
    result = result_event(events)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    synthetic = any(e.get("subtype") == "synthetic_notice" for e in events if e.get("type") == "system")
    model = init.get("model") or next(iter(result.get("modelUsage") or {}), "")
    p_in, p_out = prices(model)
    calls = lead_calls(events)
    results = tool_results(events)
    n = len(calls)
    reads, seen_calls, texts = set(), {}, []
    last_error_key = None
    rows, waste = [], []

    def carried_cost(tokens, index):
        later = max(0, n - index - 1)
        if later == 0:
            return 0.0
        return tokens * p_in / 1e6 * (W_WRITE + W_READ * (later - 1))

    for index, call in enumerate(calls):
        usage = call["usage"]
        context = sum(int(usage.get(k) or 0) for k in
                      ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
        row = {"turn": index + 1, "context": context, "output": int(usage.get("output_tokens") or 0),
               "items": []}
        text = call["text"].strip()
        if text:
            flag = ""
            tokens = est_tokens(text)
            if len(words(text)) >= 25:
                for earlier in texts:
                    ratio = difflib.SequenceMatcher(None, words(earlier), words(text), autojunk=False).ratio()
                    if ratio >= 0.6:
                        flag = "restated plan"
                        break
                texts.append(text)
            item = {"kind": "text", "label": text.replace("\n", " ")[:70], "tokens": tokens, "flag": flag}
            if flag:
                item["cost"] = tokens * p_out / 1e6 + carried_cost(tokens, index)
                waste.append({"flag": flag, "turn": index + 1, "what": item["label"][:50],
                              "tokens": tokens, "cost": item["cost"]})
            row["items"].append(item)
        for tool in call["tools"]:
            data = tool["input"]
            path_arg = data.get("file_path") or data.get("path")
            outcome = results.get(tool["id"], {"tokens": 0, "error": False})
            flag = ""
            key = (tool["name"], json.dumps(data, sort_keys=True))
            if tool["name"] in EDIT_TOOLS:
                if path_arg:
                    reads.discard(path_arg)
                seen_calls.clear()  # the repo changed: re-running things is legitimate now
                last_error_key = None
            elif tool["name"] == "Read" and path_arg:
                if path_arg in reads and not (data.get("offset") or data.get("limit")):
                    flag = "re-read"
                reads.add(path_arg)
            else:
                if key in seen_calls:
                    flag = "blind retry" if seen_calls[key] or last_error_key == key else "repeat"
                seen_calls[key] = outcome["error"]
            if outcome["error"]:
                last_error_key = key
            item = {"kind": "tool", "label": f"{tool['name']} {tool_target(tool)}".strip(),
                    "tokens": outcome["tokens"], "error": outcome["error"], "flag": flag}
            if flag:
                call_tokens = est_tokens(json.dumps(data))
                item["cost"] = carried_cost(outcome["tokens"], index) + call_tokens * p_out / 1e6
                waste.append({"flag": flag, "turn": index + 1, "what": item["label"][:50],
                              "tokens": outcome["tokens"] + call_tokens, "cost": item["cost"]})
            row["items"].append(item)
        flagged = [item for item in row["items"] if item.get("flag")]
        if flagged and len(flagged) == len(row["items"]):
            # The whole API call was spent on waste: add what that call itself cost
            # (its cached context read, fresh input, cache write and output).
            turn_cost = (int(usage.get("input_tokens") or 0) * p_in
                         + int(usage.get("cache_read_input_tokens") or 0) * p_in * W_READ
                         + int(usage.get("cache_creation_input_tokens") or 0) * p_in * W_WRITE
                         + int(usage.get("output_tokens") or 0) * p_out) / 1e6
            flagged[0]["cost"] += turn_cost
            flagged[0]["whole_turn"] = True
            for entry in reversed(waste):
                if entry["turn"] == index + 1:
                    entry["cost"] += turn_cost
                    break
        rows.append(row)

    labrun = load_json(Path(path).parent / "labrun.json", {}) or {}
    check = load_json(Path(path).parent / "check.json")
    passed = None if check is None else check.get("score") == 1.0
    total_cost = result.get("total_cost_usd")
    return {
        "path": str(path), "synthetic": synthetic, "model": model, "api_calls": n,
        "turns": result.get("num_turns"), "cost_usd": total_cost,
        "task": labrun.get("task"), "variant": labrun.get("variant"), "passed": passed,
        "rows": rows, "waste": waste,
    }


def fmt_usd(value):
    return f"${value:.4f}" if isinstance(value, (int, float)) else "n/a"


def fmt_tokens(value):
    return f"{value / 1000:.1f}k" if value >= 1000 else str(int(value))


def render(report):
    lines = []
    head = Path(report["path"]).parent.name if Path(report["path"]).name == "transcript.jsonl" else Path(report["path"]).name
    meta = [f"model {report['model'] or '?'}", f"{report['api_calls']} API calls",
            f"cost {fmt_usd(report['cost_usd'])}"]
    if report["task"]:
        meta.insert(0, f"task {report['task']} ({report['variant']})")
    if report["passed"] is not None:
        meta.append("passed" if report["passed"] else "FAILED")
    lines.append(f"## {head}" + ("  [SYNTHETIC SAMPLE]" if report["synthetic"] else ""))
    lines.append(" · ".join(meta))
    lines.append("")
    lines.append("```")
    lines.append(f"{'turn':>4} {'context':>8} {'out':>6}  what")
    for row in report["rows"]:
        first = True
        for item in row["items"] or [{"label": "(answer)", "flag": "", "tokens": 0}]:
            prefix = f"t{row['turn']:<3} {fmt_tokens(row['context']):>8} {fmt_tokens(row['output']):>6}  " if first \
                else " " * 22
            whole = ", whole turn" if item.get("whole_turn") else ""
            flag = (f"  <-- {item['flag']} (~{fmt_tokens(item['tokens'])} tok, ~{fmt_usd(item['cost'])}{whole})"
                    if item.get("flag") else "")
            err = " [error]" if item.get("error") else ""
            lines.append(f"{prefix}{item['label']}{err}{flag}")
            first = False
    lines.append("```")
    counts = Counter(w["flag"] for w in report["waste"])
    tokens = Counter()
    cost = Counter()
    for w in report["waste"]:
        tokens[w["flag"]] += w["tokens"]
        cost[w["flag"]] += w["cost"]
    table = ["| Flag | Count | Tokens into context (est) | Cost (est) | Share of session cost |",
             "|---|---|---|---|---|"]
    for flag in FLAGS:
        share = (f"{100 * cost[flag] / report['cost_usd']:.1f}%"
                 if report["cost_usd"] and counts[flag] else "-")
        table.append(f"| {flag} | {counts[flag]} | {fmt_tokens(tokens[flag])} | {fmt_usd(cost[flag]) if counts[flag] else '-'} | {share} |")
    lines += [""] + table + [""]
    return "\n".join(lines)


def main(argv):
    parser = argparse.ArgumentParser(description="flag wasted turns in Claude Code transcripts")
    parser.add_argument("transcripts", nargs="+")
    parser.add_argument("--md", help="also write the report to this Markdown file")
    parser.add_argument("--json", help="also write the analysis as JSON")
    args = parser.parse_args(argv[1:])
    reports = [analyse(p) for p in args.transcripts if Path(p).is_file()]
    if not reports:
        print("no transcripts found", file=sys.stderr)
        return 1
    out = ["# Trace report", "",
           "Estimates: tool output ~4 chars/token; cost = cache write 1.25x + 0.1x per later call "
           "(+ output price for text the model wrote). Session cost is Claude Code's total_cost_usd.", ""]
    if any(r["synthetic"] for r in reports):
        out += ["**Includes SYNTHETIC sample traces (sample-results/traces/), not real sessions.**", ""]
    for report in reports:
        out.append(render(report))
    counts, cost, session = Counter(), Counter(), 0.0
    for report in reports:
        session += report["cost_usd"] or 0.0
        for w in report["waste"]:
            counts[w["flag"]] += 1
            cost[w["flag"]] += w["cost"]
    wasted = sum(cost.values())
    out += ["## All traces", "",
            f"{len(reports)} transcripts, session cost {fmt_usd(session)}, flagged waste {fmt_usd(wasted)}"
            + (f" ({100 * wasted / session:.1f}%)" if session else ""),
            "", "| Flag | Count | Cost (est) |", "|---|---|---|"]
    out += [f"| {flag} | {counts[flag]} | {fmt_usd(cost[flag])} |" for flag in FLAGS]
    out += ["", "Read the flagged turns in the transcript before blaming the agent: a re-read after a long",
            "gap can be deliberate, and a retry after a flaky build is not blind. The flags point; you judge."]
    text = "\n".join(out) + "\n"
    print(text)
    if args.md:
        Path(args.md).write_text(text, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(reports, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
