# Agentic Engineering — Optional Reference: per-slide inventory and mapping

Source `agentic-engineering-reference.html` (Ember, 10 slides) → `agentic-engineering-reference-ivory.html` (Ivory, 10 slides). Order unchanged.

"Twin" means a committed, parent-reviewed Ivory slide with the same `data-label`, raw notes and visible text. Its markup was reused verbatim. Only `data-origin-slide` and the crumb (reference banner merged in) differ.

| # | Origin | Label | Ember pattern | Ivory component | Size | Clay | Notes |
|---|---|---|---|---|---|---|---|
| 01 | — | Reference guide | dark; inline-styled `h1` ("reference title") + `.cards.c2` (`h3.k` + `p`) + `.note` link | Content slide: crumb + `h2` + `.cards.c2` (`h3` + `p`) + `.note` | 40px | none (two equal tiles) | Inline-styled `h1` → `h2` (no title-slide subtitle/meta in source, so not `.title-slide`). No `data-origin-slide` in source; none added |
| 02 | 8 | Explore a transformer | `.reference-banner` + `.cards.c2` with links + `<br>` | `.cards.c2` (`h3` + one `p` with `<br>`) | 40px | none | Banner → crumb |
| 03 | 18 | Request anatomy | banner + `ul.bul` (4) | twin cost-and-context: `ul.bul` | 30px | none | Banner → crumb |
| 04 | 28 | Growth arithmetic | banner + raw-text `.code` (8 lines incl. 2 blank) | `.code.reg`, 8 `span.l`; assumption lines `.c`; terms `.k` | 30px | the total-input formula `nB + d × n(n − 1) / 2` (the quadratic) | Same pattern as twin slide 05; blank lines kept as empty lines |
| 05 | 33 | Cache break-even | banner + raw-text `.code` (9 lines incl. 2 blank) | twin subagents-prompt-caching: `.code.reg` | 30px | the break-even inequality | Banner → crumb |
| 06 | 47 | Workflow sketch | banner + raw-text `.code` (11 lines incl. 1 blank) | `.code.reg`; header `.c`; `for`/`if`/`return` `.k` | 30px | `latest_failures = result.failures` (the retry edge named in the headline) | Indentation preserved |
| 07 | 53 | Skill file example | banner + raw-text `.code` (8 lines) | twin orchestrating-agents / working-smarter: `.code.reg` | 30px | none | Banner → crumb |
| 08 | 56 | Further skill systems | banner + `.cards.c2` with links + `<br>` | `.cards.c2` (`h3` + one `p` with `<br>`) | 40px | none | Banner → crumb |
| 09 | 58 | Plugin publication recipe | banner + raw-text `.code` (8 lines incl. 1 blank) + `.note` with 2 links | `.code.reg` (plain lines) + `.note` | 30px | none (equal steps) | Banner → crumb |
| 10 | 60 | Sources | banner + `.cards.c2` with `<br>` links | twin agentic-engineering 30: `.links` (two `.linkcol`, 3 links each, `.u` URL lines) | 30px | none | Root mapping "Sources slide made of `.cards` with `<br>` links → `.links`" |

## Reference-deck mappings (root DESIGN.md)

- `.reference-banner` ("Optional reference · <a>Back to the talk</a>", slides 02–10) → merged into the header `.crumb` as `<section label> · Optional reference · <a href="agentic-engineering.html">Back to the talk</a>`. Same words and same href; the section label comes first and one `·` separator joins the two. The longest crumb ("Publication reference · …") ends at x ≈ 950, well short of the slide number, so no ellipsis is triggered.
- `reference-slide` / `reference-title`: not present as classes in this source, and root DESIGN.md has no rows for them. Slide 01's inline-styled `h1` (the de-facto reference title) became an `h2` on a normal content slide. No title-slide clay label is used.

## Brief's class list, as it applies here

- Present and mapped: `dark`/`light`/`reveal`/`slide-content` (removed); `h3.k` (→ `h3`); `.reference-banner` (→ crumb); `.cards.c2`; `.code`; `ul.bul`; `.note`.
- Not present in this source: `lead`, `gloss`/`term`/`def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-slide`, `reference-title` (as classes), `dg-dash`/`dg-tangle`, `dense`, `tight`, `muted`, `outer`, `c4`, title `.dot`, `.ts-loopline`. (`.lead`, `.gloss`, `.divider`, `.thanks`, `.pills`, `.extag` exist only as CSS rules, not used by any element.)
- No SVG, no `<video>`, no images.
