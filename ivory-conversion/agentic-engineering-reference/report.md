# Agentic Engineering — Optional Reference: Ivory conversion report

- **Output:** `agentic-engineering-reference-ivory.html` (new file). The source `agentic-engineering-reference.html` was only read. It is still untracked (`??`), and its mtime is still 2026-10-03 21:59.
- **Slide count:** 10 source → 10 Ivory, order unchanged. `data-origin-slide`: (none), 8, 18, 28, 33, 47, 53, 56, 58, 60. Slide 01 has no origin in the source either.
- **Artifacts in this folder:**
  - `inventory.md`: per-slide mapping;
  - `audit.json`: output of the shared `ivory-conversion/audit.py`;
  - `content-diff.txt`: per-slide label, origin, raw notes, hrefs and text, with every difference explained;
  - this report.
- **Scope:** nothing was staged or committed. The only files written are the deck and this folder. `ivory_design_system/` is unchanged (`git diff` is clean, and `git status` shows nothing for it). No media, other decks, references, README/index, `reviews/`, `workshops/` or `style-mockups/shots/` were touched.

## Content comparison

- `audit.py` exits 0, with no structural errors and no per-slide errors.
- `data-label`, `data-origin-slide` and the raw `data-speaker-notes` are byte-identical on all 10 slides.
- Hrefs are identical on every slide, including all 10 links to the original deck `agentic-engineering.html`.
- All 44 source code lines (including blank lines and indentation) appear character for character in the output.
- Text differences, all explained in `content-diff.txt`:
  - **A.** On slides 02–10, the reference banner merged into the crumb, with the label first and one `·` added.
  - **B.** Slide 10 gains mono URL lines under the link titles (`.links` anatomy, verbatim from the committed twin agentic-engineering 30).
  - **C.** The Ember `.snum` digits are now filled by deck.js.

## Removed source text

- None.
- There was no title `.dot` and no `.ts-loopline` in this source.
- Nothing was moved into the notes or hidden.

## Additions

- `·` separator in the crumb on slides 02–10.
- Six mono URL `.u` lines on slide 10.
- CSS line numbers on the 5 code panels.
- `.c`, `.k` and `.key` emphasis spans inside code (text unchanged).
- No mono tile labels were added.
- No `--deck-total` `<style>`: deck.js sets `NN / 10`.

## Decisions

- **Slide 01:**
  - The inline-styled `h1` ("Engineering reference") became an `h2` on a normal content slide with `.cards.c2`. The source has no subtitle or meta for `.title-slide`, and its two cards plus the return link need a zone and a `.note`.
  - It has no clay. The title-slide clay header label does not apply, because this is not a title slide.
- **Twins reused verbatim:** 03 (cost-and-context), 05 (subagents-prompt-caching), 07 (orchestrating-agents / working-smarter) and 10 (agentic-engineering 30).
- **Size steps:** every code panel is `.code.reg` at 30px. They have 8–11 lines, and the twins 05 and 07 are `.reg`. Cards are at 40px and the `ul.bul` at 30px.
- **Clay**, one element each:
  - 04: the quadratic total formula;
  - 05: the break-even inequality (twin);
  - 06: `latest_failures = result.failures`, the "retry edge" named in the headline.

  All other slides have none.

## Unfit slides / new components needed

- None. Every headline is one or two lines, every footnote is one line, and no code line is clipped.
- No new component was needed. However, **root DESIGN.md has no rows for `reference-slide` / `reference-title`**. The parent may want to record the crumb-merge and `h1`→`h2` decisions there before the remaining eight reference decks.

## Unavailable media

- None. This deck has no video, SVG or images.

## Three weakest slides

1. **01 Reference guide.** Two short tiles bottom-aligned in a 562px zone leave the top ~60% of the zone empty. That is valid ks-05 anatomy, but sparse. It is also the deck opener with no title-slide treatment.
2. **02 Explore a transformer.** The left tile is two links only, so its text ends about 55px above the right tile's. The cells are uneven, though the headings align.
3. **09 Plugin publication recipe.** It has no clay and an empty line 04. The tree lines and the numbered steps 1–4 sit beside generated line numbers 05–08, which could be misread as references. They are not; the text is unchanged.

## Checks run

All Chrome runs were outside the sandbox, one at a time, with `shoot.sh` unmodified and no `--disable-gpu`. Every run exited 0.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/aer-chrome1.log ivory_design_system/tools/shoot.sh agentic-engineering-reference-ivory.html /tmp/agentic-engineering-reference-pass1` | 10 PNGs, **all opened**, §10 checklist passed, no fixes needed |
| Pass 2 | `CHROME_LOG=/tmp/aer-chrome2.log … /tmp/agentic-engineering-reference-pass2` | 10 PNGs, **all opened**, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/aer-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf agentic-engineering-reference-ivory.html /tmp/agentic-engineering-reference.pdf`, then `pdfinfo` | Pages: 10; 1440 × 810 pt. PDF pages were not opened |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/aer-chrome-notes.log … /tmp/agentic-engineering-reference-notes 2 2` | Opened: "NOTES · EXPLORE A TRANSFORMER · 2 / 10", full notes, buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/aer-chrome-pw.log … /tmp/agentic-engineering-reference-pw 6 6` | Opened: 6 / 10 current, next = Skill file example, notes, timer, clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0, 0, 0, 0, 0 |
| Content | `python3 ivory-conversion/audit.py agentic-engineering-reference.html agentic-engineering-reference-ivory.html` | Exit 0; differences only as listed |
| Static | grep | 1 `<link>` (styles.css), 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 10/10 empty `.snum`. 0 dark/light/reveal/dot/ts-*/slide-content. 0 Ember or Google Fonts references |

### §10 checklist (both passes)

- Header label, `NN / 10` and the hairline at 108 are correct on every slide. Headlines start at 172:
  - one line: 01, 03, 06, 07, 09, 10;
  - two lines: 02, 04, 05, 08.
- Cards, rows, code panels and link columns all end on 888. Nothing crosses the margins, and no code is clipped.
- The footer holds only `.note`.
- Content text is 30/40px only, and labels are mono uppercase. Clay appears as listed above. All slides are light; the only paper fill is the code panels.
- Letterforms are Geist / Geist Mono. The `→` on slide 05 comes from the fallback font, as the spec expects.

### Screenshot paths

- `/tmp/agentic-engineering-reference-pass1/01–10.png`
- `/tmp/agentic-engineering-reference-pass2/01–10.png`
- `/tmp/agentic-engineering-reference-notes/02.png`
- `/tmp/agentic-engineering-reference-pw/06.png`
- `/tmp/agentic-engineering-reference.pdf`

## Parent acceptance

The parent opened all ten final pass-2 images, the notes panel on 02 and the presenter view on 06. No fixes were needed. Independent audit passed with 10 slides and no structural or per-slide errors; PDF count is 10, all five logs have zero CONSOLE lines, and all 138 protected files retain their original hashes.

The reference-banner merge into the header and the ordinary content-slide opener are accepted as the pattern for the remaining references. These use existing components and need no design-system addition. The sources layout matches the finished example. Parent's three weakest slides are 01 (sparse opener), 02 (unequal text heights in the pair), and 09 (generated line numbers alongside numbered steps); all fit and preserve content. The historical worker scope statements above precede this parent review and commit.
