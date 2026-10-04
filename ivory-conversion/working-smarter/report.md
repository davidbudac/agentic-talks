# Working Smarter with Agents: Ivory conversion report

- **Output:** `working-smarter-ivory.html` (new file). Source `working-smarter.html` was only read (mtime still 2026-10-03 21:59; its `M` git status predates this task).
- **Slide count:** 44 source → 44 Ivory, order unchanged. `data-origin-slide`: 1, 2, 49, 50, 51, 52, 53, 54, 56, 57, 58, 4, 6, 13, 15, 18, 19, 24, 25, 21, 22, 28, 31, 33, 34, 36, 38, 43, 41, 46, 47, 44, 60, 63, 65, 67, 72, 74, 75, 77, 79, 80, 82, 83.
- **Artifacts in this folder:** `inventory.md` (per-slide mapping), `audit.json` (shared `ivory-conversion/audit.py`), `content-diff.txt` (per-slide label/origin/raw-notes/href/media/text comparison with every difference explained), this report.
- Worker staged or committed nothing. No file outside `working-smarter-ivory.html` and this folder was written. `ivory_design_system/`, `assets/`, other decks, references, README/index, `reviews/`, `workshops/` and `style-mockups/shots/` are untouched.

## Parent acceptance after authorized resume

The user authorized continuation after the screenshot failure. The parent captured slide 10 alone successfully, then slides 11–44 sequentially, with no other capture worker running. `/tmp/working-smarter-pass2/` now contains all 44 images. The parent personally opened every pass-2 image, plus notes 21 and presenter 13. No layout changes were needed. Both complete visual passes are now finished.

The parent independently confirmed the PDF has 44 pages, the audit has no structural or per-slide errors, and all 138 protected file hashes remain unchanged. `/tmp/ws-resume.log` contains zero `CONSOLE` lines, as do the three earlier logs. The weakest slides remain 21 (early video frame), 08 (dense 40px table, fits), and 02 (uneven content across equal-width schedule columns). No unfit content or unavailable media. Memory pressure is a possible cause of the initial failure, not a confirmed diagnosis.

The following incident record describes the earlier incomplete run; it is retained for transparency.

## Initial screenshot failure (resolved by parent)

- **Pass 1** (`/tmp/working-smarter-pass1/01–44.png`) completed: 44 PNGs, all opened.
- **Pass 2** (`CHROME_LOG=/tmp/ws-chrome2.log ivory_design_system/tools/shoot.sh working-smarter-ivory.html /tmp/working-smarter-pass2`) failed with `shoot.sh: Chrome failed on slide 10; remaining slides not attempted`. The run was outside the sandbox and shoot.sh was unmodified, with no `--disable-gpu`.
  - The log has no output from the slide-10 Chrome process. Its last lines are slide 09's normal write and shutdown, plus the usual `CVDisplayLinkCreateWithCGDisplay` noise. So the process exited non-zero without logging a cause. It contains 0 `CONSOLE` lines.
  - `/tmp/working-smarter-pass2/` holds 01–09 only. I opened all nine.
- **I did not restart the pass**, as instructed. **Pass 2 slides 10–44 still need to be shot and viewed by the parent.**
- **Process slip:** I chained the PDF, notes and presenter commands after the pass-2 command with `&&` through `| tail -1`. That made the chain ignore the pass-2 failure, so those three Chrome runs went ahead **after** it. All three succeeded (outputs below).
- No markup changed between pass 1 and pass 2: the deck's mtime (18:47) is before both runs. Pass-2 slides 10–44 should therefore match pass-1 images that were already viewed. Still, that is not a second visual pass, and I do not claim one.

## Content comparison (`audit.py` → `audit.json`, plus `content-diff.txt`)

- `audit.py` exits 0 with no structural errors and no per-slide errors.
- `data-label`, `data-origin-slide` and the **raw** `data-speaker-notes` attribute text are byte-identical on all 44 slides.
- Hrefs are identical on every slide:
  - slide 43: `working-smarter-reference.html` (link to the original reference deck, kept as is);
  - slide 44: the 5 documentation URLs.
- Media: slide 21 `assets/anim/subagents-light.mp4` → `assets/anim/subagents-ivory.mp4` (existing file, as instructed).
- Code panels: every non-blank source line is reproduced character for character, including leading indentation (slides 29, 35).
- Visible text (whitespace-normalized) is identical on all slides except:
  - **01:**
    - title dot `.` removed;
    - "Revised October 2026" moved from `.ts-top .meta` to the `.meta` row as label "Revised" + "October 2026" (same words);
    - mono label "Author" added before "David Budáč".
  - **03, 05, 27, 36:** mono labels `01 02 03` added to the three-card tiles.
  - All slides: the Ember hand-written `.snum` digits were removed (deck.js numbers the slides).
- Whitespace-only changes:
  - slides 06, 10, 39 and 41 drop the blank lines inside the Ember raw-text code;
  - slide 43's second `.note` (the reference link) became `.src`, with the same text and href, because Ivory allows one footnote per slide.

## Removed source text

- The title dot "." (`<span class="dot">`) on slide 01. Nothing else.
- There was no `.ts-loopline` in this deck.
- No text was moved into speaker notes or hidden.

## Additions

- The "Author" and "Revised" meta labels on slide 01.
- `01–03` labels on slides 03, 05, 27 and 36.
- CSS-generated line numbers on the 12 code panels.
- `.k`/`.c`/`.key` emphasis spans inside code (text unchanged).
- **Not added:** a "Length 44 slides" meta cell (new text; same decision as cost-and-context and subagents-prompt-caching), and no `--deck-total` style line (deck.js sets `NN / 44`).

## Decisions

- **Twins reused:** slides 12–36 reuse the committed, parent-reviewed markup from `cost-and-context-ivory.html`, `orchestrating-agents-ivory.html` and `agentic-engineering-ivory.html`, because their sources match these slides word for word. Only `data-origin-slide` and the comment changed, and slide 36's hand-written `20` became empty.
- **Slides 03–11 and 37–41 have twins only in the uncommitted `measuring-what-works-ivory.html`.** I used those as reference, made the same component choices, and checked each one myself. One difference: slide 08 uses `.tbl.lg` to match committed slide 24, which has the same shape.
- **Clay**, one element each:
  - 01: the header label (title-slide rule);
  - 06: `pass`, the single success;
  - 13: total `$0.0506`;
  - 15: the Keep tile;
  - 17: the After tile;
  - 26: the Concrete control header;
  - 41: `WITHOUT`, the negation.

  Every other slide has none. Slide 42 (intended vs faulty transcript) is deliberately neutral: the error is a *missing* word, so no element can carry the point.
- **Size steps:**
  - Code at 40px everywhere except slide 31 (`.reg`, 8 lines). The longest 40px line is 60 chars against the 64 limit, and nothing is clipped.
  - Tables use `.lg` only for 3-row two-column tables (08, 12, 14, 24, 26, 28).

## Unfit slides / new components needed

- None. Every slide maps to an existing kitchen-sink component.
- Every headline is at most two lines, and every footnote is one line.
- No SVG, so nothing to redraw.

## Unavailable media

- None. `assets/anim/subagents-ivory.mp4` exists and loads with no console errors.
- As in the other decks, the static shot shows only the video's first frame (a lone "MAIN AGENT" box).

## Three weakest slides

1. **21 Subagents.** In static shots, the PDF and thumbnails, the right half reads as almost empty (the video's first frame). It plays live. A media re-render would fix it, which is out of scope.
2. **08 Annotated trace** (and its twin 24). A 40px three-row table under a two-line headline packs the two-line cells right under the header rule. That makes it the tightest table in the deck. Dropping to 30px (`.tbl` default) would loosen it, but would diverge from approved slide 24. Parent's call.
3. **02 Workshop route.** `.tbl.c3` gives "Time" (`50 min`) a 568px column. The last column's longest cell ends at about x 1778, so it fits but uses the full width, and the Break row's empty cell leaves a gap. There is no better existing component for a 3 × 5 schedule.

Runners-up:

- **31:** the generated line numbers 05–08 sit beside the markdown steps "1."–"4.". These are not line references, so nothing in the text is wrong.
- **20, 22, 32:** sparse two-card slides (valid ks-05 anatomy).

## Checks run

All Chrome runs were outside the sandbox. `shoot.sh` was unmodified and `--disable-gpu` was not used.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/ws-chrome1.log ivory_design_system/tools/shoot.sh working-smarter-ivory.html /tmp/working-smarter-pass1` | 44 PNGs, **all 44 opened** and checked against §10. No markup fix was needed (slide 08 was reconsidered and kept for consistency with 24) |
| Pass 2 | `CHROME_LOG=/tmp/ws-chrome2.log … /tmp/working-smarter-pass2` | **Failed on slide 10**. 01–09 written and all opened (identical to pass 1). Not restarted |
| Console | `grep -c CONSOLE /tmp/ws-chrome1.log /tmp/ws-chrome2.log /tmp/ws-chrome-extra.log` | 0, 0, 0 |
| PDF | `CHROME_LOG=/tmp/ws-chrome-extra.log ivory_design_system/tools/shoot.sh --pdf working-smarter-ivory.html /tmp/working-smarter.pdf`, then `pdfinfo` | Pages: 44; 1440 × 810 pt (ran after the pass-2 failure, see above). PDF pages were not opened |
| Notes panel | `QUERY=chrome … /tmp/working-smarter-notes 21 21` | Opened: "NOTES · SUBAGENTS · 21 / 44", full notes text, Notes/Present/Fullscreen buttons |
| Presenter | `QUERY=pw … /tmp/working-smarter-pw 13 13` | Opened: current 13 / 44 with clay total, next slide 14, notes, elapsed timer, clock |
| Content | `python3 ivory-conversion/audit.py working-smarter.html working-smarter-ivory.html` | Exit 0; differences only as listed |
| Static | grep / python | 1 `<link>` (styles.css), 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 44/44 empty `.snum`. 0 dark/light/reveal/dot/ts-* classes. 0 Ember or Google Fonts refs. Exactly 1 `.zone` + 1 `.note` per content slide |

### §10 checklist from the pass-1 images (01–44) and pass-2 images (01–09)

- Header label, `NN / 44` and the 108 hairline are correct on every slide. Headlines start at 172:
  - one line: 02, 04, 07, 09–14, 16, 18, 20, 22, 23, 26, 30–34, 43, 44;
  - two lines: the rest.
- Zones end on 888: table rows, card cells, row lists and code panels. The split on 21 ends its rows at 888.
- Nothing crosses the margins, and no code line is clipped. The footer holds only `.note`, plus `.src` on 43.
- Content text is 30/40px only, and labels are mono uppercase. Clay appears as listed under Decisions. All slides are light, with no fills except the paper code panels.
- Letterforms are Geist and Geist Mono. `→`, `≈` and `÷` come from the fallback font, as the spec expects.

### Screenshot paths

- `/tmp/working-smarter-pass1/01–44.png`
- `/tmp/working-smarter-pass2/01–09.png` (incomplete)
- `/tmp/working-smarter-notes/21.png`
- `/tmp/working-smarter-pw/13.png`
- `/tmp/working-smarter.pdf`
