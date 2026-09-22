# First three talks: detailed review and revision plan

Date: 22 September 2026. Scope: three independent `-v2.html` editions, with the original decks preserved. Prepared before the slide rewrite.

## Editorial direction

Each talk must answer a different question:

1. **The AI Toolbox:** Which kind of tool would help with my work, and how do I judge the output?
2. **Intro to Agentic AI:** How do I give an agent a bounded task and check what it did?
3. **Agentic Engineering:** How do I make a repeatable workflow whose failures I can detect and recover from?

Keep Ember typography, colours, slide stage, presenter notes and useful concept animations. Rewrite the slide bodies and notes. Keep explanations on slides to roughly 35–80 words; code and source slides can differ. Move qualifications and teaching cues into notes without hiding material limitations. Keep every original file byte-identical. The current fixed-canvas component scales a 1920×1080 stage; preserve that architecture and test at 1280×720 and 1920×1080 rather than mixing viewport sizing into its internal canvas.

## 01 — The AI Toolbox (original: 59 physical slides)

### Findings

- The opening promises finished work, but the first worked task does not arrive until physical slides 22–23. Pricing and terminology precede the reason to care.
- Slides 11–20 create a dense tour of labs, models, products, tiers and product churn. Slides 27–40 then introduce another ten categories, many with several competing tools. A nontechnical listener cannot retain this catalogue.
- Useful distinctions recur in multiple forms: the plan ladder, the $20 comparison, the landscape map, the cheat sheet, the connector decision table and two closing recaps.
- The marketing examples are concrete but skew the audience toward creative work. A document review and a spreadsheet are more broadly useful anchors.
- Five stories interrupt the path from task to adoption. The shop and research stories offer complementary lessons; exam results and advertising anecdotes are less relevant to tool selection.
- “Finished files”, “without breaking formulas”, “brand compliance, solved” and similar assurances skip the actual review work. A missing-data example should be a requested behaviour and a visible check, not proof that agents never invent data.
- Current product pages and historical announcements need to be distinguished. The previous fact-check document is not independent evidence for every statement it labels verified.

### Plan

1. Open with an ordinary review task, its source files and an actual downloadable teaching artifact built from synthetic data.
2. Show the output early, including a missing value. State what the audience must check.
3. Explain chatbot/agent/loop briefly, then organise the landscape by jobs: documents, research, media, apps and automation.
4. Keep a small set of linked product examples; remove competitive rankings, market-share claims and price grids. Put an expanded selection guide in a Markdown handout with vendor links, not copied prices.
5. Retain two sourced stories: Project Vend and the AI co-scientist. Remove the “ten years in two days” equivalence; distinguish a hypothesis from experimental validation.
6. Explain document uploads, connectors and in-app assistance through the same task. Put data access and approval beside the action they govern.
7. End with one task to try, one way to check it and a clear stopping point.

### Acceptance

About 28 slides; no live-demo dependency; artifact accessible from the slide; no implied guaranteed correctness; no unsourced product rankings; one closing action slide; short vendor/source appendix.

## 02 — Intro to Agentic AI (original: 43 physical slides)

### Findings

- The invoice hook is a useful spine, but the live-demo header references a different Pomodoro project outside this repository. The deck cannot currently reproduce its own demonstration from checked-in materials.
- The agenda and a nine-term glossary appear before the beginner has needed most terms.
- Model/harness/statelessness/loop each receive repeated definitions. Some repetition helps, but too much delays the user's first practical decision.
- Slides 17–27 are an eleven-slide interruption covering models, harnesses, video products and prices. This belongs mainly in the toolbox talk or reference material.
- Permissions arrive at physical slide 33 even though the agent is launched at slide 4. Starting conditions should be established before launching a demo.
- The context section first calls a percentage a heuristic, then presents 40–50% as a usable failure boundary. Replace the universal threshold with observable symptoms and task-specific judgment.
- Notes claim “no coding background needed” while examples assume tests and source files. Align the promise with the series chooser: developers new to agents.
- The close favours metaphors over the concrete steps for a first session.

### Plan

1. Keep the invoice task throughout. Check in a small Python fixture, before/after implementations, tests, a demo prompt and a repeatable fallback.
2. Put workspace boundaries, permissions and the no-publish condition before the demo starts. Do not disable approvals to keep the talk moving.
3. Give each essential term a job in the example: model chooses, harness executes, tool result supplies evidence, context supplies information.
4. Use prepared checkpoints that work even if the live run finishes early or stalls. Label prepared results as such; never present them as a captured agent trace.
5. Cover the failure case, patch review and independent checks, not just the passing test.
6. Compress model/tool choice to one practical slide. Remove creative-tool tours and price comparisons.
7. Explain instructions, memory, skills and MCP only to the depth needed to start. Keep exact provider mechanics in linked documentation.
8. End with a five-step first-session routine and a prompt the audience can use.

### Acceptance

About 26 slides; one consistent example; fixture reproduces failure before the fix and passes afterward; live demo optional; notes contain specific checkpoints; permissions before launch; no universal context percentage threshold.

## 03 — Agentic Engineering (original: 60 physical slides)

### Findings

- The “each chapter fixes a limitation” structure and recurring context thread are worth preserving.
- The first 18 slides repeat much of the intro: prediction, thinking, model/harness/client, statelessness and request contents. Keep only the recap needed to explain engineering choices.
- The verifier section is the strongest practical part, but “exit code 0” and “a goal prompt that can't be gamed” overstate what tests or instructions can prove.
- Context and cost material mixes distinct layers: tokens transmitted, attention computation, prompt-cache billing and retained thinking. The deck contradicts itself on whether thinking tokens are retained. Avoid universal claims and explain only the distinctions required for decisions.
- The routing section depends heavily on July model names, benchmarks and specific effort defaults. This makes durable advice look like a temporary buying guide.
- Advisor, orchestrator, cross-vendor wrappers, workflows, skill frameworks and plugin publishing compete for time. Several are already the subjects of later talks.
- There is little treatment of retries, exhausted budgets, partial edits, bad tests, integration ownership or recovery after a failed run.

### Plan

1. Retain the evolution story as a sequence of engineering problems: vague request → explicit contract → insufficient evidence → independent checks → noisy context → selective retrieval → repeated failure → bounded recovery → repeated work → durable instructions.
2. Extend the invoice example into CSV export. Carry a single acceptance contract through tests, context selection, delegation and review.
3. Show a complete workflow: inspect → plan → implement → verify → review, with explicit stop/recovery paths.
4. Separate “the command passed” from “the requirement was met”. Demonstrate quoting, rounding and empty-input cases; use a checked-in valid export artifact.
5. Treat cost as the cost of accepted work, including retries and review. Use clearly labelled hypothetical comparisons, not vendor benchmark claims.
6. Teach model/effort selection through a repeatable trial on representative tasks. Start with one agent; add delegation only for bounded independent work and keep integration ownership explicit.
7. Keep one short instructions/skills example. Move detailed cache economics, orchestration recipes and plugin packaging to existing later decks and linked references.
8. End with a concrete workflow improvement to make this week.

### Acceptance

About 32 slides; reliability and recovery receive substantial space; no model leaderboard; one coherent example; all illustrative measurements labelled; success requires evidence plus review; links to later deep dives.

## Delivery plan and validation

- Write a reproducible Python builder that derives each new file from its own original shell; source content lives in that builder and the final HTML remains static and independently viewable.
- Generate new slide maps and speaker notes. Add a separate v2 chooser and links from the existing index/README.
- Preserve original hashes and the two unrelated dirty files. Do not stage unrelated work.
- Browse primary sources for retained product capabilities and technical claims. Record evidence and any scope limits in SOURCES.md. Do not carry forward blanket “all facts verified” claims.
- Check unique slide labels/IDs, local links, source links, media files, text density, layout bounds and browser errors.
- Render every slide in Chrome at both target resolutions; visually inspect contact sheets and full-size outliers. Exercise navigation, deep links, notes, presenter window and reduced motion.
- Run the demo fixture before and after; check the CSV with Python's CSV reader. Record actual results separately from simulated teaching examples.
- Stage named files, check the staged diff, commit, push the current branch, and verify the remote commit. The user explicitly authorised commit and push; no merge or deployment to a different branch is implied.
