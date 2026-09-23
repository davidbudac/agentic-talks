# Changes delivered — first three talks v2

All original decks are preserved. The new editions are linked from the series index and from `first-three-v2.html`.

## Content size

| Deck | Original slides | New slides | Original visible words | New visible words | New average per slide |
|---|---:|---:|---:|---:|---:|
| ai-toolbox | 59 | 28 | 6523 | 1037 | 37 |
| agentic-ai | 43 | 26 | 4260 | 998 | 38 |
| agentic-engineering | 60 | 32 | 6202 | 1324 | 41 |

Counts include visible titles, labels, references, code and diagram labels, but exclude speaker notes and text inside videos. Before the visual pass the totals were 935, 859 and 1145; the increase is diagram labels and wayfinding, not new copy. The new maximum is 78 visible words (the illustrative cost chart).

## Talk 01

- Moved the review task and downloadable synthetic report to the opening. The output exposes missing data and gives the audience a check to perform.
- Replaced the model/product/price catalogue with task categories and a small set of representative tools. Added an expanded handout with current vendor links.
- Reduced five stories to two, with primary sources and more precise claims.
- Combined repeated summary/decision slides into one first-trial routine.

## Talk 02

- Made the invoice example the continuous thread and checked in everything needed to reproduce it.
- Moved permissions and workspace boundaries before the optional live demo. Added four prepared checkpoints and explicit fallback notes.
- Reduced the landscape tour to one practical choice; removed creative-tool detours and price lists.
- Replaced universal context thresholds and confident-success language with observable symptoms, diff review and actual checks.
- Added recovery advice and a five-step first-session routine.

## Talk 03

- Kept the evolution structure, with each section solving a failure in the invoice-export workflow.
- Compressed the introductory mechanics to one recap.
- Added a precise acceptance contract, checked CSV example, verification boundaries, retry policy and recovery path.
- Replaced named-model routing and benchmark claims with a repeatable trial and explicitly illustrative cost comparison.
- Kept delegation bounded and integration owned; compressed skills to one inspectable procedure and linked later deep dives.

## Presentation and delivery

- Derived each new deck from its own original shell and preserved the shared Ember component.
- Rewrote all new slide bodies and speaker notes; generated original/new maps.
- Used the existing local fonts, added reduced-motion-aware media control and static posters, and initialised notes correctly for deep links.
- Added a reproducible builder, browser QA script, fixture results, source record and visual contact sheets.
- Preserved unrelated edits in `.claude/launch.json` and `cost-and-context.html`.

## Visual pass (23 September 2026)

Implemented the approved mock-up (`visual-mockups-v2.html`) in the builder. Slide wording, notes, order and count are unchanged.

- Shared helpers now fill the 1920×1080 stage: 88px titles, 34–42px body text, content centred in the full height, fixed pixel sizes instead of viewport units. Cards became tiles with icons; step lists became a station rail; code became terminal and editor windows; link lists became reference rows and link cards.
- Ported the nine reference designs: failing test, checkpoint route, checkpoint 1, model ⇄ harness, job tiles, claim chain, problem beat, caching vs compaction and the accepted-work chart.
- Wayfinding: talk 02 checkpoint slides show a four-station rail with the current station lit; talk 03 shows a problem tracker (1–7) on every slide in a problem chapter, all complete on the synthesis slide.
- Rhythm: all seven talk 03 problem slides use the problem beat (ink, coral edge, giant numeral, drawn visual). Closing slides in each talk have a coral edge.
- Bespoke drawings: talk 01 — inputs → output, report chart, brief, chat vs agent, loop, context sources, document and media panels, app journey, access scope, stories, first-task grid. Talk 02 — boundaries, sequence of a tool call, code and diff views, context window, crowded context, session handoff, thinking vs evidence, test cards, interruption, rules and skills, repo boundary. Talk 03 — demo vs repeated runs, CSV, system loop, unspecified request, contract, process choices, workflow with send-back, exit code, claim check, test and CSV artifact, two actors, stage inputs, handoff note, retry budget, retry policy, recovery timeline, cost fraction, delegation, fan-in, procedure, workflow way back, series cards.
- Diagram labels are taken from each slide or its notes. Video posters now match each video's aspect ratio.

## Prose pass (23 September 2026)

Edited slide wording and speaker notes in the builder. Slide order, count and visual structure are unchanged; visible word counts stay within 19–78 per slide.

- Headlines: rewrote 20 of 86, mostly the "X, not Y" contrasts and announcements, to state the point directly. Kept "Some tools answer. Others take steps." and "The model chooses; the harness executes", where the contrast is the lesson.
- Notes: rewrote all 86 for the presenter's voice. Cut editorial instructions that referred to the original decks ("the original deck said", "this replaces the landscape tour") and repeated teaching cues. Kept every qualification and source caveat, in shorter form.
- Removed all em dashes from slide text, notes, page titles and the presenter pop-up message, and the unicode arrows from two video captions and two workflow labels. Em dashes remain only in HTML and CSS comments inherited from the original shells.
- Talk 03, slides 21–22: the cost chart now labels its per-task figure as model and tool cost, which matches problem 5 (review time belongs in the total). The notes say that B is cheaper once review time is added.
- Talk 03, slide 29: the notes explain that the four-stage rail folds Inspect and Plan into Contract.
- Talk 01: a specific Copilot and Gemini example on the "existing tools" slide; clearer wording on the Project Vend and animation slides.
- Regenerated the maps, notes files and contact sheets. Browser QA passes at both resolutions.
