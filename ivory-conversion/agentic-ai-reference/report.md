# Agentic AI — Reference: Ivory conversion report

**Final status: accepted after the parent image-containment fix in 331727d.** The worker findings below describe the initial state; the final acceptance section supersedes the resolved image blocker.

- **Output:** `agentic-ai-reference-ivory.html` (new, untracked). The source `agentic-ai-reference.html` was only read: its sha1 `25a26d97…` and mtime are unchanged, and its sha256 matches `protected-files.json`.
- **Slide count:** 13 → 13, order unchanged. Origins: (none), 7, 18, 19, 20, 22, 23, 24, 25, 27, 34, 42, 43.
- **Artifacts in this folder:**
  - `inventory.md`: per-slide mapping and class inventory;
  - `audit.json`: output of the shared `audit.py`;
  - `content-diff.txt`: every difference explained;
  - this report.
- **Scope:**
  - Nothing was staged or committed. The only files written are the deck and this folder; the generator script is at `/tmp/aar_build.py`, outside the repo.
  - `ivory_design_system/` is unchanged.
  - All 138 protected-file hashes still match.
  - The `git status` list of tracked modifications is identical to the start of the session.
  - No media files were touched.

## Needs a parent decision (blocking for image fidelity)

1. **`.fig > img` is stretched, not contained.**
   - `styles.css:246` gives `.fig > img` `width:100%; height:100%`. Only `video` gets `object-fit:contain` (`styles.css:247`), although spec §7 says "Images (`<img>`) follow the same rules".
   - Measured in pass-2 PNGs: on 06, 07 and 08 the image box is exactly 828 × 562 (x 120–947 or 972–1799, y 326–887), aspect 1.473 vs the files' 1.600. That is an **8.6% vertical stretch**. It is subtle but real: text in the screenshots is slightly tall.
   - I did not edit the DS and did not work around it. The rejected workarounds were an SVG `<image>`, an invented `.lab` caption, or putting the img outside `.fig`.
   - Suggested one-line DS fix (parent/DS owner): `.fig>img{object-fit:contain;object-position:center}`. With it the images would render 828 × 518, centred, with 22px of ivory above and below, and no markup change is needed.
2. **All three images clash with Ivory's ground.**
   - Lovable is a dark → vivid pink/orange gradient hero.
   - Higgsfield is a black UI with saturated green/purple thumbnails.
   - HyperFrames is a black UI with green accents.
   - None has the `#FAF9F5` ground (§7 media rules), so they read as dark rectangles. Even after the fix above they will sit as dark boxes, not merge with the slide.
   - These are third-party product screenshots that cannot be "re-rendered to Ivory" honestly. They are kept unchanged, as instructed.

## Content comparison

- `audit.py` exits 0, with no structural errors and no per-slide errors.
- Labels, origins and the raw notes bytes are identical on all 13 slides.
- Hrefs are an identical ordered list on every slide:
  - 13 × `agentic-ai.html` (the original deck): the 01 note and the 02–13 crumbs;
  - the 22 source URLs, with `target`/`rel` kept.
- Img `src` and `alt` are identical.
- Text differences (details in `content-diff.txt`):
  - A: the banner merged into the crumb (02–13);
  - B: snum digits now come from deck.js;
  - C: on 03, the note now follows the stats;
  - D: a def-row join artifact in the comparator (05);
  - E: a title/URL cell split on 12/13 (the accepted main-deck layout).

## Removed source text

None. The source has no emoji, no title `.dot` and no `.ts-loopline`. Nothing was moved to the notes.

## Additions

- One `·` separator per crumb (02–13).
- `width="1600" height="1000"` attributes on the three `<img>`.
- No `--deck-total` style: deck.js sets `NN / 13`.

## Decisions

- **Opener (01):** a regular `h2` slide, the same as the AE and toolbox reference openers.
- **03 Today's models:** the source had a table, the note *between* the table and the stats, and three `.stat` tiles. A zone takes one component.
  - First attempt (pass 1): a second header row with the stat values as `th`. The equal-height table rows pushed the 3-line ARC-AGI-3 cell past 888.
  - Final: the stats are the 4th row of the same `.tbl.c3`, each value as an inline mono `span.lab` ("96%", "2× THE FIELD", "~6 MONTHS") before its sentence.
  - The note is the 2-line footnote, so its "How fast does it move? —" now follows the stats instead of introducing them.
- **Clay: none on any slide.**
  - 04 (fill on Large): three equal tiers.
  - 05 (fill on Claude Code): equal list, and the notes name two tools.
  - 10: two equal options.
  - This follows the parent's correction on toolbox refs 9, 17 and 19.
- **05:** 6 tiles → `ul.bul.def.wide` (the toolbox precedent).
- **02:** 9-row `ul.bul.def.wide` (the toolbox glossary precedent).
- **06/08:** the image comes first in the source, so they use `.split.flip`.
- **07:** bullets first, so it uses `.split`.
- **12/13:** the same `.tbl.num` + rowgroup markup as the accepted `agentic-ai-ivory.html` 25/26 (the source links are identical). The crumb gets the banner merge.

## Unfit slides / new components needed

- **06, 07, 08:** the image stretch and dark grounds above. The fix is a DS rule, not a deck change.
- **03:** no stat-tile component. The stats are restructured into a table row with small mono value labels, so they lose their visual prominence. If the parent wants big figures, a component for "table + stat strip" would be new.
- Otherwise all slides use existing components.
  - Headlines are all one line.
  - Footnotes are ≤ 2 lines, with no `.src` anywhere. 2-line footnotes: 03, 04, 06, 09.
  - Nothing crosses 888 or the margins.

## Unavailable media

None. All three images exist and render. There is no video in this deck.

## Three weakest slides

1. **06 / 07 / 08 (image splits).**
   - The images are stretched 8.6% vertically (DS gap above).
   - Three dark, saturated screenshots break the ivory, low-decoration look.
   - 07 (Higgsfield) is the loudest.
2. **03 Today's models.**
   - The densest slide: 4 table rows, the 3-line ARC cell ends about 13px above 888, and there is a 2-line footnote.
   - The stat values are demoted to 20px mono labels.
   - "MAKER" heads a column whose last cell is a stat.
3. **12 Sources 1 of 2.**
   - 13 table rows of about 40px (accepted twin layout), with the URL column in mono at 30px.
   - Legible but crowded, and it leaves the footer empty. The source has no note on this slide.

## Checks run

All Chrome runs were outside the sandbox, strictly one at a time, with `shoot.sh` unmodified and no `--disable-gpu`. Every run exited 0. There were no pipes on capture commands.

| Check | Command | Result |
|---|---|---|
| Content | `python3 ivory-conversion/audit.py agentic-ai-reference.html agentic-ai-reference-ivory.html > ivory-conversion/agentic-ai-reference/audit.json` | Exit 0; 13/13, no errors (re-run on the final deck) |
| Pass 1 | `CHROME_LOG=/tmp/aar-chrome1.log ivory_design_system/tools/shoot.sh agentic-ai-reference-ivory.html /tmp/agentic-ai-reference-pass1` | 13 PNGs, all opened. Found: 03 overflow past 888; image stretch on 06–08 |
| Fix check | `CHROME_LOG=/tmp/aar-chrome-s3.log … /tmp/agentic-ai-reference-s3check 3 3` | 03 fits; opened |
| Pass 2 | `CHROME_LOG=/tmp/aar-chrome2.log … /tmp/agentic-ai-reference-pass2` | 13 PNGs, all opened. 03 fixed; 06–08 image box measured 828 × 562 from the PNG pixels |
| PDF | `CHROME_LOG=/tmp/aar-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf agentic-ai-reference-ivory.html /tmp/agentic-ai-reference.pdf`; `pdfinfo` | Pages: 13; 1440 × 810 pt (PDF pages not opened) |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/aar-chrome-notes.log … /tmp/agentic-ai-reference-notes 6 6` | Opened: "NOTES · LOVABLE · 6 / 13", notes text, 3 buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/aar-chrome-pw.log … /tmp/agentic-ai-reference-pw 3 3` | Opened: 3 / 13 current, next = Which tier when, full notes, elapsed timer, clock |
| Console | `grep -c CONSOLE` on all 6 logs | 0, 0, 0, 0, 0, 0 |
| Static | grep | 1 `<link>` (styles.css) + 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 13/13 empty `.snum`. 0 legacy classes. 0 `ember_design_system` or googleapis references |
| Protected | sha256 vs `ivory-conversion/protected-files.json` | 138 checked, 0 changed |

### §10 checklist (pass 2, from the PNGs)

1. Header label left, `NN / 13` right, hairline at 108. All headlines are one line at 172; the crumbs fit without ellipsis (the longest is 13).
2. Zone top is at 326. Rows, cells, tables and link tables end on 888. The images span 326–887.
3. Nothing crosses 888 or the margins. The footer holds only `.note`.
4. Content text is 30/40px only, and labels are mono uppercase. The 03 stat labels are 20px mono `.lab`.
5. No clay anywhere (equal items throughout).
6. The figures sit at 120–948 (flip) and 972–1800 (split). The images are not invisible-edged: they have dark grounds, and are **stretched** (see top).
7. All slides are light, with no fills, shadows, icons or pills. The only dark areas are inside the screenshots.
8. Footnotes are at most 2 lines, with no `.src`.
9. Letterforms are Geist / Geist Mono. The arrows (→) and "≈" come from the fallback font, as the spec expects.

### Screenshot paths

- `/tmp/agentic-ai-reference-pass1/01–13.png`
- `/tmp/agentic-ai-reference-pass2/01–13.png` (final)
- `/tmp/agentic-ai-reference-s3check/03.png`
- `/tmp/agentic-ai-reference-notes/06.png`
- `/tmp/agentic-ai-reference-pw/03.png`
- `/tmp/agentic-ai-reference.pdf`

## Parent review: stopped at shared stylesheet defect

Parent opened pass-2 screenshots 06, 07 and 08 and confirmed the distortion. All three PNG sources are 1600 × 1000. The stylesheet forces their element boxes to 828 × 562 and applies `object-fit:contain` only to video, contrary to DESIGN.md section 7's instruction that images follow the same rules. All three source screenshots also visibly contrast with the Ivory ground; keep them unchanged as requested.

Per the user's stop-and-report instruction for shared stylesheet defects, parent stopped without changing the stylesheet, committing this deck or starting another conversion. The remaining ten slide images have not yet received parent review. All 138 protected file hashes still match.

Proposed correction: add `.fig>img{object-fit:contain;object-position:center}` to the shared stylesheet. Before accepting it, add a kitchen-sink image example using an existing-token layout, document the image behavior and bump the version to 1.1, then re-shoot the kitchen sink and compare all original 26 slides pixel-for-pixel against the existing shots. Recheck this deck's image slides and notes shot, regenerate its PDF, finish parent review and content checks, then commit. No change has been made under ivory_design_system/.


## Final parent acceptance

- Reviewed every pass-2 slide personally, plus corrected slides 06–08 after the shared fix in 331727d. Worker completed and opened every slide in two complete look-and-fix passes. The corrected image screenshots are `/tmp/agentic-ai-reference-parent/06.png` through `08.png`.
- Images now preserve their 1600 × 1000 proportions, centered at 828 × 517.5 within the figure. No slide content overflows. No source text removed and no unavailable media. The unchanged Lovable, Higgsfield and HyperFrames images all contrast with the Ivory ground.
- Re-ran content audit: 13 slides, zero structural or per-slide errors. All 138 protected files match their original hashes. Labels, raw notes, origins, words and href targets remain preserved, subject to the layout ordering/separator changes explained above.
- Final PDF `/tmp/agentic-ai-reference-final.pdf`: 13 pages at 1440 × 810 pt. Opened rendered page 07 and checked image proportions and layout.
- Parent opened presenter screenshot 03 and corrected notes screenshots 06 and 10. Slide 10 notes fit clearly. On 06, long notes extend into the bottom-right button area in the fixed screenshot; complete raw notes are preserved. No notes-panel layout changes were made as part of this image correction.
- No CONSOLE errors in parent image, notes and PDF captures. All Chrome runs completed sequentially outside the restricted sandbox.
- Final three weakest slides: **07**, because the saturated dark product screenshot dominates the neutral slide; **03**, because its dense table and 20px stat labels reduce figure prominence; **12**, because the 13-row sources table is crowded. All fit the slide bounds.
- Not checked: a physical projector, external link availability, or every PDF page visually. Dark source images were intentionally kept intact.
