# Best Practices Reference: inventory and mapping

Source: `best-practices-reference.html` (working tree, untracked, only read; mtime 3 Oct 21:59:02, sha1 c6c3291964c24c24d89ddef44c5863f1136ba0d0, unchanged after work). Output: `best-practices-reference-ivory.html`. 5 slides → 5 slides, same order. No media, no SVG, no video, no images.

| # | origin | data-label | Ember pattern | Text | Links | Ivory component | Clay |
|---|---|---|---|---|---|---|---|
| 01 | 0 | Title | `.slide.dark.title-slide`: `.reference-banner`, `.ts-top` (`.k` "Optional reference", `.meta` "Revised October 2026"), `.ts-hero h1` "Claude Best Practices<br>Reference" + `.dot`, `.ts-sub` + link, `.ts-foot .ts-author` | Title, subtitle, author, date, banner | `best-practices.html` ×2 (banner, subtitle) | Accepted subagents/cost reference opener: regular `.slide`, crumb "Optional reference", `h2` (2 lines, `<br>` kept), `.cards.c2` (tile 1 = subtitle + "Return to the main talk"; tile 2 = `h3` author + `p` "Revised October 2026"), footer `.note` = banner verbatim | None |
| 02 | 43 | Command reference | `.slide.light`: banner, head (snum 2, crumb "In practice"), `h2`, `table.tbl` 2 cols × 3 rows, `.note` = one link | 3 short rows | `best-practices.html` (banner), `https://code.claude.com/docs/en/interactive-mode` (note) | Crumb + banner merged by `·`; `table.tbl.lg` (40px; ≤3 short rows per §4) | None (equal rows) |
| 03 | 45 | Sources | `.slide.dark`: banner, head (snum 3, crumb "Sources"), `h2`, `ul.bul` of 5 links, `.note` | 5 one-line link rows | `best-practices.html` + 5 claude.dev | Crumb + banner; `ul.bul` with `<a>` per row (same as the accepted main-deck Sources twin in `best-practices-ivory.html`) | None |
| 04 | 0 | Sources | as 03 (snum 4) | 5 one-line link rows | `best-practices.html` + 5 claude.dev | as 03 | None |
| 05 | 0 | Sources | as 03 (snum 5), 3 links | 3 one-line link rows | `best-practices.html` + 3 claude.dev | as 03 | None |

Why not `.links` for 03–05: `.links` needs two columns with equal link counts and a column heading each; the source has 5/5/3 links with no headings, so it would need invented headings and an uneven split. `ul.bul` keeps the source structure unchanged.

Ember classes removed: `dark`, `light`, `title-slide`, `ts-top/ts-hero/ts-sub/ts-foot/ts-author`, `.dot`, `slide-content`, `reveal`, `reference-banner`, hand-written `.snum` digits, all `<style>` blocks (deck-stage hide, main Ember block, `presenter-ui-css`), the inline reveal/video script, the presenter-UI markup and script, Google Fonts preconnect/links, `ember_design_system/*`. No `.ts-loopline`, `.lead`, `.gloss`, `.term`, `.def`, `.kcard`, `.fill`, `.stat`, `.big`, `.row`, `.shot`, `dg-dash`, `dg-tangle`, `.dense`, `.tight`, `.muted`, `.outer` or `.c4` were present in this source's slides.
