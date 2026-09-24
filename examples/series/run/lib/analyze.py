#!/usr/bin/env python3
"""Read Claude Code headless transcripts and turn them into slide numbers.

Input is what `claude -p --output-format stream-json --verbose` writes: one JSON
event per line (system/init, assistant, user, result). A single JSON object from
`--output-format json` also works for the session totals.

Where each number comes from:
  * result event: total_cost_usd, num_turns, duration_ms, usage (main loop only)
    and modelUsage (every model call, subagents included). These are Claude
    Code's own client-side figures.
  * assistant events: message.usage per API call. Events that share a
    message.id are one API call; parent_tool_use_id is null for the lead and the
    Agent tool_use id for a subagent.
  * user events: tool results; tool_use_result is the structured output
    (AgentOutput for the Agent tool: totalTokens, totalToolUseCount, ...).
  * /context runs: the assistant event carries context_usage (categories,
    memory_files, mcp_tools, skills).
Anything marked "est" is estimated from transcript text at ~4 characters per
token; it is an attribution aid, not a meter reading.

Usage:
  analyze.py session TRANSCRIPT.jsonl       session metrics as JSON
  analyze.py trace TRANSCRIPT.jsonl         turn-by-turn trace with waste flags
  analyze.py context TRANSCRIPT.jsonl       /context breakdown as JSON
  analyze.py summarise TALK RESULTS_DIR     write summary.json + summary.md
"""
import json
import statistics
import sys
from collections import Counter, OrderedDict
from pathlib import Path

CHARS_PER_TOKEN = 4
# Input-equivalent weights for the bill attribution (slide 05·6): cache write
# 1.25x, cache read 0.1x, output 5x input (the ratio across the current family).
W_WRITE, W_READ, W_OUTPUT = 1.25, 0.1, 5.0


# ── loading ────────────────────────────────────────────────────────────────

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
        if not line.startswith("{"):
            continue
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


def est_tokens(text):
    return round(len(text or "") / CHARS_PER_TOKEN)


def content_text(content):
    """Flatten tool_result content (str or list of blocks) to text."""
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
        else:
            parts.append(str(block))
    return "\n".join(parts)


def usage_total(usage):
    usage = usage or {}
    return sum(int(usage.get(key) or 0) for key in (
        "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


# ── API calls and tool results ─────────────────────────────────────────────

def api_calls(events):
    """One entry per API call, in order: usage, parent, tool_use blocks, text."""
    calls = OrderedDict()
    for event in events:
        if event.get("type") != "assistant":
            continue
        message = event.get("message") or {}
        key = message.get("id") or event.get("uuid") or f"anon-{len(calls)}"
        call = calls.get(key)
        if call is None:
            call = calls[key] = {"id": key, "parent": event.get("parent_tool_use_id"),
                                 "model": message.get("model"), "usage": {},
                                 "tool_uses": [], "text": "", "thinking_chars": 0}
        for field, value in (message.get("usage") or {}).items():
            if isinstance(value, (int, float)):
                call["usage"][field] = max(call["usage"].get(field, 0), value)
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                call["tool_uses"].append({"id": block.get("id"), "name": block.get("name"),
                                          "input": block.get("input") or {}})
            elif block.get("type") == "text":
                call["text"] += block.get("text", "")
            elif block.get("type") == "thinking":
                call["thinking_chars"] += len(block.get("thinking", ""))
    return list(calls.values())


def tool_results(events):
    results = {}
    for event in events:
        if event.get("type") != "user":
            continue
        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                text = content_text(block.get("content"))
                results[block.get("tool_use_id")] = {
                    "text": text, "tokens_est": est_tokens(text),
                    "is_error": bool(block.get("is_error")),
                    "structured": event.get("tool_use_result"),
                    "parent": event.get("parent_tool_use_id"),
                }
    return results


def short_path(value):
    """Make temp-dir paths readable: /tmp/series-x.abc/repo/invoicing/a.py -> invoicing/a.py."""
    for marker in ("/repo/", "/wt-"):
        if marker in value:
            tail = value.rsplit(marker, 1)[1]
            return tail.split("/", 1)[1] if marker == "/wt-" and "/" in tail else tail
    return value


def tool_target(tool):
    data = tool.get("input") or {}
    for key in ("file_path", "path", "pattern", "command", "description", "query", "url"):
        if data.get(key):
            value = short_path(str(data[key]).replace("\n", " "))
            return value if len(value) <= 70 else value[:67] + "..."
    return ""


# ── session metrics ────────────────────────────────────────────────────────

def model_usage_totals(result):
    per_model = {}
    totals = Counter()
    for model, usage in (result.get("modelUsage") or {}).items():
        entry = {
            "input_tokens": int(usage.get("inputTokens") or 0),
            "output_tokens": int(usage.get("outputTokens") or 0),
            "cache_read_tokens": int(usage.get("cacheReadInputTokens") or 0),
            "cache_creation_tokens": int(usage.get("cacheCreationInputTokens") or 0),
            "cost_usd": float(usage.get("costUSD") or 0),
        }
        per_model[model] = entry
        totals.update({k: v for k, v in entry.items() if k != "cost_usd"})
    if not per_model and result.get("usage"):
        usage = result["usage"]
        totals.update({
            "input_tokens": int(usage.get("input_tokens") or 0),
            "output_tokens": int(usage.get("output_tokens") or 0),
            "cache_read_tokens": int(usage.get("cache_read_input_tokens") or 0),
            "cache_creation_tokens": int(usage.get("cache_creation_input_tokens") or 0),
        })
    return per_model, dict(totals)


def reads_and_rereads(calls, results, parent=None):
    """File reads on one thread; a re-read is a Read of a path already read
    with no Edit/Write to it in between."""
    seen, reads, rereads = set(), [], []
    for call in calls:
        if call["parent"] != parent:
            continue
        for tool in call["tool_uses"]:
            data = tool["input"]
            path = data.get("file_path") or data.get("path")
            if tool["name"] in ("Edit", "Write", "MultiEdit", "NotebookEdit") and path:
                seen.discard(path)
            if tool["name"] != "Read" or not path:
                continue
            tokens = results.get(tool["id"], {}).get("tokens_est", 0)
            entry = {"path": path, "tokens_est": tokens,
                     "partial": bool(data.get("offset") or data.get("limit"))}
            (rereads if path in seen else reads).append(entry)
            seen.add(path)
    return reads, rereads


def duplicate_calls(calls, results, parent=None):
    """Tool calls repeated with identical input, and blind retries of failures."""
    seen, duplicates, retries = {}, [], []
    for index, call in enumerate(calls):
        if call["parent"] != parent:
            continue
        for tool in call["tool_uses"]:
            if tool["name"] in ("Read", "Edit", "Write"):
                continue  # reads are counted as re-reads; edits legitimately repeat
            key = (tool["name"], json.dumps(tool["input"], sort_keys=True))
            if key in seen:
                earlier = seen[key]
                entry = {"tool": tool["name"], "target": tool_target(tool)}
                if results.get(earlier, {}).get("is_error"):
                    retries.append(entry)
                else:
                    duplicates.append(entry)
            seen[key] = tool["id"]
    return duplicates, retries


def subagent_stats(calls, results):
    agents = []
    for call in calls:
        if call["parent"] is not None:
            continue
        for tool in call["tool_uses"]:
            if tool["name"] not in ("Agent", "Task"):
                continue
            result = results.get(tool["id"], {})
            structured = result.get("structured") if isinstance(result.get("structured"), dict) else {}
            sub_calls = [c for c in calls if c["parent"] == tool["id"]]
            usage = Counter()
            for sub in sub_calls:
                usage.update({k: v for k, v in sub["usage"].items() if isinstance(v, (int, float))})
            first = sub_calls[0]["usage"] if sub_calls else {}
            report_text = content_text(structured.get("content")) if structured.get("content") else result.get("text", "")
            agents.append({
                "tool_use_id": tool["id"],
                "subagent_type": tool["input"].get("subagent_type") or structured.get("agentType"),
                "description": tool["input"].get("description", ""),
                "status": structured.get("status"),
                "total_tool_use_count": structured.get("totalToolUseCount"),
                "total_tokens_final_request": structured.get("totalTokens"),
                "total_duration_ms": structured.get("totalDurationMs"),
                "tool_stats": structured.get("toolStats"),
                "api_calls_seen": len(sub_calls),
                "usage_seen": dict(usage),
                "first_call_cache_read": int(first.get("cache_read_input_tokens") or 0),
                "first_call_cache_creation": int(first.get("cache_creation_input_tokens") or 0),
                "first_call_input": int(first.get("input_tokens") or 0),
                "returned_tokens_est": est_tokens(report_text),
            })
    return agents


def session_metrics(transcript, meta=None):
    events = load_events(transcript)
    meta = meta or {}
    result = result_event(events)
    calls = api_calls(events)
    results = tool_results(events)
    per_model, totals = model_usage_totals(result)
    main = [c for c in calls if c["parent"] is None]
    lead_sizes = [usage_total(c["usage"]) for c in main if c["usage"]]
    first = main[0]["usage"] if main else {}
    reads, rereads = reads_and_rereads(calls, results)
    duplicates, retries = duplicate_calls(calls, results)
    tools_main = Counter(t["name"] for c in main for t in c["tool_uses"])
    tools_sub = Counter(t["name"] for c in calls if c["parent"] is not None for t in c["tool_uses"])
    lead_tool_tokens = sum(results.get(t["id"], {}).get("tokens_est", 0)
                           for c in main for t in c["tool_uses"] if t["name"] not in ("Agent", "Task"))
    agents = subagent_stats(calls, results)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    metrics = {
        "transcript": str(transcript),
        "ok": bool(result) and not result.get("is_error", False),
        "subtype": result.get("subtype"),
        "terminal_reason": result.get("terminal_reason"),
        "num_turns": result.get("num_turns"),
        "duration_ms": result.get("duration_ms"),
        "duration_api_ms": result.get("duration_api_ms"),
        "wall_ms": meta.get("wall_ms"),
        "duration_s": round((result.get("duration_ms") or meta.get("wall_ms") or 0) / 1000, 1),
        "cost_usd": result.get("total_cost_usd"),
        "model": init.get("model") or (main[0]["model"] if main else None),
        "model_usage": per_model,
        **{key: totals.get(key, 0) for key in (
            "input_tokens", "output_tokens", "cache_read_tokens", "cache_creation_tokens")},
        "total_tokens": sum(totals.get(key, 0) for key in (
            "input_tokens", "output_tokens", "cache_read_tokens", "cache_creation_tokens")),
        "api_calls_main": len(main),
        "api_calls_subagents": len(calls) - len(main),
        "lead_context_final": lead_sizes[-1] if lead_sizes else None,
        "lead_context_peak": max(lead_sizes) if lead_sizes else None,
        "first_call": {
            "input_tokens": int(first.get("input_tokens") or 0),
            "cache_read_tokens": int(first.get("cache_read_input_tokens") or 0),
            "cache_creation_tokens": int(first.get("cache_creation_input_tokens") or 0),
        },
        "tools_main": dict(tools_main),
        "tools_subagents": dict(tools_sub),
        "file_reads": len(reads),
        "file_rereads": len(rereads),
        "read_tokens_est": sum(r["tokens_est"] for r in reads),
        "reread_tokens_est": sum(r["tokens_est"] for r in rereads),
        "reread_paths": sorted({r["path"] for r in rereads}),
        "duplicate_tool_calls": len(duplicates),
        "blind_retries": len(retries),
        "lead_tool_result_tokens_est": lead_tool_tokens,
        "subagents": agents,
        "subagent_return_tokens_est": sum(a["returned_tokens_est"] for a in agents),
        "permission_denials": len(result.get("permission_denials") or []),
        "result_text": (result.get("result") or "")[:4000],
    }
    return metrics


# ── trace and bill attribution ─────────────────────────────────────────────

def trace(transcript):
    """Lead-thread turns with usage and waste flags (slides 07·15 and 07·16)."""
    events = load_events(transcript)
    calls = api_calls(events)
    results = tool_results(events)
    rows, seen_reads, seen_calls = [], set(), {}
    for index, call in enumerate(c for c in calls if c["parent"] is None):
        tools = []
        for tool in call["tool_uses"]:
            data = tool["input"]
            path = data.get("file_path") or data.get("path")
            flag = ""
            if tool["name"] in ("Edit", "Write", "MultiEdit") and path:
                seen_reads.discard(path)
            if tool["name"] == "Read" and path:
                flag = "re-read" if path in seen_reads else ""
                seen_reads.add(path)
            elif tool["name"] not in ("Edit", "Write", "MultiEdit"):
                key = (tool["name"], json.dumps(data, sort_keys=True))
                if key in seen_calls:
                    flag = "blind retry" if results.get(seen_calls[key], {}).get("is_error") else "repeat"
                seen_calls[key] = tool["id"]
            result = results.get(tool["id"], {})
            tools.append({"tool": tool["name"], "target": tool_target(tool),
                          "result_tokens_est": result.get("tokens_est", 0),
                          "error": result.get("is_error", False), "flag": flag})
        usage = call["usage"]
        rows.append({
            "turn": index + 1,
            "input_tokens": int(usage.get("input_tokens") or 0),
            "cache_read_tokens": int(usage.get("cache_read_input_tokens") or 0),
            "cache_creation_tokens": int(usage.get("cache_creation_input_tokens") or 0),
            "output_tokens": int(usage.get("output_tokens") or 0),
            "text": call["text"][:160],
            "tools": tools,
        })
    return rows


def bill_attribution(transcript):
    """Split one session's input-equivalent spend into the slide 05·6 lines.

    Each piece of context is written to the cache once (1.25x) and read on every
    later API call (0.1x); output costs 5x. The fixed prefix is the first call's
    whole input. Tool results are sized at ~4 chars/token.
    """
    rows = trace(transcript)
    if not rows:
        return {}
    n = len(rows)
    first = rows[0]
    prefix = first["input_tokens"] + first["cache_read_tokens"] + first["cache_creation_tokens"]
    buckets = Counter()
    counts = Counter()
    buckets["cached prefix"] += prefix * (W_WRITE if first["cache_creation_tokens"] else W_READ)
    buckets["cached prefix"] += prefix * W_READ * (n - 1)
    for index, row in enumerate(rows):
        later_calls = n - index - 1  # a tool result enters the next call's input
        for tool in row["tools"]:
            size = tool["result_tokens_est"]
            if tool["tool"] == "Read":
                bucket = "re-reads" if tool["flag"] == "re-read" else "file reads"
            else:
                bucket = "other tool results"
            counts[bucket] += 1
            if later_calls > 0:
                buckets[bucket] += size * (W_WRITE + W_READ * (later_calls - 1))
        buckets["thinking + answer"] += row["output_tokens"] * W_OUTPUT
    total = sum(buckets.values()) or 1
    order = ["cached prefix", "file reads", "re-reads", "other tool results", "thinking + answer"]
    return {
        "api_calls": n,
        "prefix_tokens": prefix,
        "file_reads": counts["file reads"],
        "re_reads": counts["re-reads"],
        "shares_pct": {name: round(100 * buckets[name] / total, 1) for name in order},
        "method": "input-equivalent weights: write 1.25x, read 0.1x, output 5x; tool results ~4 chars/token",
    }


# ── /context ───────────────────────────────────────────────────────────────

def context_report(transcript):
    events = load_events(transcript)
    usage = None
    text = ""
    for event in events:
        if event.get("type") == "assistant":
            if event.get("context_usage"):
                usage = event["context_usage"]
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "text":
                    text += block.get("text", "")
    result = result_event(events)
    if usage is None and result.get("result"):
        text = text or result["result"]
    report = {"transcript": str(transcript), "source": "context_usage" if usage else "text",
              "cost_usd": result.get("total_cost_usd")}
    if usage:
        report.update({
            "model": usage.get("model"),
            "total_tokens": usage.get("total_tokens"),
            "window": usage.get("raw_max_tokens"),
            "categories": [{"name": c.get("name"), "tokens": c.get("tokens"), "kind": c.get("kind")}
                           for c in usage.get("categories") or []],
            "memory_files": usage.get("memory_files") or [],
            "mcp_tools": usage.get("mcp_tools") or [],
            "skills": usage.get("skills") or [],
        })
    else:
        report["raw_text"] = text[:4000]
    memory = report.get("memory_files") or []
    report["claude_md_tokens"] = sum(int(m.get("tokens") or 0) for m in memory
                                     if str(m.get("path", "")).endswith("CLAUDE.md")
                                     and str(m.get("type", "")).lower().startswith("project"))
    report["user_memory_loaded"] = [m.get("path") for m in memory
                                    if str(m.get("type", "")).lower().startswith("user")]
    report["mcp_tool_tokens"] = sum(int(t.get("tokens") or 0) for t in report.get("mcp_tools") or [])
    return report


# ── helpers for summaries ──────────────────────────────────────────────────

def mean(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return round(statistics.mean(values), 2) if values else None


def total(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return round(sum(values), 4) if values else None


def fmt_tokens(value):
    if not isinstance(value, (int, float)):
        return "n/a"
    return f"{value / 1000:.1f}k" if value >= 1000 else str(int(value))


def fmt_usd(value, places=2):
    return f"${value:.{places}f}" if isinstance(value, (int, float)) else "n/a"


def md_table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines)


def session_dir_metrics(directory):
    directory = Path(directory)
    metrics = session_metrics(directory / "transcript.jsonl", load_json(directory / "meta.json", {}))
    status = directory / "tests.status"
    metrics["tests"] = status.read_text().strip() if status.is_file() else None
    check = load_json(directory / "check.json")
    if check is not None:
        metrics["check"] = check
    return metrics


# ── per-talk summaries ─────────────────────────────────────────────────────

def summarise_talk03(root):
    plan = load_json(root / "plan.json", {})
    setups = plan.get("setups") or {}
    out = {"talk": "03", "plan": plan, "setups": {}}
    rows = []
    for label in sorted(setups):
        runs = sorted(p for p in (root / "runs").glob(f"{label}-*") if p.is_dir())
        sessions = [session_dir_metrics(p) for p in runs]
        accepted = [s for s in sessions if (s.get("check") or {}).get("accepted")]
        cost = total(s.get("cost_usd") for s in sessions)
        diff_lines = [sum(1 for line in (p / "diff.patch").read_text(errors="replace").splitlines()
                          if line.startswith(("+", "-")) and not line.startswith(("+++", "---")))
                      for p in runs if (p / "diff.patch").is_file()]
        entry = {
            "label": setups[label].get("label", label), "model": setups[label].get("model"),
            "prompt": setups[label].get("prompt"), "runs": len(sessions),
            "accepted": len(accepted), "cost_usd": cost,
            "cost_per_accepted_usd": round(cost / len(accepted), 4) if cost and accepted else None,
            "mean_turns": mean(s.get("num_turns") for s in sessions),
            "mean_duration_s": mean(s.get("duration_s") for s in sessions),
            "mean_total_tokens": mean(s.get("total_tokens") for s in sessions),
            "mean_diff_lines": mean(diff_lines),
            "reasons": Counter((s.get("check") or {}).get("reason", "no check") for s in sessions
                               if not (s.get("check") or {}).get("accepted")),
        }
        out["setups"][label] = entry
        rows.append([f"{label}: {entry['label']}", entry["model"], f"{entry['accepted']}/{entry['runs']}",
                     fmt_usd(entry["cost_usd"]), fmt_usd(entry["cost_per_accepted_usd"], 3),
                     entry["mean_turns"], entry["mean_duration_s"], entry["mean_diff_lines"]])
    md = ["# Talk 03 · cost per accepted task (slide 22)", "",
          md_table(["Setup", "Model", "Accepted", "Model+tool cost", "Cost / accepted",
                    "Mean turns", "Mean time (s)", "Mean diff lines (review proxy)"], rows), "",
          "Accepted = hidden acceptance tests and the attempt's own tests pass "
          "(talk03/check.py). Review time is not measured; diff lines are a proxy."]
    return out, "\n".join(md)


def summarise_talk04(root):
    out = {"talk": "04"}
    md = ["# Talk 04 · subagents and caching", ""]
    survey = {}
    for variant in ("inline", "subagents"):
        directory = root / f"survey-{variant}"
        if directory.is_dir():
            survey[variant] = session_dir_metrics(directory)
    out["survey"] = survey
    if survey:
        rows = []
        for variant, m in survey.items():
            into_lead = (m["lead_tool_result_tokens_est"] if variant == "inline"
                         else m["subagent_return_tokens_est"] + m["lead_tool_result_tokens_est"])
            m["tokens_into_lead_est"] = into_lead
            rows.append([variant, m["file_reads"], fmt_tokens(into_lead), fmt_tokens(m["lead_context_final"]),
                         fmt_tokens(m["total_tokens"]), m["duration_s"], fmt_usd(m["cost_usd"], 3),
                         len(m["subagents"])])
        md += ["## Survey: inline vs subagents (slides 8, 11, 12, 14, 17)", "",
               md_table(["Variant", "Lead file reads", "Tool output into lead (est)", "Lead context at end",
                         "Total tokens (all agents)", "Wall-clock (s)", "Cost", "Subagents"], rows), ""]
        agents = survey.get("subagents", {}).get("subagents") or []
        if agents:
            md += ["Subagent lines, in Claude Code's format (slide 17):", "```"]
            for agent in agents:
                md.append(f"⏺ {agent['subagent_type'] or 'Agent'}({agent['description']})")
                md.append(f"  ⎿ Done ({agent['total_tool_use_count'] or '?'} tool uses · "
                          f"{fmt_tokens(agent['total_tokens_final_request'])} tokens · "
                          f"{round((agent['total_duration_ms'] or 0) / 1000)}s) · returned ~{agent['returned_tokens_est']} tokens")
            md += ["```", "",
                   "Subagent first-call cache (slide 34): "
                   + "; ".join(f"{a['description'] or a['tool_use_id']}: read {fmt_tokens(a['first_call_cache_read'])}, "
                               f"write {fmt_tokens(a['first_call_cache_creation'])}" for a in agents), ""]
    cache = []
    first_start = None
    for directory in sorted(root.glob("cache-*")):
        m = session_dir_metrics(directory)
        m["label"] = directory.name
        started = (load_json(directory / "meta.json", {}) or {}).get("started_ms")
        first_start = first_start if first_start is not None else started
        m["started_after_s"] = round((started - first_start) / 1000) if started and first_start else None
        denominator = m["input_tokens"] + m["cache_read_tokens"] + m["cache_creation_tokens"]
        m["cache_hit_pct"] = round(100 * m["cache_read_tokens"] / denominator, 1) if denominator else None
        cache.append(m)
    out["cache"] = cache
    if cache:
        md += ["## Same prompt twice (slides 29, 31, 32)", "",
               md_table(["Run", "Started", "First call: cache write", "First call: cache read",
                         "Session cache write", "Session cache read", "Fresh input", "Hit %", "Cost"],
                        [[m["label"], f"+{m['started_after_s']}s" if m["started_after_s"] is not None else "n/a",
                          fmt_tokens(m["first_call"]["cache_creation_tokens"]), fmt_tokens(m["first_call"]["cache_read_tokens"]),
                          fmt_tokens(m["cache_creation_tokens"]), fmt_tokens(m["cache_read_tokens"]),
                          fmt_tokens(m["input_tokens"]), m["cache_hit_pct"], fmt_usd(m["cost_usd"], 4)] for m in cache]), ""]
    return out, "\n".join(md)


def summarise_talk05(root):
    out = {"talk": "05", "variants": {}}
    rows, overhead_rows = [], []
    for variant in ("bloated", "lean"):
        context = root / f"context-{variant}" / "transcript.jsonl"
        ctx = context_report(context) if context.is_file() else {}
        sessions = [session_dir_metrics(p) for p in sorted(root.glob(f"task-{variant}-*")) if p.is_dir()]
        claude_md = ctx.get("claude_md_tokens") or None
        claude_md_source = "/context"
        if claude_md is None:  # no context_usage in this Claude Code version: estimate from the file
            md_file = Path(__file__).resolve().parents[2] / "claude-md" / f"{variant}.md"
            if md_file.is_file():
                claude_md = est_tokens(md_file.read_text(encoding="utf-8"))
                claude_md_source = "estimate (chars/4)"
        entry = {
            "context": ctx,
            "runs": len(sessions),
            "turns": mean(s.get("num_turns") for s in sessions),
            "api_calls": mean(s.get("api_calls_main") for s in sessions),
            "total_tokens": mean(s.get("total_tokens") for s in sessions),
            "cost_usd": mean(s.get("cost_usd") for s in sessions),
            "duration_s": mean(s.get("duration_s") for s in sessions),
            "claude_md_tokens_per_turn": claude_md,
            "claude_md_tokens_source": claude_md_source,
            "claude_md_tokens_session": round(claude_md * mean(s.get("api_calls_main") for s in sessions))
            if claude_md and sessions else None,
            "passed": sum(1 for s in sessions if (s.get("check") or {}).get("score") == 1.0),
            "file_reads": mean(s.get("file_reads") for s in sessions),
            "file_rereads": mean(s.get("file_rereads") for s in sessions),
            "sessions": [{k: s.get(k) for k in ("num_turns", "total_tokens", "cost_usd", "duration_s",
                                                "file_reads", "file_rereads", "tests")} for s in sessions],
        }
        entry["outcome"] = f"{entry['passed']}/{entry['runs']} pass" if sessions else None
        out["variants"][variant] = entry
        rows.append([variant, entry["turns"], fmt_tokens(entry["total_tokens"]), fmt_tokens(claude_md),
                     fmt_tokens(entry["claude_md_tokens_session"]), entry["outcome"],
                     fmt_usd(entry["cost_usd"], 3), entry["file_reads"], entry["file_rereads"]])
        if ctx.get("categories"):
            overhead_rows.append([variant] + [f"{c['name']}: {fmt_tokens(c['tokens'])}" for c in ctx["categories"]
                                              if c.get("kind") in ("used", "deferred") and c.get("tokens")])
    bill_source = next((p for v in ("lean", "bloated") for p in sorted(root.glob(f"task-{v}-*"))), None)
    out["bill"] = bill_attribution(bill_source / "transcript.jsonl") if bill_source else {}
    out["bill_source"] = str(bill_source) if bill_source else None
    lean_ctx = out["variants"].get("lean", {}).get("context") or {}
    out["overhead"] = {c["name"]: c["tokens"] for c in lean_ctx.get("categories") or [] if c.get("kind") == "used"}
    md = ["# Talk 05 · bloated vs lean CLAUDE.md", "",
          "## Fallback table (slide 25) and live demo (slide 24)", "",
          md_table(["CLAUDE.md", "Turns (mean)", "Total tokens (mean)", "CLAUDE.md tokens per turn",
                    "CLAUDE.md tokens per session", "Outcome", "Cost (mean)", "File reads", "Re-reads"], rows), "",
          "CLAUDE.md tokens per turn come from /context (memory_files); per session = per turn x lead API calls."]
    if overhead_rows:
        md += ["", "## Overhead before you type (slide 17), from /context", ""]
        md += [f"- **{row[0]}**: " + " · ".join(row[1:]) for row in overhead_rows]
    if out["bill"]:
        bill = out["bill"]
        md += ["", f"## One session's bill (slide 6), from {Path(out['bill_source']).name}", "",
               md_table(["Line", "Share of input-equivalent spend"],
                        [[k, f"{v}%"] for k, v in bill["shares_pct"].items()]), "",
               f"{bill['api_calls']} lead API calls, prefix {fmt_tokens(bill['prefix_tokens'])}, "
               f"file reads x{bill['file_reads']}, re-reads x{bill['re_reads']}. Method: {bill['method']}."]
    return out, "\n".join(md)


def summarise_talk06(root):
    out = {"talk": "06", "agents": {}}
    md = ["# Talk 06 · parallel agents and MCP vs CLI", ""]
    for directory in sorted(root.glob("agent-*")):
        m = session_dir_metrics(directory)
        out["agents"][directory.name] = {k: m.get(k) for k in (
            "num_turns", "total_tokens", "cost_usd", "duration_s", "tests", "subtype")}
        out["agents"][directory.name]["check"] = m.get("check")
    merge = load_json(root / "merge.json")
    out["merge"] = merge
    if out["agents"]:
        md += ["## Two agents, two worktrees (slide 13)", "",
               md_table(["Agent", "Turns", "Tokens", "Cost", "Time (s)", "Own tests", "Hidden check"],
                        [[name, a["num_turns"], fmt_tokens(a["total_tokens"]), fmt_usd(a["cost_usd"], 3),
                          a["duration_s"], a["tests"], (a.get("check") or {}).get("notes", "n/a")]
                         for name, a in out["agents"].items()]), ""]
    if merge:
        md += [f"Parallel wall-clock: {merge.get('parallel_wall_s')} s. Merge of {merge.get('first')}: "
               f"{merge.get('first_merge')}. Merge of {merge.get('second')}: {merge.get('second_merge')}"
               + (f" (conflicts in {', '.join(merge.get('conflicted_files') or [])})" if merge.get("conflicted_files") else ""), ""]
    paths = {}
    for kind in ("mcp", "cli"):
        ctx_file = root / f"{kind}-context" / "transcript.jsonl"
        task_dir = root / f"{kind}-task"
        entry = {}
        if ctx_file.is_file():
            ctx = context_report(ctx_file)
            entry["context_total_tokens"] = ctx.get("total_tokens")
            entry["mcp_tool_tokens"] = ctx.get("mcp_tool_tokens")
            entry["deferred_tokens"] = sum(c["tokens"] or 0 for c in ctx.get("categories") or []
                                           if c.get("kind") == "deferred")
        if task_dir.is_dir():
            m = session_dir_metrics(task_dir)
            entry.update({k: m.get(k) for k in ("total_tokens", "cost_usd", "duration_s", "num_turns",
                                                 "tools_main", "wall_ms")})
            entry["correct"] = (m.get("check") or {}).get("correct")
        if entry:
            paths[kind] = entry
    out["mcp_vs_cli"] = paths
    if paths:
        md += ["## One capability both ways (slide 30)", "",
               md_table(["Row", "MCP server", "CLI + docs"], [
                   ["Tokens before the first call (/context)", fmt_tokens(paths.get("mcp", {}).get("context_total_tokens")),
                    fmt_tokens(paths.get("cli", {}).get("context_total_tokens"))],
                   ["  of which MCP tool schemas (deferred)", fmt_tokens(paths.get("mcp", {}).get("mcp_tool_tokens")) + " (" +
                    fmt_tokens(paths.get("mcp", {}).get("deferred_tokens")) + ")", "0"],
                   ["Tokens for the whole task", fmt_tokens(paths.get("mcp", {}).get("total_tokens")),
                    fmt_tokens(paths.get("cli", {}).get("total_tokens"))],
                   ["Cost", fmt_usd(paths.get("mcp", {}).get("cost_usd"), 4), fmt_usd(paths.get("cli", {}).get("cost_usd"), 4)],
                   ["Wall-clock (s)", paths.get("mcp", {}).get("duration_s"), paths.get("cli", {}).get("duration_s")],
                   ["Right result?", paths.get("mcp", {}).get("correct"), paths.get("cli", {}).get("correct")],
               ]), ""]
    return out, "\n".join(md)


def summarise_talk07(root):
    grades = load_json(root / "grades.json", {}) or {}
    rows = grades.get("rows") or []
    out = {"talk": "07", "engine": (load_json(root / "plan.json", {}) or {}).get("engine"), "cells": {}}
    groups = {}
    for row in rows:
        variant = row.get("config") if len({r.get("config") for r in rows}) > 1 else row.get("model")
        groups.setdefault((row.get("task"), variant), []).append(row)
    variants = sorted({key[1] for key in groups})
    tasks = sorted({key[0] for key in groups})
    for (task, variant), items in groups.items():
        passes = [r.get("outcome") == "pass" for r in items]
        metrics = [r.get("metrics") or {} for r in items]
        out["cells"][f"{task}|{variant}"] = {
            "task": task, "variant": variant, "k": len(passes), "passes": sum(passes),
            "pass_at_k": any(passes), "pass_hat_k": all(passes) if passes else False,
            "cost_usd": total(m.get("cost_usd") for m in metrics),
            "mean_turns": mean(m.get("num_turns") for m in metrics),
        }
    per_variant = {}
    for variant in variants:
        cells = [c for c in out["cells"].values() if c["variant"] == variant]
        runs = sum(c["k"] for c in cells)
        passes = sum(c["passes"] for c in cells)
        cost = total(c["cost_usd"] for c in cells)
        per_variant[variant] = {
            "tasks": len(cells), "runs": runs, "passes": passes,
            "pass_rate": round(passes / runs, 3) if runs else None,
            "pass_at_k_tasks": sum(c["pass_at_k"] for c in cells),
            "pass_hat_k_tasks": sum(c["pass_hat_k"] for c in cells),
            "k": min((c["k"] for c in cells), default=0),
            "cost_usd": cost,
            "cost_per_pass_usd": round(cost / passes, 4) if cost and passes else None,
            "mean_turns": mean(c["mean_turns"] for c in cells),
        }
    out["variants"] = per_variant
    # Trace examples (slides 15 and 16): waste counts over all runs, one example trace.
    waste = Counter()
    example = None
    for row in rows:
        transcript = Path(row.get("run_dir", "")) / "transcript.jsonl"
        if not transcript.is_file():
            continue
        steps = trace(transcript)
        flags = Counter(t["flag"] for step in steps for t in step["tools"] if t["flag"])
        waste.update(flags)
        waste["turns"] += len(steps)
        waste["runs"] += 1
        if example is None and row.get("outcome") == "pass" and 4 <= len(steps) <= 12:
            example = {"run_dir": row.get("run_dir"), "task": row.get("task"), "steps": steps}
    out["waste"] = dict(waste)
    out["example_trace"] = example
    md = ["# Talk 07 · minimal eval", ""]
    if variants:
        md += ["## Scored sheet (slides 12-13)", "",
               md_table(["Task"] + [f"{v} (passes/k)" for v in variants],
                        [[task] + [f"{out['cells'].get(f'{task}|{v}', {}).get('passes', '-')}/"
                                   f"{out['cells'].get(f'{task}|{v}', {}).get('k', '-')}" for v in variants]
                         for task in tasks]), "",
               md_table(["Variant", "Pass rate", "pass@k tasks", "pass^k tasks", "k", "Cost", "Cost / pass", "Mean turns"],
                        [[v, p["pass_rate"], f"{p['pass_at_k_tasks']}/{p['tasks']}", f"{p['pass_hat_k_tasks']}/{p['tasks']}",
                          p["k"], fmt_usd(p["cost_usd"]), fmt_usd(p["cost_per_pass_usd"], 3), p["mean_turns"]]
                         for v, p in per_variant.items()]), ""]
    if waste:
        md += [f"Waste across {waste.get('runs', 0)} runs / {waste.get('turns', 0)} lead turns (slide 16): "
               f"re-reads {waste.get('re-read', 0)}, repeated calls {waste.get('repeat', 0)}, "
               f"blind retries {waste.get('blind retry', 0)}.", ""]
    if example:
        md += [f"Example trace (slide 15): {example['task']}, {example['run_dir']}", "```"]
        for step in example["steps"]:
            tools = "; ".join(f"{t['tool']} {t['target']}" + (f" [{t['flag']}]" if t["flag"] else "")
                              for t in step["tools"]) or (step["text"][:60] or "(answer)")
            md.append(f"t{step['turn']:<2} in {fmt_tokens(step['input_tokens'] + step['cache_read_tokens'] + step['cache_creation_tokens']):>6}"
                      f" out {fmt_tokens(step['output_tokens']):>5}  {tools}")
        md.append("```")
    return out, "\n".join(md)


SUMMARISERS = {"talk03": summarise_talk03, "talk04": summarise_talk04, "talk05": summarise_talk05,
               "talk06": summarise_talk06, "talk07": summarise_talk07}


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    command = argv[1]
    if command == "session":
        meta = load_json(Path(argv[2]).parent / "meta.json", {})
        print(json.dumps(session_metrics(argv[2], meta), indent=2, ensure_ascii=False))
    elif command == "trace":
        for row in trace(argv[2]):
            print(json.dumps(row, ensure_ascii=False))
    elif command == "context":
        print(json.dumps(context_report(argv[2]), indent=2, ensure_ascii=False))
    elif command == "summarise" and len(argv) == 4:
        talk, root = argv[2], Path(argv[3])
        data, markdown = SUMMARISERS[talk](root)
        (root / "summary.json").write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n")
        (root / "summary.md").write_text(markdown + "\n")
        print(markdown)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
