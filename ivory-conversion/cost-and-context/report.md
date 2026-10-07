# Cost & Context: Ivory conversion report

- **Output:** `cost-and-context-ivory.html` (new conversion). Source `cost-and-context.html` was only read.
- **Slide count:** 17 source → 17 Ivory. The order is unchanged and `data-origin-slide` matches 1, 2, 13, 4, 5, 6, 15, 17, 18, 19, 21, 22, 23, 24, 25, 26, 28.
- **Artifacts in this folder:** `inventory.md` (per-slide mapping), `compare.py` (content comparator plus static checks) and `content-diff.txt` (its output).
- The conversion worker wrote only the new deck and this audit folder. The parent reviewed and committed the finished result separately.

## Content comparison (compare.py → content-diff.txt)

- `data-label`, `data-origin-slide` and the raw `data-speaker-notes` attribute are identical on all 17 slides (byte comparison of the attribute text).
- The hrefs are identical on all slides: `cost-and-context-reference.html` on slide 16, plus the three source URLs on slide 17. The only media change is on slide 12: `assets/anim/subagents-light.mp4` → `assets/anim/subagents-ivory.mp4` (existing file, as instructed).
- Visible text, ignoring whitespace and the old hand-written slide digits, is identical on slides 02–17.
- Slide 01 differences, all intended:
  1. **Removed:** the title dot `.` (`<span class="dot">.</span>` after "Cost & Context").
  2. **Moved:** "Revised October 2026" goes from the top bar (`.ts-top .meta`) into the `.meta` row as label "Revised" + "October 2026". Same words.
  3. **Added:** the mono label "Author" in front of "David Budáč" (Ivory title `.meta` anatomy).
  4. **Added:** a `<br>` in the subtitle after "Measure a whole task." This is whitespace only and stops "finish." from wrapping alone.
- Added decoration on other slides: `01–03` row counters on slide 02 (agenda) and slide 16 (`ol.bul`), and code line numbers `01–05` on slides 09 and 14. These come from CSS, not text.

## Removed source text

Only the title dot "." on slide 01. The deck had no `.ts-loopline`, so no loopline text was removed. No other source text was removed or moved into notes.

## Additions

- The "Author" label on slide 01.
- CSS counters and line numbers, as listed above.
- The `.lab` mono labels on slides 07, 10 and 11 are the former `h3.k` card titles, restyled with the same text.
- **Not added:** a "Length 17 slides" meta cell, which the agentic-engineering example has, because it would be new visible text. The parent may want it for consistency.
- **Not added:** a `<style>:root{--deck-total:…}` line. The brief forbids style elements, and deck.js sets the total (the screenshots show `NN / 17`).

## Structural changes worth a look

- **Slide 16:** the source had two `.note` paragraphs. Ivory allows one footnote, so the second (the reference link) became `.src`. It has the same text and href and now renders as a mono 20px link at y 1027.
- **Slide 17:** sources stay a `ul.bul` of three links. `.links` needs two balanced columns with headings, and the source has neither.
- **Clay:** used on slides 06 (total `$0.0506`), 07 (Keep tile) and 10 (After tile), one element each. Every other slide has none.

## Unfit slides / new components needed

None. Every slide maps to an existing kitchen-sink component, and no headline exceeds two lines. No code line exceeds its limit: the longest is 59 chars against a 64-char limit at 40px. No new component is needed.

## Unavailable media

None. `assets/anim/subagents-ivory.mp4` exists and renders, and its ivory ground is invisible against the slide in the screenshots. Media files were not changed.

## Three weakest slides

1. **12 Subagents.** At the screenshot's virtual-time budget the video shows only the opening frame (a lone "MAIN AGENT" box). The right half of the slide reads as empty in a static shot, PDF or thumbnail. It plays live, and the example deck's slide 19 has the same behaviour.
2. **11 Continue or reset.** Two short card bodies sit on the zone bottom with mono labels at the top, leaving a large empty middle. This is valid `.cards.c2` anatomy (it matches ks-05), but it is the sparsest content slide. The same applies to a lesser degree to 07 and 10.
3. **17 Sources.** Three short link rows at 30px across full width leave each row mostly empty. Without headings or URL lines it looks plainer than the example's `.links` slide. That was a deliberate choice to avoid adding text.

Also worth a decision: **15** might deserve `th.key` on column B (the rewrite under test). It was left neutral as a set of equal checks.

## Checks run (all Chrome runs outside the sandbox; shoot.sh unmodified, no `--disable-gpu`)

| Check | Command | Result |
|---|---|---|
| Pass 1 screenshots | `CHROME_LOG=/tmp/cc-chrome1.log ivory_design_system/tools/shoot.sh cost-and-context-ivory.html /tmp/cost-and-context-pass1` | 17 PNGs. All opened and checked against the §10 checklist. One fix: the slide 01 subtitle orphan |
| Pass 2 screenshots | `CHROME_LOG=/tmp/cc-chrome2.log ivory_design_system/tools/shoot.sh cost-and-context-ivory.html /tmp/cost-and-context-pass2` | 17 PNGs. All opened and checked; no issues |
| Console | `grep -c CONSOLE /tmp/cc-chrome1.log /tmp/cc-chrome2.log` | 0 and 0 |
| PDF | `ivory_design_system/tools/shoot.sh --pdf cost-and-context-ivory.html /tmp/cost-and-context.pdf`; `pdfinfo` | Pages: 17; page size 1440 × 810 pt |
| Notes panel | `QUERY=chrome … /tmp/cost-and-context-notes 12 12` | `/tmp/cost-and-context-notes/12.png`: notes panel shows "NOTES · SUBAGENTS · 12 / 17" and the full notes; buttons present |
| Presenter | `QUERY=pw … /tmp/cost-and-context-pw 6 6` | `/tmp/cost-and-context-pw/06.png`: current slide 06, next slide 07, notes, timer and clock |
| Static | `python3 ivory-conversion/cost-and-context/compare.py` | 1 `<link>` (Ivory styles.css) and 2 `<script src>` (deck-stage.js, deck.js). 0 inline script bodies, 0 `<style>` elements, 0 `style=` attributes. 17 empty `.snum`. No dark/light/reveal/dot/ts-* classes. 0 Ember refs, 0 Google Fonts refs. One `.note` per content slide |

### §10 checklist summary (from looking at the pass 2 PNGs)

- Header label, `NN / 17` and the hairline at 108 are correct on every slide. Headlines are one line (02–04, 06, 08, 09, 11, 14, 16, 17) or two lines (05, 07, 10, 12, 13, 15).
- Zones end on the 888 hairline: rows, cells, table bottoms and code panels.
- Nothing crosses the margins, and no code line is clipped. The footer holds only `.note` (plus `.src` on slide 16).
- Content text is 30px or 40px only, and labels are mono uppercase. Clay appears as listed above. All slides are light, with no fills, shadows or icons.
- Letterforms are Geist and Geist Mono, and match `shots/`.

Screenshot paths: `/tmp/cost-and-context-pass1/01–17.png`, `/tmp/cost-and-context-pass2/01–17.png`, `/tmp/cost-and-context-notes/12.png`, `/tmp/cost-and-context-pw/06.png`, `/tmp/cost-and-context.pdf`.

## Parent review

The parent opened all 17 pass-2 images and both notes/presenter images, independently checked metadata and href preservation, confirmed the 17-page PDF and zero CONSOLE messages, and accepted the conversion. No unfit slides found. The worker completed both full look-and-fix passes; the parent performed an additional full final-image review.
