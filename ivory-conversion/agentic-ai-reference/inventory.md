# Agentic AI — Reference: per-slide inventory and mapping

Source: `agentic-ai-reference.html` (working tree, read only; sha1 25a26d97…, mtime unchanged; sha256 matches `protected-files.json`). Output: `agentic-ai-reference-ivory.html`.
13 slides, order unchanged. No `<video>`, no inline SVG. Three `<img>`: `assets/tools/lovable.png`, `higgsfield.png`, `hyperframes.png` (each 1600 × 1000, unchanged).

Slides 02–13 in the source carried `.reference-banner` "Reference · September 2026 snapshot · Back to the talk" (`href="agentic-ai.html"`). It follows the accepted model (`agentic-engineering-reference-ivory.html`, `ai-toolbox-reference-ivory.html`): the banner is merged into the header `.crumb` after the original section crumb, with one `·`. The crumb `<b>` is dropped, keeping its text. Headline `.o` spans are removed. `reveal`, `dark`/`light`, `reference-slide`, `dense` and `slide-content` are removed. `.snum` is empty. `<section>` opening tags were copied byte for byte from the source by script, with only the class value replaced by `slide`.

| # | Label (origin) | Source pattern | Ivory component | Size | Clay |
|---|---|---|---|---|---|
| 01 | Reference guide (—) | dark; crumb; `h1.reference-title`; `.cards.c2` (span.k + p); note link | `h2` + `.cards.c2` (h3 + p) + `.note` link (same as both accepted reference openers) | 40 | none |
| 02 | Glossary (7) | `.gloss`, 9 `.row > .term + .def` | `ul.bul.def.wide`, 9 rows (term 40 · def 30); `<i>` kept | 30/40 | none |
| 03 | Today's models (18) | `.dense`; `table.tbl` 3×3 with inline-style muted span; long `.note` *between* table and stats; `.cards.c3 > .tile.stat` (span.k value + p) with inline margin | One `.tbl.c3`: 3 maker rows + a 4th row whose three cells are the stats, each value as an inline mono `span.lab` before its text. Inline style → `span.mut`. The note becomes the `.note` footnote (2 lines) | 30 | none |
| 04 | Which tier when (19) | dark; `.cards.c3`, `.tile.fill` on Large | `.cards.c3` (span.k → h3) | 40 | none (three equal tiers; fill not mapped to key) |
| 05 | Today's harnesses (20) | `.cards.c3` with 6 tiles, `.fill` on Claude Code | `ul.bul.def.wide`, 6 rows (cards take 2–4) | 30/40 | none (equal list; the notes name *two* tools) |
| 06 | Lovable (22) | `.split` = `.diagram > img.shot` + `ul.bul` | `.split.flip` = `.fig > img` (828) + `ul.bul` (686) | 30 | none |
| 07 | Higgsfield (23) | dark; `.split` = `ul.bul` + `.diagram > img.shot` | `.split` = `ul.bul` + `.fig > img` | 30 | none |
| 08 | HyperFrames (24) | `.split` = `.diagram > img.shot` + `ul.bul` | `.split.flip` = `.fig > img` + `ul.bul` | 30 | none |
| 09 | Subscriptions (25) | `table.tbl` 3×3; inline-style muted span | `.tbl.c3`; inline style → `span.mut` | 30 | none |
| 10 | Cost per task (27) | dark; `.cards.c2` (span.k + p) | `.cards.c2` (h3 + p) | 40 | none (two equal options) |
| 11 | Unattended runs (34) | dark; `ul.bul`, 4 rows | `ul.bul` | 30 | none |
| 12 | Sources 1 of 2 (42) | `.links` 8 + 4 | `.tbl.num` with a rowgroup `th` row. Markup copied from the accepted twin `agentic-ai-ivory.html` 25 (identical source links) | 30 | none |
| 13 | Sources 2 of 2 (43) | `.links` 6 + 4 + note | `.tbl.num` + rowgroup row (twin `agentic-ai-ivory.html` 26) | 30 | none |

## Class inventory (root DESIGN.md mapping, then §8 no-equivalent rules)

- Present and mapped:
  - `gloss/row/term/def` → `ul.bul.def.wide` (02);
  - `stat` (tile with a big `span.k` value) → no equivalent. Restructured into one table row with mono value labels (03), because a zone takes one component;
  - `fill` → no clay on 04 and 05 (equal items, per the parent's toolbox correction);
  - `shot` / `.diagram > img` → `.fig > img`;
  - `reference-banner` → crumb;
  - `reference-slide` → removed;
  - `reference-title` → `h2`;
  - `dense` → removed (size steps only);
  - inline `style="color:var(--s-muted)"` → `.mut`;
  - `c3`/`c2` → `.cards.cN` / `.tbl.c3`;
  - `dark`/`light`/`reveal`/`slide-content`/`span.k`/`h2 .o` → removed or mapped as above.
- Not present in this source: `lead`, `kcard`, `big`, `dg-dash`, `dg-tangle`, `tight`, `muted` (class), `outer`, `c4`, title `.dot`, `.ts-loopline`, `.title-slide`, `.extag`, `.pills`, SVG, video.
- Head and body machinery removed:
  - Google Fonts link/preconnect and `ember_design_system/styles.css`;
  - the `deck-stage:not(:defined)` style, the big inline style, the reference-banner/reference-title style, the `.note a` style, `#presenter-ui-css` and the `.pui-*` markup;
  - the inline presenter/video-restart scripts;
  - the duplicated `ember_design_system/deck-stage.js` tag (it appeared twice) → one `ivory_design_system/deck-stage.js` + `deck.js`.
