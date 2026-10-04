# Ivory: the slide design system

Ivory is the design system for the HTML decks in this repo (talks by David Budáč for developers and IT admins, shown on a projector). This file is the whole spec. A deck needs two things: the Google Fonts link and `ivory_design_system/styles.css`.

| File | What it is |
|---|---|
| `ivory_design_system/styles.css` | Tokens, the slide template, every component, the deck chrome (notes, presenter window), print rules |
| `ivory_design_system/deck-stage.js` | `<deck-stage>` web component: scaling, keys, print. A byte-for-byte copy of the Ember one. Never edit it |
| `ivory_design_system/kitchen-sink.html` | One slide per component. It is the reference markup and the visual-regression page. Copy from it |
| `ivory_design_system/shots/ks-NN.png` | Approved screenshots of the kitchen sink |
| `style-mockups/a3-ivory-technical.html` | The approved mockup. Its values are authoritative |

---

## 1. Brief and principles

The owner's requirements, verbatim:

- "make it more rigid in the style of OpenAI's presentations which are typically very low on fluff and decorations"
- "more technical and cleaner"
- on type: "the headings dont really fit the contents of the slides". This was resolved by using one family: Geist 600 for headlines, Geist for body, Geist Mono for labels, figures and code. No serif anywhere.

What follows from the brief:

1. **One fixed template.** Header, headline, zone and footer sit at the same coordinates on every slide.
2. **Content fills the zone.** Rows share the zone height. Columns and panels run its full height. Nothing floats in the middle of empty space.
3. **Two content sizes:** 30px and 40px. Nothing in between.
4. **One accent (clay), only for the point of the slide.**
5. **No decoration:** no illustrations, icons, textures, shadows, gradients, pills or filled cards. Corner radius is 0–4px (2px in practice). Hairlines separate things.
6. **All slides are light.** Ember's dark/light alternation is gone.

---

## 2. Tokens

| Token | Value | Use |
|---|---|---|
| `--ivory` | `#FAF9F5` | Slide ground. Also the background of every re-rendered video |
| `--paper` | `#F0EEE6` | Code and terminal panels only (and the presenter/notes chrome) |
| `--slate` | `#141413` | Headlines, primary text, diagram strokes, strong rules (1.5px) |
| `--body` | `#2E2E2B` | Running text inside cards, rows and tables |
| `--ink2` | `#5E5D59` | Secondary text, mono labels, footnote, "before" text |
| `--faint` | `#8A877E` | Code line numbers only |
| `--rule` | `#C9C3B4` | Every hairline (1px), dim diagram lines, the neutral bar segment |
| `--clay` | `#D97757` | The accent for fills and strokes |
| `--clay-ink` | `#C6613F` | The accent for text |
| `--sans` | `"Geist"` | Headlines (600) and body (400/500) |
| `--mono` | `"Geist Mono"` | Labels, counters, numbers in tables, code, diagram text |
| `--reg` / `--lg` | `30px` / `40px` | The two content size steps |
| `--lab` | `20px` | Mono labels: 500, uppercase, tracking .08em |
| `--foot` | `26px` | Footnote |
| `--gap` | `72px` | Headline's last line to the zone top |
| `--zone-bottom` | `888px` | Zone bottom edge |

Font link to paste (the only font link a deck carries):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
```

---

## 3. The template

**Canvas and grid.** The canvas is 1920 × 1080. Side margins are 120px. There are 12 columns of 118px with 24px gutters. Column *n* starts at x = 120 + 142(*n*−1); a span of *n* columns is 142*n* − 24 wide. Useful spans: 2 cols = 260, 4 = 544, 5 = 686, 6 = 828, 7 = 970, 10 = 1396, 12 = 1680.

**Fixed coordinates** (y, measured from the top of the slide):

| y | Element |
|---|---|
| 60–108 | `.slide-head`: mono label left, `NN / TT` right, text top at 64, 1px hairline at 108 |
| 172 | Headline top. Geist 600, 78/82px, tracking −.034em, max width 1396 (10 cols), **max two lines**, balanced |
| 326 or 408 | Zone top = the headline's last line + 72. One line gives 326, two lines give 408 |
| 888 | Zone bottom. Fixed |
| 960 | Footer hairline. Drawn on every slide by `.slide::after` |
| 983 | Footnote `.note`: Geist 26/36, `--ink2` |
| 1027 | Source line `.src`: mono 20/24, `--ink2`. It moves to 989 if the slide has no `.note` |

**The zone.** `<div class="zone">` is 1680 wide and 562 tall (one-line headline) or 480 tall (two lines). Exactly one component goes inside it, and that component fills it: `height:100%` is built into every component.

**Size steps.**

- **40px (`--lg`)** is for few, short items: card text, 2–3 row tables, code panels up to about 6 lines and 64 characters per line. Definition-row terms are always 40px.
- **30px (`--reg`)** is for rows, tables with 3+ rows or 3 columns, split-layout rows, 4 cards, and code with longer lines (up to about 85 characters).

Each component has a default step. Override it with the class `.lg` or `.reg` on the component.

**Footnote rules.** One line when a `.src` follows. Otherwise at most two lines. One footnote per slide.

**Slide numbers.** Write `NN` in `.snum` with two digits (`07`). The total comes from one line in `<head>`:

```html
<style>:root{--deck-total:"30"}</style>
```

The stylesheet renders `07 / 30`. If `--deck-total` is not set, only `07` shows. The number is written by hand rather than produced by a CSS counter so that rail thumbnails and presenter-window clones, which see one slide at a time, still show the right number. Renumber after reordering slides.

---

## 4. The accent rule

Clay marks **the one element that is the point of the slide, and only when there is one.** A slide of equal items carries no clay. Never use clay in a headline, footnote or header label (the title slide's audience label is the only header exception). Never use more than one clay element per slide. A data series of bars counts as one element.

| Slide | Clay? | Where |
|---|---|---|
| Three parts (model / harness / client) | No | Three equals |
| Agenda, sources, numbered steps, a stage-by-stage workflow | No | Equal items |
| Vague vs checkable request | Yes | `.tile.key` on the checkable one |
| Hold constant / Compare table | Yes | `th.key` on Compare |
| Acceptance contract | Yes | `.key` on the `VERIFY:` line |
| Test trace | Yes | `.key` on `PASS` |
| Cost with and without cache | Yes | `.bar.key` on the cache-hit bar |
| Agent loop diagram | Yes | The loop path (`.dg-line.key`) |
| Attention diagram | Yes | The predicted token box (`.dg-box.key`) |
| Context growth | Yes | The short new message segment (`.dg-fill-key`) |
| Title slide | Yes | Audience label in the header |

---

## 5. Component catalogue

Every slide is built the same way. Copy whole slides from `kitchen-sink.html` (slide numbers in brackets).

```html
<section class="slide" data-label="Short label" data-speaker-notes="…">
  <div class="slide-head"><span class="crumb">Section label</span><span class="snum">07</span></div>
  <h2>Headline, one or two lines</h2>
  <div class="zone"> …one component… </div>
  <p class="note">Footnote.</p>
  <p class="src">Applied example · <a href="…">supporting documentation</a></p>   <!-- optional -->
</section>
```

### Title slide [01]

```html
<section class="slide title-slide" data-label="Title" data-speaker-notes="…">
  <div class="slide-head"><span class="crumb">Audience or kicker</span><span class="snum">01</span></div>
  <h1>Agentic<br>Engineering</h1>
  <p class="sub">From token prediction to bounded, verified work.</p>
  <div class="meta">
    <div><span class="lab">Author</span><a href="https://davidbudac.cz">David Budáč</a></div>
    <div><span class="lab">Revised</span>October 2026</div>
    <div><span class="lab">Length</span>30 slides</div>
  </div>
</section>
```

- `h1` is 176px/.94 Geist 600. Its last line ends at y 712 and it grows upward. Use at most two lines.
- `.sub` is 38px, `--ink2`, at y 752, 7 columns wide.
- `.meta` has three cells of 4 columns each, under the footer hairline. No `.zone`, no `.note`.

### Cards: equal items in cells [04, 05, 07]

Use for 2–4 parallel items. This replaces Ember `.cards.c2/.c3 > .tile`.

```html
<div class="zone"><div class="cards c3">
  <div class="tile"><span class="lab">01</span><h3>Model</h3><p>Proposes text or a structured tool call.</p></div>
  <div class="tile"><span class="lab">02</span><h3>Harness</h3><p>Builds context, applies permissions and runs tools.</p></div>
  <div class="tile"><span class="lab">03</span><h3>Client</h3><p>The terminal or editor where you inspect and steer.</p></div>
</div></div>
```

- Cells are full height, with a top hairline, vertical hairlines between them and a bottom hairline on the zone edge.
- The label sits at the top. The `h3` and the `p` sit on the bottom edge, and headings line up across cells.
- The column count comes from the number of tiles. `.c2/.c3/.c4` are optional, except that `.c4` drops to 30px.
- Each part is optional: label (mono, e.g. `01` or a name), `h3`, and **one** `p` (use `<br>` for a second line). Default size is 40px; add `.reg` for long text.
- Ember's `.tile .k` heading class is harmless; drop it.

### Before / after [06]

```html
<div class="cards c2">
  <div class="tile was"><span class="lab">Before</span><p>…</p></div>
  <div class="tile key"><span class="lab">After</span><p>…</p></div>
</div>
```

`.was` greys the text. `.key` adds a 2px clay top rule and a clay label. Use `.key` only for the side that is the point.

### Rows: bullets, numbered steps, definition rows [08–11]

All rows share the zone height and have hairlines between them.

| Markup | Looks like | Use for |
|---|---|---|
| `<ul class="bul"><li>…</li></ul>` | Text rows, no marker | Unordered points (full width or in a split) |
| `<ol class="bul"><li>…</li></ol>` | `01` label in column 1, text from column 2 | Numbered steps |
| `<ol class="bul def"><li><b>Start:</b> text…</li></ol>` | `01` · 40px term (2 cols) · 30px text from column 4 | Bullets with a bold lead-in |
| `<ol class="bul def wide">…` | Term column is 4 cols wide; text starts at column 6 | **Agenda** (section titles + one-line descriptions) |

- `ul.bul.def` is the same layout without numbers.
- Inline `<b>` in a plain row is 500 slate. Use it for a short lead-in when the list sits in a split.
- In `.def` rows the first `<b>` becomes the term. If the definition contains a link, `<code>` or `<b>`, wrap it: `<li><b>Term</b><span>text with <code>x</code></span></li>`.
- In plain `ol.bul`, start the text right after `<li>` (no newline or space) so it lines up exactly on column 2.
- Use 3–5 rows. Beyond about 5, use a table.

### Tables [12, 13, 14, 26]

```html
<table class="tbl">                 <!-- 2 cols: col 1–6 | col 7–12 -->
  <thead><tr><th>Category</th><th class="key">What to record</th></tr></thead>
  <tbody><tr><td>…</td><td>…</td></tr></tbody>
</table>
```

- The header row holds mono labels with a 1.5px slate rule under it. Body rows share the remaining height and have hairline separators.
- Default size is 30px. `.lg` is 40px and is meant for 2–3 short rows (matches A3).
- `.c3` makes 3 columns of 4 grid cols each. `.c4` makes 4 columns of 3 each.
- `.num` makes a numeric table: the label column fills, the last column is right-aligned Geist Mono. `<tr class="tot">` is the total row: weight 500 with a 1.5px slate rule above it. Ember decks wrote the total as `<td><b>…</b></td>` with no class; add `class="tot"`.
- `th.key` is the only accent a table takes.

### Code panel and terminal trace [15, 16, 17]

This replaces Ember's pre-formatted `.code` div. Each line is a `<span class="l">` so CSS can number it and spread the lines evenly. Whitespace between the spans is ignored; spaces inside a line are preserved.

```html
<div class="zone"><div class="code">
  <span class="l"><span class="k">GOAL:</span> export invoice net, VAT and gross values to CSV.</span>
  <span class="l"><span class="key">VERIFY:</span> pytest tests/test_export.py -q</span>
  <span class="l">  SKILL.md     indented lines keep their spaces</span>
</div></div>
```

- The panel spans all 12 columns and the full zone height, on `--paper` with 2px radius. Lines are evenly distributed. Line numbers `01…` sit right-aligned in column 1; code starts at column 2.
- Default size is 40px (about 64 characters per line). Use `.reg` for 30px (about 85 characters). Lines longer than that are clipped, so shorten or break them by hand.
- Spans inside a line: `.k` keyword (500), `.c` comment and `.a` arrow (`--ink2`), `.key` the one clay token. Ember's `.o .d` map to `.k` and `.g .b` to plain text; they render harmlessly.
- A terminal trace is the same panel. Align columns with spaces and mute the arrows with `<span class="a">→</span>`.
- An Ember caption line such as "Illustrative check, not a hidden reasoning trace:" becomes a `.c` comment line or moves into the footnote.

### Hero figure with to-scale bars [14]

```html
<div class="split even">
  <div class="hero">
    <div class="big">$0.0506</div>
    <div class="bars">
      <div class="bar key" style="--v:.3373"><span class="lab">With the cache hit</span><div class="track"><i></i><b>$0.0506</b></div></div>
      <div class="bar" style="--v:.8187"><span class="lab">Without it</span><div class="track"><i></i><b>$0.1228</b></div></div>
      <div class="axis"><span style="--v:0">$0.00</span><span style="--v:.3333">$0.05</span><span style="--v:.6667">$0.10</span><span style="--v:1">$0.15</span></div>
    </div>
  </div>
  <table class="tbl num">…</table>
</div>
```

- `--v` is value ÷ axis maximum, so the bars are to scale. Pick an axis maximum that leaves room for the value label after the longest bar (about 0.85 at most).
- `.big` is 168px Geist 500 at the top of the zone. The bars sit on the zone bottom.

### Split: rows + figure [18–21]

```html
<div class="zone"><div class="split">
  <ul class="bul">…3–4 rows…</ul>          <!-- columns 1–5 (686px) -->
  <div class="fig"> svg | video </div>      <!-- columns 7–12 (828px); column 6 stays empty -->
</div></div>
```

- `.split.even` gives 6 | 6 columns (828 + 24 + 828). Use it for hero + table.
- `.split.flip` puts the wide column first, for a figure on the left.
- Both sides run the full zone height.
- An Ember slide with a diagram stacked above bullets (e.g. Attention) becomes either a split or a full-width figure with the bullets folded into the footnote or the speaker notes.

### Full-width figure [22–24]

```html
<div class="zone"><div class="fig">
  <span class="lab">Illustrative · three requests, including history</span>   <!-- optional caption -->
  <svg viewBox="0 0 1680 440">…</svg>
</div></div>
```

The optional `.lab` caption takes 24px plus a 16px gap at the top of the figure. This replaces Ember `.extag`.

### Sources and link lists [25]

```html
<div class="links">
  <div class="linkcol">
    <h3>Mechanisms</h3>
    <a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need<span class="u">arxiv.org/abs/1706.03762</span></a>
    …
  </div>
  <div class="linkcol"><h3>Implementation details</h3>…</div>
</div>
```

- Two 6-column lists. The header label has a slate rule; rows share the height; the title is 30px with a mono URL below it.
- Give both columns the same number of links (3–5) so their rows line up.
- This replaces both Ember `.links > .linkcol` and the "Sources" slide built from `.cards` with `<br>`-separated links.

### Inline text

| Element | Rendering |
|---|---|
| `<a>` | Inherits the text colour. 1.5px `--ink2` underline. Clay on hover |
| `<code>` | Geist Mono at .92em, no background |
| `<b>` / `<strong>` | 500 slate |
| `<span class="key">` | Clay text, for one word that is the point |
| `.mut` | `--ink2` |

### Authoring aids (never ship)

- `.show-grid` on a section overlays the 12 columns, the headline-top and zone-bottom lines, and the zone outline [02, 03]. It is hidden in print.
- `.fig-ph` is a dashed placeholder box for a figure that is not rendered yet.

---

## 6. Diagram idiom and video placement

Diagrams are engineering figures:

- rectangles with 2px slate strokes
- orthogonal connectors (`H`/`V` path segments, no curves)
- small solid arrowheads
- mono labels
- at most one clay element

**Draw at 1:1.** Set `viewBox` to the pixel size the figure gets, so `font-size` in the SVG is real pixels and edges land on the grid:

| Figure position | One-line headline | Two-line headline |
|---|---|---|
| Full width | `0 0 1680 562` | `0 0 1680 480` |
| Full width with `.lab` caption | `0 0 1680 522` | `0 0 1680 440` |
| Split, columns 7–12 | `0 0 828 562` | `0 0 828 480` |

A viewBox drawn for the wrong height still renders, but it scales down and leaves the grid; slide 22's first draft showed this. Place boxes on multiples of 142 (2 cols = 260 wide, then +284 for the next) so they line up with the columns. Keep everything inside the viewBox.

SVG classes (styling comes from CSS, so give them no `fill`/`stroke`/`font` attributes):

| Class | Rendering |
|---|---|
| `.dg-box` | Ivory fill, 2px slate stroke. Use `rx="2"` |
| `.dg-box.mid` | Secondary component: 1.5px `--ink2` stroke |
| `.dg-box.outer` | Boundary: dashed 1.5px `--ink2`, no fill |
| `.dg-box.key` (alias `.hot`) | Clay stroke: the one key component |
| `.dg-line` | 2px slate connector |
| `.dg-line.dim` | 1.5px `--rule`: lifelines, weak links, replies |
| `.dg-line.dash` | Dashed |
| `.dg-line.key` | Clay |
| `.dg-line.axis` | 1.5px slate: chart axis and ticks [24] |
| `.dg-t` | Component name: mono 26px 500 slate |
| `.dg-t.acc` | Annotation: mono 20px slate |
| `.dg-t.mut` | Annotation: mono 20px `--ink2` |
| `.dg-t.key` (alias `.on`) | Clay text |
| `.dg-fill-0` | `--rule` bar segment |
| `.dg-fill-1` | `--ink2` bar segment |
| `.dg-fill-2` | Slate bar segment |
| `.dg-fill-key` | Clay bar segment |

Ember aliases: `.dg-fill-a` → 1, `.dg-fill-g` → 2, `.dg-fill-r` → key.

Write label text in the case you want shown; component names are UPPERCASE by convention, code tokens keep their case. Position text with `x`, `y`, `text-anchor`. In Geist Mono at 20px, one character plus tracking is about 13.6px wide; at 26px it is about 17px. Use this to check that labels fit.

Arrowheads: one marker per style per slide, with a slide-unique `id` (all slides share one document):

```html
<defs>
  <marker id="s09-a" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L12,6 L0,12 Z"/></marker>
  <marker id="s09-k" class="key" …same…><path d="M0,0 L12,6 L0,12 Z"/></marker>   <!-- clay -->
  <marker id="s09-d" class="dim" …same…><path d="M0,0 L12,6 L0,12 Z"/></marker>   <!-- hairline -->
</defs>
<path class="dg-line" d="M240,88 H339" marker-end="url(#s09-a)"/>   <!-- end 1px short of the target edge -->
```

**Charts** are drawn to scale (state the scale in an SVG comment, e.g. "75px per 1k tokens"). Leave 2px ivory gaps between stacked segments. Use a 1.5px slate axis (`<path class="dg-line axis">`, no inline style) with 10px ticks and 20px mono tick labels, and a legend row of 20 × 20 swatches with mono labels.

**Video.** Use the re-rendered `assets/anim/<name>-ivory.mp4` files (ivory `#FAF9F5` background). Put the video alone in a `.fig`, normally in the right side of a `.split`:

```html
<div class="fig"><video src="assets/anim/next-token-ivory.mp4" width="1200" height="750" autoplay muted loop playsinline aria-label="…"></video></div>
```

- The video fills the figure box (828 × zone height) with `object-fit: contain`, centred both ways.
- **No frame, border or background.** The ivory video ground merges with the slide.
- Keep the deck's slide-change script (in the skeleton below) that restarts the video when its slide opens.

---

## 7. Deck skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Deck title — subtitle</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="ivory_design_system/styles.css">
<style>:root{--deck-total:"30"}</style>
</head>
<body>
<deck-stage width="1920" height="1080">

<section class="slide title-slide" data-label="Title" data-speaker-notes="…">…</section>

<section class="slide" data-label="The hook" data-speaker-notes="…">
  <div class="slide-head"><span class="crumb">The invoice task</span><span class="snum">02</span></div>
  <h2>A useful task has a finish line</h2>
  <div class="zone">…</div>
  <p class="note">…</p>
</section>

</deck-stage>
<script src="ivory_design_system/deck-stage.js"></script>
<script>
  /* restart embedded explainer videos when their slide becomes active */
  document.querySelector('deck-stage').addEventListener('slidechange', function(e){
    var v = e.detail.slide && e.detail.slide.querySelector('video');
    if (v) { v.currentTime = 0; var p = v.play(); if (p && p.catch) p.catch(function(){}); }
  });
</script>
<!-- presenter aids: copy the .pui-controls + .pui-notes markup and the
     "Presenter aids" <script> verbatim from ivory_design_system/kitchen-sink.html.
     Do NOT copy the last <script> there ("kitchen-sink only — screenshot hooks"). -->
</body>
</html>
```

Requirements:

- **No `<style>` block** other than the `--deck-total` line. The stylesheet already contains `deck-stage:not(:defined){visibility:hidden}`.
- Every `<section>` has `data-label` (shown in the notes header and the presenter window) and `data-speaker-notes`. N, P and F read these.
- **The notes and presenter script.** The markup and keyboard handling are unchanged from Ember. The one change is that the Ivory presenter window **injects no CSS**. In the Ember script, delete the whole `var st = pd.createElement('style'); st.textContent = '…'; pd.head.appendChild(st);` block. The window already copies every `<link rel=stylesheet>` and `<style>` from the deck `<head>`, so `styles.css` styles both the slide clones and the `.pw-*` UI (paper ground, hairlines, mono bar, animations off). Also delete the old `<style id="presenter-ui-css">` block; the `.pui-*` rules live in `styles.css`.
- Fullscreen (F) still sets `no-rail` on `<deck-stage>`. That is unchanged.

---

## 8. Migration from Ember

### Delete from the deck

- The Ember font link (Space Grotesk / IBM Plex) and `ember_design_system/styles.css`. Replace them with the Ivory font link and `ivory_design_system/styles.css`.
- **Every inline `<style>` block:** the big one in `<head>`, the "Clarity batch" one, and `<style id="presenter-ui-css">`. Add the `--deck-total` line instead.
- The `dark` / `light` classes on sections. They are harmless if left, but remove them; all slides are light.
- The `reveal` classes. They are a no-op in Ivory; remove them for clean markup.
- The presenter window's injected CSS string (see §7).
- Change `ember_design_system/deck-stage.js` to `ivory_design_system/deck-stage.js`. The two files are identical.

### Class mapping

| Ember | Ivory |
|---|---|
| `<div class="slide-content">` wrapper | Remove it. If left, it is `display:contents` and harmless |
| `.slide-head > .snum + .crumb` | Same markup. Write `snum` with two digits (`2` → `02`). Order does not matter |
| `.crumb b` (accent) | Neutral. Drop the `<b>` |
| `h2`, `h2 .o` | `h2`. Remove `.o`; headlines never take clay. Keep to ≤ 2 lines at 1396px |
| content component directly under `h2` | Wrap it in `<div class="zone">…</div>` |
| `.note` | `.note` (same) |
| `.src` (best-practices) | `.src` (same). Keep the `.note` to one line on those slides |
| `.title-slide .ts-top / .ts-hero h1 / .ts-sub / .ts-foot` | `.slide-head` + `h1` + `p.sub` + `.meta` (§5). Drop `.dot` and `.ts-loopline` |
| `.cards.c2/.c3/.c4 > .tile > h3.k + p` | Same classes. Add `<span class="lab">01</span>` labels for numbered equals. One `p` per tile |
| `.tile.fill` / `.kcard` (callout) | `.tile.key` inside a `.cards` |
| `ul.bul > li` | `ul.bul` (or `ol.bul` if the order matters) |
| `ul.bul > li` starting with `<b>Lead:</b>` | `ol.bul.def` (full width) or `ul.bul` with inline `<b>` (in a split) |
| `.cards.c3` used as an agenda | `ol.bul.def.wide` |
| `table.tbl` | `table.tbl` (+ `.lg` for ≤ 3 short rows, `.c3`, `.num`, `tr.tot`) |
| `.code` with raw text lines | `.code` with one `<span class="l">` per line (+ `.reg` for long lines) |
| `.split > ul.bul + .diagram` | `.split > ul.bul + .fig` |
| `.diagram > svg` / `video` | `.fig > svg` / `video`. **Redraw the SVG at 1:1** (§6). Use the `-ivory.mp4` video |
| `.dg-*` SVG classes | Same names, restyled. Remove inline `fill`/`font-size`/`style` attributes. Replace curves with orthogonal paths. Default lines are now slate; mark the one clay line with `.key` |
| `.extag` | `.fig > .lab` caption |
| `.links > .linkcol > h3 + a(.u)` | Same |
| Sources slide made of `.cards` with `<br>` links | `.links` |
| `.lead` | Fold it into the headline or a `.tile`. There is no lead component |
| `.reference-banner` (reference decks) | Not covered. Put the text in the header `.crumb` |
| `.gloss`, `.uses`, `.divider`, `.thanks`, `.pills`/`.pill` | Not covered (unused in agentic-engineering). Map to `.tbl` / `.cards` / `ol.bul.def`. Do not add pills |

### Per-slide checklist

Screenshot every slide with the command below and open each image:

1. Header label left, `NN / TT` right, hairline at 108. The headline starts at 172 and is at most 2 lines.
2. The zone starts 72px under the headline and **content reaches 888**: rows and cells end on the bottom hairline, panels touch it.
3. Nothing crosses 888 or the 120px margins. No clipped code lines. No text in the footer except `.note` and `.src`.
4. Only 30px and 40px content text. Labels are mono uppercase.
5. Clay appears on at most one element, and only if that element is the point (§4).
6. Figures are drawn 1:1 with left/right edges on 120/1800 (full) or 972/1800 (split). The video background is invisible.
7. No dark slide, card fill, shadow, icon, pill or rounded box.
8. The footnote is one line (two at most without `.src`).

### Screenshot command (verified)

Run from the repo root. Change the slide number in both the output name and the `#N` hash:

```sh
cd /Users/davidbudac/claude_projects/agentic-talks && "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1920,1080 --virtual-time-budget=6000 --screenshot=ivory_design_system/shots/ks-03.png "file://$PWD/ivory_design_system/kitchen-sink.html?_snthumb=1#3" 2>/dev/null
```

- **`?_snthumb=1` is required.** Without it, deck-stage draws its thumbnail rail and letterboxes the slide. `_snthumb` is deck-stage's own switch, used for its presenter thumbnails, and sets `no-rail`. Adding `no-rail` to `<deck-stage>` would also work, but would remove the rail for the audience.
- `#N` selects the slide (1-based).
- **Do not pass `--disable-gpu`.** On the software path Chrome renders the full-range Ivory videos as pure white. The GPU path shows the correct `#FAF9F5`.
- Kitchen-sink-only hooks: `?_snthumb=1&chrome#9` shows the buttons and the open notes panel; `?_snthumb=1&pw#14` renders the presenter window in-page.
- Print check: `--print-to-pdf=/tmp/deck.pdf` instead of `--screenshot` should give one 1920 × 1080 page per slide (the kitchen sink gives 26 pages).

---

## 9. Do / don't

**Do**

- Put one component per zone and let it fill the zone.
- Use rows and columns on the 12-column grid, with hairlines between them.
- Use mono for every label, number column, code line and diagram label.
- Write SVGs at 1:1 with grid-aligned boxes, orthogonal lines and slide-unique marker ids.
- Use clay once, for the point, or not at all.
- Keep headlines to one line where possible and two at most. Keep the footnote to one line.
- Number slides `NN` and update `--deck-total`.

**Don't**

- Add inline `<style>` (beyond `--deck-total`) or inline `style` on slide elements. The exceptions are `--v` on bars and axis ticks.
- Add sizes other than 30/40 for content, or bold whole paragraphs.
- Add filled or tinted boxes (paper is for code panels only), shadows, gradients, icons, emoji, pills, rounded cards, or dark slides.
- Use curved connectors, diagonal arrows, or several clay elements in a diagram.
- Center content vertically in an empty zone, or leave the zone half empty. Pick a component that fills it.
- Put clay in headlines, labels, footnotes or across a set of equal items.
- Edit `deck-stage.js`.

---

## 10. Status

- Ivory was approved in October 2026 after several mockup rounds. The history is in `style-mockups/` (`index.html`, A → A2 → A3; A3 is the approved one).
- Ember (`ember_design_system/`) stays in place for the decks not yet migrated. Do not mix the two stylesheets in one deck.
- Migrating a deck means: swap the head, delete the inline styles, wrap the content in `.zone`, convert code and diagrams, then run the checklist.
