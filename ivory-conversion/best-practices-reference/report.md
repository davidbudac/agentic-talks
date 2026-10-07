# Best Practices Reference: Ivory conversion report

## Status

- **The deck is ready for parent review.**
  - **Output:** `best-practices-reference-ivory.html` (new file).
  - **Source:** `best-practices-reference.html` was only read. It is still untracked; mtime (3 Oct 21:59:02) and sha1 `c6c3291964c24c24d89ddef44c5863f1136ba0d0` are unchanged before and after.
- **Slide count:** 5 → 5, in source order. `data-origin-slide` is 0, 43, 45, 0, 0.
- **Scope:** nothing was staged or committed, and no subagent was used.
  - The only files written are the deck and this folder (`inventory.md`, `content-diff.txt`, `audit.json`, `report.md`).
  - `ivory_design_system/`, media, other decks, references, README/index, `reviews/`, `workshops/` and `style-mockups/shots/` were not touched. The pre-existing `M`/`??` entries in `git status` are unchanged.

## Decisions

Every decision follows an accepted precedent.

- **01:** the accepted subagents/cost reference opener. Regular `.slide`, crumb "Optional reference", `h2` "Claude Best Practices<br>Reference" (2 lines), `.cards.c2` (tile 1 = subtitle + "Return to the main talk" link; tile 2 = `h3` "David Budáč" + "Revised October 2026"), footer `.note` = banner "Optional reference · Back to the talk" verbatim with its link.
- **02–05:** crumb and banner merged with a middle dot ("In practice · Optional reference · Back to the talk", "Sources · Optional reference · Back to the talk"), link kept in the crumb.
- **02:** `table.tbl.lg` (40px), because it has 3 short rows (§4). Fits in the 480px zone under the 2-line headline; rows end on 888.
- **03–05:** `ul.bul` with one link per row, the same markup as the accepted main-deck Sources twin in `best-practices-ivory.html`. `.links` was rejected because it needs equal-count columns with headings; the source has 5/5/3 links and no headings, so it would require invented labels.
- **Clay:** none on any slide (all equal items).

## Content comparison

- **Shared audit:** `python3 ivory-conversion/audit.py best-practices-reference.html best-practices-reference-ivory.html` exits 0, counts 5/5, no structural or per-slide errors. Saved as `audit.json`.
- **Raw comparison** (`content-diff.txt`): `data-label`, `data-origin-slide` and `data-speaker-notes` are byte-identical on 5/5. Hrefs are identical in order and count on 5/5 (2, 2, 6, 6, 4): `best-practices.html` ×2 on 01 and ×1 on each of 02–05; `https://code.claude.com/docs/en/interactive-mode` on 02; the 13 claude.dev URLs on 03–05.
- **Visible text:** 01 has the same words reordered into the opener (the source extractor glued "reference"+"Revised" from adjacent spans; not a real change). 02–05 differ only by the removed hand-written slide digit and one added `·`.

## Removed source text

- The title `.dot` "." on slide 01.
- The hand-written `.snum` digits 2/3/4/5 (deck.js now generates `01–05 / 05`).
- No `.ts-loopline` existed. Nothing was moved into the notes.

## Additions

- One `·` in the crumb on each of slides 02–05. No labels invented, no other additions.

## Unfit slides, missing components, unavailable media

- None unfit. No new component needed. No media expected or present.

## Three weakest slides

1. **01:** same limitations as the accepted opener: ~270px of empty space above the bottom-aligned tile content, tile last lines not on a shared baseline (≈840 vs ≈785), title uses ~45% of the measure, "Optional reference" appears twice (crumb + footer) to keep both source occurrences.
2. **05:** only 3 one-line link rows in a 562px zone (~187px per row) and lines at ~55–60% of the measure. Airy, but valid `ul.bul` anatomy and consistent with 03–04.
3. **02:** the headline needs 2 lines (wider than 1396px on one), leaving a 480px zone; each Check cell wraps to 2 lines at 40px while Need cells are 1 line, so the right column reads denser than the left. Everything fits and ends on 888.

## Checks run

All Chrome runs were outside the sandbox and strictly serial (one invocation at a time). No failures, no retries. Pre-existing Chrome processes seen were the user's desktop browser, not headless runs.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/bpr-chrome1.log ivory_design_system/tools/shoot.sh best-practices-reference-ivory.html /tmp/best-practices-reference-pass1` | exit 0, 5 PNGs, all opened. §10 checklist clean; no fixes needed |
| Pass 2 | `CHROME_LOG=/tmp/bpr-chrome2.log … /tmp/best-practices-reference-pass2` | exit 0, 5 PNGs, all opened, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/bpr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf best-practices-reference-ivory.html /tmp/best-practices-reference.pdf`, then `pdfinfo` | Pages: 5, 1440 × 810 pt. Page 2 rendered (`pdftoppm -f 2 -l 2 -r 60 -png`) to `/tmp/bpr-pdf-p-2.png` and opened; matches PNG 02 |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/bpr-chrome-notes.log … /tmp/best-practices-reference-notes 2 2` | Opened. "NOTES · COMMAND REFERENCE · 2 / 5", full notes, buttons clear of text |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/bpr-chrome-pw.log … /tmp/best-practices-reference-pw 3 3` | Opened. "3 / 5 Sources → next: Sources", current + next previews, notes, timer, clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 in each |
| Static | grep | 1 `<link>` (styles.css), 2 `<script src>` (deck-stage.js, deck.js), 0 inline scripts, 0 `<style>`, 0 `style=`, 5/5 empty `.snum`, 0 `h1`, no dark/light/reveal/dot/slide-content/Google Fonts/reference-banner/clay. Residual keyword hits are only comments ("keys", "Ember …") and the `what-a-task-costs` URL |

## Screenshot paths

- `/tmp/best-practices-reference-pass1/01–05.png`
- `/tmp/best-practices-reference-pass2/01–05.png`
- `/tmp/best-practices-reference.pdf`, `/tmp/bpr-pdf-p-2.png`
- `/tmp/best-practices-reference-notes/02.png`
- `/tmp/best-practices-reference-pw/03.png`

## Parent acceptance

Parent opened all five final pass-2 slides, notes-2, presenter-3 and PDF page 2. No overflow or corrections needed; notes now clear of controls. Worker opened all ten images across two full passes. Parent reran the audit (5/5, zero errors), confirmed five PDF pages and zero CONSOLE entries, and verified all 138 protected hashes unchanged. Weakest: 01 (sparse opener), 05 (airy three-link list), 02 (denser wrapped right column). Removed title dot only; numbering is generated. No unavailable media or new component. Physical projector and external URL availability were not checked.
