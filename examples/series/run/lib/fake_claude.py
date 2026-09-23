#!/usr/bin/env python3
"""A stand-in for `claude -p ... --output-format stream-json` that calls nothing.

For smoke-testing the runners, the analysis and summarise.py without spending
usage: `CLAUDE_BIN=run/lib/fake_claude.py run/talk05.sh --yes`. It emits
synthetic stream-json events shaped like Claude Code's (init, assistant with
per-call usage, user tool results, result with total_cost_usd/modelUsage), and
a context_usage payload for a `/context` prompt. The numbers are fake.

To make checkers pass it can copy a reference solution into the working dir:
  FAKE_OVERLAY=DIR                   always copy DIR over the cwd
  FAKE_OVERLAY_MAP="kw=DIR;kw2=DIR2"  copy DIR when the prompt contains kw
  FAKE_FAIL=1                         exit 1 without a result (a harness error)
"""
import json
import os
import random
import shutil
import sys
import time
import uuid
from pathlib import Path


def arg_value(args, name, default=None):
    if name in args:
        index = args.index(name)
        if index + 1 < len(args):
            return args[index + 1]
    return default


def emit(event):
    sys.stdout.write(json.dumps(event, ensure_ascii=False) + "\n")


def overlay(prompt):
    targets = []
    if os.environ.get("FAKE_OVERLAY"):
        targets.append(os.environ["FAKE_OVERLAY"])
    for pair in filter(None, os.environ.get("FAKE_OVERLAY_MAP", "").split(";")):
        keyword, _, directory = pair.partition("=")
        if keyword and keyword in prompt:
            targets.append(directory)
    for directory in targets:
        if Path(directory).is_dir():
            shutil.copytree(directory, Path.cwd(), dirs_exist_ok=True)


def usage(inp, read, write, out):
    return {"input_tokens": inp, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": write, "output_tokens": out}


def main():
    args = sys.argv[1:]
    if "--version" in args:
        print("0.0.0 (fake claude)")
        return 0
    if os.environ.get("FAKE_FAIL"):
        print("fake failure", file=sys.stderr)
        return 1
    prompt = arg_value(args, "-p", "") or sys.stdin.read()
    model = arg_value(args, "--model", "claude-sonnet-5")
    session = str(uuid.uuid4())
    rng = random.Random(hash(prompt) & 0xFFFF)
    cwd = Path.cwd()
    claude_md = cwd / "CLAUDE.md"
    md_tokens = len(claude_md.read_text(encoding="utf-8")) // 4 if claude_md.is_file() else 0
    has_mcp = "--mcp-config" in args
    emit({"type": "system", "subtype": "init", "session_id": session, "model": model, "cwd": str(cwd),
          "tools": ["Task", "Bash", "Read", "Edit"] + (["mcp__invoicing__invoice_report"] if has_mcp else []),
          "mcp_servers": [{"name": "invoicing", "status": "connected"}] if has_mcp else []})
    prefix = 18000 + md_tokens

    if prompt.strip() == "/context":
        categories = [
            {"name": "System prompt", "tokens": 4200, "kind": "used"},
            {"name": "System tools", "tokens": 11800, "kind": "used"},
            {"name": "Memory files", "tokens": md_tokens + 90, "kind": "used"},
            {"name": "Skills", "tokens": 450, "kind": "used"},
            {"name": "Messages", "tokens": 8, "kind": "used"},
            {"name": "Free space", "tokens": 960000, "kind": "free"},
        ]
        if has_mcp:
            categories.append({"name": "MCP tools", "tokens": 1350, "kind": "deferred"})
        emit({"type": "assistant", "session_id": session, "parent_tool_use_id": None,
              "message": {"id": "msg_ctx", "model": "<synthetic>", "role": "assistant",
                          "content": [{"type": "text", "text": "## Context Usage\n(fake)"}]},
              "context_usage": {"model": model, "total_tokens": sum(c["tokens"] for c in categories if c["kind"] == "used"),
                                "raw_max_tokens": 1000000, "percentage": 2, "categories": categories,
                                "memory_files": ([{"path": str(claude_md), "type": "Project", "tokens": md_tokens}]
                                                 if md_tokens else []),
                                "mcp_tools": ([{"name": "mcp__invoicing__invoice_report", "server_name": "invoicing",
                                                "tokens": 450}] * 3 if has_mcp else []),
                                "agents": [], "skills": []}})
        emit({"type": "result", "subtype": "success", "is_error": False, "session_id": session,
              "num_turns": 0, "duration_ms": 40, "duration_api_ms": 0, "total_cost_usd": 0,
              "result": "## Context Usage\n(fake)", "usage": usage(0, 0, 0, 0), "modelUsage": {},
              "permission_denials": []})
        return 0

    overlay(prompt)
    calls = []
    files = sorted(p for p in cwd.rglob("*.py") if ".git" not in p.parts)[:4]
    context = prefix
    turn = 0

    def assistant(content, parent=None, grow=0, write=None):
        nonlocal context, turn
        turn += 1
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        u = usage(3, context if turn > 1 else 0, write if write is not None else (context if turn == 1 else grow + 50),
                  rng.randint(80, 600))
        emit({"type": "assistant", "session_id": session, "parent_tool_use_id": parent,
              "message": {"id": msg_id, "model": model, "role": "assistant", "content": content, "usage": u}})
        calls.append(u)
        context += grow + 50

    def tool_result(tool_id, text, parent=None, structured=None, error=False):
        event = {"type": "user", "session_id": session, "parent_tool_use_id": parent,
                 "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_id,
                                                          "content": text, "is_error": error}]}}
        if structured is not None:
            event["tool_use_result"] = structured
        emit(event)

    if "use the Agent tool" in prompt:
        agent_ids = []
        for index, area in enumerate(["money and invoice", "customers and report", "dates, fixtures and export"]):
            tool_id = f"toolu_agent{index}"
            agent_ids.append((tool_id, area))
            assistant([{"type": "tool_use", "id": tool_id, "name": "Agent",
                        "input": {"description": f"Survey {area}", "subagent_type": "Explore", "prompt": area}}])
        for tool_id, area in agent_ids:
            sub_context = 9000
            for step, path in enumerate(files[:3]):
                sub_id = f"{tool_id}_r{step}"
                emit({"type": "assistant", "session_id": session, "parent_tool_use_id": tool_id,
                      "message": {"id": f"msg_{tool_id}_{step}", "model": model, "role": "assistant",
                                  "content": [{"type": "tool_use", "id": sub_id, "name": "Read",
                                               "input": {"file_path": str(path)}}],
                                  "usage": usage(3, 0 if step == 0 else sub_context, sub_context if step == 0 else 900, 120)}})
                sub_context += 900
                tool_result(sub_id, path.read_text(encoding="utf-8"), parent=tool_id)
            report = f"{area}: 3 modules, pure functions, one risk each."
            tool_result(tool_id, report, structured={
                "status": "completed", "agentId": tool_id, "agentType": "Explore",
                "content": [{"type": "text", "text": report}], "totalToolUseCount": 3,
                "totalDurationMs": rng.randint(20000, 60000), "totalTokens": sub_context,
                "usage": usage(3, sub_context - 900, 900, 400), "prompt": area})
    else:
        for index, path in enumerate(files + files[:1]):  # the last one is a re-read
            tool_id = f"toolu_read{index}"
            text = path.read_text(encoding="utf-8")
            assistant([{"type": "tool_use", "id": tool_id, "name": "Read", "input": {"file_path": str(path)}}],
                      grow=len(text) // 4)
            tool_result(tool_id, text)
        tool_id = "toolu_bash"
        assistant([{"type": "tool_use", "id": tool_id, "name": "Bash",
                    "input": {"command": "python3 -m unittest", "description": "Run tests"}}])
        tool_result(tool_id, "Ran 50 tests in 0.1s\n\nOK")
        if "mcp__" in " ".join(args) or has_mcp:
            tool_id = "toolu_mcp"
            assistant([{"type": "tool_use", "id": tool_id, "name": "mcp__invoicing__invoice_report",
                        "input": {"file": "data/invoices.csv"}}])
            tool_result(tool_id, "Total EUR 5,331.13 EUR")
    assistant([{"type": "text", "text": "Done (fake run). Total EUR 5,331.13 EUR; largest: Østfold Fisk AS."}])
    time.sleep(0.05)
    totals = {key: sum(c[key] for c in calls) for key in calls[0]}
    cost = round(totals["input_tokens"] * 2e-6 + totals["output_tokens"] * 10e-6
                 + totals["cache_read_input_tokens"] * 0.2e-6 + totals["cache_creation_input_tokens"] * 2.5e-6, 6)
    emit({"type": "result", "subtype": "success", "is_error": False, "session_id": session,
          "num_turns": turn, "duration_ms": 1200 + 400 * turn, "duration_api_ms": 1000 + 350 * turn,
          "total_cost_usd": cost, "result": "Done (fake run). Total EUR 5,331.13 EUR; largest: Østfold Fisk AS.",
          "stop_reason": "end_turn", "terminal_reason": "completed", "usage": totals,
          "modelUsage": {model: {"inputTokens": totals["input_tokens"], "outputTokens": totals["output_tokens"],
                                 "cacheReadInputTokens": totals["cache_read_input_tokens"],
                                 "cacheCreationInputTokens": totals["cache_creation_input_tokens"],
                                 "webSearchRequests": 0, "costUSD": cost, "contextWindow": 1000000,
                                 "maxOutputTokens": 64000}},
          "permission_denials": []})
    return 0


if __name__ == "__main__":
    sys.exit(main())
