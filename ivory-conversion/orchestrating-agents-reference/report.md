# Orchestrating Agents Reference: Ivory conversion report

## Status

- **Ready for parent review.** Output: `orchestrating-agents-reference-ivory.html` (new). Source `orchestrating-agents-reference.html` only read; still untracked, mtime unchanged (3 Oct 21:59).
- **Slides:** 4 → 4, source order, `data-origin-slide` 0, 5, 21, 29.
- **Scope:** nothing staged or committed; no subagent. Only files written: the deck and this folder (`inventory.md`, `content-diff.txt`, `audit.json`, `report.md`). `ivory_design_system/`, media, other decks, references, README/index, `reviews/`, `workshops/`, `style-mockups/shots/` untouched.
- **Head:** exactly 3 tags (styles.css, deck-stage.js, deck.js); 0 `<style>`, 0 `style=`, no font links, no inline scripts; all `.snum` empty; all slides plain `.slide` (light).

## Decisions (all follow accepted precedent)

- **01:** accepted subagents/cost reference opener (crumb "Optional reference", 2-line `h2`, `.cards.c2` subtitle+Return link | author `h3` + date, banner in footer `.note`).
- **02–04:** crumb merged with banner by `·` (root mapping for `.reference-banner`).
- **02:** `ul.bul`, 4 rows, linked tool names inline with "—" kept; no clay (equal items).
- **03:** `.code.reg`, markup byte-identical to accepted twin in `agentic-engineering-reference-ivory.html` (8 lines incl. empty line 04).
- **04:** `.code` at 40px (max 59 chars), markup identical to accepted twin in `orchestrating-agents-ivory.html` (`.k` on "Task:").
- **Clay:** none on any slide.

## Removed source text

- Title `.dot` "." (slide 01). Hand-written `.snum` 2/3/4 (replaced by generated numbers). No `.ts-loopline` existed. Nothing moved into notes.

## Additions

- One `·` in the crumb on 02–04. `.k` span on 04 (style only). CSS line numbers on 03/04. No invented labels.

## Unfit slides / new components / media

- None unfit; no new component needed; no media expected or present.

## Three weakest slides

1. **01:** same limits as the accepted opener: bottom-aligned cells leave ~270px empty above; tile last lines don't share a baseline (≈840 vs ≈785); "Optional reference" appears twice by design.
2. **03:** `.code.reg` (30px) with lines ≤52 chars uses only ~65% of panel width, and the empty line 04 shows a bare line number; kept to match the accepted twin.
3. **02:** four one-line rows at ~50% of the measure in a 480px zone read airy; valid `ul.bul` anatomy.

## Checks run (all Chrome runs serial, outside sandbox; no failures, no retries)

| Check | Command | Result |
|---|---|---|
| Audit | `python3 ivory-conversion/audit.py orchestrating-agents-reference.html orchestrating-agents-reference-ivory.html` | exit 0, no errors; `audit.json` |
| Pass 1 | `CHROME_LOG=/tmp/oar-chrome1.log ivory_design_system/tools/shoot.sh orchestrating-agents-reference-ivory.html /tmp/orchestrating-agents-reference-pass1` | exit 0; 01–04.png all opened; §10 clean, no fixes |
| Pass 2 | `CHROME_LOG=/tmp/oar-chrome2.log … /tmp/orchestrating-agents-reference-pass2` | exit 0; 01–04.png all opened; byte-identical to pass 1 (`cmp`) |
| PDF | `CHROME_LOG=/tmp/oar-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf orchestrating-agents-reference-ivory.html /tmp/orchestrating-agents-reference.pdf`; `pdfinfo` | Pages: 4, 1440 × 810 pt; page 3 rendered to `/tmp/oar-pdf-p-3.png` and opened, matches PNG |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/oar-chrome-notes.log … /tmp/orchestrating-agents-reference-notes 3 3` | Opened `03.png`: "NOTES · PLUGIN PUBLICATION RECIPE · 3 / 4", full notes, buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/oar-chrome-pw.log … /tmp/orchestrating-agents-reference-pw 2 2` | Opened `02.png`: 2 / 4, next "Plugin publication recipe", notes, timer, clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 each |

## Parent acceptance

Parent opened all four pass-2 slides, notes-3, presenter-2 and rendered PDF page 3. All fit and follow the accepted series patterns. Worker opened all eight PNGs across two complete passes. Parent reran the content audit (4/4, zero errors), verified PDF count four and no CONSOLE entries in the five logs, and checked all 138 protected hashes unchanged. Weakest slides remain 01 (sparse opener), 03 (small code with duplicate numbering and blank line), 02 (airy linked rows). Only the title dot is removed as source decoration; slide numbers are generated. No unavailable media or design-system additions. Physical projector and external link availability were not checked.
