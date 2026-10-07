# Claude Best Practices: per-slide inventory and mapping

Source `best-practices.html` (Ember, 30 slides, read only) → `best-practices-ivory.html`. Every content slide in the source has `.note`, and most also have `.src` ("Applied example · supporting documentation"), which maps to Ivory `.src` unchanged. In the source, `dark` and `light` alternate. All Ivory slides are light.

| # | Origin | Label | Ember pattern | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` + `.dot`, `.ts-sub`, `.ts-author` | `.title-slide`: `.slide-head` crumb, `h1` (2 lines), `p.sub`, `.meta` (Author, Revised) | Header label (title-slide rule) | `.dot` dropped. No `.ts-loopline` in source. No Length cell, no author link (source has none; matches cost-and-context-ivory) |
| 02 | 2 | Agenda | light `.cards.c3`, `h3.k` + `p` as agenda | `ol.bul.def.wide` | none (equals) | Root mapping row ".cards.c3 used as an agenda"; same as cost-and-context-ivory 02 |
| 03 | 4 | Simplifying prompts | dark `.cards.c2`, `h3.k` + `p`; `.note` is a single link | `.cards.c2`, titles → `.lab` | `.tile.key` on "Your next step" | Reported claim vs. your test; the test is the point of "…a reason to test" |
| 04 | 6 | Instruction file before and after | light `.cards.c2` Before / After + `.src` | `.cards.c2` `.was` + `.key` | `.tile.key` After | Identical to cost-and-context-ivory 10, plus `.src` |
| 05 | 7 | Instruction audit | light `.code` 6 raw lines (one blank) | `.code` (40px); caption → `.c`; blank line kept as an empty numbered line | `.key` on "Replacement:" | Longest line 56 chars |
| 06 | 9 | A verification skill | dark `.code` 4 lines; `<b>` + → in note | `.code` (40px) | none | Identical to agentic-engineering-ivory 26, plus `.src`. Longest line 55 chars |
| 07 | 11 | Skill interface | dark `.cards.c2` | `.cards.c2`, titles → `.lab` | none (equals) | |
| 08 | 12 | Skill structure | light `.code` 4 lines | `.code` (40px) | none | Longest line 52 chars |
| 09 | 14 | Shared prefix example | light `.code` 7 lines (two blank); link in `.note` + `.src` | `.code` (40px) | none | Identical to subagents-prompt-caching-ivory 13, plus `.src` |
| 10 | 15 | Worked cost example | dark `table.tbl` + bold total cell | `table.tbl.num`, `tr.tot`, `b.key` total | `$0.0506` | Identical to cost-and-context-ivory 06, plus `.src` |
| 11 | 16 | Cache tradeoffs | dark `.cards.c2` | `.cards.c2`, titles → `.lab` | none (equals) | |
| 12 | 17 | Compaction | light `.code` 5 lines (heading + 4 items) | `.code` (40px); heading → `.k` | none | Longest line 53 chars |
| 13 | 19 | Effort comparison | dark `table.tbl` 2 × 2 | `table.tbl.lg` | `th.key` Compare | Same as kitchen sink 12 |
| 14 | 21 | Build and verify | light `.cards.c2`; `.note` starts with a link, no `.src` | `.cards.c2`, titles → `.lab` | `.tile.key` "Acceptance test" | Proposal vs. the test that decides it; same reasoning as 03 |
| 15 | 22 | Routing and escalation | dark `ul.bul` with `<b>Lead:</b>` | `ol.bul.def` | none | Identical to agentic-engineering-ivory 21, plus `.src` |
| 16 | 23 | Cost per accepted task | light `.cards.c3`, `h3.k` + `p` | `.cards.c3`, `lab 01–03` + `h3` + `p` | none (equals) | Identical to agentic-engineering-ivory, plus `.src` |
| 17 | 27 | Real verification | dark `.code` header + "1."–"4." lines | `.code` (40px); header → `.k` | none | The literal "1."–"4." are source text and stay. The panel numbers them 02–05 (see report) |
| 18 | 26 | Progress and regression checks | light `.cards.c2` | `.cards.c2`, titles → `.lab` | none (metric and guardrail are equal halves) | |
| 19 | 28 | Grading methods | dark `.cards.c3` | `.cards.c3`, `lab 01–03` + `h3` + `p` | none (equals) | Identical to measuring-what-works-ivory 05, plus `.src` |
| 20 | 29 | Avoid overfitting | dark `ul.bul` 3 rows | `ul.bul` | none | |
| 21 | 31 | A bounded task contract | light `.code` 6 lines | `.code` (40px); field names `.k` | `.key` on `VERIFY:` | Identical to agentic-engineering-ivory 13 / kitchen sink 15, plus `.src` |
| 22 | 32 | Handoff | light `.code` 6 lines (one blank) | `.code` (40px); `TASK STATE`/`HELPER TASK` → `.k` | none | Longest line 60 chars (limit is about 64), ends at about x 1700 |
| 23 | 33 | Human decisions | dark `.cards.c3` | `.cards.c3`, `lab 01–03` + `h3` + `p` | none (equals) | |
| 24 | 36 | Two useful patterns | light `.cards.c2` | `.cards.c2`, titles → `.lab` | none (equals) | |
| 25 | 38 | Cost and containment | dark `.cards.c2` | `.cards.c2`, titles → `.lab` | none (equals) | |
| 26 | 40 | Tool interface | light `.code` 6 lines | `.code` (40px); title → `.c`, field names → `.k` | `.key` on "failed" | Like the PASS token in kitchen sink 17 |
| 27 | 41 | Useful HTML output | dark `.cards.c2` | `.cards.c2`, titles → `.lab` | none (equals) | |
| 28 | 42 | Hooks and extensions | light `ul.bul` 3 rows; link in `.note` + `.src` | `ul.bul` | none | |
| 29 | 44 | Tomorrow | dark `ul.bul`; `.note` + `.src` + a second `.note` (reference link) | `ul.bul`; `.note` + one `.src` holding both links | none | Second `.note` merged into `.src` with a `·` separator (Ivory allows one footnote) |
| 30 | 45 | Sources | dark `ul.bul` of 4 links | `ul.bul` | none | Same as cost-and-context-ivory 17 |

Removed with no visible-text loss: `.slide-content` wrappers, `.reveal`, `dark`/`light`, `h3.k`'s `.k`, hand-written `.snum` digits (2–30, now filled by deck.js), the Ember font links, every inline `<style>`, the inline slide-change script, the presenter-UI script and markup, and `ember_design_system/` includes.
