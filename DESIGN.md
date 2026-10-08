# Design system: Ivory

This repo's decks are moving to **Ivory**. The spec, the stylesheet, the fonts, the runtime, the starter deck, the kitchen sink and the screenshot tool all live in [`ivory_design_system/`](ivory_design_system/), which is self-contained and portable. **The spec is [`ivory_design_system/DESIGN.md`](ivory_design_system/DESIGN.md).** Read it first; this file only holds what is specific to this repo.

A deck in this repo sits at the repo root and needs:

```html
<link rel="stylesheet" href="ivory_design_system/styles.css">
…
<script src="ivory_design_system/deck-stage.js"></script>
<script src="ivory_design_system/deck.js"></script>
```

Videos for decks live in `assets/anim/`; use the `<name>-ivory.mp4` renders (ivory `#FAF9F5` ground), e.g. `<video src="assets/anim/next-token-ivory.mp4" …>`. The kitchen sink uses its own copies in `ivory_design_system/demo/`.

---

## Status

| Deck | Style |
|---|---|
| `agentic-engineering-ivory.html` | **Ivory** (32 slides; previously completed model) |
| `cost-and-context-ivory.html` | **Ivory** (17 slides; converted and verified) |
| `ai-toolbox-ivory.html` | **Ivory** (31 slides; converted and verified) |
| `agentic-ai-ivory.html` | **Ivory** (26 slides; converted and verified) |
| `subagents-prompt-caching-ivory.html` | **Ivory** (21 slides; converted and verified) |
| `orchestrating-agents-ivory.html` | **Ivory** (19 slides; converted and verified) |
| `measuring-what-works-ivory.html` | **Ivory** (19 slides; converted and verified) |
| `best-practices-ivory.html` | **Ivory** (30 slides; converted and verified) |
| `working-smarter-ivory.html` | **Ivory** (44 slides; converted and verified) |
| `agentic-engineering-reference-ivory.html` | **Ivory** (10 slides; converted and verified) |
| `ai-toolbox-reference-ivory.html` | **Ivory** (22 slides; converted and verified) |
| `agentic-ai-reference-ivory.html` | **Ivory** (13 slides; converted and verified) |
| `subagents-prompt-caching-reference-ivory.html` | **Ivory** (4 slides; converted and verified) |
| `cost-and-context-reference-ivory.html` | **Ivory** (4 slides; converted and verified) |
| `orchestrating-agents-reference-ivory.html` | **Ivory** (4 slides; converted and verified) |
| `measuring-what-works-reference-ivory.html` | **Ivory** (5 slides; converted and verified) |
| `best-practices-reference-ivory.html` | **Ivory** (5 slides; converted and verified) |
| `working-smarter-reference-ivory.html` | **Ivory** (8 slides; converted and verified) |

The 17 new conversions contain 282 slides. See [the conversion report](ivory-conversion/report.md) for commits, content differences, visual review and verification limits.

Original main and `*-reference.html` working copies remain unchanged in Ember; links in the Ivory copies still point to those original filenames for the later replacement. `title-mockups.html` is out of scope.

- Ember (`ember_design_system/`) stays in place for the preserved originals. Do not mix the two stylesheets in one deck.
- Migrating a deck means: swap the head, delete the inline styles and scripts, wrap the content in `.zone`, convert code and diagrams, then run the checklist in the Ivory spec (§10). Follow the generic porting procedure in the Ivory spec (§8) plus the Ember specifics below.

## History

Ivory was approved in October 2026 after several mockup rounds. The history is in `style-mockups/` (`index.html`, A → A2 → A3; `a3-ivory-technical.html` is the approved one, and its values became the Ivory tokens). The other directions there (B black stage, C colour block, D blueprint, E Swiss grid) were not chosen. `style-mockups/shots/` holds their screenshots.

---

## Ember → Ivory

### Delete from the deck

- The Ember font link (Space Grotesk / IBM Plex) and `ember_design_system/styles.css`. Replace them with `ivory_design_system/styles.css` (Ivory bundles its fonts; no font link).
- **Every inline `<style>` block:** the big one in `<head>`, the "Clarity batch" one, and `<style id="presenter-ui-css">`.
- **The inline presenter script** (notes overlay, presenter window, fullscreen) and the "restart embedded explainer videos" script, plus the `.pui-controls` / `.pui-notes` markup. `ivory_design_system/deck.js` provides all of them.
- The `dark` / `light` classes on sections. They are harmless if left, but remove them; all slides are light.
- The `reveal` classes. They are a no-op in Ivory; remove them for clean markup.
- Change `ember_design_system/deck-stage.js` to `ivory_design_system/deck-stage.js`. The two files are identical.

### Class mapping

| Ember | Ivory |
|---|---|
| `<div class="slide-content">` wrapper | Remove it. If left, it is `display:contents` and harmless |
| `.slide-head > .snum + .crumb` | Same markup. Leave `.snum` empty (deck.js numbers it) or write two digits (`2` → `02`). Order does not matter |
| `.crumb b` (accent) | Neutral. Drop the `<b>` |
| `h2`, `h2 .o` | `h2`. Remove `.o`; headlines never take clay. Keep to ≤ 2 lines at 1396px |
| content component directly under `h2` | Wrap it in `<div class="zone">…</div>` |
| `.note` | `.note` (same) |
| `.src` (best-practices) | `.src` (same). Keep the `.note` to one line on those slides |
| `.title-slide .ts-top / .ts-hero h1 / .ts-sub / .ts-foot` | `.slide-head` + `h1` + `p.sub` + `.meta`. Drop `.dot` and `.ts-loopline` |
| `.cards.c2/.c3/.c4 > .tile > h3.k + p` | Same classes. Add `<span class="lab">01</span>` labels for numbered equals. One `p` per tile. The `.k` heading class is harmless; drop it |
| `.tile.fill` / `.kcard` (callout) | `.tile.key` inside a `.cards` |
| `ul.bul > li` | `ul.bul` (or `ol.bul` if the order matters) |
| `ul.bul > li` starting with `<b>Lead:</b>` | `ol.bul.def` (full width) or `ul.bul` with inline `<b>` (in a split) |
| `.cards.c3` used as an agenda | `ol.bul.def.wide` |
| `table.tbl` | `table.tbl` (+ `.lg` for ≤ 3 short rows, `.c3`, `.num`, `tr.tot`). Ember wrote the total row as `<td><b>…</b></td>` with no class; add `class="tot"` |
| `.code` with raw text lines | `.code` with one `<span class="l">` per line (+ `.reg` for long lines). Ember's `.o .d` map to `.k`, `.g .b` to plain text; they render harmlessly |
| Ember caption line in a code panel ("Illustrative check, not a hidden reasoning trace:") | A `.c` comment line, or move it into the footnote |
| `.split > ul.bul + .diagram` | `.split > ul.bul + .fig` |
| `.diagram > svg` / `video` | `.fig > svg` / `video`. **Redraw the SVG at 1:1.** Use the `-ivory.mp4` video |
| `.dg-*` SVG classes | Same names, restyled. Remove inline `fill`/`font-size`/`style` attributes. Replace curves with orthogonal paths. Default lines are now slate; mark the one clay line with `.key`. Aliases: `.hot`/`.on` → `.key`, `.dg-fill-a` → `-1`, `.dg-fill-g` → `-2`, `.dg-fill-r` → `-key` |
| `.extag` | `.fig > .lab` caption |
| `.links > .linkcol > h3 + a(.u)` | Same |
| Sources slide made of `.cards` with `<br>` links | `.links` |
| `.lead` | Fold it into the headline or a `.tile`. There is no lead component |
| `.reference-banner` (reference decks) | Not covered. Put the text in the header `.crumb` |
| `.gloss`, `.uses`, `.divider`, `.thanks`, `.pills`/`.pill` | Not covered (unused in agentic-engineering). Map to `.tbl` / `.cards` / `ol.bul.def`. Do not add pills |
| Attention slide (diagram stacked above bullets) | A split, or a full-width figure with the bullets folded into the footnote or speaker notes |
