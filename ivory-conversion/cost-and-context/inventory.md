# cost-and-context.html → cost-and-context-ivory.html: per-slide inventory and mapping

Source: `cost-and-context.html` (Ember, 17 slides, read only). Output: `cost-and-context-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and `data-speaker-notes` byte for byte (checked by `compare.py`).
Ember `dark`/`light`/`reveal`/`.slide-content` and hand-written `.snum` digits are removed on every slide. `.snum` is left empty, and deck.js numbers it.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` with `.dot`, `.ts-sub`, `.ts-foot` author | `.title-slide`: `.crumb` kicker, `h1`, `p.sub`, `.meta` (Author, Revised) | header label (title exception) | `.dot` "." dropped (as instructed). There was no `.ts-loopline` in this deck. A `<br>` was added in `.sub` after "task." to avoid a one-word orphan. No Length cell was added, so no new text appears |
| 02 | 2 | Agenda | light `.cards.c3` with `h3.k` + `p` (3 short items) | `ol.bul.def.wide` (Ember map: cards used as agenda) | none (equal items) | Adds `01–03` counters |
| 03 | 13 | Choose the route | `table.tbl` 2 cols × 3 rows | `table.tbl.lg` | none (equal needs) | |
| 04 | 4 | Token volume and cost | `table.tbl` 2 × 3 | `table.tbl.lg` | none | Same decision as agentic-engineering-ivory slide 15 |
| 05 | 5 | Output cost | dark `ul.bul` 3 rows | `ul.bul` | none | |
| 06 | 6 | Worked cost example | dark `table.tbl` with bold total `<td><b>` | `table.tbl.num` + `tr.tot`, `b.key` on total | `$0.0506` total | Same as example slide 16. The hero + bars variant was not used because it adds visible text |
| 07 | 15 | Useful context | dark `.cards.c2`, `h3.k` titles | `.cards.c2`, `.lab` titles, `.tile.key` on Keep | Keep tile | Same as example slide 18 |
| 08 | 17 | Request anatomy | dark `ul.bul` 4 rows | `ul.bul` | none | |
| 09 | 18 | Project instructions | `.code` raw 5 lines | `.code` (40px), first line `.c` comment | none | Same as example slide 25. Longest line is 56 chars (limit is 64) |
| 10 | 19 | Instruction file before and after | `.cards.c2` Before/After `h3.k` | `.cards.c2`: `.tile.was` + `.tile.key`, `.lab` | After tile | Ember map: before/after |
| 11 | 21 | Continue or reset | dark `.cards.c2` `h3.k` | `.cards.c2`, `.lab` titles | none (two equal states) | Like the example's Worker/Reviewer slide |
| 12 | 22 | Subagents | `.split > ul.bul + .diagram > video` (subagents-light.mp4) | `.split > ul.bul + .fig > video` (subagents-ivory.mp4) | none | Same as example slide 19. `.crumb b` dropped |
| 13 | 23 | Read selectively | `ul.bul` 3 rows | `ul.bul` | none | Two-line headline |
| 14 | 24 | Compare instruction variants | dark `.code` raw 5 lines | `.code` (40px). Line 1 `.c`; `A:`/`B:`/`Record:` `.k` | none | Longest line is 59 chars |
| 15 | 25 | Static comparison worksheet | `table.tbl` 3 cols × 4 rows | `table.tbl.c3` (30px) | none | See report: B column could arguably take `th.key` |
| 16 | 26 | Next task | dark `ul.bul` 3 steps + **two** `.note` (2nd = reference link) | `ol.bul` (ordered steps) + `.note` + `.src` link | none | Ivory allows one footnote, so the link moved to `.src` (same text and href) |
| 17 | 28 | Sources | dark `ul.bul` of 3 links | `ul.bul` of 3 links | none | `.links` not used: it needs two balanced columns and `h3` headings that do not exist in the source |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-*`, `.dot`, `.cards.c2/.c3`, `h3.k`, `ul.bul`, `table.tbl`, `.code`, `.split`, `.diagram > video`, `.crumb b`, `dark/light/reveal`, `.slide-content`, `.note` (×2 on slide 16).

Not present in this deck: `lead`, `gloss/term/def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-banner` (CSS rule only, no element), `reference-slide`, `reference-title`, `dg-dash`, `dg-tangle`, `dense`, `tight` (CSS rules only), `muted`, `outer`, `c4`, `.ts-loopline`, inline SVG (so there was nothing to redraw).
