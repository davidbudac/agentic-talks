# Working Smarter Reference: source inventory and mapping

- **Source:** `working-smarter-reference.html`, Ember. It is untracked, and I only read it.
  - sha256 `51a2f4e8…6193d2993`, 38831 bytes, mtime 1791057542. Unchanged after conversion.
- **Slide count:** 8.
- **Media:** none. There are no `<video>`, `<img>` or SVG elements.
- **Visible on every source slide:**
  - A `.reference-banner`: "Optional reference · Back to the talk" (`working-smarter.html`).
  - A hand-written `.snum`.

| # | origin | data-label | Ember pattern | Text | Links (besides the banner) | Ivory component | Accepted twin | Clay |
|---|---|---|---|---|---|---|---|---|
| 01 | 0 | Title | `title-slide dark`: `.ts-top` (k "Optional reference", meta "Revised October 2026"), `h1` + `.dot`, `.ts-sub` + link, `.ts-foot` author | short | `working-smarter.html` (subtitle) | h2 opener + `.cards.c2`; banner → `.note` | subagents / cost / best-practices reference 01 | none |
| 02 | 7 | Plan comparison worksheet | `table.tbl`, 4 rows | medium | `claude.com/pricing` (note) | `.tbl` 30px | cost-and-context-reference 02 | none (equal rows) |
| 03 | 11 | Cloud route worksheet | `ul.bul`, 3 rows | short | — | `ul.bul` | cost-and-context-reference 03 | none |
| 04 | 29 | Tool examples | `ul.bul`, 4 rows with links | short | herdr, conductor, symphony, sandcastle | `ul.bul` | orchestrating-agents-reference 02 | none |
| 05 | 45 | Plugin publication recipe | `.code`, 8 lines, 1 blank | medium | plugins, plugin-marketplaces (note) | `.code.reg` | orchestrating-agents / agentic-engineering reference | none |
| 06 | 68 | Configuration worksheet | `table.tbl`, 4 rows | medium | — | `.tbl` 30px | measuring-what-works-reference 02 | none |
| 07 | 52 | Repeated-run probabilities | `.code`, 6 lines, 2 blank | short | — | `.code` 40px (longest line 52 chars) | measuring-what-works-reference 03 | `.key` on "independently" |
| 08 | 76 | Local model memory | `ul.bul`, 3 rows | short | — | `ul.bul` | measuring-what-works-reference 04 | none |

## Header mapping

- **01:** the crumb is "Optional reference". The banner moves verbatim to the footer `.note`.
- **02–08:** the crumb is `<source crumb> · Optional reference · <a href="working-smarter.html">Back to the talk</a>`.

## Root-mapping classes

**Present in the source:**
- `reference-banner`
- `title-slide`
- `dark` and `light`
- `reveal`
- `slide-content`
- `.dot`
- `ts-top`, `ts-hero`, `ts-sub` and `ts-foot`

**Not present in the source** (so nothing to map):
- `lead`, `gloss`, `term`, `def`, `kcard`, `fill`
- `stat`, `big`, `row`, `shot`
- `reference-slide`, `reference-title`
- `dg-dash`, `dg-tangle`
- `dense`, `tight`, `muted`, `outer`, `c4`
- `ts-loopline`
