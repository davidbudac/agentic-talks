#!/usr/bin/env python3
"""Build three static v2 decks from the preserved original presentation shells.

Run from any directory: PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_first_three_v2.py
Edit slide content below; shared original deck styles and stage remain untouched.
"""
from pathlib import Path
from html import escape as esc
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'reviews/first-three-v2'


def p(text):
    return f'<p class="lead">{text}</p>'


def cards(*items):
    return '<div class="cards c%s">%s</div>' % (3 if len(items) == 3 else 2, ''.join(
        f'<div class="tile"><h3>{title}</h3><p>{body}</p></div>' for title, body in items))


def flow(*items):
    return '<ol class="v2-flow">' + ''.join(f'<li><span>{i:02}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items, 1)) + '</ol>'


def code(text):
    return '<pre class="code"><code>' + esc(text) + '</code></pre>'


def split(left, right):
    return '<div class="split">' + f'<div class="v2-stack">{left}</div><div class="v2-stack">{right}</div></div>'


def table(headers, rows):
    return '<table class="tbl"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table>'


def callout(title, text):
    return f'<div class="kcard"><div class="big">{title}</div><p>{text}</p></div>'


def links(*items):
    return '<div class="v2-links">' + ''.join(f'<a href="{url}" target="_blank" rel="noopener">{title}<span>↗</span></a>' for title, url in items) + '</div>'


def video(name, caption):
    return f'<figure class="v2-media"><video muted loop playsinline preload="metadata" poster="assets/v2/{name}.svg" aria-label="{esc(caption)}"><source src="assets/anim/{name}.mp4" type="video/mp4"></video><button type="button" class="v2-play" data-video-toggle aria-pressed="false">Play animation</button><figcaption>{caption}</figcaption></figure>'


def slide(title, body, notes, origin, chapter='', dark=False, foot=''):
    return dict(title=title, body=body, notes=notes, origin=origin, chapter=chapter, dark=dark, foot=foot)


def title(name, subtitle, audience, notes):
    return dict(title=name.replace('<br>', ' '), hero=name, subtitle=subtitle, audience=audience, notes=notes, origin='1', chapter='Start')


def report():
    return '''<div class="v2-report"><div class="v2-report-head">QUARTERLY REVIEW <span>Teaching example · synthetic data</span></div>
<h3>April–May grew. June is incomplete.</h3>
<div class="v2-bars"><div><span>April</span><i style="--bar-width:66.67%"></i><b>80</b></div><div><span>May</span><i style="--bar-width:100%"></i><b>120</b></div><div><span>June</span><i class="missing"></i><b>Missing</b></div></div>
<p>Completed orders · May vs April: +50%</p><div class="v2-report-flag">Q2 total withheld until June is supplied.</div></div>'''


# TALK 01 — choose a tool by the work and the evidence it returns.
TOOLBOX = [
 title('The AI<br>Toolbox', 'Find a useful tool. Check the work it returns.', '01 · No coding needed · v2', 'Promise a practical selection method, not a tour of everything on the market. The new edition starts with one ordinary task and returns to it throughout.'),
 slide('Start with a task you already do', p('Turn this month’s files into a review someone can use.') + cards(('Inputs', 'A results CSV, last month’s report and a short brief.'), ('Output', 'A draft report with checked numbers and visible gaps.')), 'Ask the audience to think of a recurring task they know well enough to review. Our review task uses synthetic data. Do not claim it is a customer case study or that a particular product produced it.', '2, 21–23', 'One real task'),
 slide('Here is the output to judge', report(), 'Show the report before introducing vendors. April has 80 completed orders, May 120, June is missing. The 50% increase is a comparison of two complete months, not a quarterly trend. This is a real downloadable teaching artifact, authored for the talk; it is not a screenshot of a vendor run.', '23 → new artifact', 'One real task', foot='<a href="examples/v2/review-report.html" target="_blank" rel="noopener">Open the report</a> · <a href="examples/v2/review-data.csv" download>Download its CSV</a>'),
 slide('A useful brief names the checks', code('Use the CSV and last month’s structure.\nShow where each number came from.\nFlag missing data; do not estimate it.\nKeep the draft to one page.\nSave a new file for me to review.'), 'The brief constrains the output, but does not guarantee compliance. Inspect the result. Open the CSV if useful and point to the blank June value. A good brief is specific about the evidence the reviewer needs.', '23, 25', 'One real task'),
 slide('Review the result, not the confidence', flow(('Trace', 'Do the numbers match the source?'), ('Inspect', 'Are gaps and assumptions visible?'), ('Decide', 'What is ready to share?')), 'For the report: recompute 120 divided by 80 minus one, confirm June is absent, then decide whether an April–May interim report meets the actual request. A polished chart can still answer the wrong question.', '24–25, 39', 'One real task', dark=True),
 slide('Some tools answer. Others take steps.', cards(('Chat', 'You ask for help, then carry the work into your files.'), ('Agent', 'The system can use tools, inspect results and continue the task.')), 'This is a working distinction, not a rigid classification of every product. Chat interfaces can expose agent features. An agent may still need clarification or approval before it continues.', '5–6', 'What changed'),
 slide('The loop is simple', flow(('Choose', 'Pick the next useful action.'), ('Act', 'A tool reads or changes something.'), ('Check', 'Use the result to decide what follows.')), 'For the report: read the CSV, calculate a comparison, write the draft, inspect it. The system needs a stopping condition. Not every image or voice generator is an agent; generation can also be a single tool call in a larger workflow.', '6–9', 'What changed'),
 slide('Your files supply the context', split(p('The assistant needs the sources, constraints and examples relevant to this task.'), callout('Give it enough to work with', 'A clear brief and the right files are usually more useful than a longer prompt.')), 'Context means the information available while producing an answer. Avoid the absolute claim that every product resends the entire conversation unchanged. Products may retrieve, summarise or store state differently. Check what the tool can access.', '7–8', 'What changed'),
 slide('Choose by the job', cards(('Documents', 'Draft, compare, summarise and present.'), ('Media', 'Create images, audio or short video.'), ('Actions', 'Build a small app or connect repeated steps.')), 'This is the map for the rest of the talk. Research appears within document work because its output is evidence to inspect. Product examples illustrate categories rather than establish winners.', '27, 40', 'The toolbox', dark=True),
 slide('Start with an assistant you can use at work', cards(('Claude', 'Work with source files and draft an output.'), ('ChatGPT', 'Explore a question, analyse data and make a draft.'), ('Gemini', 'Use an assistant alongside your Google work.')), 'These are representative general assistants. The practical choice depends on your organisation’s approved access, integrations and limits. Do not imply all plans include the same capabilities. Sources and current product links are in the handout.', '11–19 → compressed', 'Documents'),
 slide('Document work has two different needs', cards(('Understand the sources', 'Gemini Notebook: explore supplied material and listen to an Audio Overview.'), ('Present the material', 'Gamma or Canva: turn an outline into a presentation you can edit.')), 'A sourced summary and a designed presentation are different outputs. Ask where a claim came from before spending time polishing its layout. An Audio Overview can contain errors; use it to orient yourself and return to the source.', '17, 24, 35, 37', 'Documents'),
 slide('Check one important claim all the way back', flow(('Answer', 'Find the claim you may rely on.'), ('Citation', 'Open the source behind it.'), ('Evidence', 'Check that the source supports the claim.')), 'A citation is a path to evidence, not an accuracy seal. Read enough surrounding material to check scope and date. If the source is missing, inaccessible or does not support the claim, leave the claim unresolved.', '24, 37', 'Research', dark=True),
 slide('For media, decide what must stay exact', cards(('Explore a look', 'Generate alternatives for an image or a short scene.'), ('Keep a template', 'Use fixed layouts for labels, numbers and repeated versions.')), 'Distinguish exploratory generation from a deterministic template. Brand colours and text should be checked in both. Do not promise perfect brand compliance simply because an output was rendered from code.', '29–34', 'Media'),
 slide('The animation in this series is an output', video('agent-loop-dark', 'An existing explainer from this repository · built with Remotion'), 'Play the animation as an example of an actual artifact. The source is the repository’s Remotion project, not a claim about a new vendor session. For narration, text-to-speech tools such as ElevenLabs are another category; review pronunciation and obtain permission for any cloned voice.', '30–32 → actual repository artifact', 'Media', dark=True),
 slide('An app draft still needs an owner', split(p('Tools such as Lovable can produce a working app from a brief.'), cards(('Before sharing', 'Check the main journey and what data it stores.'), ('Before relying on it', 'Have someone own access, testing and maintenance.'))), 'An app is executable software, even if a nondeveloper created it. Start with a prototype using synthetic data. A working demo does not establish security, correctness or maintainability.', '28', 'Apps'),
 slide('Automate the repeatable part', flow(('Trigger', 'A new report arrives.'), ('Draft', 'Summarise the changes.'), ('Review', 'A person approves the message.')), 'This is an illustrative workflow, not a connected automation we have deployed. Tools such as Zapier can connect the steps. A fixed rule may be sufficient for routing; use AI where interpreting the content adds value.', '38, 54', 'Automation'),
 slide('There are three ways into your work', cards(('Upload', 'Give the assistant selected files.'), ('Connect', 'Let it reach an approved data source.'), ('Work in the app', 'Use an assistant beside the document.')), 'Return to the review report. You can upload a CSV, connect a source or work in the spreadsheet itself. These routes differ in convenience and access. Choose the smallest scope that covers the task.', '47–55 → compressed', 'Access'),
 slide('A connection grants access', split(p('Read a folder and send an email are different permissions.'), callout('Check the scope', 'Which account, which data and which actions are you granting?')), 'MCP is one standard through which tools and data can be exposed to assistants. It does not itself grant permission to use every connected system. The audience only needs the access decision here; protocol details belong later.', '48–49', 'Access', dark=True),
 slide('Check your existing tools first', cards(('Microsoft 365', 'Look for approved assistance inside your Office workflow.'), ('Google Workspace', 'Look for approved assistance in the apps you already use.')), 'Examples include Microsoft 365 Copilot and Gemini in Workspace. Availability varies by licence and administrator settings. Verify the actual account before purchasing another subscription. Do not turn this into a price comparison.', '50–55', 'Access'),
 slide('Budget for attempts and review', table(['What you pay for', 'What to check'], [('Subscription', 'Usage limits and required features'), ('Credits', 'How many attempts one usable result takes'), ('Team access', 'Seats, admin controls and data settings'), ('Your time', 'Review, corrections and rework')]), 'Remove the promise that a fixed monthly price unlocks an equivalent toolbox everywhere. Ask the supplier about the applicable plan. Comparing the cost per usable result is more informative than comparing a headline fee.', '4, 18–19, 39', 'Cost'),
 slide('A shop agent could act—and lose money', cards(('What happened', 'Project Vend found suppliers and adjusted its stock, but also sold items below cost.'), ('What to learn', 'Check the business result, not just whether the agent completed its steps.')), 'Historical example: Anthropic and Andon Labs, first Project Vend report, June 2025. It also invented payment details. Avoid calling it literal bankruptcy or claiming the experiment represents all agent deployments.', '42', 'Two useful stories', dark=True, foot='<a href="https://www.anthropic.com/research/project-vend-1" target="_blank" rel="noopener">Source: Anthropic &amp; Andon Labs · June 2025</a>'),
 slide('Research ideas still need experiments', cards(('What happened', 'Google’s AI co-scientist proposed hypotheses that researchers assessed and tested.'), ('What to learn', 'Use AI to widen the search. Keep the evidence standard for the conclusion.')), 'Historical example: Google Research, February 2025. The system helped generate and refine hypotheses; laboratory work remained part of validation. Do not equate a quickly proposed hypothesis with replacing years of experiments.', '43', 'Two useful stories', foot='<a href="https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/" target="_blank" rel="noopener">Source: Google Research · February 2025</a>'),
 slide('Some tasks are poor starting points', cards(('Hard to judge', 'You cannot tell whether the result is correct.'), ('Hard to undo', 'A mistake would already have reached customers or changed records.')), 'This is a selection rule for a first trial. Choose a familiar draft task with a human checkpoint. A specialised production system may address these risks, but that is a different adoption decision from trying a general assistant.', '25, 39, 45', 'Choose a first task'),
 slide('Try one familiar task this week', flow(('Choose', 'A small job you can review.'), ('Brief', 'Give sources, an example and a check.'), ('Compare', 'Was the result useful after corrections?')), 'Invite the audience to choose the task they considered at the beginning. Measure total effort, including review. Stop or change tools if repeated corrections erase the time saved. No need to subscribe to several products.', '56–57 → one close', 'Your next step', dark=True),
 slide('Keep the guide; skip the memorisation', links(('Tool selection handout', 'reviews/first-three-v2/TOOLBOX-HANDOUT.md'), ('Example report', 'examples/v2/review-report.html'), ('Next: use an agent on a bounded task', 'agentic-ai-v2.html')), 'Pause for questions here. The following slides are a short reference appendix, not another teaching chapter. The expanded handout preserves breadth without filling the talk with product tables.', '40, 55–57', 'Questions'),
 slide('Reference · document tools', links(('Claude', 'https://claude.com/product/overview'), ('ChatGPT', 'https://chatgpt.com/overview/'), ('Gemini', 'https://gemini.google/overview/'), ('Gemini Notebook', 'https://notebook.google/')), 'Product links are examples, not rankings. Consult the linked pages and your administrator for current features, availability and data settings.', '58 → curated', 'Reference'),
 slide('Reference · create and connect', links(('Gamma', 'https://gamma.app/'), ('Canva', 'https://www.canva.com/canva-ai/'), ('ElevenLabs', 'https://elevenlabs.io/text-to-speech'), ('Lovable', 'https://lovable.dev/'), ('Zapier', 'https://zapier.com/')), 'The handout adds selection questions. It deliberately does not reproduce a price list that will age separately from the vendor page.', '59 → curated', 'Reference'),
 slide('Reference · evidence and access', links(('Project Vend', 'https://www.anthropic.com/research/project-vend-1'), ('AI co-scientist', 'https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/'), ('Microsoft 365 Copilot', 'https://www.microsoft.com/en-us/microsoft-365-copilot/business'), ('MCP introduction', 'https://modelcontextprotocol.io/docs/getting-started/intro')), 'These sources support the historical stories and access examples. The editorial source log distinguishes facts, examples and recommendations.', '58–59 → curated', 'Reference'),
]

# TALK 02 — one task, one agent, observable evidence.
INTRO = [
 title('Agentic<br>AI', 'Give an agent a task. Understand and check its work.', '02 · Developers new to agents · v2', 'This talk assumes the audience recognises files and tests, but has not used a coding agent. The invoice task is intentionally small so we can follow every stage.'),
 slide('One failing test, one bounded task', split(code("gross('100', '0.21')\n\nexpected: 121.00\nactual:   100.00"), p('Find the cause, apply the supplied rate and preserve the tests.')), 'These are the checked-in fixture values. The 21% rate is a supplied teaching input, not advice about tax law. A passing result for this one input is only the first check.', '2, 13', 'The task'),
 slide('Set the boundaries before you start', cards(('Workspace', 'Use a disposable copy of the demo files.'), ('Actions', 'Allow this task’s edits and test commands.'), ('Limits', 'No installs, credentials, messages or publication.')), 'Show the actual workspace and permission settings. Keep approval prompts for anything outside the task. Do not use bypass mode for presentation convenience. A separate folder is convenient scoping; it is not a security sandbox.', '33–34 moved before demo', 'Before the demo', dark=True),
 slide('Give it the outcome and the checks', code('Fix the failing invoice tests. Explain the cause.\nApply the supplied rate; round once, half up.\nPreserve the tests. Work only in this demo folder.\nDo not install or publish anything.\nRun python3 -m unittest -v.\nShow the result and the diff.'), 'Use the full prompt in examples/v2/invoice/README.md. Before the talk, copy before/ to a disposable directory. Start the agent here only after showing boundaries. Approve necessary actions deliberately. If a live run is unavailable, use the prepared checkpoints.', '4, 40 → concrete prompt', 'Start the demo', foot='<a href="examples/v2/invoice/README.md" target="_blank" rel="noopener">Demo setup and fallback</a>'),
 slide('We will inspect four checkpoints', flow(('Failure', 'What broke?'), ('Evidence', 'What did it read?'), ('Change', 'What did it edit?'), ('Check', 'What passed?')), 'These are teaching checkpoints, not a promise that every agent takes the same path. If it finishes early, inspect the completed trace. If it stalls, switch to the prepared fixtures and say so.', '4, 12, 15, 30, 33 → coordinated callbacks', 'The route'),
 slide('The model chooses; the harness executes', cards(('Model', 'Proposes an answer or an action from the information it receives.'), ('Harness', 'Supplies context, runs permitted tools and returns their results.')), 'Agent is the combined system when it iterates through a task. The model does not directly execute Python; the harness runs a tool. Harness is a useful term because it explains why the same model behaves differently in different products.', '6, 10', 'Two parts'),
 slide('The agent repeats that exchange', video('agent-loop-dark', 'Choose an action → run the tool → read the result → continue or stop'), 'Checkpoint: show a tool call from the live run, if available. Use the animation to connect the three parts; do not narrate a fictitious live result. Our failure output is the next slide.', '12', 'The loop', dark=True),
 slide('Checkpoint 1 · the failure is evidence', split(code('python3 -m unittest -v\n\nRan 3 tests\nFAILED (failures=2)'), p('The fixture ignores tax. The zero-rate case already passes.')), 'Prepared fallback, validated from before/. The actual output also contains test names and tracebacks; this is an excerpt. Ask what the agent should read next. If live output differs, explain the difference rather than claiming it matches.', '2, 13 → checked fallback', 'Inspect the run', foot='Prepared fixture result · not an agent trace'),
 slide('A tool call produces something inspectable', flow(('Request', 'Read invoice.py.'), ('Execution', 'The harness opens the file.'), ('Result', 'The model receives its contents.')), 'Show the file-read entry in the live trace or open before/invoice.py. Tool schemas and message formats vary across providers. The key is that the result—not the model’s claim that it read something—is the evidence.', '11–13', 'Tools'),
 slide('Checkpoint 2 · the code explains the failure', code("def gross(net, tax_rate):\n    return Decimal(net).quantize(\n        Decimal('0.01'), rounding=ROUND_HALF_UP\n    )\n\n# tax_rate is accepted but never used"), 'The excerpt omits type annotations and the docstring to keep the slide readable. The full source is in before/invoice.py. The passing zero-rate case is consistent with this bug; the failing nonzero cases distinguish it.', '9, 11 → same task', 'Inspect the run'),
 slide('Context is what the model can use now', cards(('Task', 'The requested behaviour and boundaries.'), ('Evidence', 'The code, failures and relevant project rules.'), ('History', 'Earlier messages and results retained by the harness.')), 'Context is broader than the latest message. A product may retrieve or summarise previous material. Avoid saying every request literally includes every previous token or that the product has no persistent storage.', '7–11, 28 → compressed', 'Context'),
 slide('More information is not always more help', split(p('Keep the task, relevant files and current evidence easy to find.'), callout('Watch the behaviour', 'Repeated mistakes or lost constraints are reasons to inspect the context.')), 'Do not teach a universal 40% or 50% threshold. The point at which performance suffers depends on the model, task and content. Missing a necessary file can be as harmful as loading too much irrelevant material.', '29–30', 'Context'),
 slide('When a session loses the thread', flow(('Summarise', 'Record decisions, files and remaining work.'), ('Restart', 'Open a fresh task session when useful.'), ('Verify', 'Check that the handoff kept the essentials.')), 'Explain compaction only as a summary that can omit details. Caching affects reused computation and billing; it does not restore omitted facts. Subagents are an optional advanced technique covered in later talks.', '31–32, 40', 'Context'),
 slide('Thinking text is not verification', cards(('Useful for orientation', 'It may explain a proposed approach or an uncertainty.'), ('Evidence of the result', 'The changed file, command output and checks matter more.')), 'Reasoning can help a model tackle a task, but displayed summaries are not a faithful record of every internal cause. Keep the distinction practical: review evidence instead of accepting a confident explanation.', '14–15', 'Reasoning', dark=True),
 slide('Checkpoint 3 · inspect the change', code("# Before\ntotal = Decimal(net)\n\n# After\ntotal = Decimal(net) * (Decimal('1') + Decimal(tax_rate))\n\n# Keep the final two-decimal rounding."), 'This slide isolates the conceptual change. The actual reference implementation names total only in after/. Check the real diff and confirm the rate comes from the argument. It must not simply return 121 or weaken the tests.', '13 → patch review', 'Inspect the run'),
 slide('Checkpoint 4 · test more than the hook', table(['Case', 'Expected result'], [('100 at 0.21', '121.00'), ('100 at 0', '100.00'), ('0.50 at 0.21', '0.61')]) + p('The three invoice tests pass on the reference fix.'), 'Prepared result: python3 -m unittest test_invoice -v in after/. These cases verify the stated fixture behaviour, not all production financial requirements. The export tests in talk 03 are separate.', '13, 40 → independent checks', 'Inspect the run', foot='Prepared fixture result · three invoice tests'),
 slide('Passing tests are part of the review', cards(('Diff', 'Does the change match the requested behaviour?'), ('Checks', 'Were the tests actually run and preserved?'), ('Scope', 'Did anything unrelated change?')), 'Inspect the actual output from the live agent if present. The agent may report success while skipping a command or changing tests. The human reviewer decides whether the evidence is sufficient.', '33, 40–41 → stronger finish', 'Review'),
 slide('If it goes wrong, interrupt early', flow(('Stop', 'Pause changes outside the task.'), ('Inspect', 'Find the first wrong assumption.'), ('Redirect', 'Supply the missing fact or narrow the task.')), 'If changes are wrong, inspect a diff and use an understood checkpoint or restore a disposable copy. Do not suggest destructive reset commands that would remove unrelated work. A second identical retry without new evidence is often unhelpful.', 'new failure recovery', 'Recovery', dark=True),
 slide('Rules can survive a new session', code('# Project instructions\n- Tests: python3 -m unittest -v\n- Use Decimal for invoice calculations.\n- Preserve tests and keep edits within the task.\n- Ask before installing dependencies.'), 'Use the instruction file your harness reads: CLAUDE.md for Claude Code, AGENTS.md where supported. These are textual instructions, not an access-control boundary. Product memory may also retain notes; inspect what is actually loaded.', '35–36', 'Project knowledge'),
 slide('Put recurring procedures in a skill', cards(('Project rules', 'Short facts and boundaries needed across tasks.'), ('Skill', 'A reusable procedure loaded for the relevant task.')), 'A release checklist is a better skill example than another agent glossary. Describe a skill as instructions and optional supporting files. Exact loading and invocation are harness-specific. Plugin packaging belongs in a later talk.', '37', 'Project knowledge'),
 slide('Tools can reach outside the repo', flow(('Local tool', 'Read files or run tests.'), ('Connected tool', 'Query another system through an API, CLI or MCP server.'), ('Permission', 'Allow only the access this task needs.')), 'MCP standardises part of the connection between assistants and external tools/data. It does not eliminate authentication or make arbitrary access safe. Our demo has no reason to connect to another system.', '38–39', 'Connected tools'),
 slide('Start with one approved agent', p('Use an interface you can inspect: its changes, commands, permissions and results.') + cards(('Examples', 'Claude Code or Codex, in the interface your team supports.'), ('First decision', 'Can it do this task within the access you are willing to grant?')), 'This replaces the landscape tour. Model selection can wait until the audience can identify a task and evaluate its result. Tool availability and account features change; point to product documentation for setup.', '17–27 → one practical choice', 'Getting started'),
 slide('Your first session, in five steps', flow(('Describe', 'Name the outcome.'), ('Provide', 'Give relevant context.'), ('Limit', 'Set access and scope.'), ('Inspect', 'Read the change.'), ('Verify', 'Run the checks.')), 'Return to the opening task and ask the audience to explain each step. The five-step routine is the takeaway. Do not add another glossary or product comparison after it.', '40–41 → one close', 'Your next step', dark=True),
 slide('Try the fixture, then a task of your own', links(('Demo files, prompt and fallback', 'examples/v2/invoice/README.md'), ('Next: engineer a repeatable workflow', 'agentic-engineering-v2.html'), ('Choose a tool for a different kind of work', 'ai-toolbox-v2.html')), 'Questions and optional practice. The fixture is small enough to inspect fully. For a real task, choose work you already understand and can verify.', '41 → practice', 'Questions'),
 slide('Reference · operating an agent', links(('Claude Code: how it works', 'https://code.claude.com/docs/en/how-claude-code-works'), ('Claude Code: permissions', 'https://code.claude.com/docs/en/permissions'), ('Claude Code: project memory', 'https://code.claude.com/docs/en/memory'), ('Claude Code: skills', 'https://code.claude.com/docs/en/skills')), 'These are provider-specific references, not a claim that every harness behaves identically. Consult current documentation for exact controls.', '42–43 → curated', 'Reference'),
 slide('Reference · context and evidence', links(('Effective context engineering', 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'), ('Reasoning reports and their limits', 'https://www.anthropic.com/research/reasoning-models-dont-say-think'), ('MCP introduction', 'https://modelcontextprotocol.io/docs/getting-started/intro'), ('Building effective agents', 'https://www.anthropic.com/engineering/building-effective-agents')), 'The sources support the conceptual explanation. The fixture and prepared test results are local evidence, separate from provider claims.', '42–43 → curated', 'Reference'),
]

# TALK 03 — an evolution of the workflow, with one invoice-export example.
ENGINEERING = [
 title('Agentic<br>Engineering', 'Build a workflow you can verify and recover.', '03 · Developers going deeper · v2', 'Assume the audience knows model, harness, tools and context from talk 02. This talk asks how to make the process repeatable. Keep the original evolution structure, but let each chapter solve an engineering failure.'),
 slide('A passing demo is only the beginning', cards(('In the demo', 'One task, a few files and a result you can inspect.'), ('In repeated work', 'Changing inputs, partial failures, review time and uncertain outcomes.')), 'The goal is not maximum autonomy. It is work that can be accepted with evidence and recovered when it fails. Distinguish repeatable workflows from one successful transcript.', '2, 23–25 → new framing', 'The problem'),
 slide('Keep one example throughout', p('Add CSV export to the invoice calculation from talk 02.') + code('invoice_id,customer,net,tax_rate,gross\nINV-001,"North, Ltd",100.00,0.21,121.00\nINV-002,"Studio ""A""",0.50,0.21,0.61'), 'This is an excerpt from the reference CSV. The complete file also exercises a newline in a customer name. Our implementation assumes validated rows; production validation and spreadsheet formula handling are separate requirements.', 'new running example', 'The task', foot='<a href="examples/v2/invoices.csv" download>Download the reference CSV</a>'),
 slide('Recap: the system you are engineering', flow(('Context', 'Task, rules and evidence.'), ('Model', 'Proposes the next step.'), ('Tools', 'Perform permitted actions.'), ('Result', 'Changes what the system knows.')), 'Compress the original prediction, thinking, tools and statelessness chapters to this recap. We can change what information the system receives, what actions it may take and how results are checked.', '3–21 → recap', 'The machine'),
 slide('Problem 1 · “Add export” leaves too much open', cards(('Unspecified', 'Columns, rounding, quoting and empty input.'), ('Consequence', 'A plausible implementation may still miss the requirement.')), 'Ask the audience what they would need to review an export. The missing information is a contract problem before it is a model problem. Do not respond to ambiguity by increasing reasoning effort.', '25 → expanded contract', 'Define the work', dark=True),
 slide('Write the acceptance contract first', table(['Requirement', 'Observable check'], [('Five named columns, input order preserved', 'Read the exported rows back'), ('Use the existing calculation rule', 'Check known totals and rounding'), ('Commas, quotes and newlines survive', 'Round-trip special customer names'), ('Empty input still has a header', 'Export an empty collection')]), 'These are the requirements implemented by the checked-in reference fixture. For the talk, the set is deliberately small and testable. Label omitted production requirements rather than implying this is a complete billing system.', '23–25 → explicit contract', 'Define the work'),
 slide('Decide how much structure the task needs', cards(('Direct change', 'A small, clear edit with a simple check.'), ('Workflow', 'Known stages and acceptance gates.'), ('Agent exploration', 'The next useful step depends on what it finds.')), 'This is a design choice, not a maturity ladder. A workflow may contain agent-driven stages. Use the simplest approach that can meet the contract and explain its result.', '20, 48', 'Choose the process'),
 slide('Make the stages and ownership visible', flow(('Inspect', 'Locate code and tests.'), ('Plan', 'Resolve the contract.'), ('Build', 'Make the bounded change.'), ('Verify', 'Run independent checks.'), ('Review', 'Accept or send back.')), 'This is the workflow for our example. Keep a named owner for integration and acceptance. The next slides show how evidence and recovery change what happens at the gates.', '46–48 → core workflow', 'The workflow'),
 slide('Problem 2 · a green command can mislead', split(code('exit code: 0'), p('It may have run the wrong tests, skipped a case or checked a weaker requirement.')), 'An exit code is an observation. It does not prove the tests cover the contract. The original deck said a goal prompt could not be gamed; replace that guarantee with independent checks and review.', '23–25', 'Check the evidence', dark=True),
 slide('Give every claim a check', cards(('Claim', 'Customer names survive export.'), ('Evidence', 'Parse the CSV and compare the original strings.'), ('Boundary', 'This does not check every spreadsheet’s interpretation.')), 'The reference test includes a comma, embedded quotes and a newline. Parsing with the CSV reader tests serialization rather than eyeballing a text file. Formula-like input remains outside this fixture’s contract.', '23–25 → example verification', 'Check the evidence'),
 slide('Keep the calculation outside the guesswork', code("total = Decimal(net) * (Decimal('1') + Decimal(tax_rate))\nreturn total.quantize(\n    Decimal('0.01'), rounding=ROUND_HALF_UP\n)"), 'Use deterministic code for a specified calculation. Let the agent inspect and change the implementation, but verify against the explicit rounding rule. This is the existing calculation from the reference fix, reused by the exporter.', '15, 25 → deterministic tool example', 'Check the evidence'),
 slide('Inspect both tests and the artifact', split(code('python3 -m unittest -v\n\nRan 5 tests\nOK'), p('Then open the CSV and compare its columns, names and totals with the contract.')), 'Prepared reference result from after/: three invoice tests and two export tests. The CSV is generated with the same implementation and parsed in validation. This is not a benchmark or a captured agent run.', '23–25 → checked evidence', 'Check the evidence', foot='Prepared reference result · five tests'),
 slide('Keep acceptance separate from implementation', cards(('Agent produces', 'The patch, commands run, output and unresolved questions.'), ('Reviewer decides', 'Whether the evidence meets the contract and the change is ready.')), 'Another model can help review but can share the same blind spots. Protect important acceptance checks outside the implementation’s control when warranted. Human review still owns the decision for this workflow.', '24–25, 42 → review ownership', 'Check the evidence'),
 slide('Problem 3 · the useful facts get buried', split(p('Exploration accumulates logs, dead ends and outdated assumptions.'), callout('Keep the working set useful', 'Retain the contract, relevant code and current evidence.')), 'Preserve the original context thread without treating attention as a simple fixed budget divided equally between tokens. More irrelevant material can harm retrieval and distract the model; exact behaviour varies.', '26–34 → context diagnosis', 'Manage context', dark=True),
 slide('Give each stage the context it needs', table(['Stage', 'Useful inputs'], [('Inspect', 'Entry points, failing case and repository map'), ('Build', 'Contract, target files and project rules'), ('Verify', 'Contract, patch and independent checks'), ('Review', 'Evidence, risks and unresolved questions')]), 'The table is our proposed design, not an automatic feature of every harness. Fresh stages must receive enough context to preserve decisions. A short handoff is only useful if it contains the necessary facts.', '18, 27, 36, 46', 'Manage context'),
 slide('Store decisions before restarting', code('Task: add invoice CSV export.\nRule: apply supplied rate; round once, half up.\nFiles: invoice.py, export.py, test_export.py.\nDone: quoting and empty-input cases pass.\nOpen: production input validation is out of scope.\nNext: inspect the diff and exported sample.'), 'This is a handoff example for the reference fixture. Keep file references and unresolved scope, not pages of tool output. A new session should verify the handoff against the files rather than trusting it blindly.', '34, 50–51 → useful handoff', 'Manage context'),
 slide('Caching and compaction solve different problems', cards(('Caching', 'Reuses eligible computation; can reduce cost and latency.'), ('Compaction', 'Replaces history with a shorter summary; can lose details.')), 'Billing rules, cache lifetimes and treatment of reasoning vary by provider and model. Avoid the original blanket claims about byte-identical requests, perpetual warm caches or thinking always being retained/stripped. Detailed mechanics belong in talk 04.', '31–34 → two distinctions', 'Manage context'),
 slide('Problem 4 · retries consume the budget', p('A failed attempt should change the next decision.') + flow(('Inspect', 'What failed?'), ('Change', 'What new evidence or approach will help?'), ('Stop', 'What limit ends the run?')), 'Do not let a retry loop keep editing indefinitely. Distinguish transient tool failure, misunderstanding and an unmet requirement. Each calls for a different response.', '22, 24 → bounded retries', 'Recover', dark=True),
 slide('Set a retry policy before the run', table(['Failure', 'Next step'], [('Transient tool error', 'Retry within a small explicit limit'), ('Same failed check again', 'Inspect cause; require a changed approach'), ('Missing access or requirement', 'Pause for the owner'), ('Time or cost budget reached', 'Stop and return partial work with evidence')]), 'This is a policy sketch, not a provider command. Choose numeric limits for the real environment. A stop should preserve useful evidence and never imply the task succeeded.', '22–25 → stop policy', 'Recover'),
 slide('Recovery starts with an inspectable boundary', flow(('Before', 'Record the baseline and isolate the work.'), ('During', 'Keep edits scoped and checkpoints understandable.'), ('After failure', 'Inspect the partial diff; resume or restore deliberately.')), 'A branch or worktree isolates edits, not credentials or network access. Use environment isolation separately when needed. Never blindly reset a shared dirty workspace; preserve unrelated changes.', '24, 44 → recovery boundary', 'Recover'),
 slide('Problem 5 · cheap tokens can buy costly work', cards(('Count the task', 'Attempts, tool use, model charges and review time.'), ('Count accepted results', 'How many met the same quality bar?')), 'Do not claim stronger or smaller models are always cheaper. Compare the total process on representative tasks and hold acceptance criteria constant. Subscription limits and API charges are different meters.', '29–31, 38–45 → cost per accepted task', 'Choose the model', dark=True),
 slide('Compare accepted work, not headline rates', table(['Illustrative trial', 'Setup A', 'Setup B'], [('Model + tool cost', '$6', '$10'), ('Accepted tasks, out of 10', '6', '10'), ('Cost per accepted task', '$1', '$1'), ('Review time, total', '40 min', '15 min')]), 'Hypothetical arithmetic, not measured model performance. Both spend one dollar per accepted task, but B accepts more of the batch and uses less review time. Track failures, latency and human effort separately rather than collapsing them into one misleading number.', '30, 38 → labelled comparison', 'Choose the model', foot='Illustrative numbers · not vendor measurements'),
 slide('Change one dial and measure again', flow(('Baseline', 'A few representative tasks and fixed checks.'), ('Trial', 'Change model or reasoning effort.'), ('Compare', 'Acceptance, cost, time and review burden.')), 'The set should include common tasks and failure-prone cases. Repeat enough to see variability. Re-evaluate after meaningful model, prompt or tool changes; do not teach a permanent ranking of named tiers.', '37–45 → evaluation method', 'Choose the model'),
 slide('Problem 6 · one agent carries too much', video('subagents-dark', 'Separate investigation → evidence back · token counts in the animation are illustrative.'), 'Delegation may help when investigation is separable or parallelism saves time. It adds coordination, context handoff and cost. It is not required for this small export fixture. The animation’s 80k/200 token counts are illustrative, not measurements of this example.', '35–36', 'Delegate selectively', dark=True),
 slide('Delegate an outcome with a boundary', code('Task: review CSV quoting and empty-input behaviour.\nRead: export.py and test_export.py.\nDo not edit files.\nReturn: finding, file reference and reproducing input.\nState what you did not check.'), 'This is a reviewer brief for the same example, not an instruction to spawn agents during this revision. Findings must be checked before acting. A short conclusion without evidence is not enough.', '42–44 → bounded delegation', 'Delegate selectively'),
 slide('Parallel work still needs integration', cards(('Workers', 'Own separate scopes and return evidence.'), ('Integrator', 'Resolves conflicts and checks the combined result.'), ('Reviewer', 'Accepts the final change against the contract.')), 'Independent read-only reviews are easier to combine than concurrent edits to the same files. Use worktrees for independent edits when appropriate; a shared test run on the integrated result still matters.', '44–48 → integration', 'Delegate selectively'),
 slide('Problem 7 · useful lessons disappear', cards(('Keep a rule', 'A short constraint needed across tasks.'), ('Keep a procedure', 'A skill for a recurring workflow.'), ('Keep evidence', 'A decision note linked to the relevant code or test.')), 'Avoid turning every solved task into permanent context. Retain what will change future behaviour and periodically remove stale instructions. Plugin distribution is a later concern.', '49–58 → durable knowledge', 'Make it repeatable', dark=True),
 slide('Write one small procedure people can inspect', code('# Invoice export review\n1. Read the export contract.\n2. Run invoice and CSV tests.\n3. Inspect the diff and exported sample.\n4. Report evidence and remaining gaps.\n5. Leave acceptance to the reviewer.'), 'This is an example skill body rather than a full provider-specific package. Keep the procedure readable and useful before distributing it. It does not itself enforce permissions or guarantee a complete review.', '51–58 → one reusable procedure', 'Make it repeatable'),
 slide('The complete workflow has a way back', flow(('Contract', 'Agree on the check.'), ('Build', 'Make a scoped change.'), ('Verify', 'Return evidence.'), ('Review', 'Accept or return it.')) + p('Failed check → diagnose within budget. Missing requirement → ask the owner.'), 'Trace the invoice export once through the workflow. Return to the relevant stage when new evidence invalidates a decision. On budget exhaustion, preserve a partial result and mark it incomplete. Success is reviewed evidence against a contract.', '46–48, 59 → synthesis', 'Bring it together'),
 slide('Improve one workflow this week', cards(('Write the contract', 'What must be true when the task is done?'), ('Add the evidence', 'Which check can establish it?'), ('Add the exit', 'How will you stop and recover when it fails?')), 'This is the single closing action. Encourage a small change to an existing workflow before adding fleets of agents or a plugin marketplace.', '59 → concrete close', 'Your next step', dark=True),
 slide('Go deeper where your work needs it', links(('04 · Subagents & prompt caching', 'subagents-prompt-caching.html'), ('05 · Cost & context (WIP)', 'cost-and-context.html'), ('06 · Orchestrating agents (WIP)', 'orchestrating-agents.html'), ('07 · Measuring what works (WIP)', 'measuring-what-works.html')), 'Questions here. The later decks are existing editions, not revised as part of this work. They retain their own date stamps and some are work in progress. Do not imply their product claims were revalidated in this revision.', 'new series handoff', 'Questions'),
 slide('Reference · workflows and evaluation', links(('Building effective agents', 'https://www.anthropic.com/engineering/building-effective-agents'), ('Demystifying evals for AI agents', 'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents'), ('Effective context engineering', 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'), ('Fixture, tests and reference implementation', 'examples/v2/invoice/README.md')), 'These sources support the design distinctions. The workflow, retry table and illustrative comparison are teaching designs, not measured production outcomes. Detailed evidence and validation are recorded with this edition.', '60 → curated', 'Reference'),
]

CSS = '''
/* V2 content styles. The original deck-stage owns viewport scaling. */
.v2 { --h2-size:clamp(64px,4.1vw,78px); --body-size:clamp(32px,2vw,38px);
  --lead-size:clamp(36px,2.4vw,44px); --small-size:clamp(24px,1.4vw,27px);
  --code-size:clamp(28px,1.7vw,32px); --h3-size:clamp(34px,2vw,38px); }
.v2 .slide-content {padding:76px 96px 70px; gap:0; max-height:100%;}
.v2 .slide-head {margin-bottom:34px; padding-bottom:20px;}
.v2 h2 {margin-bottom:42px; max-width:31ch;}
.v2 .v2-body {display:flex; flex-direction:column; gap:32px; min-height:0;}
.v2 .lead {max-width:53ch; line-height:1.4;}
.v2 .tile {padding:36px; gap:20px;}
.v2 .tile h3 {color:var(--s-accent);}
.v2 .cards {gap:28px;}
.v2 .split {gap:56px;align-items:center;}
.v2-stack {display:flex; flex-direction:column;gap:28px;min-width:0;}
.v2 .split .cards {grid-template-columns:1fr;}
.v2 .kcard {padding:44px;}
.v2 .kcard .big {font-size:clamp(48px,3.3vw,62px);line-height:1.1;}
.v2 .kcard p {font-size:var(--body-size);}
.v2 .code {line-height:1.6; white-space:pre-wrap;overflow-wrap:anywhere;padding:34px 40px;}
.v2 .code code {font:inherit;}
.v2 .tbl {font-size:var(--body-size);}
.v2 .tbl td,.v2 .tbl th {padding:22px 24px;line-height:1.35;}
.v2 .tbl th {font-size:var(--small-size);}
.v2 .note {margin-top:32px;line-height:1.4;}
.v2 a {color:var(--s-accent);text-underline-offset:.18em;}
.v2 a:focus-visible {outline:3px solid var(--s-accent);outline-offset:8px;}
.v2-flow {display:flex;list-style:none;gap:26px;}
.v2-flow li {flex:1;min-width:0;border-top:4px solid var(--s-accent);padding-top:24px;}
.v2-flow li span {font:500 clamp(24px,1.5vw,28px) var(--font-m);color:var(--s-muted);}
.v2-flow h3 {margin:22px 0 18px;color:var(--s-accent);}
.v2-flow p {font-size:var(--body-size);line-height:1.4;}
.v2-links {display:grid;gap:12px;}
.v2-links a {display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--s-line);padding:18px 0;font-size:var(--body-size);text-decoration:none;}
.v2-links a:hover {text-decoration:underline;}
.v2-media {text-align:center;min-height:0;}
.v2-media video {display:block;margin:auto;max-width:100%;width:auto;height:440px;border-radius:16px;}
.v2-play {display:block;margin:12px auto 0;padding:10px 22px;font:500 clamp(22px,1.3vw,25px) var(--font-m);color:var(--s-accent);background:transparent;border:1px solid var(--s-accent);border-radius:8px;cursor:pointer;}
.v2-play:focus-visible {outline:3px solid var(--s-accent);outline-offset:5px;}
.v2-media figcaption {font-size:var(--small-size);color:var(--s-muted);margin-top:20px;}
.v2-report {padding:42px 48px;border:2px solid var(--s-line);background:var(--s-card-bg);border-radius:16px;}
.v2-report-head {font:500 24px var(--font-m);color:var(--s-accent);display:flex;justify-content:space-between;margin-bottom:34px;}
.v2-report-head span {color:var(--s-muted);font-size:22px;}
.v2-report h3 {font-size:44px;margin-bottom:30px;}
.v2-bars {display:grid;gap:20px;max-width:1200px;margin-bottom:24px;}
.v2-bars>div {display:grid;grid-template-columns:120px 1fr 160px;align-items:center;gap:24px;font-size:28px;}
.v2-bars i {display:block;width:var(--bar-width);height:36px;background:var(--s-accent);}
.v2-bars i.missing {width:100%;height:36px;background:none;border:2px dashed var(--s-muted);}
.v2-report p {font-size:26px;color:var(--s-muted);}
.v2-report-flag {font-size:28px;color:var(--s-accent);border-top:1px solid var(--s-line);padding-top:24px;margin-top:24px;}
.v2.title-slide .ts-hero h1 {font-size:clamp(150px,10vw,184px);line-height:.95;}
.v2.title-slide .ts-sub {font-size:clamp(36px,2.4vw,44px);max-width:45ch;line-height:1.35;}
@media (prefers-reduced-motion:reduce) {
 .v2 *, .v2 *::before, .v2 *::after {animation:none!important;transition:none!important;}
}
/* Canvas scaling already handles short screens; hide only optional UI. */
@media (max-height:700px) {.pui-controls {bottom:8px;}}
@media (max-height:600px) {.pui-controls button {padding:7px 10px;}}
@media (max-height:500px) {.pui-notes {max-height:50vh;}}
'''

VIDEO_JS = '''
<script>
// Play only the active explainer; reduced-motion users start it explicitly.
(function(){
 const ds=document.querySelector('deck-stage');
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 ds.querySelectorAll('.v2-media').forEach(figure=>{
  const v=figure.querySelector('video'),button=figure.querySelector('[data-video-toggle]');
  function sync(){button.textContent=v.paused?'Play animation':'Pause animation';button.setAttribute('aria-pressed',String(!v.paused));}
  button.addEventListener('click',()=>{if(v.paused)v.play().catch(()=>{});else v.pause();});
  v.addEventListener('play',sync);v.addEventListener('pause',sync);sync();
 });
 function update(){
  ds.querySelectorAll('video').forEach(v=>{
   if(!v.closest('[data-deck-active]') || motion.matches){v.pause();return;}
   v.currentTime=0;v.play().catch(()=>{});
  });
 }
 ds.addEventListener('slidechange',update);motion.addEventListener('change',update);update();
})();
</script>
'''


def build(original, slides, number):
    text = (ROOT / original).read_text()
    head = text[:text.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>' + esc(slides[0]['title']) + ' — v2</title>', head, flags=re.S)
    # Self-host the existing bundled fonts; do not change the originals or shared CSS.
    head = re.sub(r'<link[^>]+(?:fonts.googleapis.com|fonts.gstatic.com)[^>]*>\s*', '', head)
    token_css='\n'.join(f'<link rel="stylesheet" href="ember_design_system/tokens/{n}.css">' for n in ['colors','typography','spacing','effects'])
    head = head.replace('<link rel="stylesheet" href="ember_design_system/styles.css">', token_css)
    font_css=''
    for family, prefix in [('Space Grotesk','space-grotesk'),('IBM Plex Sans','ibm-plex-sans'),('IBM Plex Mono','ibm-plex-mono')]:
        for weight in [400,500,600,700]:
            font_css+=f'@font-face{{font-family:"{family}";font-weight:{weight};font-style:normal;font-display:swap;src:url("remotion/public/fonts/{prefix}-{weight}.woff2") format("woff2")}}\n'
    head += '<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n'+font_css+CSS+'\n</style>\n</head>\n<body>\n'
    out = original.replace('.html','-v2.html')
    sections=[]
    for i,s in enumerate(slides,1):
        attrs=f'id="slide-{i}" data-label="{esc(s["title"], quote=True)}" data-speaker-notes="{esc(s["notes"], quote=True)}"'
        if 'hero' in s:
            content=f'''<section class="slide dark title-slide v2" {attrs}>
<div class="ts-top"><span class="k">{s['audience']}</span><span class="meta">September 2026</span></div>
<div class="ts-hero"><h1>{s['hero']}<span class="dot">.</span></h1><p class="ts-sub">{s['subtitle']}</p></div>
<div class="ts-foot"><div class="ts-author"><a href="https://davidbudac.cz" target="_blank" rel="noopener">David Budáč</a></div><div class="ts-loopline">{number:02} / 03 · Revised edition</div></div></section>'''
        else:
            foot=f'<p class="note">{s["foot"]}</p>' if s['foot'] else ''
            content=f'''<section class="slide {'dark' if s['dark'] else 'light'} v2" {attrs}>
<div class="slide-content"><div class="slide-head"><span class="snum">{i:02}</span><div class="crumb">{s['chapter']}</div></div>
<h2>{s['title']}</h2><div class="v2-body">{s['body']}</div>{foot}</div></section>'''
        sections.append(content)
    tail=text[text.index('</deck-stage>'):]
    # Replace the inherited unconditional video playback with active/reduced-motion handling.
    tail=re.sub(r'<script>\s*/\* restart embedded explainer videos.*?</script>', '', tail, flags=re.S)
    # Initialise presenter notes at the actual deep-linked slide, even before a nav event.
    tail=tail.replace('var current = 0, presenter = null, mouseT = null;', "var current = Math.max(0, Array.from(ds.children).findIndex(s => s.hasAttribute('data-deck-active'))), presenter = null, mouseT = null;")
    tail=tail.rsplit('</body>', 1)[0]+VIDEO_JS+'\n</body>'+tail.rsplit('</body>', 1)[1]
    result=head+'<!-- Derived from '+original+'; content source: scripts/build_first_three_v2.py -->\n<deck-stage width="1920" height="1080" no-rail>\n'+'\n\n'.join(sections)+'\n'+tail
    (ROOT/out).write_text(result)
    rows=['# '+slides[0]['title']+' — v2 slide map','',f'{len(slides)} slides. Original references use physical section numbers; originals remain unchanged.','', '| New | Title | Original material |','|---|---|---|']
    notes=['# '+slides[0]['title']+' — v2 speaker notes','', 'Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.','']
    for i,s in enumerate(slides,1):
        rows.append(f'| {i} | {s["title"]} | {s["origin"]} |')
        notes += [f'## {i}. {s["title"]}', '',s['notes'],'']
    (REVIEW/(out.replace('.html','-map.md'))).write_text('\n'.join(rows)+'\n')
    (REVIEW/(out.replace('.html','-notes.md'))).write_text('\n'.join(notes).rstrip()+'\n')
    print(out, len(slides), 'slides')


def artifacts():
    folder=ROOT/'examples/v2'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'review-data.csv').write_text('month,completed_orders\nApril,80\nMay,120\nJune,\n')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Example review report</title><style>
body{font-family:system-ui,sans-serif;background:#f8f5f0;color:#242019;margin:0;padding:clamp(20px,5vw,70px)}main{max-width:1000px;margin:auto}h1{font-size:clamp(30px,5vw,52px)}p,li{font-size:20px;line-height:1.5}table{border-collapse:collapse;width:100%;font-size:22px}td,th{text-align:left;padding:18px;border-bottom:1px solid #c7bfb2}.gap{color:#a93819}a{color:#a93819}aside{border-left:4px solid #a93819;padding-left:20px;margin-top:32px}footer{margin-top:40px;font-size:16px}</style>
<main><p>Teaching example · synthetic data · draft</p><h1>April–May grew. June is incomplete.</h1><table><thead><tr><th scope="col">Month</th><th scope="col">Completed orders</th></tr></thead><tbody><tr><th scope="row">April</th><td>80</td></tr><tr><th scope="row">May</th><td>120</td></tr><tr><th scope="row">June</th><td class="gap">Missing</td></tr></tbody></table><p>May increased by 40 completed orders compared with April: (120 − 80) / 80 = <strong>50%</strong>.</p><aside><h2>Review required</h2><p>A complete Q2 total cannot be calculated from this file. Supply June before presenting quarterly results.</p></aside><footer>Source: <a href="review-data.csv" download>review-data.csv</a>. Created for The AI Toolbox v2. This artifact demonstrates the desired output; it is not evidence of a particular vendor run.</footer></main></html>'''
    (folder/'review-report.html').write_text(html+'\n')
    # Import only the committed reference fixture; there are no external side effects.
    import sys
    sys.path.insert(0,str(folder/'invoice/after'))
    from export import export_invoices
    rows=[dict(invoice_id='INV-001',customer='North, Ltd',net='100.00',tax_rate='0.21'),dict(invoice_id='INV-002',customer='Studio "A"',net='0.50',tax_rate='0.21'),dict(invoice_id='INV-003',customer='Line\nbreak',net='100.00',tax_rate='0')]
    (folder/'invoices.csv').write_text(export_invoices(rows))
    posters=ROOT/'assets/v2';posters.mkdir(parents=True,exist_ok=True)
    for name,labels in [('agent-loop-dark',['Choose action','Run tool','Read result']),('subagents-dark',['Bounded task','Separate worker','Evidence back'])]:
        boxes=''.join(f'<rect x="{40+i*420}" y="165" width="380" height="210" rx="18" fill="#211d16" stroke="#ff5c35" stroke-width="3"/><text x="{230+i*420}" y="280" text-anchor="middle" fill="#f8f5f0" font-size="36" font-family="sans-serif">{label}</text>' for i,label in enumerate(labels))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="540" viewBox="0 0 1320 540"><rect width="1320" height="540" fill="#0e0c08"/>{boxes}<text x="660" y="460" text-anchor="middle" fill="#ff5c35" font-size="28" font-family="sans-serif">Press play to view the animation</text></svg>'
        (posters/(name+'.svg')).write_text(svg+'\n')


def main():
    REVIEW.mkdir(parents=True,exist_ok=True)
    hashes=json.loads((REVIEW/'original-hashes.json').read_text())
    for path in ['ai-toolbox.html','agentic-ai.html','agentic-engineering.html']:
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==hashes[path], f'Original changed: {path}'
    artifacts()
    for n,(original,slides) in enumerate([('ai-toolbox.html',TOOLBOX),('agentic-ai.html',INTRO),('agentic-engineering.html',ENGINEERING)],1):
        build(original,slides,n)


if __name__=='__main__':
    main()
