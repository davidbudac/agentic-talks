# agentic-ai.html → agentic-ai-ivory.html: per-slide inventory and mapping

Source: `agentic-ai.html` (Ember, 26 slides, read only). Output: `agentic-ai-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and the raw `data-speaker-notes` attribute byte for byte. The section opening tags were copied from the source; only the words `dark`/`light` were removed from `class`.
On every slide, Ember's `dark`/`light`/`reveal` classes, the `.slide-content` wrapper, `.crumb b` and `h2 .o` spans, and the hand-written `.snum` digits are removed. `.snum` is left empty and deck.js numbers it.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` "Agentic AI" + `.dot`, `.ts-sub`, `.ts-foot` (author link + `.ts-loopline`) | `.title-slide`: `.crumb`, `h1`, `p.sub`, `.meta` (Author, Revised) | header label (title exception) | `.dot` "." and `.ts-loopline` "model → harness → agent ↺" dropped, as instructed. "Revised October 2026" became the `Revised` label + "October 2026" (same as cost-and-context). No Length cell, because that would be new text |
| 02 | 2 | The hook | dark `.code`, 7 raw lines incl. 1 blank; `.o .b .c .g` spans | `.code` 40px, 6 `.l` lines (terminal trace) | `PASS ✓` | The blank line is dropped (whitespace only). `.o`→`.k`, `.b`→plain, `.g`→`.key`. Longest line 57 chars (limit 64) |
| 03 | 3 | Chatbot vs agent | dark `.split` of `.tile` + `.tile.fill`, `span.k` titles | `.cards.c2`, `.lab` titles, `.tile.key` on Agent | Agent tile | Root map: `.tile.fill` → `.tile.key`. The left tile stays plain, not `.was`, because the source did not mute it |
| 04 | 5 | Agenda | `.cards.c3` used as agenda | `ol.bul.def.wide` | none (equals) | Root map. Adds `01–03` counters |
| 05 | 10 | Model in the cloud | dark `.diagram > svg` 820×320 (curves, coral lines, `.hot` box) | `.fig > svg` 1680 × 480 (two-line headline), redrawn 1:1 | CLAUDE CODE box (`.dg-box.key`) | Orthogonal connectors, slate lines, return arrow `.dim`. All 17 SVG strings kept in their original case. Two-line footnote (no `.src`) |
| 06 | 9 | No memory in practice | `.lead` + `.code` (4 lines, one 78 chars) + note | `.split`: `ul.bul` (the lead, 2 rows split at the sentence boundary) + `.fig > svg` 828 × 562 redrawn 1:1: the source comment as a two-line mono caption, three message boxes in source order (label + quoted utterance), the trailing comment under them with a dim connector back to the first box | first message box (`.dg-box.key`) | Round 2: replaced the round-1 numbered `.code.reg`, where "line 1" and "Delete the first line" pointed at line **04**. No line numbers now; the first utterance is the first box. No words changed |
| 07 | 11 | What one turn sends | dark `.code` 5 raw lines | `.code` 40px, group names `.k` | none (five equal groups) | Two-line headline |
| 08 | 4 | Optional demo | dark `.code` 3 raw lines | `.code` 40px | none | |
| 09 | 12 | The agent loop | dark `.split`: video (agent-loop-dark.mp4) then `ul.bul` with bold leads | `.split`: `ol.bul` with inline `<b>` then `.fig > video` (agent-loop-ivory.mp4) | none added (video carries its own) | Same as kitchen-sink 18 (ordered steps). Round 2: text left, video right, as in agentic-engineering-ivory and DESIGN.md §7 video placement (the source's figure-first order is not a content requirement) |
| 10 | 13 | The loop, worked example | `.code` 5 raw lines | `.code` terminal trace, `.a` arrows | `PASS` | Same as kitchen-sink 17 |
| 11 | 14 | Thinking | dark `.split`: svg 400×300 then `ul.bul` | `.split.flip`: `.fig > svg` 828 × 562, redrawn 1:1; `ul.bul` | ANSWER box (`.dg-box.key`) | `.hot` → `.key`; `outer` box dashed |
| 12 | 21 | Choose an interface | `.cards.c3`, `span.k` titles | `.cards.c3`: `.lab` 01–03 + `h3` + `p` | none | Same as the example's equal c3 slides |
| 13 | 26 | Choose a billing route | dark `.cards.c2` | `.cards.c2`, `.lab` titles | none | |
| 14 | 28 | What context is | `.split`: `ul.bul` then svg 400×250 (fill-r + hot rows, `dg-dash` free space) | `.split`: `ul.bul` + `.fig > svg` 828 × 480 (headline wraps to two lines), redrawn | none (equal parts) | `dg-fill-r`/`.hot` clay rows neutralised; `dg-dash` → `.dg-box.outer`. No `.note` in the source |
| 15 | 29 | Context quality | dark `.cards.c2` | `.cards.c2`, `.lab` titles | none | Left neutral (the source did not emphasise either side) |
| 16 | 30 | Keep context useful | `.cards.c3` | `.cards.c3` `.lab` 01–03 + `h3` | none | Two-line headline |
| 17 | 31 | Caching and compaction | dark `.cards.c2` | `.cards.c2`, `.lab` titles | none | |
| 18 | 32 | Sub-agents | `.split`: video (subagents-light.mp4) then `ul.bul` | `.split`: `ul.bul` then `.fig > video` (subagents-ivory.mp4) | none added | Two-line headline. No `.note` in the source. Round 2: text left, video right, as in the example deck |
| 19 | 33 | Permissions | dark `.cards.c3` | `.cards.c3` `.lab` 01–03 + `h3` | none | |
| 20 | 36 | Project rules | `.code` 5 raw lines | `.code` 40px, first line `.c` | none | |
| 21 | 37 | Skills and plugins | dark `.code` 4 raw lines | `.code` 40px | none | |
| 22 | 38 | Tools for the invoice task | `.cards.c3` | `.cards.c3` `.lab` 01–03 + `h3` | none | |
| 23 | 39 | MCP | dark `.split`: svg 440×250 (diagonal `dg-tangle` + coral hub lines) then `ul.bul` | `.split.flip`: `.fig > svg` 828 × 562, redrawn; `ul.bul` | MCP hub (`.dg-box.key`) | The diagonal tangle becomes 9 orthogonal hairline (`.dim`) routes. Hub lines are slate. Boxes stay unlabeled, as in the source |
| 24 | 40 | Your first agent task | dark `ul.bul` with bold leads (full width) + note with 2 links | `ol.bul.def.wide` + `.note` (both links) | none | Same as example slide 29 |
| 25 | 42 | Sources 1 of 2 | `.links`: 8 links + 4 links | `table.tbl.num`: `thead` = group 1 label, `th` row = group 2 label, `td` title link + `td` grey URL | none | **Unfit for `.links`**: 8 rows overflowed and collided (pass-1 screenshot). See report |
| 26 | 43 | Sources 2 of 2 | `.links`: 6 links + 4 links, one 2-line title | same table layout as 25 | none | **Unfit for `.links`**: the long title wrapped and overflowed (pass 1) |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-*` (`.ts-top`, `.ts-hero`, `.ts-sub`, `.ts-foot`, `.ts-author`, `.ts-loopline`), `.dot`, `.cards.c2/.c3`, `span.k` titles, `.tile.fill`, `ul.bul` (incl. bold leads), `.code` with `.o .b .c .g` spans, `.split`, `.diagram > svg/video`, `.lead`, `.dg-box` (`.hot`, `.outer`, `.mid`), `.dg-t` (`.on`, `.mut`, `.acc`), `.dg-line` (`.dim`), `.dg-tangle`, `.dg-dash`, `.dg-fill-r`, `.links/.linkcol/.u`, `.crumb b`, `h2 .o`, `dark/light/reveal`, `.slide-content`.

Not present as elements (only CSS rules in the old `<style>` block): `gloss/term/def/row`, `kcard`, `stat`, `big`, `shot`, `reference-banner/-slide/-title`, `dense`, `tight`, `muted`, `c4`, `pills/pill`, `extag`, `divider`, `thanks`.

Removed head/body machinery: Google Fonts preconnect/links, `ember_design_system/styles.css`, the three inline `<style>` blocks in `<head>`, the inline video-restart script, `<style id="presenter-ui-css">`, the `.pui-*` markup and the presenter script. `ember_design_system/deck-stage.js` → `ivory_design_system/deck-stage.js`; `ivory_design_system/deck.js` was added. The pre-deck `<!-- OPTIONAL DEMO … -->` authoring comment is kept.
