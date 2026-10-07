# Subagents & Prompt Caching Reference: Ivory conversion report

## Final status (round 2)

- **The deck is ready for parent review.** It has 4 slides and they are in source order.
- **Slide 01 is restructured.** The other slides are unchanged from round 1, where the parent accepted slides 02–04 and the clay on `cache_control`.
- **The r1 "unfit" item is resolved.** The slide 01 title now wraps to 2 lines instead of 3.
- **Scope:** nothing was staged or committed, and nothing outside this folder and the deck was written.
  - The source mtime is unchanged (3 Oct 21:59) and the file is still untracked.
  - There were no design-system changes and no media.

### What changed on slide 01 (r2)

- **Structure:** regular `.slide` with the existing crumb "Optional reference".
- **Title:** `h2` "Subagents &amp; Prompt Caching<br>Reference", 2 lines.
- **Zone:** `.zone > .cards.c2`.
  - Tile 1 holds the `p` subtitle "Supporting procedures and worksheets." and its link "Return to the main talk".
  - Tile 2 holds the `h3` "David Budáč" and the `p` "Revised October 2026".
- **Footer:** `p.note` "Optional reference · Back to the talk", the source banner verbatim with its link.
- **Removed from r1:** `.title-slide`, `h1`, `.sub`, `.meta`, the added "Author" label and the label/value split of "Revised October 2026".
- **Href order:** subtitle link, then footer link. Both point to `subagents-prompt-caching.html`, so the ordered target list is identical to the source.

### Content comparison (r2)

- Raw `data-label`, `data-origin-slide` and `data-speaker-notes` are byte-identical on 4/4 slides. Hrefs are identical in order and count on 4/4 slides.
- `audit.py` exits 0 with no structural errors (`audit-r2.json`).
- Slide 01 has the same words as the source, reordered. The only removed text is the title dot ".".
- Slides 02–04 are as in r1: crumb and banner merged, with one `·` added.

### Removed source text (final)

- The title `.dot` "." on slide 01.
- The `.snum` digits 2/3/4.
- There was no `.ts-loopline`. Nothing was moved into the notes.

### Additions (final)

- The extra crumb `·` on slides 02–04.
- `.key` (clay) on `"cache_control"` on slide 02.
- No added labels on slide 01.

### Unfit slides / unavailable media

- No slide is unfit.
- No new component is needed.
- No media is expected and none is present.

### Three weakest slides (final, concrete layout limitations)

1. **01:**
   - `.cards.c2` bottom-aligns the tiles in the zone, so about 270px of empty tile space sits above the content.
   - The two tiles' last lines do not share a baseline: tile 1 is a 2-line paragraph ending at about y 820, while tile 2 is h3 + 1 line ending at about y 765.
   - The title occupies only about 60% of the measure.
   - "Optional reference" appears twice (crumb and footer), by design, to keep both source occurrences.
2. **04:** two short tiles bottom-aligned in a 480px zone leave the top ~55% of the zone empty. This is valid `.cards` anatomy but sparse.
3. **03:** three one-line `ul.bul` rows are spread over the full zone height. Each row is about 187px tall for one line of 34px text, so the slide reads airy and the lines are only about 60% of the measure.

### Checks run (r2; all Chrome outside the sandbox, strictly serial, no failures, no retries)

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/spcr-r2-chrome1.log ivory_design_system/tools/shoot.sh subagents-prompt-caching-reference-ivory.html /tmp/subagents-prompt-caching-reference-r2-pass1` | exit 0, 4 PNGs, all opened. 01 title is 2 lines, tiles and footer are clear, 02–04 unchanged |
| Pass 2 | `CHROME_LOG=/tmp/spcr-r2-chrome2.log … /tmp/subagents-prompt-caching-reference-r2-pass2` | exit 0, 4 PNGs, all opened, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/spcr-r2-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf subagents-prompt-caching-reference-ivory.html /tmp/subagents-prompt-caching-reference-r2.pdf`, then `pdfinfo` | Pages: 4, 1440 × 810 pt. Page 1 rendered (`pdftoppm -f 1 -l 1 -r 60`) to `/tmp/spcr-r2-pdf-p-1.png` and opened; it matches the PNG |
| Console | `grep -c CONSOLE` on the 3 r2 logs | 0 in each |
| Notes / presenter | reused from r1 (slides 04 and 02 are unchanged) | `/tmp/subagents-prompt-caching-reference-notes/04.png`, `/tmp/subagents-prompt-caching-reference-pw/02.png` |
| Content | `python3 ivory-conversion/audit.py subagents-prompt-caching-reference.html subagents-prompt-caching-reference-ivory.html` | exit 0, saved as `audit-r2.json`. A raw attribute/href re-check gave all OK |
| Static | grep | 1 `<link>`, 2 `<script src>`, 0 inline `<script>`, 0 `<style>`, 0 `style=`. 4/4 empty `.snum`. 0 `h1`, 0 `title-slide` |

### Final screenshot paths

- `/tmp/subagents-prompt-caching-reference-r2-pass1/01–04.png`
- `/tmp/subagents-prompt-caching-reference-r2-pass2/01–04.png`
- `/tmp/subagents-prompt-caching-reference-r2.pdf` and `/tmp/spcr-r2-pdf-p-1.png`
- Notes and presenter shots (r1, still valid): `/tmp/subagents-prompt-caching-reference-notes/04.png` and `/tmp/subagents-prompt-caching-reference-pw/02.png`

### Artifacts

- `inventory.md` (row 01 updated for r2)
- `content-diff.txt` (r2 section appended)
- `audit.json` (r1, historical)
- `audit-r2.json` (final)
- `report.md` (this file)

---

## Round 1 report (historical; slide 01 superseded by round 2)

- **Output:** `subagents-prompt-caching-reference-ivory.html` (new file).
- **Source:** `subagents-prompt-caching-reference.html` was only read. It is still untracked (`??`), and its mtime is still 3 Oct 21:59.
- **Slide count:** 4 source → 4 Ivory. Order is unchanged. `data-origin-slide` is 0, 23, 30, 36.
- **Artifacts in this folder:** `inventory.md`, `audit.json` (shared `ivory-conversion/audit.py`, exit 0), `content-diff.txt` (raw attribute and href byte comparison), and this report.
- **Scope:** nothing was staged or committed. The only files written are the deck and this folder. `ivory_design_system/`, media, other decks, references, README/index, `reviews/`, `workshops/` and `style-mockups/shots/` were not touched. No subagent was used.

### Content comparison

- `data-label`, `data-origin-slide` and raw `data-speaker-notes` are byte-identical on all 4 slides.
- Hrefs are identical, in order and count, on every slide:
  - `subagents-prompt-caching.html` appears ×2 on slide 01 and ×1 on each of slides 02–04.
  - The platform prompt-caching docs link is on slide 03.
  - The code.claude.com legal-and-compliance link is on slide 04.
- Media: 0 in the source, 0 in the output.
- Visible text (audit.py) differs only as follows:
  - **01**
    - The banner "Optional reference · Back to the talk" became the third `.meta` cell: the mono label "Optional reference" plus the link "Back to the talk". The `·` separator was dropped, because the label/value gap now separates them.
    - "Revised October 2026" became the label "Revised" plus "October 2026", the same as in the main-deck twin.
    - The title dot `.` was removed.
    - The mono label "Author" was added.
  - **02–04:** the crumb and banner merged into "In practice · Optional reference · Back to the talk" (one `·` added), following the accepted precedents. audit.py reports this as the crumb moving to the front.
  - **All slides:** the Ember `.snum` digits 2/3/4 were dropped. deck.js now writes `01–04 / 04`.
- Code line numbers 01–05 on slide 02 come from CSS decoration.

### Removed source text

- The title `.dot` "." (slide 01).
- One "·" separator from the slide 01 banner, which is now a label/value pair.
- The hand-written `.snum` digits.
- There was no `.ts-loopline`. Nothing was moved into the notes.

### Additions

- The meta labels "Author" and "Revised" (slide 01).
- The extra crumb `·` on slides 02–04.
- `.key` on `"cache_control"` (slide 02). The text is unchanged.

### Unfit slides / needs parent decision

- **Slide 01: the `h1` wraps to 3 lines, which breaks the spec maximum of two.**
  - The source title "Subagents & Prompt Caching<br>Reference" cannot keep its `<br>` in two lines at the fixed 176px: "Subagents & Prompt Caching" is wider than 1396px.
  - I kept the source markup exactly. It wraps to "Subagents &" / "Prompt Caching" / "Reference". The top sits at about y 216, clear of the header, and the last line still ends at 712. The `.sub` wraps to 2 lines in its 970px box.
  - Visually it holds (pass 1, pass 2 and the PDF), but it is a spec deviation. Alternatives for the parent:
    - (a) Accept it.
    - (b) Use the accepted reference-opener pattern: a regular `h2` (fits in 2 lines with the `<br>` kept) plus a zone component. That would need `.cards` built from the subtitle, author and date, which is a heavier restructuring with no precedent.
    - (c) A system-level smaller title variant. That is a design-system change, which I did not make.
  - I chose `.title-slide` because this source, unlike the three accepted reference openers, has a genuine title slide with subtitle, author and date. Those openers had h1 + cards and no title-slide content.
- No new component is needed. No footnote wraps. All other headlines are 1–2 lines: 02 and 04 have two, 03 has one.

### Unavailable media

None expected and none present.

### Three weakest slides

1. **01:** the 3-line `h1` (above) and the 2-line subtitle make it the densest title in the series.
2. **04:** two short tiles bottom-aligned in a 480px zone leave the top ~55% empty. This is valid ks-05 anatomy and matches the accepted precedent opener, but sparse.
3. **02:** clay on `"cache_control"` is my judgement of the focal element (the "marker" in the headline). The source had no accent there. The parent may prefer no clay.

### Checks run (all Chrome runs outside the sandbox, strictly serial, no failures)

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/spcr-chrome1.log ivory_design_system/tools/shoot.sh subagents-prompt-caching-reference-ivory.html /tmp/subagents-prompt-caching-reference-pass1` | exit 0, 4 PNGs, **all opened**, §10 checklist: only the 01 `h1` line count deviates. No fixes were possible without a content or system change |
| Pass 2 | `CHROME_LOG=/tmp/spcr-chrome2.log … /tmp/subagents-prompt-caching-reference-pass2` | exit 0, 4 PNGs, **all opened**, identical to pass 1 |
| PDF | `CHROME_LOG=/tmp/spcr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf subagents-prompt-caching-reference-ivory.html /tmp/subagents-prompt-caching-reference.pdf`, then `pdfinfo` | Pages: 4; 1440 × 810 pt. Pages 1 and 4 rendered with pdftoppm and opened (`/tmp/spcr-pdf-p-1.png`, `/tmp/spcr-pdf-p-4.png`) |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/spcr-chrome-notes.log … /tmp/subagents-prompt-caching-reference-notes 4 4` | Opened: "NOTES · CHOOSE AUTHENTICATION · 4 / 4", full notes, buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/spcr-chrome-pw.log … /tmp/subagents-prompt-caching-reference-pw 2 2` | Opened: 2 / 4, next = Multiple breakpoints, notes, timer, clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0 in each |
| Content | `python3 ivory-conversion/audit.py subagents-prompt-caching-reference.html subagents-prompt-caching-reference-ivory.html` | exit 0, no structural errors; differences only as listed |
| Static | grep | 1 `<link>` (styles.css), 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 4/4 empty `.snum`. No dark/light/reveal/dot/ts-*/slide-content/Ember/Google Fonts/reference-banner (the `ts-` grep hits are only "subagents-prompt…" filenames). Clay: 1 element (slide 02) plus the title header label |

### Screenshot paths

- `/tmp/subagents-prompt-caching-reference-pass1/01–04.png`
- `/tmp/subagents-prompt-caching-reference-pass2/01–04.png`
- `/tmp/subagents-prompt-caching-reference-notes/04.png`
- `/tmp/subagents-prompt-caching-reference-pw/02.png`
- `/tmp/subagents-prompt-caching-reference.pdf`

## Parent acceptance

Parent opened every final round-2 pass-2 slide, the rendered title PDF page, and the unchanged notes-4/presenter-2 shots. The two-line opener now complies without a system change; all four slides fit. Re-ran the shared audit: 4/4 slides, zero structural or per-slide errors. PDF has four pages; all eight capture logs have no CONSOLE entries. All 138 protected file hashes remain unchanged. Accepted weakest slides: 01 (sparse, unequal card content), 04 (short bottom-aligned cards), 03 (airy one-line rows). Only the title dot is removed as source decoration; slide numbers are generated. No unavailable media. Physical projector and external link availability were not checked.
