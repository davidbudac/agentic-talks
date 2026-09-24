# Evals workshop: hands-on lab kit (Java)

A half-day, hands-on companion to talk 07 (`measuring-what-works.html`): 20
Java developers in about 10 pairs measure a coding agent on a small Java/Maven
repository with their own Claude Code subscriptions, then pool the results on a
shared board. It reuses the design of the talk 03–07 demo kit
(`examples/series/`: the invoice app, the smevals layout with hidden tests,
lean vs bloated CLAUDE.md, the trace analysis), rewritten for Java.

> **Sample data is SYNTHETIC.** `sample-results/` was generated without calling
> any model, so labs 2–5 and the board work offline. It is not a measurement.
> The facilitator replaces it with `./record-facilitator-run.sh` during the dry run.

Nothing in this folder calls Claude until you run `lab1.sh`, `lab2.sh`,
`lab5.sh`, `lab6.sh`, `judge.sh` or `record-facilitator-run.sh` without
`--dry-run` and confirm the plan they print. `./selftest.sh` checks the whole
kit with a fake `claude` and costs nothing.

## Participant commands (quote these)

| Block | Time | Command | Model sessions (default) |
|---|---|---|---|
| 0 · Setup check | 15 min | `PAIR=your-team ./check-setup.sh` | 0 |
| 1 · Guess, then measure | 35 min | `./predict.sh lean` (or `bloated`), then `./lab1.sh` | 4 |
| 2 · Variance | 30 min | `./lab2.sh`, then `./export-results.sh --lab lab2 --latest` | 6 |
| 3 · Break the grader | 40 min | `./lab3.sh`, `./lab3.sh check`, `./lab3.sh answer` | 0 |
| 4 · Read the traces | 30 min | `./lab4.sh` (or `./trace-report.sh FILE...`) | 0 |
| 5 · Judge model | 30 min | fill in `lab5/my-scores.csv`, then `./lab5.sh` | 8 judge calls (tiny) |
| 6 · Route by the numbers | 35 min | `./lab6.sh` (`OPUS=1`, `LOCAL_MODEL=qwen3-coder ./lab6.sh --local` optional) | ~8 (6 Haiku + ~2 Sonnet) |
| 7 · Take it home | 20 min | read `take-home/GUIDE.md`, copy `take-home/template/eval/` | 0 |
| Board | any time | `./export-results.sh` (one JSON line per run, paste into the board) | 0 |

Every model-calling runner accepts `--dry-run` (print the plan and the exact
commands, spend nothing) and `--yes` (skip the confirmation). Labs 2, 4, 5 and
6 accept `--sample` to work on the synthetic set with no model calls.
`LITE=1` in front of any command halves the runs (table below).

**Splitting a pair across two laptops.** Both partners have a subscription, so
share the load: set the same pair name on both (`PAIR=your-team
./check-setup.sh` writes `.pair`), then run `ROLE=a` on one laptop and `ROLE=b`
on the other. Lab 1–2: `a` runs the lean CLAUDE.md, `b` the bloated one, at the
same time, so each lab also takes half the wall-clock time. Lab 6: `a` runs
Sonnet (reusing its lean runs), `b` runs Haiku. Run lab 5 on laptop `a`.

## Usage budget

Participants spend their own plan. The defaults keep one pair at **18 agent
sessions plus 8 one-turn judge calls for the whole workshop**, and at 7–11
agent sessions per laptop when the pair splits with `ROLE`.

Per session, from the list prices the decks use (Sonnet 5 $2/$10, Haiku 4.5
$1/$5, Opus 5.5 $4/$20 per million input/output tokens; cache reads 0.1×,
cache writes 1.25×) and small tasks on this repo (8–20 API calls over a
~25–35k-token cached prefix):

| Session kind | Tokens processed | ≈ of which cache reads | API-price estimate | Wall-clock |
|---|---|---|---|---|
| Sonnet 5 agent session | 0.25–0.6M | 90% | $0.15–0.45 | 2–5 min |
| Haiku 4.5 agent session | 0.25–0.7M | 90% | $0.05–0.20 | 1.5–4 min |
| Opus 5.5 agent session (optional) | 0.25–0.6M | 90% | $0.30–0.90 | 2.5–6 min |
| Judge call (no tools, 1 turn) | 2–5k | 0% | $0.005–0.02 | 5–20 s |

Per lab, for one pair on one laptop (`ROLE=both`):

| Lab | Default sessions | Tokens | API-price estimate | Model time | `LITE=1` |
|---|---|---|---|---|---|
| 0 Setup | 0 | 0 | $0 | 0 (Maven prefetch ~2 min) | 0 |
| 1 Guess, then measure | 4 Sonnet (2 tasks × 2 variants × 1) | 1.0–2.4M | $0.60–1.80 | 8–20 min | 2 (1 task) |
| 2 Variance | 6 Sonnet (1 task × 2 variants × 3) | 1.5–3.6M | $0.90–2.70 | 12–30 min | 4 (k = 2) |
| 3 Break the grader | 0 | 0 | $0 | Maven only, ~1 min per check | 0 |
| 4 Read the traces | 0 | 0 | $0 | seconds | 0 |
| 5 Judge model | 8 judge calls (Sonnet) | 0.02–0.04M | $0.04–0.16 | 1–3 min | 8 calls (Haiku) |
| 6 Route by the numbers | 6 Haiku + ~2 Sonnet top-ups (4 Sonnet runs reused from labs 1–2) | 2.0–5.4M | $0.60–2.10 | 13–34 min | 2 Haiku, 0 Sonnet |
| 7 Take it home | 0 | 0 | $0 | 0 | 0 |
| **Total** | **18 agent + 8 judge** | **4.5–11.4M** | **$2.10–6.80** | **34–87 min** | **8 agent + 8 judge; 2–5M; $1.0–3.2** |

With `ROLE` split: laptop `a` runs 7 Sonnet sessions + 8 judge calls (≈1.8–4.2M
tokens, $1.10–3.30); laptop `b` runs 5 Sonnet + 6 Haiku sessions (≈2.8–7.2M
tokens, $1.05–3.45). `REUSE=0 ./lab6.sh` adds 4 Sonnet sessions; `OPUS=1` adds
6 Opus sessions. The runners print their own estimate before they start.

**The Pro limit is not published.** Anthropic's help centre (checked
2026-09-24) says Pro has a session limit that resets every five hours and a
weekly limit, that usage is shared between claude.ai and Claude Code, and that
the number of messages "will vary based on message length, … the length of
your current conversation, and the model or feature you use"; Max 5x and 20x
have "five times" and "20 times the Pro plan's per-session usage allowance".
No token or prompt count is given. Figures such as "10–40 Claude Code prompts
per 5 hours" circulate in third-party write-ups, attributed to an older
version of the help article; we could not verify them on a primary source, so
the design does not rely on them. A headless session here is one prompt but
8–20 model calls, so we count it as several prompts. The conservative design:

- at most ~11 agent sessions per subscription (split with `ROLE`), most of
  them small, one Haiku-heavy lab, and judge calls with no tools and a short
  system prompt;
- the room pools results (10 pairs × 3 runs gives the statistics), so no pair
  needs many runs;
- `LITE=1` roughly halves everything, and `--sample` keeps every analysis lab
  working if a partner hits a limit;
- the facilitator calibrates once: run `./record-facilitator-run.sh` on a
  **Pro** account and read `/usage` in an interactive `claude` session before
  and after. If it uses more than about half of a 5-hour window, announce
  `LITE=1` for the day.

Sources: support.claude.com/en/articles/8325606-what-is-the-pro-plan,
/11049741-what-is-the-max-plan, /11145838-use-claude-code-with-your-pro-or-max-plan.

## Facilitator checklist

1. A week before: send `prework.md`. Ask everyone to run `./check-setup.sh`.
2. Replace the four stand-in "human" commit messages in `lab5/samples/` with
   real hand-written ones for the same diff (e.g. ask two colleagues), and
   update `lab5/authors.json`. Until then lab 5's self-preference check
   compares Claude with Claude (see the note in `authors.json`).
3. Dry run: `./selftest.sh` (free), then `./record-facilitator-run.sh`
   (≈ one pair's budget). It replaces `sample-results/` with real data;
   review and commit it. Check `/usage` on a Pro account (above).
4. On the day: the board ingests the lines from `./export-results.sh`
   (schema: `RESULTS-SCHEMA.md`). Filter out `SYNTH-*` pairs.
5. Suggested rhythm: while pairs discuss lab 1's result, they can start
   `./lab2.sh --yes`; while they hand-score lab 5, laptop `b` can start
   `ROLE=b ./lab6.sh --yes`.

## Blocks in detail

**0 · Setup check.** `./check-setup.sh` prints PASS/FAIL for: JDK 21+, the
Maven wrapper, a dependency prefetch (`./mvnw -q dependency:go-offline`) and an
offline test run (`./mvnw -q -o test`) so venue Wi-Fi does not matter later,
python3 3.10+, uv and smevals (`uvx --from smevals==0.2.0 smevals`), `claude
--version`, sign-in via `claude auth status` (reads the stored login, exit 0
when signed in, no model request; verified on 2.1.281), and git.

**1 · Guess, then measure.** Two CLAUDE.md files for the same repo
(`claude-md/`): `lean.md` (~270 tokens: rules, commands, conventions) and
`bloated.md` (~3,800 tokens: the same rules inside an architecture essay, a
package listing with stale entries, stale session notes, conventions stated
twice and slightly contradicting, a glossary and a FAQ). Predict first, then
run 2 tasks × 2 variants × 1 run. The summary compares turns, tokens, cost per
pass and tells you whether your prediction held, on n = 1.

**2 · Variance.** One task (`report-sort-accents`), 3 runs per variant.
Reports pass@k (any run passed), pass^k (all passed), a Wilson interval on the
pass rate and the spread of turns and cost. Export to the board; the pooled
view (`./lab2.sh --sample` shows its shape) is where lean vs bloated can
actually be compared.

**3 · Break the grader.** See `lab3/README.md`. A weak checker (compiles, one
header test) passes two shipped cheats; pairs write a third, then strengthen a
copy of the checker with hidden JUnit tests and a property check until the
cheats fail and the reference passes.

**4 · Read the traces.** `./lab4.sh` runs `trace-report` over your lab 1–2
stream-json transcripts (or the two synthetic ones): per turn, the context
size, output tokens and tool calls, and four flags with tokens and estimated
cost attributed: re-read of an unchanged file, repeated identical call,
blind retry after a failure, restated plan. Method in `lib/traces.py`.

**5 · Judge model.** See `lab5/HANDOUT.md`. Eight commit messages for one
diff, a four-criterion rubric, hand scores first, then `judge.sh` (one
`claude -p` call per sample, no tools, JSON out), then agreement, Spearman,
bias and a self-preference check with an explicit "what 8 samples cannot show".

**6 · Route by the numbers.** Haiku 4.5 vs Sonnet 5 (optionally Opus 5.5) on
the same 3 tasks, 2 runs each: pass rate, cost per run, and cost per
**accepted** task. Background reading: `lab6-routing-notes.md` (talk 07 slides
19–30: why no model wins everywhere, Cursor, OpenRouter, Pi, open-weight
models, when local makes sense, and the verified local-model recipe).

**7 · Take it home.** `take-home/GUIDE.md` and `take-home/template/`: task
YAML, a Maven/JUnit hidden-test checker, an smevals runner, a GitHub Actions
job and a generic CI shell script, for three tasks from your own repo.

## How a run works

Each agent session (labs 1, 2, 6) is one smevals run: `uvx --from
smevals==0.2.0 smevals run eval -c lean|bloated -m MODEL -t TASK -g --runs-dir
results/<lab>/<ts>/runs`, looped once per round because smevals 0.2.0 has no
`-n`. If uv/smevals is missing, `ENGINE=direct` (automatic fallback) runs the
same runner and checker without smevals and writes the same files.

The runner (`eval/run-claude`) copies `invoice-app/` into a fresh temp dir,
adds the chosen CLAUDE.md, runs `git init` with a baseline commit, then runs:

```sh
claude -p "$PROMPT" --model "$MODEL" --output-format stream-json --verbose \
  --max-turns 25 --max-budget-usd 0.75 --permission-mode dontAsk \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(./mvnw *),Bash(java *),Bash(ls *),Bash(cat *),Bash(grep *),Bash(find *),Bash(git diff*),…" \
  --disallowedTools "Agent,WebFetch,WebSearch" \
  --setting-sources project,local --strict-mcp-config --no-session-persistence
```

Anything not allowed is denied (`dontAsk`), so no session can install
packages, fetch URLs or push. `ISOLATE=0` drops the last line to measure your
own setup. The checker (`eval/checkers/hidden-tests`) grades a scratch copy:
it copies `eval/hidden/<task>/*.java` into the tests, restores the pristine
`pom.xml`, `mvnw` and `.mvn/`, runs `./mvnw -q -o test`, and passes only if the
hidden tests ran and passed and the own tests (at least as many as the
untouched repo's 57) passed.

Each run folder holds `transcript.jsonl` (raw stream-json), `command.sh`,
`labrun.json`, `metrics.json`, `check.json`, `diff.patch`, `meta.json` and the
edited `repo/`. Each lab folder holds `export.json` and `summary.md`.

Settings (environment variables): `PAIR`, `ROLE` (both|a|b), `LITE`, `MODEL`
(claude-sonnet-5), `HAIKU_MODEL` (claude-haiku-4-5), `OPUS_MODEL`
(claude-opus-5-5), `OPUS=1`, `REUSE` (1), `LOCAL_MODEL`, `LOCAL_BASE_URL`,
`MAX_TURNS` (25), `MAX_BUDGET_USD` (0.75 per session), `ENGINE`
(smevals|direct), `ISOLATE` (1), `CLAUDE_BIN`, `RESULTS_ROOT`,
`KEEP_WORKDIRS=1`, `TASKS`/`TASK`/`RUNS` per lab, `JUDGE_MODELS`, `SCORES`.

## The repo and the tasks

`invoice-app/` is a Maven project (Java 21, JUnit 5.14, nothing else; Maven
wrapper 3.3.4 pinned to Maven 3.9.16 with a SHA-256): `Money`, `Invoice`
(record), `Invoices`, `CustomerNames` (NFC, `Collator`, grapheme-safe
truncation), `InvoiceDates`, `CsvReader`, `FixtureLoader`, `CsvExport`,
`Report`, `Cli`, plus two exception classes. 57 deterministic tests, all
passing, with fixed locale and time zone. It carries the same latent bugs as
the Python kit, and the tests do not cover them:

| Task (`eval/tasks/`) | Latent bug |
|---|---|
| `fix-date-parser` | dotted dates fall back to month-first: `05.09.2026` becomes 9 May |
| `fixtures-bom` | the UTF-8 BOM in `data/legacy-export.csv` breaks the header |
| `jpy-rounding` | JPY missing; `format` and `allocate` hard-code two decimals |
| `report-sort-accents` | the report sorts by raw code point, not with the Collator |
| `export-currency-column` | feature: a sixth CSV column |
| `rename-customer-field` | refactor: `Invoice.customer` → `customerName` across callers |

`eval/solutions/` holds a reference fix per task (to check the checkers, never
shown to the agent). Every checker passes on its reference and fails on the
untouched repo; `./selftest.sh` verifies this plus the lab 3 cheats.

## Files

```
check-setup.sh  prework.md  README.md  RESULTS-SCHEMA.md  lab6-routing-notes.md
lab1.sh … lab6.sh  predict.sh  judge.sh  trace-report.sh  export-results.sh
record-facilitator-run.sh  selftest.sh
invoice-app/        the Java repo (pom.xml, mvnw, .mvn/wrapper, src/, data/, backlog/)
claude-md/          lean.md, bloated.md (outside the app: the agent never sees the other one)
eval/               smevals layout: eval.yaml, tasks/, configs/, graders/, checkers/hidden-tests,
                    hidden/<task>/Hidden*Test.java, solutions/<task>/, run-claude(-lean|-bloated)
lab3/               weak/, answer-key/, cheats/, checker.sh, README.md
lab5/               rubric.md, change.diff, samples/s1-s8.txt, authors.json, my-scores.csv, HANDOUT.md
sample-results/     SYNTHETIC: export.jsonl, traces/, lab5-judge/, lab5-human-scores.csv, generator
take-home/          GUIDE.md, template/eval/, ci/github-actions.yml, ci/run-evals.sh
lib/                common.sh, labkit.py, traces.py, judge.py, surefire_summary.py,
                    setup-repo.sh, fake_claude.py
results/            (gitignored) everything the runs write
```

## CLI facts this kit relies on

Checked on Claude Code 2.1.281 on 2026-09-24, from `claude --help` and the
docs (code.claude.com/docs/en/cli-reference, /headless, /llm-gateway):

- `claude -p` with `--output-format json|stream-json` (stream-json needs
  `--verbose`), `--model`, `--max-budget-usd`, `--permission-mode dontAsk`,
  `--allowedTools`/`--disallowedTools`, `--setting-sources project,local`,
  `--strict-mcp-config`, `--no-session-persistence`, `--tools ""` (no tools)
  and `--system-prompt` (both used by `judge.sh`).
- `--max-turns` works but is not listed in `--help`; hitting it is data, not
  an error.
- The result event carries `total_cost_usd`, `num_turns`, `duration_ms`,
  `usage` (main loop) and `modelUsage` (per model, everything). Costs are
  client-side estimates.
- `--bare` would isolate more tightly but needs an API key; the kit uses
  `--setting-sources project,local --strict-mcp-config` so a Pro/Max login works.
- `claude auth status` prints JSON (`loggedIn`, `authMethod`,
  `subscriptionType`) and exits 1 when signed out; it makes no model request.
- smevals 0.2.0 on PyPI: `run -m -c -t -g --runs-dir`, `report --json`; no `-n`.
- Local models: feasible but unsupported by Anthropic; see
  `lab6-routing-notes.md`.
