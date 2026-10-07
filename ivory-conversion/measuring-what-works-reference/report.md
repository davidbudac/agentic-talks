# Measuring What Works Reference: Ivory conversion report

## Status

- **The deck is ready for parent review.**
  - **Output:** `measuring-what-works-reference-ivory.html` (new file).
  - **Source:** `measuring-what-works-reference.html` was only read. It is still untracked and its mtime is unchanged (3 Oct 21:59).
- **Slide count:** 5 → 5, in source order. `data-origin-slide` is 0, 16, 7, 24, 28.
- **Scope:** nothing was staged or committed, and no subagent was used.
  - The only files written are the deck and this folder (`inventory.md`, `content-diff.txt`, `audit.json`, `report.md`).
  - `ivory_design_system/`, media, other decks, references, README/index, `reviews/`, `workshops/` and `style-mockups/shots/` were not touched.
  - The `M` entries in `git status` were there before I started.

## Decisions

- **01:** uses the accepted cost/subagents-reference opener.
  - Regular `.slide`, crumb "Optional reference".
  - `h2` "Measuring What Works<br>Reference", 2 lines.
  - `.cards.c2`: tile 1 holds the subtitle and "Return to the main talk"; tile 2 holds `h3` "David Budáč" and "Revised October 2026".
  - The footer `.note` holds the banner "Optional reference · Back to the talk" verbatim, with its link.
- **02–05:** the crumb and the banner are merged with a middle dot: "In practice · Optional reference · Back to the talk".
- **02:** `table.tbl` at the default 30px, because it has 4 rows. No clay: the layers are equal.
- **03:** `.code` at 40px.
  - The longest line is 56 characters.
  - Both source blank lines are kept as empty `.l` lines, which has precedent in two accepted references.
  - Clay `.key` is on "independently", the assumption the headline names. **There is no twin for this slide, so this is my call. The parent may prefer no clay.**
- **04:** `ul.bul`, the same markup as the main-deck twin (slide 14). No clay.
- **05:** `.code`, the same markup as the main-deck twin (slide 17).
  - The single blank line is dropped.
  - `.k` is on "Spoken:" and "Check the transcription for:".
  - `.key` is on "WITHOUT".

## Content comparison

- **Shared audit:** `python3 ivory-conversion/audit.py measuring-what-works-reference.html measuring-what-works-reference-ivory.html` exits 0 with no structural or per-slide errors. Output is saved as `audit.json`.
- **Raw byte comparison:** see `content-diff.txt`.
  - `data-label`, `data-origin-slide` and `data-speaker-notes` match on 5/5 slides.
  - Hrefs are identical in order and count on 5/5 slides: `measuring-what-works.html` appears twice on 01 and once on each of 02–05. There are no external links.
  - The code lines on 03 and 05 are byte-identical, including internal spaces.
- **Visible text:**
  - 01 has the same words, reordered into the opener structure. The only removed text is the title dot.
  - 02–05 differ only by the merged crumb and the one added `·`.

## Removed source text

- The title `.dot` "." on slide 01.
- The hand-written `.snum` digits 2/3/4/5. deck.js generates `01–05 / 05` instead.
- Blank code lines on 05 only (one, whitespace only), matching the twin.
- There was no `.ts-loopline`. Nothing was moved into the notes.

## Additions

- One `·` in the crumb on each of slides 02–05.
- `.k` and `.key` spans on 03 and 05. These are styling only; the text is unchanged.
- CSS line numbers in the code panels.
- No labels were invented.

## Unfit slides, missing components, unavailable media

- No slide is unfit.
- No new component is needed.
- No media is expected and none is present.

### Source issues, preserved as found

- **03:** the source's two aligned equations are one space off. The second `=` sits one column left of the first (string index 35 vs 36), and it shows in the render. I kept it byte-for-byte because whitespace in a code line is content. Fixing it means adding one space to the source wording; that is the parent's or user's call.

### Design-system observation, no change made

- In the `QUERY=chrome` notes shot, the panel shows only the first line of the slide 3 notes, and the NOTES / PRESENT / FULLSCREEN buttons overlap that line's end.
  - This is the deck.js/styles.css chrome, not the deck, and the presenter window shows the full notes.
  - Approved `ks-chrome-notes.png` only has a one-line note, so it does not exercise this case.

## Three weakest slides

1. **01:** the same limitations as the accepted openers.
   - The bottom-aligned `.cards.c2` leaves about 270px of empty space above the tile content.
   - The tiles' last lines do not share a baseline: tile 1 ends at about y 840, tile 2 at about y 785.
   - "Optional reference" appears twice (crumb and footer), on purpose.
2. **03:** the second `=` is visibly one column off, inherited from the source. The two blank lines also leave visible gaps in a 6-line panel.
3. **04:** three one-line rows fill a 480px zone, with lines at about 60–70% of the measure. The slide reads airy, but this is valid `ul.bul` anatomy and identical to the accepted twin.

## Checks run

All Chrome runs were outside the sandbox and strictly serial. Each command was run on its own, with no pipes. There were no failures and no retries.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/mwwr-chrome1.log ivory_design_system/tools/shoot.sh measuring-what-works-reference-ivory.html /tmp/measuring-what-works-reference-pass1` | exit 0, 5 PNGs, all opened. §10 checklist clean. No fixes needed; the 03 alignment was traced to the source (above) |
| Pass 2 | `CHROME_LOG=/tmp/mwwr-chrome2.log … /tmp/measuring-what-works-reference-pass2` | exit 0, 5 PNGs, all opened, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/mwwr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf measuring-what-works-reference-ivory.html /tmp/measuring-what-works-reference.pdf`, then `pdfinfo` | Pages: 5, 1440 × 810 pt. Page 3 rendered (`pdftoppm -f 3 -l 3 -r 60`) to `/tmp/mwwr-pdf-p-3.png` and opened; it matches the PNG |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/mwwr-chrome-notes.log … /tmp/measuring-what-works-reference-notes 3 3` | Opened. Shows "NOTES · REPEATED-RUN PROBABILITIES · 3 / 5", notes text and buttons. Panel limitation noted above |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/mwwr-chrome-pw.log … /tmp/measuring-what-works-reference-pw 4 4` | Opened. Shows 4 / 5 with next "Voice input", the full notes, the timer and the clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 in each |
| Static | grep | 1 `<link>` (styles.css) and 2 `<script src>` (deck-stage.js, deck.js). 0 inline scripts, 0 `<style>`, 0 `style=`. 5/5 empty `.snum`. 0 `h1`. No dark/light/reveal/dot/ts-/slide-content/Ember/Google Fonts/reference-banner/pui. Clay: one `.key` on each of 03 and 05 only |

## Screenshot paths

- `/tmp/measuring-what-works-reference-pass1/01–05.png`
- `/tmp/measuring-what-works-reference-pass2/01–05.png`
- `/tmp/measuring-what-works-reference.pdf`
- `/tmp/mwwr-pdf-p-3.png`
- `/tmp/measuring-what-works-reference-notes/03.png`
- `/tmp/measuring-what-works-reference-pw/04.png`

## Parent review: stopped at shared notes-control overlap

Parent opened all five pass-2 slides, notes-3, presenter-4, and rendered PDF page 3. Slide content fits; the independently/WITHOUT focal accents are accepted. Source equation spacing is preserved. Worker opened all ten images over two complete passes. Parent reran the audit (5/5, no errors), verified five PDF pages, zero CONSOLE entries, and all 138 protected hashes unchanged.

The notes-3 image confirms controls obscuring the end of the speaker-note line. The shared `.pui-controls` is fixed at bottom 18px with z-index 40; `.pui-notes` spans the full width with only 24px bottom padding at z-index 39 (styles.css lines 317–334). Thus visible controls cover notes text in the same bottom-right area. Normal mouse activity shows controls for 1.8 seconds; the QUERY=chrome hook keeps them visible. The note is not deleted or intrinsically truncated; the controls obscure part of it. This is the same overlap earlier recorded on agentic-ai-reference slide 6, now isolated as a shared chrome defect.

Following the explicit stop-and-report rule, parent has not committed this deck, changed the design system, or started another worker. Proposed correction: reserve space in the notes overlay for the control row using existing spacing tokens, document and demonstrate long-note behavior in the kitchen sink, and re-run original-slide regression plus notes/presenter checks. No deck-stage.js change is needed. The main slides and PDF are otherwise ready.

## Final parent acceptance after shared fix

The notes overlap is resolved by 1dfdc80. Parent opened the corrected notes-3 screenshot at `/tmp/mwwr-notes-fixed/03.png`: the entire note fits above the buttons. Parent already opened all five final slides, presenter-4 and PDF page 3; worker opened all ten PNGs across two full passes. Final content audit rerun: 5/5, zero errors. Five-page PDF and clean console remain verified. No slide-content changes were needed. Weakest: 01 (sparse opener), 03 (source equation alignment and blank lines), 04 (airy rows). Removed title dot and one blank code line on 05; numbers are generated. No missing media, no unfit slide. Physical projector not checked. All 138 protected hashes remain unchanged.
