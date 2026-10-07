# Cost & Context Reference: Ivory conversion report

## Status

- **The deck is ready for parent review.**
  - **Output:** `cost-and-context-reference-ivory.html` (new file).
  - **Source:** `cost-and-context-reference.html` was only read. It is still untracked and its mtime is unchanged (3 Oct 21:59).
- **Slide count:** 4 → 4, in source order. `data-origin-slide` is 0, 7, 11, 20.
- **Scope:** nothing was staged or committed, and no subagent was used.
  - The only files written are the deck and this folder (`inventory.md`, `content-diff.txt`, `audit.json`, `report.md`).
  - `ivory_design_system/`, media, other decks, references, README/index, `reviews/`, `workshops/` and `style-mockups/shots/` were not touched.
  - The `M` on `cost-and-context.html` and `ivory-conversion/progress.json` was there before I started.

## Decisions

Every decision follows an accepted precedent.

- **01:** uses the accepted subagents-reference r2 opener.
  - Regular `.slide`, crumb "Optional reference".
  - `h2` "Cost &amp; Context<br>Reference", 2 lines.
  - `.cards.c2`: tile 1 holds the subtitle and its return link; tile 2 holds the author as `h3` and "Revised October 2026".
  - The footer `.note` holds the banner "Optional reference · Back to the talk" verbatim, with its link.
- **02–04:** the crumb and the banner are merged with a middle dot: "In practice · Optional reference · Back to the talk", following the root mapping and the accepted precedents.
- **02:** `table.tbl` at the default 30px, because it has 4 rows (§4).
- **03:** `ul.bul`.
- **04:** `.code` at 40px. The longest line is 59 characters, under the 64 limit. The markup is identical to the accepted main-deck twin in `cost-and-context-ivory.html`.
- **Clay:** none on any slide. Slides 02–04 are equal items, and the main-deck twin of 04 has no clay either.

## Content comparison

- **Shared audit:** `python3 ivory-conversion/audit.py cost-and-context-reference.html cost-and-context-reference-ivory.html` exits 0 with no structural or per-slide errors. Output is saved as `audit.json`.
- **Raw byte comparison:** see `content-diff.txt`.
  - `data-label`, `data-origin-slide` and `data-speaker-notes` match on 4/4 slides.
  - Hrefs are identical in order and count on 4/4 slides:
    - `cost-and-context.html` appears twice on 01 and once on each of 02–04.
    - `https://claude.com/pricing` is on 02.
- **Visible text:**
  - 01 has the same words, reordered into the opener structure. The only removed text is the title dot.
  - 02–04 differ only by the merged crumb and the one added `·`.

## Removed source text

- The title `.dot` "." on slide 01.
- The hand-written `.snum` digits 2/3/4. deck.js generates `01–04 / 04` instead.
- There was no `.ts-loopline`. Nothing was moved into the notes.

## Additions

- One `·` in the crumb on each of slides 02–04.
- On slide 04, the `.c` and `.k` spans and the CSS line numbers 01–05. These are styling only; the text is unchanged.
- No labels were invented.

## Unfit slides, missing components, unavailable media

- No slide is unfit.
- No new component is needed.
- No media is expected and none is present.

## Three weakest slides

1. **01:** the same limitations as the accepted subagents opener.
   - The bottom-aligned `.cards.c2` leaves about 270px of empty space above the tile content.
   - The tiles' last lines do not share a baseline: tile 1 ends at about y 840, tile 2 at about y 785.
   - The title uses only about 40% of the measure.
   - "Optional reference" appears twice (crumb and footer), on purpose, to keep both source occurrences.
2. **03:** three one-line rows fill a 562px zone, about 187px per row, with lines at about 55–60% of the measure. The slide reads airy, but this is valid `ul.bul` anatomy.
3. **02:** the headline needs 2 lines because it is wider than 1396px on one line. That leaves a 480px zone for 4 rows. Row 2 wraps to 2 lines, so row heights are slightly uneven, but everything fits and ends on 888.

## Checks run

All Chrome runs were outside the sandbox and strictly serial. There were no failures and no retries.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/ccr-chrome1.log ivory_design_system/tools/shoot.sh cost-and-context-reference-ivory.html /tmp/cost-and-context-reference-pass1` | exit 0, 4 PNGs, all opened. §10 checklist clean, no fixes needed |
| Pass 2 | `CHROME_LOG=/tmp/ccr-chrome2.log … /tmp/cost-and-context-reference-pass2` | exit 0, 4 PNGs, all opened, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/ccr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf cost-and-context-reference-ivory.html /tmp/cost-and-context-reference.pdf`, then `pdfinfo` | Pages: 4, 1440 × 810 pt. Page 2 rendered (`pdftoppm -f 2 -l 2 -r 60`) to `/tmp/ccr-pdf-p-2.png` and opened; it matches the PNG |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/ccr-chrome-notes.log … /tmp/cost-and-context-reference-notes 3 3` | Opened. Shows "NOTES · CLOUD ROUTE WORKSHEET · 3 / 4", the full notes and the buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/ccr-chrome-pw.log … /tmp/cost-and-context-reference-pw 2 2` | Opened. Shows 2 / 4 with next "Cloud route worksheet", the notes, the timer and the clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 in each |
| Static | grep | 1 `<link>` (styles.css) and 2 `<script src>` (deck-stage.js, deck.js). 0 inline scripts, 0 `<style>`, 0 `style=`. 4/4 empty `.snum`. 0 `h1`. No dark/light/reveal/dot/ts-/slide-content/Ember/Google Fonts/reference-banner. 0 clay |

## Screenshot paths

- `/tmp/cost-and-context-reference-pass1/01–04.png`
- `/tmp/cost-and-context-reference-pass2/01–04.png`
- `/tmp/cost-and-context-reference.pdf`
- `/tmp/ccr-pdf-p-2.png`
- `/tmp/cost-and-context-reference-notes/03.png`
- `/tmp/cost-and-context-reference-pw/02.png`

## Parent acceptance

Parent opened every pass-2 slide, notes-3 and presenter-2 shots, and rendered PDF page 2. All slides fit; no corrections needed. The worker opened all eight images across two complete passes. Parent reran the content audit (4/4, zero errors), checked the four-page PDF and console logs (zero CONSOLE entries), and verified all 138 protected hashes unchanged. Final weakest slides: 01 (sparse opener), 03 (airy single-line rows), 02 (wrapped table row below a two-line heading). Removed source decoration: title dot only; slide numbers are generated. No unavailable media or design-system additions. Physical projector and external link availability were not checked.
