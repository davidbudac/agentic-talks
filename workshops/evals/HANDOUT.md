# Evals, hands on: participant sheet

You and your partner measure a coding agent on a small Java repository with
your own Claude Code plans, then pool the numbers with the room.
Work in `workshops/evals/lab/` on both laptops.

**Room board:** <https://claude.ai/artifact/MgSgfU5azvZ7JpKynnGUrc>
(sign in to claude.ai; paste into the box and press **Add to the board**)

## Two laptops, one pair name

Run the setup check on **both** laptops with the **same** pair name, then put
`ROLE=a` or `ROLE=b` in front of every model lab. The split halves the waiting
time and spreads the usage across both plans: about 7 sessions on laptop a and
11 on laptop b over the whole day.

| | Laptop a (`ROLE=a`) | Laptop b (`ROLE=b`) |
|---|---|---|
| Labs 1 and 2 | the lean CLAUDE.md | the bloated CLAUDE.md |
| Lab 5 | the judge, with your hand scores | starts lab 6 in the background |
| Lab 6 | Sonnet (reuses your lean runs) | Haiku |

## The labs

| Lab | Time | Commands | Paste to the board |
|---|---|---|---|
| 0 · Setup check | 09:10 | `PAIR=your-team ./check-setup.sh` (both laptops) | nothing |
| 1 · Guess, then measure | 09:20 | `./predict.sh lean` or `./predict.sh bloated`, then `./export-results.sh --lab lab1 --latest`; then `ROLE=a ./lab1.sh` and `ROLE=b ./lab1.sh` | your guess first, then the runs from both laptops |
| 2 · Variance | 09:55 | `ROLE=a ./lab2.sh --yes` and `ROLE=b ./lab2.sh --yes` | 3 runs from each laptop |
| Break | 10:25 | leave lab 2 running | |
| 3 · Break the grader | 10:40 | `./lab3.sh`, `./lab3.sh check`, `./lab3.sh answer` (no model calls) | nothing |
| 4 · Read the traces | 11:15 | `./lab4.sh` (or `./trace-report.sh FILE...`) | nothing |
| Break | 11:40 | | |
| 5 · Judge model | 11:50 | laptop b first: `ROLE=b ./lab6.sh --yes`. Laptop a: fill `lab5/my-scores.csv`, then `./lab5.sh` | laptop a: judge runs and score lines |
| 6 · Route by the numbers | 12:20 | laptop a: `ROLE=a ./lab6.sh --yes` | both laptops |
| 7 · Take it home | 12:45 | read `take-home/GUIDE.md` | nothing |

**What to paste.** At the end of each model lab, on each laptop:

```sh
./export-results.sh --lab lab1 --latest      # lab1, lab2, lab5 or lab6
./export-results.sh --lab lab2 --latest | pbcopy   # macOS: straight to the clipboard
```

Each line is one run, one prediction or one judge score. Pasting the same lines
twice is safe: the board keeps one row per run.

## When something goes wrong

| Flag or variable | What it does |
|---|---|
| `--dry-run` | prints the plan and the exact commands, calls nothing |
| `--yes` | skips the "Proceed?" question |
| `LITE=1` | roughly halves the runs, for example `LITE=1 ROLE=a ./lab2.sh` |
| `--sample` | labs 2, 4, 5 and 6 work offline on the shared sample data |
| `OPUS=1` | lab 6 on laptop a also runs Opus (6 more sessions; only if your plan includes it) |
| `LOCAL_MODEL=qwen3-coder ... --local` | lab 6 on laptop b also runs a local model through Ollama (slow; not supported by Anthropic) |

Hit a usage limit? Tell the facilitator, move the rest of that lab to your
partner's laptop, and use `LITE=1` from then on. Every analysis still works
with `--sample`.

## Four definitions

- **pass@k:** a task passes if at least one of k runs passed. It answers "can
  it do the task at all?"
- **pass^k:** a task passes only if every one of k runs passed. It answers
  "can I leave it running unattended?" It falls fast: an agent that passes 70%
  of single runs passes three in a row only 34% of the time (0.7³).
- **Cost per accepted task:** everything a model or variant spent, divided by
  the runs that passed the hidden tests. A cheap model that often fails can
  cost more per accepted task than an expensive one that usually passes. (In
  lab 1 we call it cost per pass.)
- **Judge self-preference:** a judge model tends to rate text from its own
  model family higher than people do (Panickssery et al., 2024). Lab 5 compares
  the judge's scores with yours, split by who wrote the message. Eight samples
  can show the method and the direction of a bias, not prove one.

Dollar figures are Claude Code's estimates at API list prices. On Pro or Max
nothing is billed; the runs use your plan's usage instead.

## Take it home: an eval on your own repo

Full steps in `lab/take-home/GUIDE.md`; budget an afternoon.

1. **Pick three solved tasks** from your git history, each with a test: a bug
   fix, a small feature, a refactor. Note the base commit (the parent) and the
   fix commit for each.
2. **Write the task YAML** from `take-home/template/eval/tasks/`: a short
   `name`, the quoted `base_ref`, and the issue text as the `prompt`.
3. **Hide the acceptance tests** as `hidden/<task>/Hidden*Test.java`, outside
   the agent's copy.
4. **Check the checker both ways**: it must fail on the base and pass on the
   fix (`eval/checkers/maven-hidden-tests --repo DIR --task NAME`). Better still,
   make one plausible wrong solution fail too.
5. **Run each task at least three times** and compare variants (a CLAUDE.md
   change, another model) by cost per accepted task.
6. **Optional CI:** `take-home/ci/github-actions.yml` or `take-home/ci/run-evals.sh`.
   CI needs `ANTHROPIC_API_KEY`, billed per token: three tasks at k = 3 on
   Sonnet is about nine sessions.
