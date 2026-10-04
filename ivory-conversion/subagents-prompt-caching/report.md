# Subagents & Prompt Caching: Ivory conversion report

- **Output:** `subagents-prompt-caching-ivory.html` (new file). Source `subagents-prompt-caching.html` was only read.
- **Slide count:** 21 source → 21 Ivory. Order is unchanged. `data-origin-slide` is 1, 2, 6, 7, 9, 10, 11, 12, 14, 16, 17, 22, 25, 27, 28, 29, 31, 33, 35, 38, 39.
- **Artifacts in this folder:** `inventory.md` (per-slide mapping), `audit.json` (output of the shared `ivory-conversion/audit.py`), `content-diff.txt` (raw attribute/href/media byte comparison plus the audit's text changes), and this report.
- The worker wrote only the new deck and this folder. The parent reviewed the result and owns staging and commits.

## Content comparison

- `data-label`, `data-origin-slide` and the raw `data-speaker-notes` text are byte-identical on all 21 slides.
- Hrefs are identical on every slide, including `subagents-prompt-caching-reference.html` (slide 20) and the 3 documentation URLs, which appear 8 times in total.
- Media changes, as instructed: slide 04 `assets/anim/subagents-light.mp4` → `subagents-ivory.mp4`, and slide 12 `assets/anim/kv-cache-light.mp4` → `kv-cache-ivory.mp4`. Both files already existed; no media files were changed.
- Visible text (`audit.py`, whitespace-normalized) is identical on slides 02–04 and 06–21. The only differences are:
  - **Slide 01:**
    - Removed the title dot `.` (`<span class="dot">`).
    - "Revised October 2026" moved from `.ts-top .meta` into the `.meta` row as the label "Revised" + "October 2026". The words are the same.
    - Added the mono label "Author" before "David Budáč".
  - **Slide 05:** added the `01 02 03` mono labels on the numbered lifecycle cards.
- **Slide 03 text order:** the SVG puts the text in source order: "Your computer", its 3 items, "Provider cloud", its 3 items, then "request → network → response". `audit.py` reports no change.
- Decoration that comes from CSS, not text: code line numbers on slides 07, 10, 11, 13, 15 and 18.

## Removed source text

- The title dot "." on slide 01. That is all.
- There was no `.ts-loopline`. Nothing was moved into the speaker notes.

## Additions

- The "Author" and "Revised" meta labels on slide 01.
- `01–03` labels on slide 05.
- The slide 03 diagram structure: boxes, arrows and dashed boundaries. It adds no new words.
- `<code>` (mono) around the two usage-field names on slide 17. The text is unchanged.
- `.k` / `.c` / `.a` emphasis spans inside the code panels. The text is unchanged.
- **Not added:** a "Length 21 slides" meta cell, which would be new text (same decision as cost-and-context). No `--deck-total` style line either.

## Structural decisions worth a look

- **Slide 03 (`.lead` + two `<br>` cards):** this has no Ivory equivalent. I restructured it into a full-width 1:1 topology SVG (§8 option a). The text is unchanged, and diagram text keeps the source case (the Ember h3 was not uppercased).
  - Pass 1 caught that its headline wraps to 2 lines, so the first `0 0 1680 562` viewBox scaled down off the grid. It was redrawn at `0 0 1680 480`. Pass 2 confirms the edges sit at 120/1800 and 408/888.
  - The parent accepted this diagram during visual review. The alternative is `.cards.c2` with the lead line folded somewhere, which would mean either a third tile or the footnote, and the footnote already exists.
- **Slide 20:** the second `.note` (reference link) became `.src`, because Ivory allows one footnote.
- **Links inside notes (slides 06, 13, 16, 18, 19):** they stay inline in the single `.note`. Each still fits on one line.
- **Clay:** the title header and the break-even formula on slide 15. Other slides are equal items, neutral procedures or tables.
  - Parent review marked only `w + (n − 1)r < n` on slide 15 with `.key`, as the single result of the calculation. Slide 17 remains neutral because reads and writes are equal categories.
- **Code size steps:** `.reg` (30px) on slides 10 and 15, which have 9 lines. The other code panels are 40px. No line exceeds its limit: the longest at 40px is slide 18 line 3, 61 chars against a limit of 64, and it is not clipped.

## Unfit slides / new components needed

- No new component is needed.
- No headline exceeds 2 lines. All are one line except slides 02–05, 10, 12, 13, 15, 18 and 19, which wrap to two balanced lines.
- No footnote wraps.
- The only slide without a direct equivalent is 03 (`.lead`), which I handled as described above.

## Unavailable media

None. Both `-ivory.mp4` files exist and load, with no console errors.

At the screenshot time budget, both videos show only their opening frame:

- Slide 04 shows a lone "MAIN AGENT" box.
- Slide 12 shows a blank ivory frame. I checked with `ffmpeg`: frame 0 of `kv-cache-ivory.mp4` is blank (3.8 KB PNG), and frames at 1 s and 2 s have content. So this is not a load failure.

## Three weakest slides

1. **12 KV caching.** In static shots, the PDF and thumbnails, the right half is empty because the video's first frame is blank. It plays live. The example deck's slide 17 has the same behaviour. A re-render with a non-blank first frame would fix it, but media changes are out of scope.
2. **04 Subagents.** The same problem, less severe: the static frame shows only "MAIN AGENT", so the figure reads as nearly empty in print.
3. **18 Warm-up before fan-out.** The source writes "1." … "4." inside a code panel, so the panel's line numbers (01–04) duplicate the step numbers. `ol.bul` would duplicate the counters too unless the "1." text were removed, which is a wording change. I kept it as is.
   - Runners-up: slides 02, 08 and 19, which are sparse two- or three-card slides (valid ks-05 anatomy, large empty middle).

## Checks run

All Chrome runs were outside the sandbox. `shoot.sh` was not modified and `--disable-gpu` was not used.

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/spc-chrome1.log ivory_design_system/tools/shoot.sh subagents-prompt-caching-ivory.html /tmp/subagents-prompt-caching-pass1` | 21 PNGs, all opened. 1 fix: the slide 03 SVG viewBox (562 → 480) |
| Pass 2 | `CHROME_LOG=/tmp/spc-chrome2.log ivory_design_system/tools/shoot.sh subagents-prompt-caching-ivory.html /tmp/subagents-prompt-caching-pass2` | 21 PNGs, all opened, no issues |
| Console | `grep -c CONSOLE /tmp/spc-chrome1.log /tmp/spc-chrome2.log` | 0 and 0 |
| PDF | `ivory_design_system/tools/shoot.sh --pdf subagents-prompt-caching-ivory.html /tmp/subagents-prompt-caching.pdf`, then `pdfinfo` | Pages: 21; 1440 × 810 pt |
| Notes panel | `QUERY=chrome … /tmp/subagents-prompt-caching-notes 4 4` | `04.png`: "NOTES · SUBAGENTS · 4 / 21", full notes, buttons visible |
| Presenter | `QUERY=pw … /tmp/subagents-prompt-caching-pw 15 15` | `15.png`: current 15, next 16, notes, elapsed timer, clock |
| Content | `python3 ivory-conversion/audit.py subagents-prompt-caching.html subagents-prompt-caching-ivory.html > …/audit.json`, plus the raw comparison in `content-diff.txt` | 21/21. No structural errors. Text differences only as listed above |
| Static | grep | 1 `<link>` (styles.css), 2 `<script src>` (deck-stage.js, deck.js), 0 inline scripts, 0 `<style>`, 0 `style=`. 21 empty `.snum`. No dark/light/reveal/dot/ts-* classes, no Ember or Google Fonts references. Exactly 1 `.zone` and 1 `.note` per content slide |

### §10 checklist (from looking at the pass-2 PNGs)

- Header label, `NN / 21` and the hairline at 108 are correct on all slides. Headlines start at 172 and are at most 2 lines.
- Zones end on the 888 hairline: card cells, table rows, row lists, code panels and the slide 03 figure.
- Nothing crosses the margins. No clipped code. The footer holds only `.note` (plus `.src` on slide 20).
- Content text is 30px or 40px only, and labels are mono uppercase. Diagram text is mono 26/20px.
- All slides are light. There are no fills except the paper code panels, and no shadows or icons. Clay appears on the title header label and, after parent review, the slide 15 formula.
- Letterforms are Geist and Geist Mono. Arrows (→) are drawn by the fallback font, which the spec expects.

Screenshot paths:

- `/tmp/subagents-prompt-caching-pass1/01–21.png`
- `/tmp/subagents-prompt-caching-pass2/01–21.png`
- `/tmp/subagents-prompt-caching-notes/04.png`
- `/tmp/subagents-prompt-caching-pw/15.png`
- `/tmp/subagents-prompt-caching.pdf`

## Parent review

The parent opened all 21 final images and both notes/presenter views; independently checked slide count, raw notes, metadata and hrefs; confirmed zero CONSOLE messages and a 21-page PDF. All content fits. The slide 03 diagram is accepted. A final accent-only adjustment highlights the slide 15 break-even formula; its screenshot and presenter view were refreshed and opened, and the PDF regenerated. Final overrides: `/tmp/subagents-prompt-caching-parent/15.png`, `/tmp/subagents-prompt-caching-parent-pw/15.png`, `/tmp/subagents-prompt-caching-final.pdf`. All other final images are in pass2.
