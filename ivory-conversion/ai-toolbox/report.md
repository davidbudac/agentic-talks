# AI Toolbox: Ivory conversion report

- **Output:** `ai-toolbox-ivory.html` (new file). Source `ai-toolbox.html` was only read; it already had uncommitted user changes before this work and was not touched.
- **Slide count:** 31 source → 31 Ivory. The order is unchanged. `data-origin-slide` sequence: 1, 2, 3, 23, 5, 6, 7, 25, 22, 18, 14, 15, 17, 4, 20, 27, 28, 29, 31, 33, 37, 38, 41, 45, 53, 49, 48, 47, 54, 56, 57.
- **Artifacts in this folder:** `inventory.md` (per-slide mapping), `audit.json` (raw output of the shared `ivory-conversion/audit.py`), `content-diff.txt` (per-slide summary plus an explanation of every difference) and this report.
- The worker wrote only `ai-toolbox-ivory.html` and this folder. The parent reviewed the result and owns staging and commits. Media and `ivory_design_system/` are unchanged.

## Content comparison

`python3 ivory-conversion/audit.py ai-toolbox.html ai-toolbox-ivory.html` → exit 0, no structural errors, and no per-slide errors on any of the 31 slides:

- `data-label`, `data-origin-slide`, the parsed notes and the **raw** `data-speaker-notes` attribute bytes are identical on all 31 slides.
- The hrefs are identical on all slides: `https://davidbudac.cz` on slide 01; `ai-toolbox-reference.html` and `index.html` on slide 29; 12 source URLs on slide 30 and 14 on slide 31. The `target="_blank" rel="noopener"` attributes are kept.
- Visible text is identical on 28 slides. The three slides with reported differences are explained in full in `content-diff.txt`:
  - **01:** the title dot and loopline were removed, "Revised October 2026" moved into `.meta`, and the "Author" label was added.
  - **03:** comparator artifact only (inline `<b>`/`<span>` in a def row are joined without a space). The words are unchanged.
  - **28:** the SVG labels follow the bullets in DOM order because the figure moved to the right column. Same text, same order.

## Removed source text

1. Slide 01: the title dot "." (`<span class="dot">`).
2. Slide 01: the `.ts-loopline` "chat → agent → toolbox ↺".

Nothing else was removed, and nothing was moved into the speaker notes.

## Additions

- Slide 01: the mono label "Author" (Ivory title `.meta` anatomy). **Not added:** a "Length 31 slides" cell (the example deck has one; it would be new text). The parent may want it for consistency.
- Slide 09: one `&nbsp;` (whitespace only) so that "→" does not start a line.
- CSS-only decoration: row counters 01–03 on slides 03 and 29, and code line numbers on slides 04, 11 and 26.
- No `<style>:root{--deck-total}` line (the brief forbids style elements). deck.js sets `NN / 31`, as the screenshots show.

## Clay

Slides 01 (header label, title exception), 02 ("An editable draft" tile), 05 (Agent tile, formerly `.tile.fill`) and 28 (the MCP hub: box + label, one element). Every other slide has none; they are equal items.

## Unfit slides / new components needed

None. Every slide maps to an existing kitchen-sink component. No headline exceeds two lines (two-line headlines: 04, 14, 23, 26, 27). No code line is over its limit (max 53 chars at 40px). Points that deviate from the spec's recommendations without needing a new component:

- **30 / 31 Sources:** the source has 7 links per column (and 7 + 5 on slide 30). Ivory recommends 3–5 equal links per column. The rows fit (74px rows for 71px of content) but sit tight against the hairlines, and slide 30's columns do not line up. Splitting into more slides or dropping links would change content, so I left both as they are.
- **28 MCP:** the source SVG had diagonal "tangle" lines. The redraw gives each of the 9 app→tool connectors its own orthogonal lane and ports, with dim (`--rule`) 1.5px strokes, so no segments overlap. The boxes are unlabelled, as in the source; I did not invent labels.
- **06 media:** the existing `agent-loop-ivory.mp4` draws curved arcs and uses Geist (sans) box text, which departs from the diagram idiom (orthogonal connectors, mono labels). This is in the asset, not the deck, and the example deck uses the same file. Flagged for whoever owns the renders.

## Unavailable media

None. `assets/anim/agent-loop-ivory.mp4` (1152×912) and `assets/anim/stateless-ivory.mp4` (1200×900) exist and render with an invisible ivory edge. They were not modified.

## Three weakest slides

1. **07 The model has no memory.** At the screenshot's virtual-time budget, `stateless-ivory.mp4` shows only its opening frame (a single "MODEL / forgets all" box at the right edge). The right half reads as empty in static shots, the PDF and thumbnails. It plays live. The parent handles the stateless render separately.
2. **30 Sources 1 of 2.** It has 7 + 5 links, so the rows in the two columns have different heights and do not line up, and the 7-row column is dense. Slide 31 has the same density, but its columns are equal.
3. **28 MCP.** The redrawn N×M tangle is honest and orthogonal, but busy: nine dim connectors with small 8px port jogs. It also has unlabelled boxes, as in the source. It reads clearly at projector scale, but it is the slide most likely to need a design pass.

Parent review fixed the one-word last line on **20** by keeping "repeatable formats" together with a non-breaking space. **13**'s footnote wraps to two lines, allowed without `.src` by sections 4 and 10. The many `.cards.c2` slides (13, 14, 16–21, 23, 24, 27) have the valid but sparse ks-05 anatomy, with a large empty middle.

## Checks run (all Chrome runs outside the sandbox; shoot.sh unmodified, no `--disable-gpu`)

| Check | Command | Result |
|---|---|---|
| Content | `python3 ivory-conversion/audit.py ai-toolbox.html ai-toolbox-ivory.html > ivory-conversion/ai-toolbox/audit.json` | exit 0. 31/31, no structural or per-slide errors |
| Pass 1 | `CHROME_LOG=/tmp/ai-toolbox-chrome1.log ivory_design_system/tools/shoot.sh ai-toolbox-ivory.html /tmp/ai-toolbox-pass1` | 31 PNGs, all opened. One fix (slide 09 arrow at line start) |
| Pass 2 | `CHROME_LOG=/tmp/ai-toolbox-chrome2.log ivory_design_system/tools/shoot.sh ai-toolbox-ivory.html /tmp/ai-toolbox-pass2` | 31 PNGs, all opened. No further fixes |
| Console | `grep -c CONSOLE` on chrome1, chrome2, chrome-notes and chrome-pw logs | 0, 0, 0, 0 |
| PDF | `ivory_design_system/tools/shoot.sh --pdf ai-toolbox-ivory.html /tmp/ai-toolbox.pdf`; `pdfinfo` | Pages: 31; 1440 × 810 pt. Page 28 rendered and viewed (`/tmp/ai-toolbox-pdfp-28.png`) |
| Notes panel | `QUERY=chrome … /tmp/ai-toolbox-notes 28 28` | `/tmp/ai-toolbox-notes/28.png`: "NOTES · MCP · 28 / 31", the full notes and the three buttons |
| Presenter | `QUERY=pw … /tmp/ai-toolbox-pw 5 5` | `/tmp/ai-toolbox-pw/05.png`: current 05, next 06, notes, elapsed timer and clock |
| Static | grep/python | 1 `<link>` (styles.css) + 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 31 empty `.snum`. 0 legacy classes (dark/light/reveal/dot/ts-*/slide-content/fill/hot/on/dg-tangle). 0 Ember or Google Fonts refs. One `.note` on every slide except 01, 28 and 30 (none in source) |

### §10 checklist (from looking at the pass-2 PNGs)

1. Header label left, `NN / 31` right, hairline at 108 on every slide. Headlines start at 172 and use at most 2 lines.
2. The zone starts 72px under the headline. Cards, rows, code panels, link columns and the split rows end on 888.
3. Nothing crosses 888 or the margins. No clipped code. The footer holds only `.note`.
4. Content text is 30/40px only. Labels are mono uppercase.
5. Clay appears as listed above, at most one element per slide.
6. The slide 28 SVG is 1:1 at 828×562 in cols 7–12 (972–1800). The video edges are invisible on 06 and 07.
7. All slides are light, with no fills, shadows, icons, pills or rounded cards.
8. Footnotes are one line, except 13 (two lines, no `.src`).
9. Letterforms are Geist and Geist Mono, matching `shots/` (the arrows → use the system fallback, as the spec expects).

Screenshot paths: `/tmp/ai-toolbox-pass1/01–31.png`, `/tmp/ai-toolbox-pass2/01–31.png`, `/tmp/ai-toolbox-notes/28.png`, `/tmp/ai-toolbox-pw/05.png`, `/tmp/ai-toolbox.pdf`.

## Parent review

The parent opened all 31 pass-2 images and the notes/presenter images, and independently verified raw notes, labels, origins and link targets. No unfit slides. The two dense sources slides are accepted with their documented spacing limitation; no content was omitted. Slide 20 received a whitespace-only orphan fix, then was captured again and opened at `/tmp/ai-toolbox-parent/20.png`. The refreshed `/tmp/ai-toolbox-final.pdf` has 31 pages, and both parent Chrome logs have zero CONSOLE messages. Other final images remain in pass2.
