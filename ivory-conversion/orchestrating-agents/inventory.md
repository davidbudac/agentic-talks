# orchestrating-agents.html → orchestrating-agents-ivory.html: per-slide inventory and mapping

Source: `orchestrating-agents.html` (Ember, 19 slides, read only). Output: `orchestrating-agents-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and `data-speaker-notes` byte for byte (checked by `ivory-conversion/audit.py`; see `audit.json` and `content-diff.txt`).
On every slide, Ember `dark`/`light`/`reveal`/`.slide-content` and the hand-written `.snum` digits are removed. `.snum` is left empty, and deck.js numbers it.
No slide has inline SVG, video, image or a link to another deck other than `orchestrating-agents-reference.html`.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` with `.dot`, `.ts-sub`, `.ts-foot` author (no link) | `.title-slide`: `.crumb` kicker, `h1`, `p.sub`, `.meta` (Author, Revised) | header label (title exception) | `.dot` "." dropped. There is no `.ts-loopline` in this deck. No Length cell, so no new text. Author stays unlinked, as in the source |
| 02 | 2 | Agenda | light `.cards.c3`, `h3.k` + `p` (3 short items) | `ol.bul.def.wide` (Ember map: cards used as an agenda) | none (equal items) | Adds `01–03` CSS counters. Same decision as cost-and-context-ivory 02 |
| 03 | 4 | Coordination and containment | dark `.cards.c2`, `h3.k` titles | `.cards.c2`, `.lab` titles | none (two equal decisions) | Same pattern as the example's Worker/Reviewer slide |
| 04 | 15 | Workflow choice | `table.tbl` 2 cols × 4 rows | `table.tbl` (30px, 4 rows) | none (equal rows) | |
| 05 | 7 | Ticket lifecycle | `.code` raw 5 lines | `.code` (40px), state names `.k` | none (equal states) | Longest line 50 chars (limit 64) |
| 06 | 9 | Static ticket walkthrough | dark `table.tbl` 2 × 3 | `table.tbl.lg` | none | Right column wraps to 2 lines at 40px; rows still end on 888 |
| 07 | 10 | Tool boundary | `ul.bul` 3 rows | `ul.bul` | none | |
| 08 | 12 | Loop failure controls | dark `table.tbl` 2 × 3 | `table.tbl.lg`, `th.key` on "Concrete control" | `th.key` | Identical to agentic-engineering-ivory slide 12 (same slide) |
| 09 | 14 | Review capacity | dark `.cards.c3`, `h3.k` + `p` (ordered phases) | `.cards.c3`, `.lab` `01–03` + `h3` + `p` | none (equal phases) | Same anatomy as the example's "Connect a few procedures" slide |
| 10 | 17 | A verification skill | dark `.code` raw 4 lines | `.code` (40px) | none | Identical to agentic-engineering-ivory slide 26 |
| 11 | 19 | Rules, procedure and tool | `table.tbl` 2 × 3 | `table.tbl.lg` | none | |
| 12 | 20 | Share the procedure | dark `.cards.c2`, `h3.k` | `.cards.c2`, `.lab` titles | none | Identical to agentic-engineering-ivory slide 28 |
| 13 | 22 | Skill exercise | dark `.code` raw 5 lines | `.code` (40px), line 1 `.c` | none | Same treatment as cost-and-context-ivory 14 ("10 minutes" as a comment). Longest line 54 chars |
| 14 | 23 | Skill file example | dark `.code` raw 8 lines (YAML frontmatter + steps); `.note` with `<code>` | `.code.reg` (30px); `---` lines `.c`; `name:`/`description:` `.k` | none | 8 lines is over the ~6-line limit for 40px, so `.reg` (§4). Longest line 60 chars |
| 15 | 25 | MCP and CLI | `.cards.c2`, `h3.k` | `.cards.c2`, `.lab` titles | none (two equal interfaces) | |
| 16 | 28 | Tool overhead | dark `ul.bul` 3 rows | `ul.bul` | none | |
| 17 | 30 | Interface comparison exercise | `.code` raw 5 lines (one indented) | `.code` (40px), `Task:` `.k`; indent preserved | none | Longest line 59 chars (limit 64); ends at x ≈ 1675 inside the panel |
| 18 | 31 | Next workflow | dark `ul.bul` 3 rows + **two** `.note` (2nd = reference link) | `ul.bul` + `.note` + `.src` link | none | Ivory allows one footnote, so the link moved to `.src` (same text and href), as in cost-and-context-ivory 16. Kept `ul` because the rows are principles, not steps |
| 19 | 32 | Sources | dark `ul.bul` of 4 links | `ul.bul` of 4 links | none | `.links` not used: it needs two headed columns that the source does not have (same decision as cost-and-context-ivory 17) |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-top/.ts-hero/.ts-sub/.ts-foot/.ts-author`, `.dot`, `.cards.c2/.c3`, `h3.k`, `ul.bul`, `table.tbl`, `.code`, `.note` (×2 on slide 18), `dark/light/reveal`, `.slide-content`, hand-written `.snum`.

Not present as elements in this deck (only as CSS rules in the Ember `<style>`, or not at all): `lead`, `gloss/term/def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-banner` (CSS rule only), `reference-slide`, `reference-title`, `dg-dash`, `dg-tangle`, `dense`/`tight` (CSS only), `muted` (CSS only), `outer` (CSS only), `c4` (CSS only), `.ts-loopline` (CSS only), `.extag`, `.pills`, `.flow`, `.divider`, `.thanks`, `.demo-badge`, `.fallback-box`, `.wip-badge`, `.diagram`, inline SVG, video. Nothing to redraw.
