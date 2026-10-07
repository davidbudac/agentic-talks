# Agentic AI: Ivory conversion report

- **Output:** `agentic-ai-ivory.html` (new file). The source `agentic-ai.html` was only read.
- **Slide count:** 26 source → 26 Ivory, in the same order. `data-origin-slide` sequence: 1, 2, 3, 5, 10, 9, 11, 4, 12, 13, 14, 21, 26, 28, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 42, 43.
- **Artifacts in this folder:** `inventory.md` (per-slide mapping), `audit.json` (raw output of `ivory-conversion/audit.py`), `content-diff.txt` (readable per-slide digest of it) and this report.
- Only `agentic-ai-ivory.html` and this folder were written. Nothing is staged or committed. The scratch template `/tmp/agentic-ai-ivory.tpl.html` lives outside the repo.

## Content comparison (`audit.py` exit 0; structural_errors: none)

- `data-label`, `data-origin-slide` and the raw `data-speaker-notes` encoding are identical on all 26 slides.
- **Hrefs:** identical on every slide (sorted-list compare). Slide 01 keeps `https://davidbudac.cz`. Slide 24 keeps `agentic-ai-reference.html` and `index.html`. Slides 25 and 26 keep all 22 source URLs, with `target="_blank" rel="noopener"` retained. The video `src` changes are as instructed: `agent-loop-dark.mp4` → `agent-loop-ivory.mp4` and `subagents-light.mp4` → `subagents-ivory.mp4`.
- **Visible text:** identical on slides 02, 03 and 05–24, except for the added counters listed below.

Every reported difference is explained here:

| Slide | audit.py difference | Explanation |
|---|---|---|
| 01 | `AI.` → `AI` | Title dot removed (instructed) |
| 01 | `model → harness → agent ↺` removed | `.ts-loopline` removed (instructed) |
| 01 | "Revised October 2026" moved | Moved from the top bar into `.meta` as label `Revised` + `October 2026`. Same words |
| 01 | `Author` added | Mono `.lab` in `.meta` (title anatomy) |
| 04 | `loop Who` → `loopWho` (×3) | Extraction artefact only: the term `<b>` and definition `<span>` are adjacent inline elements in `.bul.def`. They render in separate grid columns |
| 12, 16, 19, 22 | `01 02 03` inserted | Mono number labels on equal `.cards.c3` tiles (allowed) |
| 25, 26 | `overviewplatform…` → `overview platform…` (every row) | Tokenisation only. Each title and its URL now sit in separate table cells, so the extractor inserts a space. The words are identical |

CSS counters also render without appearing in the DOM text: `01–04` on 04/09/24 (`ol.bul`) and code line numbers on 02, 07, 08, 10, 20 and 21. Slide 06 no longer has a code panel, so it has no line numbers.

## Removed source text

1. Slide 01: the title dot `.`.
2. Slide 01: the `.ts-loopline` text `model → harness → agent ↺`.
3. Slide 02: one **blank** line in the code block (whitespace only, no characters).

Nothing else was removed. No visible text was moved into the speaker notes.

## Additions

- The `Author` and `Revised` labels on 01. No "Length" cell was added, so no slide count was invented.
- The `01–03` labels on 12, 16, 19 and 22, plus the CSS counters and line numbers.
- No `--deck-total` style line was added (style elements are forbidden). deck.js sets the total, and the screenshots show `NN / 26`.

## Structural decisions worth a parent look

- **06 No memory (round 2):** the Ember `.lead` has no Ivory component. It is now the two rows of a `ul.bul` on the left of a `.split`, split at the sentence boundary. The source code block became a 1:1 SVG (828 × 562) on the right: the `# What the model is handed on turn 3 — the WHOLE chat, again:` comment is a two-line mono caption (broken after the dash because 61 characters do not fit 828px at 20px); the three utterances are three boxes in source order with their `you said:` / `it replied:` / `you now ask:` labels; `← answerable only because line 1 was re-sent` sits under the boxes with a dim orthogonal connector back to the first box. There are no generated line numbers, so "line 1" and the footnote's "Delete the first line" both point at the first box, which carries the clay. Round 1's numbered `.code.reg` (where those referred to line 04) is gone.
- **09 and 18 (round 2):** the video splits now put the text left and the video right (`.split`, not `.split.flip`), matching agentic-engineering-ivory and DESIGN.md §7. 09 was changed along with 18 because it is the same video-split pattern. 11 and 23 (SVG figures) still use `.split.flip`, as round 1 had them; DESIGN.md documents `flip` for a figure on the left.
- **03:** the `.tile.fill` callout became `.tile.key` (Agent). The chatbot tile was left plain rather than `.was`.
- **Diagrams 05, 11, 14 and 23** were redrawn 1:1: 1680×480, 828×562, 828×480 and 828×562. They have orthogonal lines, mono text in the source's case, no fill/stroke/font attributes, and the slide-unique markers `s05-a`, `s05-d` and `s11-a`. Slide 14's source had two clay rows; both are neutral now. Slide 23's diagonal "N×M" tangle became nine orthogonal hairline routes.
- **Clay** is used once each on 01 (header label), 02 (`PASS ✓`), 03 (Agent tile), 05 (CLAUDE CODE box), 06 (the first message box), 10 (`PASS`), 11 (ANSWER box) and 23 (MCP hub). No other slide adds clay; the 09 and 18 videos carry their own.

## Unfit slides / new component needed

**25 Sources 1 of 2** and **26 Sources 2 of 2** do not fit `.links`. Pass 1 rendered the source structure as-is and showed the problem:
- Slide 25 has 8 links in one column against the 3–5 the spec allows. Each row needed ~71px but got ~65px, so the titles and URLs collided with the hairlines.
- On slide 26, "Anthropic — Reasoning models don't always say what they think" (~875px) wraps in an 828px column and overflowed into the neighbouring row and below the zone.

I also tried flowing the links across both columns in source order, which also failed: the second group heading landed mid-column in a stretched row and read as detached.

**Shipped fallback:** one `table.tbl.num` per slide.
- The first group label is the `thead` label. The second group label is a `th` row.
- Each row holds the title `<a>` (same href and attributes) and the URL as grey `<span class="mut">` text in the right-hand column.
- Every row is one line. The zone ends at 888 and nothing collides.

Costs of this fallback:
- The URL text is no longer inside the anchor; only the title is clickable.
- Every title is underlined (default inline-link style).
- Slide 25 has 13 rows at a ~40px pitch, which is dense.

**Proper fix (needs a design-system change, which I am not allowed to make):** a compact link-list variant, for example `.links.dense`, with the title and URL on one line, ~40px rows, and no underline in the list. Alternatively, allow more than 5 rows per `.linkcol` with an auto-height first row. Changing the source content (splitting into more slides) is not allowed.

## Unavailable media

None. `assets/anim/agent-loop-ivory.mp4` and `assets/anim/subagents-ivory.mp4` exist and render, and their ivory ground is invisible against the slide. No media files were changed.

## Three weakest slides

1. **25 Sources 1 of 2:** the dense 13-row ledger described above. It is legible, but it is not the `.links` look and it underlines every row.
2. **06 No memory (after round 2):** the line-reference problem is fixed, but the left column holds only two short rows, so it is airy next to the figure. The `←` in the source comment points left at nothing in particular; the connector, not the arrow glyph, does the linking.
3. **18 Sub-agents:** at the screenshot time budget the video shows only its opening frame (a lone MAIN AGENT box). The figure half reads as empty in static shots, the PDF and thumbnails; it plays live. This matches example slide 19 and cost-and-context slide 12. **26** shares 25's fallback (12 rows, less dense), and **23**'s unlabeled boxes are faithful to the source but abstract.

## Checks run (all Chrome runs outside the sandbox; `shoot.sh` unmodified; no `--disable-gpu`)

| Check | Command | Result |
|---|---|---|
| Pass 1 | `CHROME_LOG=/tmp/aa-chrome1.log ivory_design_system/tools/shoot.sh agentic-ai-ivory.html /tmp/agentic-ai-pass1` | 26 PNGs, all opened. Fixes: 14 (headline wraps → SVG redrawn at 828×480), 25 and 26 (`.links` overflow → table). Those slides were re-shot into the same folder (`/tmp/aa-chrome1b/c/d.log`), and 25–26 were shot twice while choosing the fallback |
| Pass 2 | `CHROME_LOG=/tmp/aa-chrome2.log ivory_design_system/tools/shoot.sh agentic-ai-ivory.html /tmp/agentic-ai-pass2` | 26 PNGs, all opened against the §10 checklist. No further issues |
| Console | `grep -c CONSOLE` on all logs (pass 1 ×4, pass 2, notes, presenter) | 0 everywhere |
| PDF | `ivory_design_system/tools/shoot.sh --pdf agentic-ai-ivory.html /tmp/agentic-ai.pdf`; `pdfinfo` | Pages: 26; 1440 × 810 pt |
| Notes | `QUERY=chrome … /tmp/agentic-ai-notes 18 18` | `/tmp/agentic-ai-notes/18.png`: "NOTES · SUB-AGENTS · 18 / 26", full notes, buttons |
| Presenter | `QUERY=pw … /tmp/agentic-ai-pw 5 5` | `/tmp/agentic-ai-pw/05.png`: current 05, next 06, notes, timer, clock |
| Static | Python checks + `audit.py` | Exactly 1 `<link>` (Ivory `styles.css`) and 2 `<script src>` (`deck-stage.js`, `deck.js`). 0 `<style>` elements, 0 `style=` attributes, 0 inline scripts. 26/26 empty `.snum`. No dark/light/reveal/dot/ts-*/lead/fill/`.o` classes. 0 Ember or Google Fonts refs. 0 fill/stroke/font attributes in SVGs. Unique marker ids. At most one `.note` per slide (none on 01, 14, 18, 23, 25: the source had none on those) |

| Round 2 | `CHROME_LOG=/tmp/agentic-ai-r2.log shoot.sh agentic-ai-ivory.html /tmp/agentic-ai-r2 N N` for N = 6, 9, 18 | `/tmp/agentic-ai-r2/06.png`, `09.png`, `18.png`, all opened. Not a full pass: only the changed slides |
| Round 2 PDF | `shoot.sh --pdf agentic-ai-ivory.html /tmp/agentic-ai.pdf`; `pdfinfo` | Pages: 26 (overwrote the round-1 PDF). Page 6 rendered with `pdftoppm` and opened |
| Round 2 notes | `QUERY=chrome … /tmp/agentic-ai-notes N N` for N = 6, 18 | `/tmp/agentic-ai-notes/06.png`, `18.png` (replaced the round-1 folder). Notes text complete on both |
| Round 2 console/static | `grep -ci console /tmp/agentic-ai-r2.log`; static grep; `audit.py` | 0 console lines. 1 `<link>`, 2 `<script src>`, 0 `style=`, 0 `<style>`, 0 fill/stroke/font attributes in SVGs, no duplicate marker ids (`s06-d` new). `audit.json` regenerated: identical to round 1 (26/26, no structural errors, slide 06 text unchanged and in source order) |

### §10 checklist summary (from looking at the pass 2 PNGs)

- Header label, `NN / 26` and the 108 hairline are correct on every slide. Headlines have at most 2 lines; 05, 07, 12, 14, 16 and 18 use two.
- Zones reach 888 (rows, cells, code panels, tables, figures).
- Nothing crosses the margins. The longest code lines are 57 characters at 40px and 78 at 30px; none is clipped.
- The footnote is one line everywhere except 05 (two lines, no `.src`).
- Content text is 30px or 40px. All slides are light, with no fills (apart from the paper code panels), shadows, icons or pills.
- Letterforms are Geist and Geist Mono. The ✓ › → ← ▸ glyphs come from the system fallback, as the spec expects.

**Screenshot paths:** `/tmp/agentic-ai-pass1/01–26.png` (14, 25 and 26 overwritten by the re-shots), `/tmp/agentic-ai-pass2/01–26.png` (06, 09 and 18 there are the round-1 layouts), round 2: `/tmp/agentic-ai-r2/06.png`, `09.png`, `18.png`, `/tmp/agentic-ai-notes/06.png`, `/tmp/agentic-ai-notes/18.png`, `/tmp/agentic-ai-pw/05.png`, `/tmp/agentic-ai.pdf`.

## Parent acceptance

The parent opened every final slide: pass 2 slides 01–26, then the replacement screenshots for 06, 09 and 18 from round 2. It also opened the round-2 notes panel on 06 and refreshed and opened the presenter view at `/tmp/agentic-ai-parent-pw/05.png` so its next-slide thumbnail shows the corrected conversation. No content is clipped. The 13-row source table is dense but legible at 30px and uses an existing component. The sparse opening frame on 18 is a video timing limitation.

The parent reran the content audit (26/26, no structural or metadata errors), confirmed the regenerated PDF has 26 pages and checked the round-2 and refreshed presenter logs: zero CONSOLE entries. Chrome emits native macOS display-link diagnostics, which are not page-console errors; the capture completed successfully. All 138 protected source and media files still match their baseline hashes. No design-system addition was required.
