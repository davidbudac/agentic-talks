# Demo kit for talks 03–07

One small repository that every talk from 03 to 07 uses, and one script per
talk that measures it with Claude Code in headless mode. Run them once before
presenting. The measured numbers replace the "illustrative" values and fill
the empty fallback slides. `run/summarise.py` then puts each number next to the
slide it belongs to.

The example is the invoice fixture from talks 02–03 (`examples/v2/invoice/`),
grown into `invoice-app/`, so the audience sees the same `gross()` and
`export_invoices()` code in every talk.

Nothing in this folder calls Claude until you run a `talkNN.sh` without
`--dry-run` and confirm the cost prompt. `run/selftest.sh` checks the whole kit
with a fake `claude` and costs nothing.

## Prerequisites

- Claude Code, signed in (`claude auth status`). This was built against
  **v2.1.281**. A Pro or Max login works: running `claude -p` as yourself counts
  as ordinary Claude Code use (talk 04, slide 38). With a subscription the
  dollar figures are Claude Code's estimates, and the runs use up your plan
  limits instead.
- `python3` (3.10 or newer, standard library only) and `git`.
- For talk 07: `uv`, so that `uvx --from smevals==0.2.0 smevals` works, or
  `smevals` on your PATH. Either one downloads smevals from PyPI the first time.
- Optional: `asciinema` and `agg` (`brew install asciinema agg`) for the
  recordings. Without them, `record.sh` uses macOS `script -r` and converts
  the recording to `.cast`.

## Quick start

```sh
cd examples/series
run/selftest.sh                 # free: tests, checkers, dry runs, a fake end-to-end run
run/talk05.sh --dry-run         # print the exact claude commands, spend nothing
run/talk05.sh                   # print the plan and cost estimate, ask, then run
python3 run/summarise.py        # write results/SUMMARY.md: every number next to its slide
```

Every runner:
- copies `invoice-app` (or the talk 03 start state) into a new temp dir and
  runs `git init` there, so each run starts from a clean copy;
- runs `claude -p … --output-format stream-json --verbose` with `--max-turns`
  and a `--max-budget-usd` cap on each session;
- saves the raw transcript, a `command.sh` holding the exact command, the diff,
  the test output and a `summary.json` plus `summary.md` to
  `results/<talk>/<UTC timestamp>/`, then prints a short summary;
- prints the plan and a cost estimate first and asks before it spends anything.
  `--yes` skips the question and `--dry-run` only prints the commands.

Settings, all of them environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `MODEL` | `claude-sonnet-5` | The model the decks price (talk 05, slides 4 and 8; talk 07, slide 9) |
| `MAX_TURNS` | 15 to 30, set per runner | Passed as `--max-turns` |
| `MAX_BUDGET_USD` | 1.00 (0.60 for talk 07) | Passed as `--max-budget-usd`: a hard stop for each session |
| `ISOLATE` | `1` | Adds `--setting-sources project,local --strict-mcp-config --no-session-persistence`. Your user CLAUDE.md, user settings, plugins and MCP servers stay out, so runs compare cleanly. Set it to `0` to measure your own setup, or if sign-in fails |
| `CLAUDE_BIN` | `claude` | Point it at `run/lib/fake_claude.py` for a free smoke test |
| `RESULTS_ROOT` | `examples/series/results` | Where results go |
| `KEEP_WORKDIRS` | `0` | `1` keeps the temp repo copies |
| `VERBOSE` | `0` | `1` prints the full command during real runs |

Permissions: every session runs with `--permission-mode dontAsk` and an allow
list: file tools, `python3`, and read-only `git`, `ls`, `cat` and `grep`.
`Agent`, `WebFetch` and `WebSearch` are denied unless a runner needs them.
Anything that would need a prompt is denied, so no session can install
packages, fetch URLs or push.

## The runners

The costs below assume `claude-sonnet-5` and small tasks on this repo. They
are estimates. The runner prints its own estimate before it starts.

| Runner | What it measures | Sessions | Expected cost | Time |
|---|---|---|---|---|
| `talk03.sh` | The same task (add `export_invoices()` to `talk03/start/`) run `RUNS`×2 times, under setups A and B. Hidden acceptance tests decide which runs are accepted. Reports accepted runs, model and tool cost, cost per accepted task, turns and diff size. `VARIANT=models` (default) compares `MODEL_A=claude-haiku-4-5` with `MODEL_B=claude-sonnet-5`. `VARIANT=contract` runs one model with and without the acceptance contract | 10 (`RUNS=5`) | $0.35–1.75 | 10–30 min |
| `talk04.sh` | (b) The same prompt twice, back to back, in the same directory: `cache_creation` against `cache_read` on the first API call and for the whole session. `CACHE_WAIT_S=360` adds a third run after the wait. (a) A codebase survey done inline (Agent tool denied) and fanned out to four Explore subagents: the lead's context at the end, the tool output that entered the lead, total tokens across all agents, wall-clock time, cost, and one `Done (N tool uses · Xk tokens · Ys)` line per subagent | 4 | $0.35–1.75 | 5–10 min, plus any wait |
| `talk05.sh` | `/context` with each CLAUDE.md, which takes no model turn. Then backlog 004 with the bloated and the lean CLAUDE.md, `RUNS` times each: turns, total tokens, CLAUDE.md tokens per turn and per session, cost, and the outcome from hidden tests. Also the overhead table for slide 17 and a per-session bill for slide 6 | 2 (+2 `/context`) | $0.10–0.50 | 3–8 min |
| `talk06.sh` | Two agents working in parallel in two git worktrees on backlog 001 and 002, which both add a column to `export.py`. It commits both branches, merges them and records the conflict. `PAIR=clean` runs 003 and 005 as the control. Then MCP against CLI: one question answered through `tools/invoice_mcp.py`, loaded with `--mcp-config`, and through `python3 -m invoicing` using Bash only. Records the `/context` tokens, the task's tokens and cost, wall-clock time, and whether the answer was right | 4 (+2 `/context`) | $0.20–1.00 | 3–8 min |
| `talk07.sh` | smevals over 6 tasks × 2 variants × `RUNS`=3. The default compares lean and bloated CLAUDE.md. `VARIANT=models` compares `MODEL_A` and `MODEL_B`. Reports pass rate, pass@k, pass^k, cost per pass, waste counted in the traces (re-reads, repeated calls, blind retries) and one example trace | 36 | $1.80–9.00 | 40–110 min |
| `record.sh SLOT` | Records a terminal session for a fallback slide (see below). It never calls Claude, except for the talk runner you choose to record | – | – | – |
| `summarise.py` | Reads every `results/talk*/*/summary.json` and writes `results/SUMMARY.md` | – | – | – |

A cheaper talk 07: `TASKS="fix-date-parser fixtures-bom jpy-rounding" RUNS=2 run/talk07.sh`,
which is 12 sessions and costs about $0.60–3.00.

Every run of all five with the defaults: about 56 model sessions, **$2.80–14.00**,
and roughly 1–3 hours, most of it talk 07.

### What the CLI does and does not break down per subagent (talk 04)

- `result.total_cost_usd` and `result.modelUsage` cover **every** model call,
  subagents included, but they are totals **per model**, not per agent.
  `result.usage` covers the main loop only.
- Per subagent, the Agent tool's structured result (`tool_use_result`, an
  `AgentOutput`) gives `totalToolUseCount`, `totalDurationMs`, `toolStats`,
  and `totalTokens` plus `usage`. The last two come **from the subagent's final
  API request only**. That makes them the size of its context window at the
  end, not a sum over its turns. `analyze.py` reports that value as the
  subagent's tokens, the same number Claude Code's `Done (… tokens …)` line
  shows.
- With `--output-format stream-json`, a subagent's `assistant` events carry
  `parent_tool_use_id` and their own `message.usage`, so the runner can
  rebuild each subagent's calls and its first-call cache read and write
  (slide 34). `--forward-subagent-text` adds the subagents' text and thinking.
- There is no per-agent dollar figure. To estimate one, apply list prices to
  a subagent's summed `usage_seen`.
- "Tokens that entered the lead from file reads" is estimated at about
  4 characters per token of tool-result text. The lead's context size itself
  (`lead_context_final`) is measured: input plus cache read plus cache write
  on the lead's last API call.

### Per-session breakdown for talk 05, slide 6

The transcript does contain enough detail for a real per-turn trace. Each API
call has `input_tokens`, `cache_read_input_tokens`,
`cache_creation_input_tokens` and `output_tokens`, and each tool result has its
text. It does **not** give a billed amount per line item. `analyze.py
bill_attribution` splits the session as follows:

- the fixed prefix is the first call's full input;
- each tool result enters the next call, is written to the cache once (1.25×)
  and read on every later call (0.1×);
- output counts 5×.

File reads and re-reads are counted exactly, from the `Read` calls. Their token
sizes are estimated at about 4 characters per token. The session totals are
Claude Code's own numbers. Present the split as an estimate built from a real
session.

## Where results go

```
results/
├── SUMMARY.md                        # run/summarise.py: every number next to its slide
├── talk03/<ts>/{plan.json, runs/A-1/…, summary.json, summary.md}
├── talk04/<ts>/{cache-1, cache-2, survey-inline, survey-subagents}/…
├── talk05/<ts>/{context-bloated, context-lean, task-bloated-1, task-lean-1}/…
├── talk06/<ts>/{agent-001-…, agent-002-…, merge.json, merge-conflict.diff, mcp-*, cli-*}/…
├── talk07/<ts>/{runs/ (smevals layout), grades.json, smevals-report.md, summary.*}
└── recordings/<slot>-<ts>.{cast,typescript}
```

Each session folder holds `transcript.jsonl` (the raw stream-json),
`command.sh`, `meta.json` (wall-clock time and exit code), and, where
relevant, `diff.patch`, `tests.txt` and `check.json`. Transcripts contain full
file contents, so read them before you commit a results folder.

Inspect any transcript by hand:
`python3 run/lib/analyze.py session|trace|context <transcript.jsonl>`.

## Slide mapping

The mapping comes from grepping the decks for "illustrative", "fill in",
"rehearsal", "your number" and the fallback slides. Talk 03 is taken from
`agentic-engineering-v2.html`, whose content is written in
`scripts/build_first_three_v2.py`. The other decks are
`subagents-prompt-caching.html`, `cost-and-context.html`,
`orchestrating-agents.html`, `measuring-what-works.html` and
`claude-design.html`. **Kind** says how complete the kit's answer is. *auto*
means a runner produces the value. *partial* means the runner gives the
numbers but a person still edits the visual or adds something unmeasured.
*manual* means it needs a recording or data the kit cannot produce.
`python3 run/summarise.py --mapping` prints this table.

| Talk | Slide | Title | Illustrative now | Runner | Field(s) | Kind |
|---|---|---|---|---|---|---|
| 03 | 22 | Measure the cost per accepted task | A $6, 6/10 accepted, $1/accepted, 40 min review; B $10, 10/10, $1, 15 min | `talk03.sh` | `setups.{A,B}.{cost_usd,accepted,runs,cost_per_accepted_usd}` | partial |
| 03 | 24 | Problem 6 · one agent carries too much | animation: 80k tokens in the worker, 200 back | `talk04.sh` | `survey.inline.lead_context_final, survey.subagents.subagent_return_tokens_est` | partial |
| 04 | 7 | A subagent works in its own window | animation token counts | `talk04.sh` | `survey.subagents.subagents[*]` | partial |
| 04 | 8 | Where fifteen file reads end up | 15 reads, 45,000 tokens stay in the lead vs 200 reach it | `talk04.sh` | `survey.inline.{file_reads,tokens_into_lead_est}, survey.subagents.subagent_return_tokens_est` | auto |
| 04 | 11 | Many turns collapse into one block | 30 turns, 41,700 tokens -> ~300 tokens | `talk04.sh` | `survey.subagents.subagents[max].{total_tool_use_count,total_tokens_final_request,returned_tokens_est}` | auto |
| 04 | 12, 14 | Fan out to cut the waiting / 15x tokens | diagram; 1x / 4x / 15x (Anthropic research system) | `talk04.sh` | `survey.{inline,subagents}.{duration_s,total_tokens,cost_usd}` | partial |
| 04 | 17 | Watch subagents run in Claude Code | Done (9 tool uses · 32.1k tokens · 48s) x3, 90k never reach the session | `talk04.sh` | `survey.subagents.subagents[*].{total_tool_use_count,total_tokens_final_request,total_duration_ms}` | auto |
| 04 | 31 | Read the usage fields to confirm a hit | call 1 writes 48,210; call 2 reads 48,210 | `talk04.sh` | `cache[0].first_call.cache_creation_tokens, cache[1].first_call.cache_read_tokens` | auto |
| 04 | 32 | Caching you only see on the usage screen | docs example: $0.55, 91% of input from cache | `talk04.sh` | `cache[*].cache_hit_pct` | partial |
| 04 | 34 | Subagents with the same prefix share a cache | 20k prefix: 80k without caching vs 31k with | `talk04.sh` | `survey.subagents.subagents[*].first_call_cache_{creation,read}` | partial |
| 05 | 6 | Where one session's tokens go | cached prefix 7 · file reads x12 42 · re-reads x4 20 · thinking + answer 31 | `talk05.sh` | `bill.{shares_pct,file_reads,re_reads}` | auto |
| 05 | 17 | The overhead you pay before you type | system prompt 4,200 · memory 960 · MCP names 120 · skills 450 · CLAUDE.md 2,120 (docs) | `talk05.sh` | `overhead (from /context context_usage.categories)` | auto |
| 05 | 24 | Same task, two CLAUDE.md files (live) | turns / total tokens / outcome counters | `talk05.sh` | `variants.{bloated,lean}` | auto |
| 05 | 25 | Fallback: the rehearsal run | 8 cells 'fill in' | `talk05.sh` | `variants.{bloated,lean}.{turns,total_tokens,claude_md_tokens_per_turn,outcome}` | auto |
| 06 | 5 | Herdr: every agent in one terminal | pane list is a mock-up | `manual` | `-` | manual |
| 06 | 9 | Fallback: the Symphony run | 'Screen recording goes here' | `record.sh 06-s9` | `-` | manual |
| 06 | 13 | Failure mode 2: merge conflicts between agents | diagram: auth.ts edited in two worktrees | `talk06.sh` | `merge.{first_merge,second_merge,conflicted_files}` | auto |
| 06 | 14 | Failure mode 3: review bottlenecks | 12 PRs opened a day, 4 reviewed -> 40 waiting by Friday | `manual` | `-` | manual |
| 06 | 23 | Fallback: the skill demo | 'Screen recording goes here' | `record.sh 06-s23` | `-` | manual |
| 06 | 30 | Measure one tool both ways | 8 cells 'your number' | `talk06.sh` | `mcp_vs_cli.{mcp,cli}.{context_total_tokens,total_tokens,duration_s,correct}` | auto |
| 07 | 3 | Why vibes don't scale | A 6/10, B 9/10 | `talk07.sh` | `variants.*.{passes,runs}` | partial |
| 07 | 4 | Start with a task-completion suite | 6 tasks from last month, 4/6 pass | `talk07.sh` | `cells[*].{task,passes,k}` | auto |
| 07 | 12-13 | Live: score two variants / Fallback: the recorded eval run | task 1-4 x variant A/B '…' | `talk07.sh + record.sh 07-s13` | `cells, variants` | auto |
| 07 | 14 | Evals tell you which model to use | A $0.10/run, 3/10 accepted, $0.33/accepted; B $0.25/run, 9/10, $0.28 | `talk07.sh VARIANT=models` | `variants.*.{pass_rate,cost_per_pass_usd}` | partial |
| 07 | 15 | A trace is the whole transcript | t1-t6 auth.ts session | `talk07.sh` | `example_trace.steps` | auto |
| 07 | 16 | Read traces for wasted turns | 3 of 6 turns repeat earlier work | `talk07.sh` | `waste.{re-read,repeat,blind retry,turns}` | auto |
| 07 | 18 | Anatomy of an agent trace | Elastic example: 8,214 input, 1,102 output, 412 ms / 96 ms tools | `manual` | `-` | manual |
| 08 | 18 | Fallback: the same run, frame by frame | five drawn stand-in frames | `manual` | `-` | manual |

Talk 07 was cut to 21 slides on 2026-09-24. Its local-model and /voice
fallbacks (old slides 28 and 33) left the deck with the routing and habits
parts: see `workshops/evals/` and the record.sh slots `ws-lab6-local` and
`habits-voice` below.

### What the kit cannot measure, and how to capture it by hand

- **03 s22 review time**: time your own review of each run's `diff.patch`. The
  runner reports diff size as a proxy.
- **03 s24, 04 s7 animations**: the numbers come from `talk04.sh`. Re-render
  the Remotion compositions (`remotion/`) yourself, or say on the slide that
  the counts come from the kit's run.
- **04 s32 `/usage` screen**: it is interactive only. Open `claude` in the
  talk 04 repo copy (`KEEP_WORKDIRS=1`), run `/usage`, and take a screenshot.
- **06 s5 Herdr, 06 s9 Symphony**: these are third-party tools (Symphony runs
  Codex from Linear). Use `run/record.sh 06-s9` for the terminal, and screen-
  record the board with Cmd+Shift+5.
- **06 s14 review backlog**: this needs a team's PR history, for example
  `gh pr list --state all --json createdAt,mergedAt`. One run cannot produce it.
- **06 s23 skill demo**: `run/record.sh 06-s23` opens a fresh repo copy with
  `demo-skill/backlog-issue/SKILL.md` ready to paste into
  `.claude/skills/backlog-issue/`. Run `claude` there and ask "do 003".
- **07 s18 OTel spans**: set `CLAUDE_CODE_ENABLE_TELEMETRY=1`,
  `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` and an OTLP exporter, with a
  collector running. For per-call tokens without a collector, use
  `analyze.py trace`.
- **Local model, evals workshop Lab 6** (was talk 07 s28; the slides are now
  in `workshops/evals/talk07-routing-archive.html`): `run/record.sh
  ws-lab6-local`, then run Ollama yourself. The kit installs no models.
- **/voice, talk 07 habits archive** (was s33; now in
  `workshops/evals/talk07-habits-archive.html`, no longer presented): a
  terminal recording has no audio. Use a screen recording with the microphone
  on (`run/record.sh habits-voice` opens `claude` in a repo copy).
- **08 s18 Claude Design**: it is a web app. Screen-record or screenshot the
  five steps. `run/record.sh 08-s18` prints the steps.

### Recordings

```sh
run/record.sh --list                      # slots: 05-s25 06-s9 06-s23 07-s13 ws-lab6-local habits-voice 08-s18
run/record.sh 06-s23                      # asciinema if installed, else `script -r` + .cast conversion
agg results/recordings/06-s23-….cast out.gif --font-size 20
ffmpeg -i out.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" out.mp4
```

## The shared repo: `invoice-app/`

Eight small modules, standard library only, with 50 deterministic tests
(`cd invoice-app && python3 -m unittest`):

| Module | Area |
|---|---|
| `money.py` | Decimal parsing, currency exponents, ROUND_HALF_UP, allocation |
| `invoice.py` | `gross()` from talk 02, multi-line totals |
| `customers.py` | Unicode customer names: NFC, accent-insensitive sort and match, safe truncation |
| `dates.py` | ISO and dotted dates, payment terms |
| `fixtures.py` | CSV loading and validation |
| `export.py` | The talk 03 `export_invoices()` contract |
| `report.py` | Totals per customer and currency |
| `cli.py` | `python3 -m invoicing report / export / due` |
| `tools/invoice_mcp.py` | A stdio MCP server (JSON-RPC over stdin/stdout) exposing the same three commands |

The repo has seeded, realistic defects that the backlog and the eval tasks
point at. Dotted dates are parsed month-first when ambiguous. JPY is missing.
The legacy CSV has a BOM that the loader rejects. The report sorts by raw code
point. Its tests pass anyway, because none of them cover those cases. That is
the point of the hidden tests.

`backlog/` holds six independent issues for talk 06. **001 and 002 both add a
sixth column to `export.py`**. That pair is the deliberate merge conflict.
003 and 005 touch different files and serve as the control.

`claude-md/` sits outside the app, so an agent never sees the other variant.
`lean.md` (about 260 tokens) holds constraints, commands and conventions,
following talk 05 slide 18. `bloated.md` (about 3,500 tokens) has the same
rules plus what slide 19 says to leave out: a history section, an architecture
essay, a directory listing (with a stale entry, `legacy_pdf.py`, that no longer
exists), a module-by-module restatement of the code, one-off session notes, a
glossary and a FAQ. `run/setup-repo.sh DEST --claude-md lean|bloated|none`
makes a fresh copy with git history, which also suits two-pane live demos.

`talk03/` holds the talk 03 trial. `start/` is the state after talk 02: the
tax fix is in and the export does not exist yet. `hidden/test_acceptance.py`
holds the acceptance contract as tests. `check.py` accepts an attempt only when
the hidden tests and its own tests both pass. `prompts/` has the bare prompt
and the prompt with the contract.

`eval/` is an smevals eval: `eval.yaml`, six `tasks/*.yaml`, `configs/`
(lean, bloated, default), `graders/default.yaml`, the `checkers/hidden-tests`
checker, one hidden test module per task in `hidden/`, and the runner
`run-claude`. `solutions/` holds a reference fix for every task. Use it to
check the checkers (`run/selftest.sh` does this), not to feed the agent.

## CLI facts this kit relies on (checked 24 September 2026, Claude Code 2.1.281)

- `claude --help` lists `-p/--print`, `--output-format text|json|stream-json`,
  `--model`, `--max-budget-usd` (print mode only), `--permission-mode`
  (`acceptEdits|auto|bypassPermissions|manual|dontAsk|plan`),
  `--allowedTools`/`--disallowedTools` (comma or space separated),
  `--append-system-prompt`, `--mcp-config`, `--strict-mcp-config`,
  `--setting-sources`, `--no-session-persistence`, `--forward-subagent-text`
  and `--bare`. There is no separate `claude -p --help`.
- `--max-turns` is **not listed in `--help`** on 2.1.281. It is documented in
  the CLI reference ("Limit the number of agentic turns (print mode only).
  Exits with an error when the limit is reached"), and the flag string is in
  the binary. The runners treat the non-zero exit as data.
- `stream-json` with `-p` needs `--verbose` (headless docs).
- `--bare` would isolate runs more tightly, but it accepts only
  `ANTHROPIC_API_KEY` or an `apiKeyHelper` and never reads an OAuth login. The
  kit therefore uses `--setting-sources project,local --strict-mcp-config`,
  which keeps a subscription login working.
- The result event (Agent SDK `SDKResultMessage`) has `subtype`, `is_error`,
  `num_turns`, `duration_ms`, `duration_api_ms`, `total_cost_usd`, `usage`
  (main loop only: `input_tokens`, `output_tokens`,
  `cache_read_input_tokens`, `cache_creation_input_tokens`), `modelUsage` (per
  model, subagents included: `inputTokens`, `outputTokens`,
  `cacheReadInputTokens`, `cacheCreationInputTokens`, `costUSD`, …),
  `permission_denials` and `terminal_reason`. Both cost figures are
  client-side estimates.
- If you send `/context` as the prompt, the reply carries `context_usage`
  (`categories`, `memory_files`, `mcp_tools`, `skills`, `agents`). talk05 and
  talk06 read the overhead and the CLAUDE.md tokens from it. If a version
  lacks it, talk05 falls back to estimating from the file size (chars/4) and
  says so in `claude_md_tokens_source`.
- smevals 0.2.0 on PyPI has `run -m -c -t -g --runs-dir`, `grade`,
  `report --json/--by-task` and `serve`. The `-n` top-up flag shown on talk 07
  slide 9 exists on smevals' main branch (commit 0c28dc6) but **not in the
  0.2.0 release**, so `talk07.sh` calls `smevals run` once per round.

Sources: `claude --help` on this machine; the CLI reference
(code.claude.com/docs/en/cli-reference); headless mode
(code.claude.com/docs/en/headless); Agent SDK TypeScript reference (result,
assistant and user message types, `AgentOutput`, `SDKContextUsage`); the
smevals README and `uvx --from smevals==0.2.0 smevals run --help`.
