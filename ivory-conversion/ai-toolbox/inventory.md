# ai-toolbox.html → ai-toolbox-ivory.html: per-slide inventory and mapping

Source: `ai-toolbox.html` (Ember, 31 slides, read only). Output: `ai-toolbox-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and `data-speaker-notes` byte for byte (checked by `ivory-conversion/audit.py`, output in `audit.json`).
On every slide, Ember `dark`/`light`/`reveal`, the `.slide-content` wrapper, the hand-written `.snum` digits, `h2 .o` and `.crumb b` were removed. `.snum` is left empty, and deck.js numbers it.
Card titles (`span.k`) become `.lab` mono labels, the same decision as agentic-engineering-ivory and cost-and-context-ivory.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Size | Clay | Notes |
|---|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` + `.dot`, `.ts-sub` with 2 `<b>`, `.ts-foot` (author link + `.ts-loopline`) | `.title-slide`: `.crumb`, `h1`, `p.sub`, `.meta` (Author link, Revised) | — | header label (title exception) | `.dot` "." and `.ts-loopline` "chat → agent → toolbox ↺" dropped. No Length cell |
| 02 | 2 | The hook | dark `.cards.c2`, 2 tiles, short quotes | `.cards.c2`: `.tile.was` + `.tile.key` | 40 | "An editable draft" tile | Same decision as example slide 02 (vague vs checkable) |
| 03 | 3 | Agenda | light `.cards.c3` used as agenda | `ol.bul.def.wide` | 40 term / 30 def | none | Root map: cards as agenda |
| 04 | 23 | One task, agent-style | dark `.code`, 5 raw lines, aligned keyword column | `.code`, `INPUT`… as `.k` | 40 | none (equal steps) | Longest line 52 chars (limit 64). Spaces preserved |
| 05 | 5 | Chatbot vs agent | dark `.split` of `.tile` + `.tile.fill` with inline `<b>` | `.cards.c2`: `.tile` + `.tile.key` | 40 | Agent tile (was `.fill`) | Root map: `.tile.fill` → `.tile.key` |
| 06 | 6 | The agent loop | dark `.split`: `.diagram > video` LEFT + `ul.bul` (3, `<b>` lead) | `.split`: `ul.bul` + `.fig > video` | 30 | none (clay inside the video asset) | `agent-loop-ivory.mp4` 1152×912. Rows-left order, as in example slide 10 |
| 07 | 7 | The model has no memory | dark `.split`: video LEFT + `ul.bul` (3) | `.split`: `ul.bul` + `.fig > video` | 30 | none | `stateless-ivory.mp4` 1200×900 |
| 08 | 25 | The human checkpoint | dark `.cards.c3` | `.cards.c3` | 40 | none (equals) | |
| 09 | 22 | Three everyday tasks | light `.cards.c3` | `.cards.c3` | 40 | none | `&nbsp;` before "→" in tile 2 (pass-1 fix) |
| 10 | 18 | Choose a starting point | dark `.cards.c3` | `.cards.c3` | 40 | none | |
| 11 | 14 | Agents for files | light `.code`, 4-line quoted prompt | `.code` | 40 | none | Longest line 38 chars |
| 12 | 15 | Design by iteration | dark `.cards.c3` | `.cards.c3` | 40 | none | |
| 13 | 17 | Research over your documents | light `.cards.c2` | `.cards.c2` | 40 | none | Footnote wraps to 2 lines (allowed, no `.src`) |
| 14 | 4 | Read the price tag | dark `.cards.c2` | `.cards.c2` | 40 | none | Two-line headline |
| 15 | 20 | Products change | light `ul.bul` (3) | `ul.bul` | 30 | none | |
| 16 | 27 | Build a small app | light `.cards.c2` | `.cards.c2` | 40 | none | |
| 17 | 28 | Generated video | dark `.cards.c2` | `.cards.c2` | 40 | none | |
| 18 | 29 | Templated video | light `.cards.c2` | `.cards.c2` | 40 | none | |
| 19 | 31 | Voice and dubbing | light `.cards.c2` | `.cards.c2` | 40 | none | |
| 20 | 33 | Images and design | light `.cards.c2` | `.cards.c2` | 40 | none | |
| 21 | 37 | Repeatable automation | light `.cards.c2` | `.cards.c2` | 40 | none | |
| 22 | 38 | Before real use | dark `.cards.c3` | `.cards.c3` | 40 | none | |
| 23 | 41 | Story: Project Vend | light `.cards.c2` | `.cards.c2` | 40 | none | Two-line headline |
| 24 | 45 | Story: the craft still matters | dark `.cards.c2` | `.cards.c2` | 40 | none | |
| 25 | 53 | Three integration routes | light `.cards.c3` | `.cards.c3` | 40 | none | |
| 26 | 49 | Files from chat | dark `.code`, 4 raw lines | `.code`, keywords `.k` | 40 | none | Longest line 53 chars. Two-line headline |
| 27 | 48 | Edit inside the app | light `.cards.c2` | `.cards.c2` | 40 | none | Two-line headline |
| 28 | 47 | MCP | dark `.split`: inline SVG LEFT (440×250 viewBox, diagonal `dg-tangle` lines, `fill`/`font-size`/`stroke` attributes, `.hot` hub) + `ul.bul` (3). No `.note` | `.split`: `ul.bul` + `.fig > svg` **redrawn 1:1 at 828×562** | 30 | MCP hub box + its label (one element) | Orthogonal paths only. No presentation attributes. `.hot`→`.key`, `.on`→`.key`, `dg-tangle`→`.dg-line.dim`. Labels keep source text and case. No footnote (none in source) |
| 29 | 54 | Choose one task | dark `ul.bul` with `<b>Lead:</b>` (3) + note with 2 links | `ol.bul.def` + `.note` (both links) | 40 term / 30 | none | Root map: bold lead-ins at full width → `ol.bul.def`. Links `ai-toolbox-reference.html`, `index.html` unchanged |
| 30 | 56 | Sources 1 of 2 | light `.links` 7 + 5 links, `target=_blank` | `.links` | 30 | none | Unequal columns from the source (Ivory recommends 3–5 equal). Rows are tight (74px). No `.note` (none in source) |
| 31 | 57 | Sources 2 of 2 | light `.links` 7 + 7 links + note | `.links` + `.note` | 30 | none | 7 rows per column, tight |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-*` (`ts-top`, `ts-hero`, `ts-sub`, `ts-foot`, `ts-author`, `ts-loopline`), `.dot`, `.meta`, `.cards.c2/.c3`, `.tile`, `.tile.fill` (→ `.tile.key`), `span.k`, `ul.bul`, `.code` (raw text), `.split`, `.diagram > video`, `.diagram > svg`, `.dg-box`, `.dg-box.hot`, `.dg-t.mut/.acc/.on`, `dg-tangle` (no Ivory class → `.dg-line.dim`), `.links/.linkcol/.u`, `.crumb b`, `h2 .o`, `dark/light/reveal`, `.slide-content`, `.note`.

Not present in this deck's slides: `lead`, `gloss/term/def`, `kcard`, `stat`, `big`, `row`, `shot`, `reference-banner`, `reference-slide`, `reference-title`, `dg-dash`, `dense`, `tight`, `muted`, `outer`, `c4`, `table.tbl`, `.extag`, `.pills`. Some of them (`dense`, `tight`, `muted`, `kcard`, `stat`, `gloss`, `dg-dash`) exist only as CSS rules in the deleted inline `<style>`.
