# measuring-what-works.html → measuring-what-works-ivory.html: per-slide inventory and mapping

Source: `measuring-what-works.html` (Ember, 19 slides, read only). Output: `measuring-what-works-ivory.html`.
Every slide keeps `data-label`, `data-origin-slide` and `data-speaker-notes` byte for byte. `ivory-conversion/audit.py` checked this; its output is in `audit.json` and `content-diff.txt`.
Every slide drops the Ember `dark`/`light`/`reveal` classes, the `.slide-content` wrapper and the hand-written `.snum` digits. `.snum` is left empty, and deck.js numbers it.

| # | origin | data-label | Ember pattern (text amount) | Ivory component | Clay | Notes |
|---|---|---|---|---|---|---|
| 01 | 1 | Title | dark `.title-slide`: `.ts-top` (kicker + "Revised October 2026"), `h1` with `.dot`, `.ts-sub`, `.ts-foot` author | `.title-slide`: `.crumb` kicker, `h1` (2 lines), `p.sub`, `.meta` (Author, Revised) | header label (title exception) | `.dot` "." dropped. No `.ts-loopline` in this deck. "Revised October 2026" moves into `.meta`. Adds the "Author" label. Adds a `<br>` in `.sub` after "failures," so "configuration." does not sit alone on line 2. No Length cell, so no new text |
| 02 | 2 | Agenda | light `.cards.c3`, `h3.k` + `p` (3 short items) | `ol.bul.def.wide` (root map: cards used as an agenda) | none (equal items) | Adds `01–03` counters. Same as cost-and-context-ivory slide 02 |
| 03 | 4 | What an eval measures | light `.cards.c3`, `h3.k` + `p` | `.cards.c3`, `.lab 01–03` + `h3` + `p` (40px) | none (three equals) | Same pattern as the example's Model/Harness/Client slide |
| 04 | 5 | Acceptance cases | `table.tbl` 2 cols × 4 rows | `table.tbl` (30px; 4 rows) | none (equal cases) | |
| 05 | 6 | Grading methods | dark `.cards.c3`, `h3.k` + `p` | `.cards.c3`, `.lab 01–03` + `h3` + `p` | none (three complementary methods) | |
| 06 | 7 | Repeated trials | light `.code`: 4 text lines + 1 blank line | `.code` (40px), 4 `span.l`. "Illustrative outcomes for one case:" is a `.c` comment, the other three labels are `.k` | `pass` token (`.key`) | Blank line dropped (whitespace only). Longest line is 60 chars (limit 64) |
| 07 | 8 | Trace evidence | dark `ul.bul` 3 rows | `ul.bul` | none | |
| 08 | 9 | Annotated trace | `table.tbl` 2 × 3 | `table.tbl` (30px) | none | Pass 1 used `.lg`. Every answer wrapped to two lines and crowded the header rule, so it changed to 30px in pass 2 |
| 09 | 10 | Telemetry versus transcripts | dark `.cards.c2`, `h3.k` titles; `.note` with link | `.cards.c2`, `.lab` titles; `.note` keeps the link | none (two equal evidence types) | Same as cost-and-context-ivory slides 11 and 07 (`h3.k` → `.lab`) |
| 10 | 11 | Results worksheet | `table.tbl` 2 × 4 | `table.tbl` (30px) | none | |
| 11 | 12 | Grading exercise | dark `.code`: 5 text lines + 2 blank lines | `.code` (40px), 5 `span.l`. Line 1 is a `.c` comment; `A:`/`B:` are `.k` | none | Blank lines dropped. Longest line is 59 chars |
| 12 | 13 | Exercise debrief | `table.tbl` 3 cols × 4 rows | `table.tbl.c3` (30px) | none | See the report: no single cell is the point |
| 13 | 15 | Cost per accepted task | `.cards.c3`, `h3.k` | `.cards.c3`, `.lab 01–03` + `h3` | none | Same markup as agentic-engineering-ivory slide 20 (identical content) |
| 14 | 20 | Local model memory | dark `ul.bul` 3 rows | `ul.bul` | none | Two-line headline. × and ÷ in the footnote render in Geist |
| 15 | 22 | Hardware experiment | `table.tbl` 2 × 4 | `table.tbl` (30px) | none | Two-line headline |
| 16 | 25 | Local or hosted | dark `.cards.c2`, `h3.k` | `.cards.c2`, `.lab` titles | none (two options, neither favoured) | |
| 17 | 27 | Voice input | light `.code`: 5 text lines + 1 blank line | `.code` (40px), 5 `span.l`. `Spoken:` and `Check the transcription for:` are `.k` | `WITHOUT` token (`.key`) | Blank line dropped. Longest line is 58 chars |
| 18 | 30 | Next experiment | dark `ul.bul` 3 steps + **two** `.note` (the second is the reference link) | `ol.bul` (ordered steps) + `.note` + `.src` link | none | Ivory allows one footnote, so the link moves to `.src`, with the same text and href. Same as cost-and-context-ivory slide 16 |
| 19 | 31 | Sources | dark `ul.bul` of 3 links | `ul.bul` of 3 links | none | `.links` is not used: it needs two balanced columns with `h3` headings, which the source does not have. Same as cost-and-context-ivory slide 17 |

## Root-mapping classes encountered

Used in this deck: `.title-slide/.ts-*`, `.dot`, `.cards.c2/.c3`, `h3.k`, `ul.bul`, `table.tbl`, `.code` (raw text lines), `dark/light/reveal`, `.slide-content`, `.note` (×2 on slide 18), `.note a`.

Not present as elements (some exist only as unused CSS rules in the source `<style>`): `lead`, `gloss/term/def`, `kcard`, `fill`, `stat`, `big`, `row`, `shot`, `reference-banner` (CSS rule only), `reference-slide`, `reference-title`, `dg-dash`, `dg-tangle`, `dense`/`tight` (CSS rules only), `muted` (CSS rule only), `outer`, `c4`, `.ts-loopline` (CSS rule only), `.extag`, `.pill`, `.flow`, `.divider`, `.thanks`. The deck has no inline SVG, so nothing was redrawn, and no `<video>`.
