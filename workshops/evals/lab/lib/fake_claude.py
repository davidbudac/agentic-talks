#!/usr/bin/env python3
"""A stand-in for `claude` that calls nothing: for the self-test and dry rehearsals.

    CLAUDE_BIN=lib/fake_claude.py ./lab1.sh --yes

Adapted for the Java lab from examples/series/run/lib/fake_claude.py. It emits
synthetic stream-json (or, with --output-format json, a single result object)
shaped like Claude Code 2.1.x output: an init event, assistant events with
per-call usage, user tool results, and a result event with total_cost_usd,
num_turns, duration_ms, usage and modelUsage. Every number is fake.

  claude --version / claude auth status   answered locally (FAKE_LOGGED_OUT=1: signed out)
  judge prompts (a "# Rubric" prompt)     a JSON score object as the result text
  task prompts                            a plausible session; copies a reference solution in
                                          when a FAKE_OVERLAY_MAP keyword matches the prompt

  FAKE_OVERLAY_MAP="kw=DIR;kw2=DIR2"  copy DIR over the cwd when the prompt contains kw
  FAKE_PASS_RATE=0.7                  skip the overlay (so the run fails) ~30% of the time,
                                      deterministically per prompt, model, CLAUDE.md and round
  FAKE_FAIL=1                         exit 1 without a result event (a harness error)
"""
import hashlib
import json
import os
import random
import shutil
import sys
import time
import uuid
from pathlib import Path

PRICES = {"haiku": (1.0, 5.0), "sonnet": (2.0, 10.0), "opus": (4.0, 20.0)}


def arg_value(args, name, default=None):
    if name in args:
        index = args.index(name)
        if index + 1 < len(args):
            return args[index + 1]
    return default


def emit(event):
    sys.stdout.write(json.dumps(event, ensure_ascii=False) + "\n")


def usage(inp, read, write, out):
    return {"input_tokens": inp, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": write, "output_tokens": out}


def price(model, u):
    p_in, p_out = next((v for k, v in PRICES.items() if k in model), PRICES["sonnet"])
    return round((u["input_tokens"] * p_in + u["output_tokens"] * p_out
                  + u["cache_read_input_tokens"] * p_in * 0.1
                  + u["cache_creation_input_tokens"] * p_in * 1.25) / 1e6, 6)


def result_event(session, model, calls, text, turns):
    totals = {key: sum(c[key] for c in calls) for key in calls[0]} if calls else usage(0, 0, 0, 0)
    cost = price(model, totals)
    return {"type": "result", "subtype": "success", "is_error": False, "session_id": session,
            "num_turns": turns, "duration_ms": 900 + 2100 * turns, "duration_api_ms": 800 + 1800 * turns,
            "total_cost_usd": cost, "result": text, "stop_reason": "end_turn", "terminal_reason": "completed",
            "usage": totals,
            "modelUsage": {model: {"inputTokens": totals["input_tokens"], "outputTokens": totals["output_tokens"],
                                   "cacheReadInputTokens": totals["cache_read_input_tokens"],
                                   "cacheCreationInputTokens": totals["cache_creation_input_tokens"],
                                   "webSearchRequests": 0, "costUSD": cost, "contextWindow": 1000000,
                                   "maxOutputTokens": 64000}},
            "permission_denials": []}


def judge(prompt, model, session, fmt):
    message = prompt.split("# The commit message to grade", 1)[-1]
    seed = int(hashlib.sha256((message + model).encode()).hexdigest(), 16)
    rng = random.Random(seed)
    base = 2 + (len(message) % 3)
    scores = {k: max(1, min(5, base + rng.choice((-1, 0, 0, 1)))) for k in ("accuracy", "why", "scope", "format")}
    scores["overall"] = max(1, min(5, round(sum(scores.values()) / 4)))
    scores["reason"] = "Fake judge: deterministic scores from a hash of the message."
    text = "```json\n" + json.dumps(scores) + "\n```"
    calls = [usage(1800, 0, 0, 90)]
    result = result_event(session, model, calls, text, 1)
    if fmt == "json":
        print(json.dumps(result))
    else:
        emit({"type": "system", "subtype": "init", "session_id": session, "model": model, "tools": []})
        emit({"type": "assistant", "session_id": session, "parent_tool_use_id": None,
              "message": {"id": "msg_judge", "model": model, "role": "assistant",
                          "content": [{"type": "text", "text": text}], "usage": calls[0]}})
        emit(result)
    return 0


def overlay(prompt, model, claude_md_len):
    targets = []
    for pair in filter(None, os.environ.get("FAKE_OVERLAY_MAP", "").split(";")):
        keyword, _, directory = pair.partition("=")
        if keyword and keyword in prompt:
            targets.append(directory)
    rate = float(os.environ.get("FAKE_PASS_RATE", "1.0"))
    key = f"{prompt}|{model}|{claude_md_len}|{os.environ.get('LAB_ROUND', '1')}"
    roll = random.Random(int(hashlib.sha256(key.encode()).hexdigest(), 16)).random()
    if roll >= rate:
        return []
    changed = []
    for directory in targets:
        if Path(directory).is_dir():
            shutil.copytree(directory, Path.cwd(), dirs_exist_ok=True)
            changed += [str(Path.cwd() / p.relative_to(directory)) for p in Path(directory).rglob("*.java")]
    return changed


def main():
    args = sys.argv[1:]
    if "--version" in args:
        print("0.0.0 (fake claude)")
        return 0
    if args[:2] == ["auth", "status"]:
        logged_in = not os.environ.get("FAKE_LOGGED_OUT")
        print(json.dumps({"loggedIn": logged_in, "authMethod": "claude.ai" if logged_in else "none",
                          "apiProvider": "firstParty", "subscriptionType": "pro" if logged_in else None}))
        return 0 if logged_in else 1
    if os.environ.get("FAKE_FAIL"):
        print("fake failure", file=sys.stderr)
        return 1
    prompt = arg_value(args, "-p", "") or sys.stdin.read()
    model = arg_value(args, "--model", "claude-sonnet-5")
    fmt = arg_value(args, "--output-format", "text")
    session = str(uuid.uuid4())
    if "# Rubric" in prompt:
        return judge(prompt, model, session, fmt)

    cwd = Path.cwd()
    claude_md = cwd / "CLAUDE.md"
    md_tokens = len(claude_md.read_text(encoding="utf-8")) // 4 if claude_md.is_file() else 0
    bloated = md_tokens > 1500
    rng = random.Random(int(hashlib.sha256(f"{prompt}{model}{md_tokens}".encode()).hexdigest(), 16))
    changed = overlay(prompt, model, md_tokens)
    java = sorted(p for p in cwd.rglob("*.java") if ".git" not in p.parts and "target" not in p.parts)
    reads = java[:3] + java[3:4]
    emit({"type": "system", "subtype": "init", "session_id": session, "model": model, "cwd": str(cwd),
          "tools": ["Bash", "Read", "Edit", "Write", "Glob", "Grep"], "mcp_servers": []})
    calls, context, turn = [], 24000 + md_tokens, 0

    def assistant(content, grow=0):
        nonlocal context, turn
        turn += 1
        u = usage(4, context if turn > 1 else 0, context if turn == 1 else grow + 60, rng.randint(90, 700))
        emit({"type": "assistant", "session_id": session, "parent_tool_use_id": None,
              "message": {"id": f"msg_{uuid.uuid4().hex[:12]}", "model": model, "role": "assistant",
                          "content": content, "usage": u}})
        calls.append(u)
        context += grow + 60

    def tool_result(tool_id, text, error=False):
        emit({"type": "user", "session_id": session, "parent_tool_use_id": None,
              "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_id,
                                                       "content": text, "is_error": error}]}})

    plan = ("Plan: read the relevant classes, write a failing test for the reported case, fix the code, "
            "then run ./mvnw -q test and make sure the whole suite passes before finishing.")
    assistant([{"type": "text", "text": plan}])
    for index, path in enumerate(reads + reads[:1]):  # the last one is a re-read
        tool_id = f"toolu_read{index}"
        text = path.read_text(encoding="utf-8")
        assistant([{"type": "tool_use", "id": tool_id, "name": "Read", "input": {"file_path": str(path)}}],
                  grow=len(text) // 4)
        tool_result(tool_id, text)
    if bloated:
        assistant([{"type": "text", "text": plan.replace("Plan:", "So the plan is:")}])
        for attempt in range(2):  # the same failing command twice: a blind retry
            tool_id = f"toolu_fail{attempt}"
            assistant([{"type": "tool_use", "id": tool_id, "name": "Bash",
                        "input": {"command": "mvn -q test", "description": "Run tests"}}])
            tool_result(tool_id, "Permission to use Bash with command mvn -q test has been denied.", error=True)
    for index, path in enumerate(changed[:2] or [str(p) for p in java[:1]]):
        tool_id = f"toolu_edit{index}"
        assistant([{"type": "tool_use", "id": tool_id, "name": "Edit",
                    "input": {"file_path": path, "old_string": "x", "new_string": "y"}}])
        tool_result(tool_id, f"The file {path} has been updated.")
    tool_id = "toolu_test"
    assistant([{"type": "tool_use", "id": tool_id, "name": "Bash",
                "input": {"command": "./mvnw -q test", "description": "Run the test suite"}}])
    tool_result(tool_id, "" if changed else "[ERROR] Tests run: 58, Failures: 1")
    final = "Done (fake run)." if changed else "I could not make the change pass (fake run)."
    assistant([{"type": "text", "text": final}])
    time.sleep(0.02)
    result = result_event(session, model, calls, final, turn)
    if fmt == "json":
        print(json.dumps(result))
    else:
        emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
