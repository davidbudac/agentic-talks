# Facilitator guide: Evals, Hands On

A half-day, hands-on evals workshop for about 20 Java developers in 10 pairs.
Each participant uses their own Claude Code plan (Pro or Max). This guide
covers the run sheet, the preparation, the room and what to do when things
break.

| You need | Where |
|---|---|
| Slides (50) | [`evals-workshop.html`](../../evals-workshop.html) at the repo root |
| Lab kit | [`lab/`](lab/) (start with [`lab/README.md`](lab/README.md)) |
| Participant sheet | [`HANDOUT.md`](HANDOUT.md), one printed copy per person |
| Live room board | <https://claude.ai/artifact/MgSgfU5azvZ7JpKynnGUrc> (source: [`board/`](board/)) |
| Concepts | Talk 07, [`measuring-what-works.html`](../../measuring-what-works.html) |
| Lab 6 background | [`lab/lab6-routing-notes.md`](lab/lab6-routing-notes.md), [`talk07-routing-archive.html`](talk07-routing-archive.html) |

**Deck controls.** Arrows or Space to move, `#14` in the URL opens slide 14.
**N** shows the speaker notes, **P** opens the presenter window (current and
next slide, notes, elapsed time and the running time box), **F** toggles
fullscreen. On a "Do this" or break slide, **T** starts or pauses the time
box, **Shift+T** resets it, and a click on the box does the same as T. A
running box keeps counting while you show another slide, and the presenter
window shows it in its top bar. With reduced motion switched on, the box stops
pulsing when time is up; the digits still count.

## Run sheet (09:00 to 13:00)

The lab kit's README lists block times that add up to about 235 minutes of
labs alone. The day below fits everything into 240 minutes by shortening the
discussion parts; the model runs keep their wall-clock time. If you start at
another time, shift every row by the same amount.

| Time | Slides | What happens | Watch for |
|---|---|---|---|
| **09:00** | 1 | Welcome while people sit down in pairs and open `workshops/evals/lab` | Anyone without a partner; anyone who skipped the prework |
| 09:01 | 2 | What they take home | Keep it under two minutes |
| 09:03 | 3 | The day, the two breaks, model labs against offline labs | |
| 09:04 | 4 | Two laptops, one `PAIR` name, `ROLE=a` and `ROLE=b` | Give laptop b to the partner with a Max plan, if any |
| 09:06 | 5 | Usage: quote your own dry-run `/usage` numbers here | If the dry run used more than half a 5-hour window, announce `LITE=1` now |
| 09:08 | 6 | The board: show the paste box on the second screen | Someone sees a read-only board: fix sharing now |
| 09:09 | 7 | The repo and the tasks | |
| **09:10** | 8 | **Lab 0** intro | |
| 09:11 | 9 | `PAIR=your-team ./check-setup.sh` on both laptops; press T (8 min) | FAIL lines, API-key sign-ins |
| 09:19 | 10 | Fixes for the last stragglers | A laptop you cannot fix: that pair runs on one laptop, no `ROLE`, `LITE=1` |
| **09:20** | 11 | **Lab 1** intro | |
| 09:21 | 12 | The two CLAUDE.md files: pairs skim `claude-md/` for two minutes | Do not reveal what you expect |
| 09:24 | 13 | The metric: cost per pass | |
| 09:26 | 14 | `./predict.sh`, paste the prediction, then `ROLE=a ./lab1.sh` and `ROLE=b ./lab1.sh`; press T (18 min) | Pairs running without `ROLE`; harness errors |
| 09:44 | 15 | Debrief 1: predictions only. Show of hands, write the split on the whiteboard | The board shows only the bets until you press Reveal the result |
| 09:48 | 16 | Debrief 2: reveal the lab 1 panel | Fewer than half the pairs posted: come back to it after the break |
| **09:55** | 17 | **Lab 2** intro | |
| 09:56 | 18 | pass@k and pass^k | One minute; talk 07 covered it |
| 09:58 | 19 | Pool the room: Wilson intervals | |
| 10:00 | 20 | `ROLE=a ./lab2.sh --yes` and `ROLE=b ./lab2.sh --yes`; press T (15 min) | Runs go past 10:15: that is fine |
| 10:15 | 21 | Debrief on the partial lab 2 panel | |
| **10:25** | 22 | **Break, 15 min**; press T | List pairs that have not posted lab 2 |
| **10:40** | 23 | **Lab 3** intro. Glance at the lab 2 panel for late arrivals | Say it: this lab calls no model |
| 10:42 | 24 | The weak checker passes wrong work | |
| 10:45 | 25 | Three ways to harden a checker | |
| 10:48 | 26 | Cheat, harden, swap, `./lab3.sh check`; press T (22 min) | Checkers that fail the reference |
| 11:10 | 27 | Debrief: `./lab3.sh answer` on the projector | |
| **11:15** | 28 | **Lab 4** intro | |
| 11:17 | 29 | Four flags in a trace | |
| 11:20 | 30 | `./lab4.sh`, then read flagged transcripts; press T (13 min) | Pairs with no transcripts: `./lab4.sh --sample` |
| 11:33 | 31 | Debrief: which flags were real waste | |
| **11:40** | 32 | **Break, 10 min**; press T | Nudge pairs with missing lab 1 or 2 lines |
| **11:50** | 33 | **Lab 5** intro. Laptop b starts `ROLE=b ./lab6.sh --yes` **now** | This background run is what makes lab 6 fit |
| 11:52 | 34 | Score first, then run the judge | |
| 11:54 | 35 | Self-preference and the limits of eight samples | Say whether you replaced the stand-in "human" samples |
| 11:57 | 36 | Hand scores in `lab5/my-scores.csv`, then `./lab5.sh` on laptop a; press T (16 min) | Anyone opening `authors.json` early |
| 12:13 | 37 | Debrief on the lab 5 panel | |
| **12:20** | 38 | **Lab 6** intro | Laptop b's Haiku runs should be done or close |
| 12:21 | 39 | Cost per accepted task | |
| 12:23 | 40 | `ROLE=a ./lab6.sh --yes` on laptop a, then export on both laptops; press T (12 min) | Pairs whose Haiku run never started |
| 12:25 | 41 | Routing 1: no model wins on cost, intelligence and taste | Runs finish while you talk |
| 12:28 | 42 | Routing 2: Cursor, OpenRouter, Pi | |
| 12:31 | 43 | Routing 3: open weights, local models | |
| 12:35 | 44 | Debrief on the lab 6 panel | |
| **12:45** | 45 | **Lab 7** intro | |
| 12:46 | 46 | Five steps to an eval on your repo | |
| 12:48 | 47 | Pick three tasks with `git log`; press T (6 min) | |
| 12:54 | 48 | Round: one task per pair | One sentence each |
| 12:57 | 49 | Recap | |
| 12:59 | 50 | Thank you, links, feedback | |
| **13:00** | | Close | |

**Sessions per laptop** with the defaults: laptop a runs 2 (lab 1) + 3 (lab 2)
+ about 2 (lab 6) Sonnet sessions and 8 judge calls; laptop b runs 2 + 3
Sonnet sessions and 6 Haiku sessions. That is about 7 and 11. `LITE=1`
roughly halves both.

**If you fall behind:** cut the lab 1 variants slide to a minute, run the lab 2
concept slides while the lab 2 runs go, trim the lab 3 swap step, and shorten
lab 7 to the recap and the handout. Never cut the start of the lab 5 block:
laptop b's background run feeds lab 6.

## One week before

- [ ] **Send [`lab/prework.md`](lab/prework.md)** to every participant. Ask them to run
      `PAIR=<team> ./check-setup.sh` and to reply with the `Result:` line. Chase
      anyone with a FAIL.
- [ ] **Share the board as "Can interact".** Open
      <https://claude.ai/artifact/MgSgfU5azvZ7JpKynnGUrc>, share it with the
      participants (or the organisation) with the "Can interact" setting, and
      test a paste from a second account. Clear any rehearsal rows afterwards
      with "Clear the board…", or plan to ignore `SYNTH-*` pairs.
- [ ] **Run `./selftest.sh`** in `lab/`. It checks every script with a fake
      `claude` and costs nothing (5 to 8 minutes, mostly Maven).
- [ ] **Do the dry run on a Pro account.** In an interactive `claude` session,
      run `/usage` and note the numbers. Then run
      `./record-facilitator-run.sh --dry-run` to read the plan, and
      `./record-facilitator-run.sh` for real: it runs labs 1, 2, 5 and 6 once
      (about one pair's budget, 45 to 90 minutes) and replaces the synthetic
      `sample-results/` with real data. Run `/usage` again. If the run used more
      than about half of a 5-hour window, plan the day with `LITE=1`. Put both
      readings into your slide 5 notes. Read the transcripts before you commit
      `sample-results/`: they contain the full lab repo files.
- [ ] **Replace the four stand-in "human" commit messages** in `lab/lab5/samples/`
      (see the note in `lab/lab5/authors.json`): ask two colleagues to write a
      commit message for `lab5/change.diff`, or take real messages of a similar
      change from your team's history. Keep quality spread across both groups,
      and update `authors.json`. Until you do, the self-preference check compares
      Claude with Claude, and you must say so on slide 35. Do this before the dry
      run, so the recorded judge scores use the real samples.
- [ ] **Decide on Opus and the local model.**
      - Opus: `OPUS=1 ROLE=a ./lab6.sh --yes` adds 6 Opus sessions on laptop a.
        Offer it only to pairs whose plan includes Opus and who have usage to
        spare; it is optional.
      - Local: `ROLE=b LOCAL_MODEL=qwen3-coder ./lab6.sh --local --yes`, started
        at the beginning of lab 5 instead of the plain Haiku command. It needs
        Ollama, a pulled model and a machine with 32 GB or more; it is slow,
        unsupported by Anthropic, and uses no plan. Suggest `LITE=1` with it.
        Tell interested people in the prework email so they pull the model at home.
- [ ] **Re-check the routing facts** on slides 42 and 43 against
      `lab/lab6-routing-notes.md` (checked September 2026). The open-model field
      moves monthly.
- [ ] Print [`HANDOUT.md`](HANDOUT.md), one copy per person, and a few spares.

## On the day

**45 minutes before:**

- Open `evals-workshop.html` on the projector (from a local clone, or GitHub
  Pages if it is enabled), press **P** for the presenter window on your laptop
  screen and **F** on the projector.
- Open the board in a browser tab on a second screen or projector input. Test
  one paste with your own pair name, then delete it or leave it as a demo row.
- Test the Wi-Fi from the room and keep a phone hotspot ready.
- Write the board URL and the Wi-Fi details on the whiteboard. Keep space for
  the lab 1 prediction split.
- Set out the printed handouts, one per person.

**Room for 10 pairs:**

- Pairs sit side by side with both laptops open: they need to see each other's
  terminals. Leave aisles so you can reach every table.
- 20 laptops for 4 hours: provide power at every table (extension leads for at
  least 20 sockets).
- A second facilitator helps a lot with 10 pairs: one presents, the other walks
  the room during every "Do this" slide.
- Number the tables and ask each pair to write their `PAIR` name on a card.
  The board shows those names, and you will call on pairs by them.
- A spare laptop with the kit cloned and the Maven dependencies cached lets a
  pair with a broken machine keep going.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `[FAIL] not signed in` | Claude Code never logged in, or logged in as another OS user | Run `claude` once and log in with Pro or Max, or `claude auth login`. `./check-setup.sh` again |
| `[WARN] signed in with an API key` | `ANTHROPIC_API_KEY` or a console login is active | Runs would bill per token. Unset the variable in that shell (`unset ANTHROPIC_API_KEY`) and log in with the subscription |
| `[FAIL] dependency prefetch` or `offline test run failed` | Proxy, corporate Maven mirror, or no network at the first run | Fix `~/.m2/settings.xml`, then `cd invoice-app && ./mvnw dependency:go-offline` on a working network (a hotspot will do). Last resort: copy `~/.m2/repository` from a working laptop |
| `uv not found` or smevals does not start | uv missing, or `uvx` cannot reach PyPI | Nothing to do: the labs fall back to `ENGINE=direct` and write the same files. Install uv later for the take-home |
| A partner hits a usage limit | Pro session limit | Switch that laptop to `LITE=1`, or move its runs to the partner's laptop without `ROLE`. The analysis labs work with `--sample`. Limits reset after five hours, so do not wait |
| Runs are slow | Busy network, or a task that takes many turns | Each session is capped at 25 turns and $0.75 of estimated cost. Let runs continue into the next lab (labs 3 and 4 call no model), and use `LITE=1` for the next model lab |
| `harness error (see .../stderr.txt)` | Sign-in expired, network drop, or Claude Code crashed | Read `stderr.txt`. The run exports as `passed: null` and the board leaves it out of pass rates. Re-run the lab later if time allows |
| Board refuses the paste, or shows read-only | Participant not signed in to claude.ai, share not set to "Can interact", or a line is not valid JSON | Check sign-in and sharing. Validate with `./export-results.sh --validate FILE`. Fallback: the pair sends you their lines and you paste them |
| `no prediction recorded` warning on laptop b | `predict.sh` ran only on laptop a | Harmless: the board has the prediction from laptop a |
| `./lab5.sh` warns you have not scored | `lab5/my-scores.csv` is empty on that laptop | Fill every cell (1 to 5) on the laptop that runs lab 5, then run it again |
| `no Ollama at http://localhost:11434` | Ollama not running, or the model not pulled | `ollama serve`, `ollama pull qwen3-coder`, or drop the local option |
| Lab 3 checker fails the reference | The pair's checker is too strict | Good debrief material: a checker that rejects correct work is broken too |

## If the network fails

Model calls and the board need the network; everything else is local. The
prework prefetched Maven, the dependencies and smevals, so builds and checkers
run offline.

1. **Partial outage:** put a few laptops on a phone hotspot. Agent sessions use
   little bandwidth. Prioritise one laptop per pair and run that pair's model
   labs without `ROLE`, with `LITE=1`.
2. **No network at all:** switch every analysis to the recorded data from your
   dry run (it is real data once `record-facilitator-run.sh` has run; before
   that it is synthetic, and you must say so):
   - Lab 1: take the predictions by show of hands, then show the lab 1 lines from
     `./export-results.sh --sample` on the projector and discuss one pair's
     cells.
   - Lab 2: `./lab2.sh --sample` prints per-pair tables and the pooled view.
   - Labs 3 and 4 run unchanged (`./lab4.sh --sample` if a pair has no
     transcripts).
   - Lab 5: hand scoring works offline; `./lab5.sh --sample` compares the real
     hand scores with recorded judge scores.
   - Lab 6: `./lab6.sh --sample`, plus the routing slides.
   - Lab 7 runs unchanged.
3. **When the network returns:** pairs run `./export-results.sh` (every lab, not
   just the latest) and paste everything. Duplicates are safe: the board keys
   rows by pair, lab, variant, task and run.

## Reading the board in each debrief

Filter out `SYNTH-*` pairs if any rehearsal rows remain. `passed: null` rows
are left out of pass rates; they are harness errors, not failures.

- **Lab 1 (slides 15 and 16).** Until you press **Reveal the result**, the
  panel shows only the bets and how many runs are in, so it can stay on the
  projector during slide 15. After the reveal it shows lean against bloated:
  pass rate, runs passed, cost per pass, mean turns, and tokens and cost per
  run. On slide 16, compare the majority prediction with the variant that was
  cheaper per pass. The reveal is remembered per browser; press **Hide the
  result again** before the next workshop. Each pair contributed one run per cell, so the room has about
  20 runs per variant; say how many pairs posted before you draw a conclusion.
- **Lab 2 (slide 21).** One row of dots per pair, filled for a pass and hollow
  for a fail, and per variant the single-run pass rate, pass@k and pass^k. Point
  first at a pair whose identical runs split. Then the gap between pass@k and
  pass^k: a large gap means the configuration can do the task but cannot be
  left alone. Only call lean against bloated if the difference is large compared
  with the spread; `./lab2.sh --sample` shows the Wilson intervals if you need
  them on screen.
- **Lab 5 (slide 37).** A scatter of the judge's score against the room's
  scores (one cell per score pair, sized by count, with the diagonal for
  perfect agreement), and a headline with the exact-agreement share and the
  self-preference gap: how far above the room the judge scored model-written
  samples, next to the same for human-written ones. A vertical
  spread for one sample means the people disagree with each other. Repeat the
  caveat: eight samples, four per group, and possibly stand-in human samples.
  Pooling ten pairs adds raters, not samples.
- **Lab 6 (slide 44).** A table per model: runs, pass rate, cost per run and
  cost per accepted task, with a headline that names the cheapest per run and
  the cheapest per accepted task. When they differ, that is the lesson of the
  lab. Sonnet rows include runs reused from labs 1 and 2 (exported again as lab
  6), so never add costs across labs. Local runs show a cost of 0.0 because the
  kit does not price local tokens.
