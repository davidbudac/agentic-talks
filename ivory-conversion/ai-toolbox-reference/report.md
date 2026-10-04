# AI Toolbox — Reference: Ivory conversion report

- **Output:** `ai-toolbox-reference-ivory.html` (new file). The source `ai-toolbox-reference.html` was only read. It is still untracked, and its sha1 `e2d1b4bd…` and mtime are unchanged.
- **Slide count:** 22 → 22, order unchanged. Origins: (none), 8, 11, 12, 13, 16, 19, 24, 30, 32, 34, 35, 36, 39, 42, 43, 44, 50, 51, 52, 56, 57.
- **Artifacts in this folder:**
  - `inventory.md`: per-slide mapping and class inventory;
  - `audit.json`: output of the shared `audit.py`;
  - `content-diff.txt`: every difference explained;
  - this report.
- **Scope:** nothing was staged or committed. The only files written are the deck and this folder.
  - `ivory_design_system/` is unchanged.
  - The `git status` list of modified tracked files is identical to the start of the session.
  - No media, other decks, references, README/index, `reviews/`, `workshops/` or `style-mockups/shots/` were touched.

## Content comparison

- `audit.py` exits 0, with no structural errors and no per-slide errors.
- Labels, origins and the raw notes bytes are identical on all 22 slides.
- Hrefs are identical on every slide. That includes the 22 `ai-toolbox.html` links (one per slide) (the original deck) and the 26 source URLs, with `target`/`rel` kept.
- Text differences (details in `content-diff.txt`):
  - the banner merged into the crumb (02–22);
  - 4 emoji removed;
  - snum digits now come from deck.js;
  - a def-row join artifact in the comparator;
  - one `&nbsp;`.

## Removed source text

- Four emoji (decoration):
  - "⚠" (06 tile label and 18 footnote);
  - "🛡" (17);
  - "⚔" (17).
- No title `.dot` and no `.ts-loopline` exist in this source.
- Nothing was moved to the notes.

## Additions

- One `·` separator per crumb (02–22).
- `&nbsp;` before "—" in the 05 headline.
- No mono labels or table headers were added. No `--deck-total` style: deck.js sets `NN / 22`.

## Decisions / precedents (first deck in the series with these patterns)

- **6-tile `.cards.c3` (04, 06) → `ul.bul.def.wide`.** Ivory cards take 2–4 items in one row, and a `.tbl` needs header text the source does not have. Six rows is one more than the §6 guidance of 3–5.
- **`.gloss` (02, 10 terms) → `ul.bul.def.wide`, 10 rows of 56px.** This follows the root mapping (`.gloss` → `ol.bul.def`/`.tbl`). A `.tbl` would wrap the definitions in its 804px column, and the non-wide `def` would wrap "Generative AI" / "Deep research". This is 2× the recommended row count.
- **`.kcard`:**
  - in a split (08, 13, 20): `.split` > `ul.bul` + `.cards` > single `.tile.key`;
  - kcard first (15): `.split.flip`;
  - kcard under a `.cards.c3` (10): `.cards.c4` with the kcard as the 4th `.tile.key`, because a zone takes one component.
- **Clay:**
  - one `.fill`/`.kcard` per slide → `.key` (06 term, 08, 09, 10, 11, 13, 15, 17, 19, 20);
  - 04 had two `.fill` tiles (Cowork, Design) → no clay;
  - all other slides are equal items → none.
- **Sizes:**
  - Long product tiles (>~150 chars) use `.reg`, following §6 "add .reg for long text" (05, 08, 09, 11, 13, 15, 19, 20). `.c4` is 30px by default.
  - 16, 17, 18 and 01 tiles stay at 40px.
  - All tables are 30px.
- **14 Cheat sheet:** the Ember `.tight` 21px table became `.tbl.c4` at 30px with 11 rows. Every cell fits on one line (verified in the screenshots).

## Unfit slides / new components needed

- None blocking. Every slide uses an existing component. Headlines are ≤ 2 lines, footnotes ≤ 2 lines (two-line footnotes have no `.src`), and nothing crosses 888 or the margins.
- Deviations to note:
  - 02 (10 rows), 04/06 (6 rows), 14 (11 table rows) and 21/22 (7-link columns) exceed the spec's recommended counts but fit.
  - Footnotes on 03, 05, 07, 09, 11, 16, 17, 18 and 19 are 2 lines (allowed without `.src`).
- The parent may want to add to root DESIGN.md:
  - the `.gloss` → `ul.bul.def.wide` mapping;
  - 6-tile grid → `ul.bul.def.wide`;
  - `.kcard` in split → `.cards > .tile.key`;
  - "multiple `.fill` → no clay".

## Unavailable media

None. This deck has no video, SVG or images.

## Three weakest slides

1. **02 Glossary.** 10 rows of 56px with 40px terms: the terms sit almost on their top hairlines, and the 568px term column is mostly empty. It is dense and reads like a list rather than the source's two-column map.
2. **08 / 13 / 20 (split + key tile).** The right-hand `.tile.key` is bottom-aligned, which leaves roughly the top half of its 828px column empty beside full-height bullet rows (the ks-05 anatomy, in a split). 08 is the clearest case.
3. **06 The ChatGPT family.** The six def rows have uneven text heights (1-line vs 2-line definitions in equal 93px rows). Three definitions wrap with short last lines ("a batch.", "a moment.").

(Runner-up: 14 Cheat sheet, with 11 rows of 47px. It is legible but at the density limit.)

## Checks run

All Chrome runs were outside the sandbox, one at a time, with `shoot.sh` unmodified and no `--disable-gpu`. Every run exited 0.

| Check | Command | Result |
|---|---|---|
| Content | `python3 ivory-conversion/audit.py ai-toolbox-reference.html ai-toolbox-reference-ivory.html > …/audit.json` | Exit 0; 22/22, no errors |
| Pass 1 | `CHROME_LOG=/tmp/atr-chrome1.log ivory_design_system/tools/shoot.sh ai-toolbox-reference-ivory.html /tmp/ai-toolbox-reference-pass1` | 22 PNGs, **all opened**. One fix: 05 headline "—" started line 2 → `&nbsp;` |
| Pass 2 | `CHROME_LOG=/tmp/atr-chrome2.log … /tmp/ai-toolbox-reference-pass2` | 22 PNGs, **all opened**. 05 fixed, no other changes needed |
| PDF | `CHROME_LOG=/tmp/atr-chrome-pdf.log ivory_design_system/tools/shoot.sh --pdf ai-toolbox-reference-ivory.html /tmp/ai-toolbox-reference.pdf`; `pdfinfo` | Pages: 22; 1440 × 810 pt (PDF pages not opened) |
| Notes | `QUERY=chrome CHROME_LOG=/tmp/atr-chrome-notes.log … /tmp/ai-toolbox-reference-notes 6 6` | Opened: "NOTES · THE CHATGPT FAMILY · 6 / 22", full notes, 3 buttons |
| Presenter | `QUERY=pw CHROME_LOG=/tmp/atr-chrome-pw.log … /tmp/ai-toolbox-reference-pw 14 14` | Opened: 14 / 22 current, next = Story 2, notes, elapsed timer, clock |
| Console | `grep -c CONSOLE` on all 5 logs | 0, 0, 0, 0, 0 |
| Static | grep | 1 `<link>` (styles.css) + 2 `<script src>` (deck-stage.js, deck.js). 0 `<style>`, 0 `style=`, 0 inline scripts. 22/22 empty `.snum`. 0 legacy classes. 0 Ember or Google Fonts references |

### §10 checklist (both passes, from the PNGs)

1. Header label left, `NN / 22` right, hairline at 108. Headlines start at 172:
   - two lines: 05, 08, 13, 15, 20;
   - all others one line.
2. Zone tops are at 326/408. Rows, cells, tables and link columns end on 888.
3. Nothing crosses 888 or the margins. The footer holds only `.note`.
4. Content text is 30/40px only, and labels are mono uppercase.
5. Clay is on at most one element per slide, as listed above.
6. No figures.
7. All slides are light, with no fills, shadows, icons or pills.
8. Footnotes are at most 2 lines, with no `.src` anywhere.
9. Letterforms are Geist / Geist Mono. The arrows (→), "≠" and "≈" come from the fallback font, as the spec expects.

### Screenshot paths

- `/tmp/ai-toolbox-reference-pass1/01–22.png`
- `/tmp/ai-toolbox-reference-pass2/01–22.png` (final)
- `/tmp/ai-toolbox-reference-notes/06.png`
- `/tmp/ai-toolbox-reference-pw/14.png`
- `/tmp/ai-toolbox-reference.pdf`

## Parent acceptance and corrections

The parent opened all 22 pass-2 images, notes 06 and presenter 14. Removed `.key` from equal-item comparison slides 09 (two avatar tools), 17 (defence/offence) and 19 (two office integrations); the Ember fill is not sufficient reason to accent one equal item. Captured and opened the corrected 09, 17 and 19 in `/tmp/ai-toolbox-reference-parent/`. These are class-only changes with no text change. All other accents remain as described above.

Final audit passed: 22 slides, no structural or per-slide errors, unchanged link targets and raw notes. All 138 protected file hashes still match. All five worker logs and `/tmp/aitr-parent.log`, `/tmp/aitr-parent-pdf.log` contain zero CONSOLE lines. Final PDF `/tmp/ai-toolbox-reference-final.pdf` has 22 pages. No stylesheet or template change.

Parent's three weakest slides: 02 (ten tightly spaced glossary definitions), 06 (mixed one/two-line definitions in equal-height rows), and 14 (eleven-row cheat sheet with little vertical breathing room). All fit at the existing size steps; wording and slide count take priority over the usual item-count guidance. The single callout alongside bullets and six definition-row mappings are accepted uses of existing components. No unfit content or unavailable media. Removed decoration remains the four emoji listed above.
