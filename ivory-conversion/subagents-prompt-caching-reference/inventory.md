# Subagents & Prompt Caching Reference: per-slide inventory

Source: `subagents-prompt-caching-reference.html` (working tree, untracked, read only). It has 4 `<section>`s and no media (`<video>`, `<img>` or `<source>`: 0). Output: `subagents-prompt-caching-reference-ivory.html`.

Every source slide also carries a `.reference-banner` reading "Optional reference · <a href="subagents-prompt-caching.html">Back to the talk</a>".

| # | origin | data-label | Source pattern | Text amount | Links | Ivory component | Clay |
|---|---|---|---|---|---|---|---|
| 01 | 0 | Title | Ember `.title-slide` (dark): `.ts-top` (`.k` "Optional reference", `.meta` "Revised October 2026"), `.ts-hero h1` "Subagents & Prompt Caching<br>Reference" + `.dot`, `.ts-sub` with link, `.ts-foot` author. Banner. No `.ts-loopline` | Title + 1 sentence + author/date | 2 × `subagents-prompt-caching.html` (banner, sub) | **r2 (final):** regular `.slide`: crumb "Optional reference", `h2` "Subagents &amp; Prompt Caching<br>Reference" (2 lines), `.zone > .cards.c2`: tile 1 = `p` subtitle + "Return to the main talk" link; tile 2 = `h3` "David Budáč" + `p` "Revised October 2026"; `p.note` "Optional reference · Back to the talk" (the banner, link kept). *r1 (superseded): `.title-slide` + 3-line `h1` + `.meta`.* | None |
| 02 | 23 | Cache block | `.code` raw JSON, 5 lines | 5 short lines (longest 41 chars) + note | banner | `.code` (40px), one `.l` per line | `.key` on the `"cache_control"` token |
| 03 | 30 | Multiple breakpoints | `ul.bul`, 3 items, note with link | 3 one-line rows | banner + prompt-caching docs | `ul.bul` (full width) + `.note` with inline link | None (equal points) |
| 04 | 36 | Choose authentication | `.cards.c2 > .tile > h3.k + p` | 2 tiles | banner + legal-and-compliance docs | `.cards.c2` (h3 + p, `.k` dropped) + `.note` with inline link | None (equal alternatives) |

Header on 02–04: the original crumb and the banner are merged with a middle dot, as in the accepted precedents: "In practice · Optional reference · Back to the talk" (link kept).

Class mapping used (root DESIGN.md):

- `title-slide` / `ts-*` → r2: regular `.slide` + `h2` + `.cards.c2` (subtitle tile, author/date tile), with `.dot` dropped (r1 used `.title-slide`, rejected: 3-line `h1`)
- `reference-banner` → `.crumb` on 02–04, and the footer `.note` on 01 (r2; r1 used a third `.meta` cell)
- `slide-content`, `reveal`, `dark`/`light` → removed
- `.snum` digits → empty
- `h3.k` → `h3`

None of lead, gloss, term, def, kcard, fill, stat, big, row, shot, reference-slide, reference-title, dg-*, dense, tight, muted, outer or c4 occur in this source.
