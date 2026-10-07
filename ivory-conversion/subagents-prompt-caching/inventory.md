# subagents-prompt-caching.html → subagents-prompt-caching-ivory.html: per-slide inventory and mapping

Source: `subagents-prompt-caching.html` (Ember, 21 slides, read only). Output: `subagents-prompt-caching-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and `data-speaker-notes` byte for byte, and every href is unchanged (see `content-diff.txt`).
On every slide, Ember `dark`/`light`/`reveal`/`.slide-content` and the hand-written `.snum` digits are removed. `.snum` is left empty, and deck.js numbers it.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` with `.dot`, `.ts-sub`, `.ts-foot` author (no link) | `.title-slide`: `.crumb` kicker, `h1` (2 lines, source `<br>` kept), `p.sub`, `.meta` (Author, Revised) | header label (title exception) | `.dot` "." dropped. No `.ts-loopline` in this deck. No Length cell, so no new text is invented. Same decision as cost-and-context-ivory |
| 02 | 2 | Agenda | light `.cards.c2`, `h3.k` + `p` (2 short items) | `.cards.c2`, titles → `.lab` | none (two equal mechanisms) | Two-line headline (balanced wrap). Kept as cards rather than `ol.bul.def.wide`: the source is two equal mechanisms, not a numbered agenda |
| 03 | 6 | Local and cloud map | light `.cards.c2` (two `<br>` lists) + centred `p.lead` "request → network → response" | full-width `.fig` with a 1:1 SVG (`0 0 1680 480`): two dashed `.dg-box.outer` boundaries (cols 1–4, 9–12), three `.dg-box` components each, request/response `.dg-line` arrows, the lead text as a `.dg-t.acc` label | none (two equal sides) | `.lead` has no Ivory equivalent, and it cannot fold into the headline without changing words. A topology diagram is the §8 "restructure" route. The text is identical and in source order, in its original case (h3 was not uppercased in Ember) |
| 04 | 7 | Subagents | `.split > ul.bul + .diagram > video` (subagents-light.mp4) | `.split > ul.bul + .fig > video` (subagents-ivory.mp4) | none | `.crumb b` dropped. Same as cost-and-context slide 12 |
| 05 | 9 | Delegation lifecycle | dark `.cards.c3`, `h3.k` + `p` (sequential steps) | `.cards.c3`, `lab 01–03` + `h3` + `p` | none (equal steps) | Same as the example's numbered three-card slides. The headline has 4 steps and the cards have 3; that is source content, unchanged |
| 06 | 10 | Fresh or forked | `table.tbl` 2 cols × 2 rows, link in `.note` | `table.tbl.lg` | none | The link stays inline in the one `.note` (one line) |
| 07 | 11 | Return contract | dark `.code` raw 7 lines | `.code` (40px); `TASK:`/`RETURN:`/`SCOPE:` as `.k` | none | Longest line is 52 chars (limit 64) |
| 08 | 12 | Parallel work | light `.cards.c3`, `h3.k` names | `.cards.c3`, names → `.lab` | none | Role names, not steps, so there are no numbers (like the example's Worker/Reviewer) |
| 09 | 14 | Delegation economics | dark `.cards.c2` | `.cards.c2`, `.lab` titles | none (benefit vs cost are weighed equally) | |
| 10 | 16 | Call versus agent | `.code` raw 9 lines with Python indentation | `.code.reg` (30px); line 1 `PSEUDOCODE` as `.c`; `while/if/else/return` as `.k` | none | 9 lines do not fit 40px in a 480 zone. Indentation preserved |
| 11 | 17 | Illustrative helper return | dark `.code` 6 lines (one blank) | `.code` (40px); caption as `.c`; speaker names `.k`; blank line kept as an empty numbered line | none | Longest line is 58 chars |
| 12 | 22 | KV caching | `.split > ul.bul + .diagram > video` (kv-cache-light.mp4) | `.split > ul.bul + .fig > video` (kv-cache-ivory.mp4) | none | `.crumb b` dropped. Identical to agentic-engineering-ivory slide 17 |
| 13 | 25 | Shared prefix example | `.code` 7 lines (two blank, one indented), link in `.note` | `.code` (40px); `Shared eligible prefix`, `Request A:`/`B:` as `.k` | none | Longest line is 57 chars |
| 14 | 27 | Token volume and cost | `table.tbl` 2 × 3 | `table.tbl.lg` | none | Identical to cost-and-context slide 04 |
| 15 | 28 | Cache break-even | dark `.code` 10 lines (2 blank) | `.code.reg` (30px); assumptions as `.c`; `Total cached cost`, `Example r = 0.10:` as `.k`; `→` as `.a` | none | `&lt;` preserved. No clay: the formula could take `.key`, but it was left neutral (see report) |
| 16 | 29 | Cache lifetime | dark `ul.bul` 3 rows, link in `.note` | `ul.bul` | none | |
| 17 | 31 | Verify cache usage | `table.tbl` 2 × 3 | `table.tbl.lg`; field names wrapped in `<code>` (mono) | none | Visible text unchanged |
| 18 | 33 | Warm-up before fan-out | dark `.code` 4 numbered lines, link in `.note` | `.code` (40px) | none | The source writes "1." … "4." in the text, so those stay. The panel's line numbers duplicate them (see report) |
| 19 | 35 | Choose authentication | light `.cards.c2` | `.cards.c2`, `.lab` titles | none (two equal routes) | |
| 20 | 38 | Takeaways | dark `ul.bul` 3 rows + **two** `.note` (2nd = reference-deck link) | `ul.bul` + `.note` + `.src` | none | Ivory allows one footnote, so the link moved to `.src` (same text and href). Same as cost-and-context slide 16 |
| 21 | 39 | Sources | dark `ul.bul` of 3 links | `ul.bul` of 3 links | none | `.links` not used: it needs two columns with `h3` headings that the source does not have. Same as cost-and-context slide 17 |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-top/.ts-hero/.ts-sub/.ts-foot/.ts-author`, `.dot`, `.cards.c2/.c3`, `h3.k`, `ul.bul`, `table.tbl`, `.code`, `.split`, `.diagram > video`, `.crumb b`, `.lead` (slide 03), `dark/light/reveal`, `.slide-content`, `.note` (×2 on slide 20).

Not present in this deck (CSS rules only or absent): `gloss/term/def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-banner` (CSS rule only, no element), `reference-slide`, `reference-title`, `dg-dash`, `dg-tangle`, `dense`, `tight` (CSS rules only), `muted` (CSS rule only), `outer`, `c4`, `.ts-loopline`, `.extag`, `.pills`, inline SVG in the source (none; slide 03's SVG is new, built from the `.cards` + `.lead` content).
