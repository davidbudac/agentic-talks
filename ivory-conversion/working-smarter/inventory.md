# Working Smarter with Agents: per-slide inventory and mapping

Source `working-smarter.html` (Ember, 44 slides) → `working-smarter-ivory.html` (Ivory, 44 slides). Order unchanged.

"Twin" means a committed Ivory slide whose source has the same `data-label`, raw notes and visible text. Its markup was reused verbatim, with this deck's `data-origin-slide` and an empty `.snum`.

| # | Origin | Label | Ember pattern | Ivory component | Size | Clay | Notes |
|---|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top`, `h1` + `.dot`, `.ts-sub`, `.ts-foot .ts-author` | Title slide: `.slide-head` + `h1` + `p.sub` + `.meta` (Author, Revised) | 176px | header label (title rule) | Dot removed; "Revised October 2026" moved to `.meta`; no "Length" cell |
| 02 | 2 | Workshop route | `table.tbl`, 3 cols × 5 rows, one empty cell | `.tbl.c3` | 30px | none | Empty Break/output cell kept empty |
| 03 | 49 | What an eval measures | `.cards.c3 > .tile > h3.k + p` | `.cards.c3`, `lab 01–03` + `h3` + `p` | 40px | none (equals) | Same decision as orchestrating/agentic-engineering c3 tiles |
| 04 | 50 | Acceptance cases | `table.tbl`, 2 cols × 4 rows | `.tbl` | 30px | none | |
| 05 | 51 | Grading methods | `.cards.c3` | `.cards.c3`, `lab 01–03` + `h3` | 40px | none (equals) | |
| 06 | 52 | Repeated trials | raw-text `.code` with blank line | `.code`, 4 `span.l`; caption line → `.c` lead | 40px | `pass` (the single success) | Blank line dropped; longest line 60 chars |
| 07 | 53 | Trace evidence | `ul.bul` (3) | `ul.bul` | 30px | none | |
| 08 | 54 | Annotated trace | `table.tbl`, 2 cols × 3 rows | `.tbl.lg` | 40px | none | Same layout as twin slide 24 (3-row `.lg` under two-line headline) |
| 09 | 56 | Results worksheet | `table.tbl`, 4 rows | `.tbl` | 30px | none | |
| 10 | 57 | Grading exercise | raw-text `.code` with blank line | `.code`, 5 lines; `10 minutes…` → `.c`; `A:`/`B:` → `.k` | 40px | none | Blank line dropped |
| 11 | 58 | Exercise debrief | `table.tbl`, 3 cols × 4 rows | `.tbl.c3` | 30px | none | |
| 12 | 4 | Token volume and cost | `table.tbl` 3 rows | twin cost-and-context 04: `.tbl.lg` | 40px | none | |
| 13 | 6 | Worked cost example | `table.tbl` with bold total | twin cost-and-context 06: `.tbl.num` + `tr.tot` | 30px | total `$0.0506` | |
| 14 | 13 | Choose the route | `table.tbl` 3 rows | twin cost-and-context 03: `.tbl.lg` | 40px | none | |
| 15 | 15 | Useful context | `.cards.c2` | twin cost-and-context 07: `.cards.c2`, `.tile.key` on Keep | 40px | Keep tile | |
| 16 | 18 | Project instructions | raw-text `.code` | twin cost-and-context 09: `.code` (comment line `.c`) | 40px | none | |
| 17 | 19 | Instruction file before and after | `.cards.c2` Before/After | twin cost-and-context 10: `.tile.was` + `.tile.key` | 40px | After tile | |
| 18 | 24 | Compare instruction variants | raw-text `.code` | twin cost-and-context 14 | 40px | none | |
| 19 | 25 | Static comparison worksheet | `table.tbl` 3 cols | twin cost-and-context 15: `.tbl.c3` | 30px | none | |
| 20 | 21 | Continue or reset | `.cards.c2` | twin cost-and-context 11 | 40px | none | |
| 21 | 22 | Subagents | `.split > ul.bul + .diagram > video` | twin cost-and-context 12: `.split > ul.bul + .fig > video` | 30px | none | `subagents-light.mp4` → `subagents-ivory.mp4`; crumb `<b>` dropped |
| 22 | 28 | Coordination and containment | `.cards.c2` | twin orchestrating-agents 03 | 40px | none | |
| 23 | 31 | Ticket lifecycle | raw-text `.code` | twin orchestrating-agents 05 (state names `.k`) | 40px | none | |
| 24 | 33 | Static ticket walkthrough | `table.tbl` 3 rows | twin orchestrating-agents 06: `.tbl.lg` | 40px | none | |
| 25 | 34 | Tool boundary | `ul.bul` | twin orchestrating-agents 07 | 30px | none | |
| 26 | 36 | Loop failure controls | `table.tbl` 3 rows | twin orchestrating-agents 08: `.tbl.lg`, `th.key` | 40px | Concrete control header | |
| 27 | 38 | Review capacity | `.cards.c3` | twin orchestrating-agents 09: `lab 01–03` + `h3` | 40px | none | |
| 28 | 43 | Rules, procedure and tool | `table.tbl` 3 rows | twin orchestrating-agents 11: `.tbl.lg` | 40px | none | |
| 29 | 41 | A verification skill | raw-text `.code` + note with `<b>` | twin orchestrating-agents 10 | 40px | none | Indentation preserved |
| 30 | 46 | Skill exercise | raw-text `.code` | twin orchestrating-agents 13 | 40px | none | |
| 31 | 47 | Skill file example | raw-text `.code`, 8 lines | twin orchestrating-agents 14: `.code.reg` | 30px | none | Line numbers 05–08 sit beside list items "1."–"4." (no line references in text) |
| 32 | 44 | Share the procedure | `.cards.c2` | twin orchestrating-agents 12 | 40px | none | |
| 33 | 60 | MCP and CLI | `.cards.c2` | twin orchestrating-agents 15 | 40px | none | |
| 34 | 63 | Tool overhead | `ul.bul` | twin orchestrating-agents 16 | 30px | none | |
| 35 | 65 | Interface comparison exercise | raw-text `.code` | twin orchestrating-agents 17 | 40px | none | Indented line 4 preserved |
| 36 | 67 | Cost per accepted task | `.cards.c3` | twin agentic-engineering 20 (hand-written snum `20` emptied) | 40px | none | |
| 37 | 72 | Local model memory | `ul.bul` | `ul.bul` | 30px | none | |
| 38 | 74 | Hardware experiment | `table.tbl` 4 rows | `.tbl` | 30px | none | |
| 39 | 75 | Static hardware exercise | raw-text `.code` with blank line | `.code`, 5 lines, first `.c` | 40px | none | Blank line dropped; longest 60 chars |
| 40 | 77 | Local or hosted | `.cards.c2` | `.cards.c2` with labels | 40px | none (equal options) | |
| 41 | 79 | Voice input | raw-text `.code` with blank line | `.code`, 5 lines; `Spoken:`/`Check…:` `.k` | 40px | `WITHOUT` (the negation) | Blank line dropped |
| 42 | 80 | Static voice exercise | `.cards.c2` | `.cards.c2` with labels | 40px | none (pair to compare) | |
| 43 | 82 | Workshop close | raw-text `.code` + 2 `.note` (2nd = reference link) | `.code` 6 lines + `.note` + `.src` link | 40px | none | Second note → `.src` (one footnote rule), same text/href |
| 44 | 83 | Sources | `ul.bul` of 5 links | `ul.bul` (5 rows) | 30px | none | `.links` would need two headed columns not in source |

Classes from the brief and how they map in this deck:

- Used and mapped: `dark`/`light`/`reveal`/`slide-content` (removed); `.title-slide` `.dot`/`.ts-*` (title slide); `h3.k` (`h3` or `.lab`); `.diagram` (`.fig`).
- Not present in this source: `lead`, `gloss`/`term`/`def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-banner`/`reference-slide`/`reference-title`, `dg-dash`/`dg-tangle`, `dense`, `tight`, `muted`, `outer`, `c4`. The `.reference-banner` CSS rule existed but no element used it.
- No SVG in this deck, so nothing to redraw.
