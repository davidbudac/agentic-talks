# Prework for the evals workshop (about 30 minutes, a week before)

The workshop is hands-on: you and a partner will run a coding agent on a small
Java project, measure it, and pool the numbers with the room. Please get your
laptop ready beforehand so the day is spent on evals, not on installs.

## 1. Install (skip what you have)

- **JDK 21 or newer** (for example Temurin 21) on your `PATH`. Maven itself is
  not needed: the project ships the Maven wrapper.
- **git**.
- **Python 3.10+** (`python3`), standard library only; macOS and most Linux
  distributions have it.
- **uv** (https://docs.astral.sh/uv/): it runs the smevals eval tool without
  installing anything into your system Python.
- **Claude Code** (https://code.claude.com/docs/en/setup). Then run `claude`
  once and **sign in with your Pro or Max account**. Windows: use WSL.

## 2. Check and prefetch

```sh
git clone <this repository> && cd <repo>/workshops/evals/lab
PAIR=<your-team-name> ./check-setup.sh
```

This takes a few minutes the first time: it downloads Maven, the project's
dependencies and smevals once, then proves an **offline** build works, so the
venue Wi-Fi does not matter on the day. It checks that you are signed in to
Claude Code without calling the model, so it costs nothing. Fix anything
marked `[FAIL]` and run it again. If you already know your partner, agree a
team name and use the same `PAIR` on both laptops.

Behind a corporate proxy? Configure `~/.m2/settings.xml` (Maven) and
`HTTPS_PROXY` (uv) before running the check; tell the facilitator if it still
fails.

## 3. Know what the day will use

The labs run Claude Code headless on your own subscription. With the default
settings a pair runs about 18 short agent sessions plus 8 tiny judge calls
over the whole workshop, split between the two partners' laptops, so roughly
7–11 sessions each. Anthropic does not publish an exact Pro limit, so please:

- start the day with most of your 5-hour window unused (avoid a heavy Claude
  session right before the workshop);
- do not run `lab1.sh` … `lab6.sh` before the day: the labs are about
  comparing fresh runs across the room (`--dry-run` is free if you are curious).

If you hit a limit on the day, your partner's laptop carries on, `LITE=1` runs
fewer sessions, and every analysis lab also works on shared sample data.

## 4. Optional

- Skim talk 07 (`measuring-what-works.html`), part 01 (evals, traces, smevals).
- For the optional local-model part of lab 6: install Ollama and pull a coding
  model (`ollama pull qwen3-coder`, several GB; needs a machine with 32 GB+
  RAM to be usable). Read `lab6-routing-notes.md` first: it works, but it is
  slow on a laptop and not supported by Anthropic.
- Think of three small, finished tasks from your own Java repository (a bug
  fix with a test, a small feature, a rename). Lab 7 turns them into your own
  eval suite.
