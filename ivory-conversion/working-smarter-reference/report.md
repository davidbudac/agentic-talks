# Working Smarter Reference: Ivory conversion report

## Status

- **The deck is ready for parent review.**
  - **Output:** `working-smarter-reference-ivory.html` (new file).
  - **Source:** `working-smarter-reference.html` was only read. Its sha256 and mtime (1791057542) are unchanged.
- **Slide count:** 8 → 8, in source order. `data-origin-slide` is 0, 7, 11, 29, 45, 68, 52, 76.
- **Scope:** nothing was staged or committed, and no subagent was used.
  - The only files written are the deck and this folder (`inventory.md`, `content-diff.txt`, `audit.json`, `report.md`).
  - `ivory_design_system/`, media, other decks, references, README/index, `progress.json`, `reviews/`, `workshops/` and `style-mockups/shots/` were not touched.
  - All 138 hashes in `protected-files.json` match.

## Decisions

Every slide reuses accepted markup. See `inventory.md` for the twins.

- **01:** uses the accepted reference opener.
  - Regular `.slide`, crumb "Optional reference".
  - `h2` "Working Smarter with Agents<br>Reference", 2 lines.
  - `.cards.c2`: tile 1 holds the subtitle and its return link; tile 2 holds "David Budáč" as `h3` and "Revised October 2026".
  - The footer `.note` holds the banner verbatim, with its link.
- **02–08:** the source crumb and the banner are merged with a middle dot, and the link is kept.
- **Tables (02, 06):** `.tbl` at 30px, because each has 4 rows.
- **Bullet lists (03, 04, 08):** `ul.bul`.
- **05:** `.code.reg`, with the blank line kept.
- **07:** `.code` at 40px, with blank lines and alignment kept.
- **Clay:** used only on slide 07, on "independently" — the assumption the headline names. This matches the accepted measuring-what-works-reference twin. Every other slide is equal items with no clay.
- **Head:** exactly 3 tags (styles.css, deck-stage.js, deck.js). There are no inline scripts, `<style>` elements, `style=` attributes or font links. All 8 `.snum` are empty.

## Content comparison

- **Shared audit:** `python3 ivory-conversion/audit.py working-smarter-reference.html working-smarter-reference-ivory.html` exits 0. It reports 8/8 slides with no structural or per-slide errors. Output is saved as `audit.json`.
- **Raw byte comparison:** see `content-diff.txt`.
  - `data-label`, `data-origin-slide` and raw `data-speaker-notes` match on 8/8 slides.
  - Hrefs are identical in order and count on 8/8 slides (15 in total).
- **Visible text:**
  - 01 has the same words, reordered into the opener structure.
  - 02–08 differ only by the merged crumb and the one added `·`.

## Removed source text

- The title `.dot` "." on slide 01.
- The hand-written `.snum` digits 2–8. deck.js generates `01–08 / 08` instead.
- There was no `.ts-loopline`. Nothing was moved into the notes, and no words were removed.

## Additions

- One `·` in the crumb on each of slides 02–08.
- On 05 and 07, the CSS code line numbers.
- On 07, the `.key` span. It changes styling only, not text.
- No labels were invented.

## Unfit slides, missing components, unavailable media

- No slide is unfit.
- No new component is needed.
- No media is expected and none is present.

## Three weakest slides

1. **01:** the same limitations as the accepted reference openers.
   - About 270px of empty space sits above the bottom-aligned tile content.
   - The tiles' last lines do not share a baseline (about y 840 versus y 785).
   - "Optional reference" appears twice, on purpose, to keep both source occurrences.
2. **03:** three one-line rows share a 562px zone, about 187px each, using about 60% of the measure. The slide reads airy, but this is valid `ul.bul` anatomy.
3. **02:** the 2-line headline leaves a 480px zone for 4 rows. Row 2 wraps, so row heights are slightly uneven, but everything fits and ends on 888.

## Checks run

All Chrome runs were outside the sandbox and strictly serial. Each had exit 0. There were no failures and no retries.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/wsr-chrome1.log ivory_design_system/tools/shoot.sh working-smarter-reference-ivory.html /tmp/working-smarter-reference-pass1` | 8 PNGs, all opened. §10 checklist clean, no fixes needed |
| Pass 2 | `CHROME_LOG=/tmp/wsr-chrome2.log … /tmp/working-smarter-reference-pass2` | 8 PNGs, all opened, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/wsr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf working-smarter-reference-ivory.html /tmp/working-smarter-reference.pdf`, then `pdfinfo` | Pages: 8, 1440 × 810 pt. Page 7 rendered (`pdftoppm -f 7 -l 7 -r 60`) to `/tmp/wsr-pdf-p-7.png` and opened; it matches the PNG |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/wsr-chrome-notes.log … /tmp/working-smarter-reference-notes 8 8` | Opened. Shows "NOTES · LOCAL MODEL MEMORY · 8 / 8", the full notes clear of the buttons, and the buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/wsr-chrome-pw.log … /tmp/working-smarter-reference-pw 5 5` | Opened. Shows 5 / 8 with next "Configuration worksheet", the notes, the timer and the clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 in each |
| Static | grep | 1 `<link>` and 2 `<script src>`. 0 inline scripts, 0 `<style>`, 0 `style=`. 8/8 empty `.snum`. 0 `h1`. 1 `.key`. "Ember" appears only in provenance HTML comments, as in the accepted decks |

## Screenshot paths

- `/tmp/working-smarter-reference-pass1/01–08.png`
- `/tmp/working-smarter-reference-pass2/01–08.png`
- `/tmp/working-smarter-reference.pdf`
- `/tmp/wsr-pdf-p-7.png`
- `/tmp/working-smarter-reference-notes/08.png`
- `/tmp/working-smarter-reference-pw/05.png`

Physical projector rendering and the availability of external links were not checked.

## Parent acceptance

Parent opened all eight final pass-2 slides, notes-8, presenter-5 and rendered PDF page 7. All fit and match accepted reference patterns; no corrections needed. Worker opened all sixteen images across two complete passes. Parent reran the audit (8/8, zero errors), confirmed eight PDF pages and clean console, and verified all 138 protected hashes unchanged. Weakest: 01 (sparse opener), 03 (airy rows), 02 (wrapped table row under two-line headline). Removed title dot only; numbering is generated. No unavailable media, unfit slides or new components. Physical projector and external link availability were not checked.
