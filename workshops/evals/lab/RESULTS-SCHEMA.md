# Results schema (version 1)

The shared board consumes one compact JSON object per line. Every lab runner
writes its lines to `results/<lab>/<timestamp>/export.json` (a JSON array);
`./export-results.sh` prints them, one per line, ready to paste.

```sh
./export-results.sh                       # everything so far: runs, predictions, judge scores
./export-results.sh --lab lab2 --latest   # one lab, most recent run only
./export-results.sh --sample              # the SYNTHETIC sample set (pairs SYNTH-01..10)
./export-results.sh --validate FILE       # check lines against this schema ("-" = stdin)
```

There are three kinds of line. Keys are exactly as listed: no extra keys, none
missing. The validator (`lib/labkit.py validate`) enforces this.

## 1. A run (labs 1, 2, 5, 6)

One agent session (labs 1, 2, 6) or one judge call (lab 5).

```json
{"v":1,"pair":"team-rocket","lab":"lab2","variant":"lean","task":"report-sort-accents","run":2,"passed":true,"turns":11,"input_tokens":44,"output_tokens":4120,"cache_read_tokens":301877,"cache_write_tokens":33012,"cost_usd":0.1861,"duration_s":94.3,"model":"claude-sonnet-5"}
```

| Key | Type | Meaning |
|---|---|---|
| `v` | int | Schema version, always `1` |
| `pair` | string | `PAIR` env var, else the `.pair` file, else `h-` + 8 hex chars of a SHA-256 of the hostname. Set the same value on both partners' laptops |
| `lab` | `"lab1"` \| `"lab2"` \| `"lab5"` \| `"lab6"` | The lab that produced the run |
| `variant` | string | lab1/lab2: `lean` \| `bloated` (the CLAUDE.md). lab6: `haiku` \| `sonnet` \| `opus` \| `local`. lab5: the judge model's alias (`sonnet`, `haiku`) |
| `task` | string | Task id from `eval/tasks/` (lab5: the sample id, `s1`..`s8`) |
| `run` | int ≥ 1 | Run number within (pair, lab, variant, task): the round |
| `passed` | bool \| null | Hidden JUnit tests and the repo's own tests pass (eval checker). `null`: not graded, either a harness error (no result event) or a lab 5 judge call |
| `turns` | int | `num_turns` from Claude Code's result event |
| `input_tokens` | int | Uncached input tokens, summed over `modelUsage` (every model call, subagents included) |
| `output_tokens` | int | Output tokens, same source |
| `cache_read_tokens` | int | `cacheReadInputTokens`, same source |
| `cache_write_tokens` | int | `cacheCreationInputTokens`, same source |
| `cost_usd` | float | `total_cost_usd`: Claude Code's client-side estimate at API list prices. On Pro/Max nothing is billed; the run uses plan usage. `local` runs are exported as `0.0` because the estimate prices local tokens at Anthropic rates |
| `duration_s` | float | `duration_ms / 1000` from the result event |
| `model` | string | The model id Claude Code reported (init event), else the one requested |

## 2. A prediction (lab 1)

Written by `./predict.sh lean|bloated` before `./lab1.sh`: which CLAUDE.md the
pair expects to be cheaper per passing run.

```json
{"v":1,"pair":"team-rocket","lab":"lab1","kind":"prediction","variant":"lean"}
```

## 3. A judge score (lab 5)

One per sample the pair scored by hand (overall, 1-5), next to the first
judge model's overall score. Samples without a hand score are not exported.

```json
{"v":1,"pair":"team-rocket","lab":"lab5","kind":"judge","sample":"s3","human":4,"judge":5,"author":"model"}
```

| Key | Type | Meaning |
|---|---|---|
| `sample` | string | `s1`..`s8` (`lab5/samples/`) |
| `human` | int 1-5 | The pair's `overall` score from `lab5/my-scores.csv` |
| `judge` | int 1-5 | The judge's `overall` score (`judge.sh`, first model in `JUDGE_MODELS`) |
| `author` | `"human"` \| `"model"` | From `lab5/authors.json`. Read its note: unless the facilitator replaced them, the "human" samples are stand-ins written by Claude |

## Things to know when aggregating

- **Lab 6 reuses Sonnet runs.** To stay inside a Pro window, `lab6.sh` reuses
  the pair's lean Sonnet runs from labs 1-2 on the same tasks and exports them
  again with `lab:"lab6"`, `variant:"sonnet"`. So do not sum `cost_usd` across
  labs to get a room total; sum within a lab. `REUSE=0` turns this off.
- **Split pairs.** With `ROLE=a` / `ROLE=b` a pair's lines come from two
  laptops. They share `pair` if both set the same `PAIR`; `run` numbers are
  per variant, so they do not collide (lab 1-2: lean on one laptop, bloated on
  the other).
- **`passed: null`** means "no verdict", not "failed". Leave it out of pass
  rates and report the count separately (it usually means a crashed or
  interrupted session).
- **pass@k and pass^k** are per (pair, variant, task) over `run`. The room view
  pools runs across pairs for the pass rate and counts pairs for pass@k/pass^k
  (`lib/labkit.py` `pooled_lab2` does both).
- **Tokens** are dominated by cache reads (~90% on these tasks). Total tokens
  processed is the sum of the four token fields; cost depends mostly on cache
  writes and output.
- **Synthetic data** uses pair ids `SYNTH-01`..`SYNTH-10`; filter them out on
  the day.
