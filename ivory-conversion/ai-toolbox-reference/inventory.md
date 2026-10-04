# AI Toolbox — Reference: per-slide inventory and mapping

Source: `ai-toolbox-reference.html` (working tree, read only; sha1 e2d1b4bd…, unchanged). Output: `ai-toolbox-reference-ivory.html`.
22 slides, order unchanged. No `<video>`, no `<img>`, no inline SVG, so there was nothing to redraw and no media is used.

Every slide 02–22 in the source carried `.reference-banner` "Reference · July 2026 snapshot · Back to the talk" (`href="ai-toolbox.html"`). Following the accepted model (`agentic-engineering-reference-ivory.html`), it is merged into the header `.crumb` after the original section crumb with one `·`. In the original crumb, `<b>` is dropped; the text is kept and uppercased by CSS. Headline `.o` spans are removed (headlines take no clay). `reveal`, `dark`/`light`, `reference-slide`, `tight` and `slide-content` are removed. `.snum` is left empty.

| # | Label (origin) | Source pattern | Ivory component | Size | Clay |
|---|---|---|---|---|---|
| 01 | Reference guide (—) | dark; crumb; `h1.reference-title`; `.cards.c2` (span.k + p); note link | ordinary content slide: `h2` + `.cards.c2` (h3 + p) + `.note` link (as in the accepted AE reference opener) | 40 | none |
| 02 | Glossary (8) | `.gloss` 2-col grid, 10 `.row > .term + .def` | `ul.bul.def.wide`, 10 rows (term 40px · def 30px) | 30/40 | none |
| 03 | Today's models (11) | `table.tbl` 3 cols × 3 rows; inline-style muted span | `.tbl.c3`; inline style → `span.mut` | 30 | none |
| 04 | The Claude family (12) | `.cards.c3` with 6 tiles, 2 of them `.fill` | `ul.bul.def.wide`, 6 rows (cards hold 2–4 items only) | 30/40 | none (two equal `.fill` tiles; no single point) |
| 05 | Claude Code and Codex (13) | `.split` of 2 tiles | `.cards.c2.reg` | 30 | none |
| 06 | The ChatGPT family (16) | `.cards.c3` with 6 tiles, 1 `.fill` ("⚠ Watch out") | `ul.bul.def.wide`, 6 rows; the fill term → `<b><span class="key">` | 30/40 | "Watch out" term |
| 07 | The plan ladder (19) | `table.tbl` 4 cols × 4 rows | `.tbl.c4` | 30 | none |
| 08 | Deep research (24) | `.split` = `ul.bul` + `.kcard` (`.big` + p) | `.split` = `ul.bul` + `.cards.reg > .tile.key` (big → h3) | 30 | key tile |
| 09 | AI avatars (30) | `.split` of tile + `.tile.fill` | `.cards.c2.reg`, HeyGen `.tile.key` | 30 | HeyGen tile |
| 10 | Music and easy editing (32) | `.cards.c3` + `.kcard` below (inline margin) + note | `.cards.c4`; kcard → 4th `.tile.key` (one component per zone) | 30 | Descript tile |
| 11 | Presentations (34) | `.cards.c3`, Gamma `.fill` | `.cards.c3.reg`, Gamma `.tile.key` | 30 | Gamma tile |
| 12 | Copy platforms (35) | `.cards.c4` (2×2 in Ember) | `.cards.c4` (4 columns) | 30 | none |
| 13 | Perplexity (36) | `.split` = `ul.bul` + `.kcard` | `.split` = `ul.bul` + `.cards.reg > .tile.key` | 30 | key tile |
| 14 | Cheat sheet (39) | `.tight`; `table.tbl` inline 21px, 4 cols × 11 rows; `td.muted` | `.tbl.c4` 30px, 11 rows; `td.muted` → `td.mut` | 30 | none |
| 15 | Story 2 · Ten years, two days (42) | `.split` = `.kcard` (big with `<br>`) + `ul.bul` | `.split.flip` = `.cards.reg > .tile.key` (828) + `ul.bul` (686) | 30 | key tile |
| 16 | Story 3 · The exams (43) | `.cards.c2` + note (inline margin) | `.cards.c2` | 40 | none |
| 17 | Story 4 · The security double (44) | `.split` of tile "🛡 Defence" + `.fill` "⚔ Offence" | `.cards.c2`, Offence `.tile.key`; emoji dropped | 40 | Offence tile |
| 18 | The ChatGPT side (50) | `.cards.c3`; note starts "⚠" | `.cards.c3`; ⚠ dropped | 40 | none |
| 19 | The built-ins (51) | `.split` of tile + `.fill`; inline-style mono span | `.cards.c2.reg`, Gemini `.tile.key`; mono span → `<code>` | 30 | Gemini tile |
| 20 | The universal adapter (52) | `.split` = `ul.bul` + `.kcard` | `.split` = `ul.bul` + `.cards.reg > .tile.key` | 30 | key tile |
| 21 | Sources 1 of 2 (56) | `.links` 7 + 5 | `.links` (same markup as committed twin ai-toolbox-ivory 30) | 30 | none |
| 22 | Sources 2 of 2 (57) | `.links` 7 + 7 + note | `.links` (twin ai-toolbox-ivory 31) | 30 | none |

## Class inventory (root DESIGN.md mapping, then §8 no-equivalent rules)

- Present and mapped:
  - `gloss/row/term/def` → `ul.bul.def.wide`;
  - `kcard` + `big` → `.tile.key` (big → `h3`) inside `.cards`;
  - `fill` → `.tile.key` when one per slide, none when two (04);
  - `reference-banner` → crumb;
  - `reference-slide` → removed;
  - `reference-title` → `h2`;
  - `tight` → removed (size steps only);
  - `muted` → `.mut`;
  - `c4` → `.cards.c4` / `.tbl.c4`;
  - `split` of two tiles → `.cards.c2`;
  - `dark`/`light`/`reveal`/`slide-content` → removed.
- Not present as elements in this source: `lead`, `stat`, `row` outside `.gloss`, `shot`, `dg-dash`, `dg-tangle`, `dense`, `outer`, title `.dot`, `.ts-loopline`, `.title-slide`, `.extag`, `.pills`, `.divider`, `.thanks`, `.diagram`, SVG, video.
- Head and body machinery removed:
  - Google Fonts preconnect/link and `ember_design_system/styles.css`;
  - the 4 inline `<style>` blocks (incl. reference-banner and `.note a`), the presenter-ui style and the `.pui-*` markup;
  - the inline presenter/video script;
  - `ember_design_system/deck-stage.js` → `ivory_design_system/deck-stage.js`, plus `deck.js`.
- The authoring comment was rewritten as a short Ivory comment (not slide content).
