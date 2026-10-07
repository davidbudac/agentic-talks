#!/usr/bin/env python3
"""Reproduce clarity batch 1 from its immutable Git baseline.

Run from anywhere with --write. Refuses to overwrite edits made after the last
recorded build. HTML remains the normal editing surface after this migration.
"""
import argparse, hashlib, html, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = '51f2e9a3479a864bf1901aa9c8e3bfa4961bcac0'
MANIFEST = HERE / 'batch1-manifest.json'
SECTION = re.compile(r'<section\b[^>]*>.*?</section>', re.S)

def esc(s): return html.escape(s, quote=True)
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def baseline(name): return subprocess.check_output(['git','show',f'{BASE}:{name}'],cwd=ROOT,text=True)
def label(s): return html.unescape(re.search(r'data-label="([^"]*)"',s).group(1))
def notes(s, text): return re.sub(r'data-speaker-notes="[^"]*"',lambda _: 'data-speaker-notes="'+esc(text)+'"',s,count=1)
def replace(s, old, new):
    if old not in s: raise ValueError('Missing replacement: '+old[:100])
    return s.replace(old,new)
def bullets(items): return '<ul class="bul reveal">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'
def cards(items): return '<div class="cards c'+str(len(items))+' reveal">'+''.join('<div class="tile"><span class="k">'+h+'</span><p>'+p+'</p></div>' for h,p in items)+'</div>'
def code(text): return '<div class="code reveal">'+esc(text)+'</div>'
def slide(label_, title, content, note, speaker, theme='light', tag='In practice'):
    return f'''<section class="slide {theme}" data-label="{esc(label_)}" data-speaker-notes="{esc(speaker)}">
    <div class="slide-content">
      <div class="slide-head reveal"><span class="snum">0</span><div class="crumb">{tag}</div></div>
      <h2 class="reveal">{title}</h2>
      {content}
      <p class="note reveal">{note}</p>
    </div>
  </section>'''

def patch_list(s, items):
    s,n = re.subn(r'<ul class="bul reveal">.*?</ul>',lambda _:bullets(items),s,count=1,flags=re.S)
    assert n==1
    return s

def patch_note(s,text):
    s,n=re.subn(r'<p class="note reveal">.*?</p>',lambda _: '<p class="note reveal">'+text+'</p>',s,count=1,flags=re.S)
    assert n==1
    return s

outputs={}; inventories={}; maps={}; metrics={}

def build(name, order, edits, refs, reasons, snapshot):
    original=baseline(name+'.html'); match=re.search(r'(<deck-stage\b[^>]*>)(.*?)(</deck-stage>)',original,re.S)
    assert match
    originals=SECTION.findall(match.group(2)); assert len(originals)==(43 if name=='agentic-ai' else 57)
    for i,s in enumerate(originals,1):
        assert 'data-speaker-notes=' in s
    revised={i:edits.get(i,s) for i,s in enumerate(originals,1)}
    def prepare(s,old,new,reference=False):
        s=re.sub(r'(<span class="snum">).*?(</span>)',lambda m:m[1]+str(new)+m[2],s,count=1)
        s=s.replace('<section ',f'<section data-origin-slide="{old}" ',1)
        # Old prose references used printed numbers, not actual order.
        s=re.sub(r'([1-5]) of 5', 'supporting example', s)
        s=re.sub(r'\(slide \d+\)', '(see the reference material)',s)
        s=re.sub(r'from slide \d+', 'introduced in the main talk',s)
        if reference:
            s=s.replace('class="slide ', 'class="slide reference-slide ',1)
            banner=f'<div class="reference-banner">Reference · {snapshot} snapshot · <a href="{name}.html">Back to the talk</a></div>'
            s=re.sub(r'(<section\b[^>]*>)',lambda m:m[1]+'\n    '+banner,s,count=1)
            oldnotes=html.unescape(re.search(r'data-speaker-notes="([^"]*)"',s).group(1))
            s=notes(s,'REFERENCE ONLY. Product details reflect the original '+snapshot+' snapshot and need verification before reuse. '+oldnotes)
        return s
    main=[prepare(revised[i],i,n) for n,i in enumerate(order,1)]
    output=original[:match.start(2)]+'\n\n  '+'\n\n  '.join(main)+'\n\n'+original[match.end(2):]
    # Replace the obsolete optional-demo instructions in the introduction.
    if name=='agentic-ai':
        output=re.sub(r'<!--(?:(?!-->).)*LIVE DEMO(?:(?!-->).)*-->', '''<!-- OPTIONAL DEMO: use a disposable local project with scoped permissions.
  Show one test failure, a bounded fix and the final test/diff. If unavailable,
  use the explicitly illustrative invoice trace in the next slides.
  Later callbacks can use the finished transcript; no live timing dependency. -->''',output,flags=re.S)
    output=output.replace('</head>', '<style>\n/* Shorter teaching copy gets a larger reading size on the existing canvas. */\n.slide{--body-size:clamp(30px,2.4vw,34px);--small-size:clamp(22px,1.8vw,26px);--code-size:clamp(24px,2vw,28px)}\n</style>\n</head>',1)
    outputs[name+'.html']=output
    cover=slide('Reference guide','Reference material',cards([
        ('Use selectively','Product details and supporting examples from the original '+snapshot+' deck.'),
        ('Verify before reuse','Check availability, prices and limits with the linked primary sources.')]),
        f'<a href="{name}.html">Return to the main talk</a>',
        'This is an optional reference deck, not a continuation of the presentation. The original snapshot date is shown on each page. Omitted slides remain recoverable from the baseline Git commit.',theme='dark',tag='Reference')
    cover=cover.replace('<h2 class="reveal">Reference material</h2>','<h1 class="reference-title">Reference material</h1>')
    cover=cover.replace('<span class="snum">0</span>','<span class="snum">1</span>')
    reference=[cover]+[prepare(revised[i],i,n,True) for n,i in enumerate(refs,2)]
    refout=original[:match.start(2)]+'\n\n  '+'\n\n  '.join(reference)+'\n\n'+original[match.end(2):]
    refout=re.sub(r'<!--(?:(?!-->).)*LIVE DEMO(?:(?!-->).)*-->', '<!-- Optional reference deck. Use the main talk for the current teaching sequence. -->', refout, flags=re.S)
    refout=re.sub(r'<title>.*?</title>', '<title>'+esc(name.replace('-',' ').title())+' — Reference</title>',refout,count=1)
    refout=refout.replace('</head>', '''<style>
.reference-title{font:var(--w-bold) clamp(48px,4vw,76px)/1.1 var(--font-display);margin-bottom:32px;color:var(--s-text)}
.reference-banner{position:absolute;top:18px;right:96px;z-index:2;font:clamp(16px,1.1vw,21px)/1.3 var(--font-body);color:var(--s-muted)}
.reference-banner a{color:inherit;text-decoration:underline}
</style>\n</head>''',1)
    outputs[name+'-reference.html']=refout
    # The stage can initialize before presenter listeners attach on a deep link.
    for target in [name+'.html', name+'-reference.html']:
        outputs[target]=outputs[target].replace('</head>', '<style>.note a{color:var(--s-text);text-decoration:underline;text-underline-offset:3px}.note a:focus-visible{outline:2px solid var(--s-accent);outline-offset:4px}</style>\n</head>',1)
        outputs[target]=outputs[target].replace('var current = 0, presenter = null, mouseT = null;', \
            "var current = Math.max(0, Array.from(ds.querySelectorAll(':scope > section')).findIndex(function(s){ return s.hasAttribute('data-deck-active'); })), presenter = null, mouseT = null;")
    inventories[name]=[{'original':i,'label':label(s),'sha256':sha(s)} for i,s in enumerate(originals,1)]
    maps[name]=[{'original':i,'label':label(s),'main':order.index(i)+1 if i in order else None,
        'reference':refs.index(i)+2 if i in refs else None,'action': 'rewritten' if i in edits else ('retained' if i in order or i in refs else 'merged/removed'),
        'reason':reasons.get(i, 'Retained in main talk.' if i in order else ('Optional reference; original snapshot date retained.' if i in refs else 'Repetition or transition removed; baseline retained in Git.'))}
        for i,s in enumerate(originals,1)]
    from html.parser import HTMLParser
    class Text(HTMLParser):
        def __init__(self): super().__init__();self.parts=[]
        def handle_data(self,d):self.parts.append(d)
    def words(s):
        p=Text();p.feed(s);return len(' '.join(p.parts).split())
    metrics[name]={'before_slides':len(originals),'after_slides':len(main),'reference_slides':len(reference),
        'before_words':sum(words(s) for s in originals),'after_words':sum(words(s) for s in main)}

# INTRO: one invoice example, one architecture diagram, one close.
intro=baseline('agentic-ai.html'); src={i:s for i,s in enumerate(SECTION.findall(re.search(r'<deck-stage\b[^>]*>(.*?)</deck-stage>',intro,re.S)[1]),1)}
e={}
e[1]=notes(src[1], 'Introduce the beginner outcome: give one bounded task and verify it. The invoice example runs throughout. A live demonstration is optional; the illustrative trace is sufficient. Product detail is in the dated reference deck.')
e[1]=e[1].replace('Internal talk · September 2026','Revised October 2026')
e[5]=slide('Agenda','Give an agent a task you can check',cards([
 ('Understand the loop','Who chooses an action, who runs it, and how the result comes back.'),
 ('Guide the work','Supply relevant context, useful project rules and scoped permissions.'),
 ('Check the result','Inspect the changed files and run the check that defines done.')]),
 'One example throughout: an invoice total that is missing VAT.',
 'Keep this agenda to twenty seconds. The outcome is confidence giving a bounded task and checking it. Product comparisons are in the separate reference deck.',tag='Our route')
e[2]=patch_note(src[2],'Illustrative trace: a passing test is evidence for that case. Review the diff and relevant edge cases before accepting the change.')
e[2]=notes(e[2],'Introduce this as an illustrative four-step invoice example, not a recording of a benchmark. The expected tax rule comes from the task and test. Passing this one test does not establish all invoice behavior. We return to the same example throughout.')
e[3]=patch_note(src[3],'The <b>model</b> proposes actions. The <b>harness</b> executes permitted tools. Together, repeating this process, they form an <b>agent</b>.')
e[10]=replace(src[10],'Claude Opus 5.5','Claude model')
e[10]=notes(e[10],'Define all three terms on this one diagram. This is the local CLI example: the harness runs with local files and tools, while inference is remote. Other products host the harness remotely; do not generalize this placement to every agent. The agent is the entire loop, not a third server.')
e[9]=notes(src[9],'Explain this request-based example: the name can be recalled because the harness provides it in the request. Products may store history or durable memories, but the model needs relevant information supplied for the current call. We no longer need the Memento analogy or a separate memory recap.')
e[11]=slide('What one turn sends','One message sits inside a larger request',code('SYSTEM       role, rules and tool descriptions\nPROJECT      how to run the invoice tests\nHISTORY      the task and earlier results\nTOOL OUTPUT  invoice.py and the failing test\nYOUR MESSAGE "fix the missing VAT"'),
 '<b>Context</b> is the information supplied for this call. <b>Tokens</b> are the chunks used to measure it.',
 'Point to the five groups. Do not imply every file in the repository is automatically sent: only supplied or retrieved content is present. Later, summaries can replace older history. We define context and tokens here instead of asking the room to memorize a glossary.',theme='dark',tag='The request')
e[4]=slide('Optional demo','Watch one bounded task',code('Fix the invoice calculation so the VAT test passes.\nDo not change the test or unrelated files.\nRun the relevant tests and show the final diff.'),
 'Optional live run: use a disposable project and scoped permissions. The next slide provides an illustrative trace if no demo is available.',
 'Use a prepared disposable project with no production credentials. Explain the allowed files and commands before starting. Inspect one tool call, the final test output and the diff. If the run finishes early, use its transcript for later discussion. Do not weaken permissions to avoid a pause. Without a prepared project, use the explicitly illustrative trace.',theme='dark',tag='Optional live example')
e[12]=patch_list(src[12],[
 '<b>Propose:</b> the model chooses the next action.',
 '<b>Run:</b> the harness executes it under the configured permissions.',
 '<b>Observe:</b> the result returns as context for the next step.',
 '<b>Check:</b> stop when the task is verified, or ask when blocked.'])
e[12]=patch_note(e[12],'In a live run or a finished transcript, point to one tool call and its result. That is one lap of the loop.')
e[12]=notes(e[12],'Let the animation run once. Use one call/result pair from a live or completed transcript; the task does not need to still be running. Distinguish the model deciding to stop from the human acceptance check. The next slide makes the loop concrete.')
e[13]=slide('The loop, worked example','The invoice fix, step by step',code('''run tests     → FAIL: expected 121, got 100
read invoice  → VAT is missing from the total
edit code     → apply the order’s 21% VAT rate
run tests     → PASS
review diff   → check scope and edge cases'''),
 'Illustrative trace. The model requests the actions; the harness runs them and returns the results.',
 'Each tool call and result is one lap. Read the trace top to bottom and point to the same task from the hook. The passing test demonstrates the example, while diff review and additional relevant checks establish acceptance.',tag='The loop')
e[14]=patch_list(src[14],[
 'Reasoning gives the model room to work through intermediate steps before answering or acting.',
 'More effort can help a difficult diagnosis; it also takes more time and tokens.',
 'For the invoice task, verify the VAT rule and run the test. A plausible explanation alone is not evidence.'])
e[14]=replace(e[14],'THINKING — hidden scratchpad','ILLUSTRATIVE REASONING')
e[14]=replace(e[14],'The model first produces a hidden thinking scratchpad of reasoning, then the final answer','Illustration of intermediate reasoning before an answer; not a captured internal trace')
e[14]=patch_note(e[14],'Visible thinking may be a summary. Judge the result and the checks, not how convincing the narration sounds.')
e[14]=notes(e[14],'The diagram is a teaching illustration, not access to a real private scratchpad. Merge the old thinking caveat here: visible reasoning is not guaranteed to faithfully expose the cause of a decision. Explain the practical tradeoff without universal effort defaults or a live timing dependency.')
e[21]=slide('Choose an interface','Choose the interface you already work in',cards([
 ('Terminal','Run a coding agent beside your commands and tests.'),
 ('Editor','Review and change code inside your existing development workflow.'),
 ('App or web','Give a task, inspect progress, and review the returned files.')]),
 'Look for clear permissions, visible changes and a way to run checks. Model and product lists are in the reference deck.',
 'The loop is the same teaching model across surfaces, but capabilities and permissions differ. Let beginners start with the surface they understand; avoid turning this into a catalogue of products.',tag='Getting started')
e[26]=slide('Choose a billing route','Two ways to pay for the work',cards([
 ('Subscription','A plan for using an app or coding tool, subject to its usage limits.'),
 ('Metered API','Usage-based billing for integrations and automated workloads. Set a budget and monitor it.')]),
 'Check the chosen product’s plan, supported access route and limits. Price per token is only one part of the cost of a completed task.',
 'Do not claim the API has no cap: budgets, rate limits and provider limits still matter. Avoid prescribing subscription credentials for custom automation. Detailed historical plan tables are in the dated reference deck.',theme='dark',tag='Getting started')
e[28]=patch_list(src[28],[
 'Context contains the instructions, conversation and tool results supplied for <b>this call</b>.',
 'The <b>context window</b> is the maximum capacity. Its size depends on the model and configuration.',
 'Supply the relevant test and invoice code. An unread file cannot guide the model through this request.'])
e[28]=replace(e[28],'CONTEXT WINDOW · 1M tokens','CONTEXT WINDOW · finite capacity')
e[28]=notes(e[28],'Use the stacked diagram to revisit the payload. Avoid equating context with all learned knowledge: the model also has pretrained knowledge. What it lacks is access to project facts that have not been supplied or retrieved. The diagram is conceptual, not a measurement of this session.')
e[29]=slide('Context quality','More context is not always more useful',cards([
 ('Useful context','The failing test, the VAT rule and the code path that computes the total.'),
 ('Distracting context','Old tasks, duplicate file dumps and unrelated logs that obscure those facts.')]),
 'Watch for ignored requirements, repeated work and missed evidence. There is no universal percentage at which quality fails.',
 'Replace the old quality animation here: its fixed curve can suggest a numerical threshold the evidence does not establish. Context behavior depends on task, model and distractors. The context research remains linked on the sources slide.',theme='dark',tag='Context')
e[30]=slide('Keep context useful','Choose the next step from the task state',cards([
 ('New task','Start a fresh conversation when the previous task is complete.'),
 ('Same task','Summarize the goal, decisions, failures and next check before continuing.'),
 ('Broad search','Delegate investigation and request findings with file references.')]),
 'Inspect the context display as a capacity indicator. Check behavior and results before deciding what to remove.',
 'No live checkpoint is required. Show a completed transcript if useful. Do not prescribe a fixed 40 or 50 percent reset rule. Preserve requirements and evidence during a handoff.',tag='Context')
e[31]=slide('Caching and compaction','Cheaper reuse and shorter context',cards([
 ('Caching','Reuses computed state for a matching prefix. It can reduce processing cost and latency; the content is still input.'),
 ('Compaction','Replaces older material with a summary. It frees room, but details omitted from that summary may be lost.')]),
 'For the invoice task, preserve the VAT rule, failing test, attempted changes and verification command.',
 'These mechanisms solve different problems. Their implementation and activation depend on the harness/provider. Do not describe cached content as permanent model memory or imply compaction preserves every detail.',theme='dark',tag='Context')
e[32]=patch_list(src[32],[
 'Delegate a focused investigation, such as finding every place invoice totals are calculated.',
 'The helper’s intermediate tool output stays in its own working context. Ask for a concise result with evidence.',
 'A fresh subagent needs a self-contained task. A conversation fork can inherit the existing history.'])
e[32]=notes(e[32],'Preserve the animation as an illustration of output isolation. It is not a universal statement about input inheritance: fresh subagents and forks differ. Claude Code subagent documentation, checked 2026-10-03, describes both. Ask for file locations and uncertainty, not a bare conclusion. Delegation has coordination and token costs.')
e[33]=slide('Permissions','Decide what the agent may touch',cards([
 ('Scope the work','Allow the project files and test commands needed for the task.'),
 ('Keep approval points','Ask before destructive actions, access changes or publishing outside the task.'),
 ('Contain mistakes','For unattended experiments, restrict filesystem, network and credentials in an actual sandbox.')]),
 'A separate folder or Git branch protects neither credentials nor the rest of the machine. Check the configured boundary.',
 'Use an actual permission decision from the prepared demo if available. Product mode names differ and should not be presented as identical. A worktree separates edits; it is not by itself a security sandbox. Keep the default approval flow for the demo.',theme='dark',tag='Permissions')
e[36]=slide('Project rules','Teach it the rules it cannot infer',code('# CLAUDE.md — invoice project\n- Run invoice checks with: python -m unittest\n- VAT rates come from the order record.\n- Do not replace the tests to make a fix pass.\n- Ask before changing the stored invoice schema.'),
 'Keep standing rules short. Use the instruction-file convention supported by your harness, such as CLAUDE.md or AGENTS.md.',
 'This is an illustrative project file, not the actual repository test command. Use the same invoice example. Persistent notes become useful only when the harness loads the relevant information; avoid repeating the no-memory analogy.',tag='Project knowledge')
e[37]=slide('Skills and plugins','Save a repeatable check as a skill',code('invoice-check/\n  SKILL.md       when to run + how to verify\n  scripts/       optional deterministic checks\n  references/    VAT and rounding rules'),
 '<b>Skill:</b> a reusable procedure loaded when relevant. <b>Plugin:</b> a way to distribute a toolkit to a team.',
 'The skill could check VAT, zero-value invoices and rounding, then report the test output and unverified cases. Its description helps the agent discover it. Descriptions and loaded content still have context cost. Keep detailed installation steps for a deeper talk.',theme='dark',tag='Project knowledge')
e[38]=slide('Tools for the invoice task','Give the agent access to the next fact',cards([
 ('CLI','Run the project’s invoice tests and inspect Git changes.'),
 ('API','Fetch a permitted record through a service interface.'),
 ('MCP connection','Expose supported issue-tracker or document tools to the agent.')]),
 'Choose the narrowest useful access. A connector does not grant permission to publish or change unrelated records.',
 'These are access mechanisms, not competing intelligence levels. CLIs can call remote APIs too. For this example, the agent might read the issue that defines the invoice bug; it should not modify financial production data.',tag='External tools')
e[39]=patch_list(src[39], ['MCP standardizes how a supported client discovers and calls tools exposed by a server.', 'Example: read the issue describing the invoice bug, then propose an update with verification evidence.', 'Each integration still needs compatible support, authentication and scoped permissions.'])
e[39]=notes(e[39],'Use the integration diagram briefly. Explain that MCP standardizes the interface between a client and server; it does not guarantee every app supports every tool. The invoice task remains the example, and posting results is a separate authorized action.')
e[40]=slide('Your first agent task','Give a bounded task. Check the result.',bullets([
 '<b>Goal:</b> name the result and the files or system in scope.',
 '<b>Context:</b> supply the relevant examples, rules and failure evidence.',
 '<b>Permissions:</b> decide what can run and where approval is needed.',
 '<b>Acceptance:</b> inspect the diff, run the relevant check, record what remains unverified.']),
 '<a href="agentic-ai-reference.html">Optional reference: terminology, products and historical pricing</a> · <a href="index.html">All talks</a>',
 'End here for questions. Ask the audience to choose one small task with a check they can run. The following two slides are source references, not another recap.',theme='dark',tag='Try this next')
# Retained reference slides receive targeted corrections, not a claim of refreshed pricing.
e[27]=slide('Cost per task','Compare the cost of an accepted result',cards([
 ('Cheap tokens, many retries','A low unit price can be offset by more tool calls, reasoning and failed attempts.'),
 ('Higher unit price, fewer attempts','A more capable model can win on a difficult task. Measure rather than assuming it will.')]),
 'Compare the same task and acceptance check. Include all attempts, cached input, fresh input and output.',
 'This replaces the crowded benchmark collection. No new measurement is claimed. For simple work, a smaller model can remain the better choice.',theme='dark',tag='Reference · task cost')
e[34]=slide('Unattended runs','Isolation must restrict real access',bullets([
 'Use a disposable environment with only the files the task needs.',
 'Limit network destinations and remove production credentials.',
 'Apply a time or token budget and retain the final diff and logs.',
 'A project copy, worktree or CI runner is not automatically a security boundary.']),
 'Keep approvals where the environment cannot safely contain the consequence.',
 'Reference guidance for discussing unattended runs. Never recommend bypass mode merely because work is in a separate folder or on CI.',theme='dark',tag='Reference · permissions')
order=[1,2,3,5,10,9,11,4,12,13,14,21,26,28,29,30,31,32,33,36,37,38,39,40,42,43]
refs=[7,18,19,20,22,23,24,25,27,34,42,43]
reasons={i:'Landscape detail moved out of the beginner teaching sequence.' for i in range(17,28)}
reasons.update({6:'Architecture merged into original 10.',8:'Memory explanation taught by original 9.',15:'Thinking tradeoff and caveat merged into original 14.',16:'General use-case grid removed to keep the invoice thread.',35:'Repeated memory transition removed.',41:'Closing summary merged into original 40.',29:'Replaced fixed quality curve with task-specific symptoms; no universal threshold.',30:'Removed 40–50% rule and live timing dependency.'})
build('agentic-ai',order,e,refs,reasons,'September 2026')

# TOOLBOX: task -> useful output -> review, with two stories and three integration routes.
toolbox=baseline('ai-toolbox.html');src={i:s for i,s in enumerate(SECTION.findall(re.search(r'<deck-stage\b[^>]*>(.*?)</deck-stage>',toolbox,re.S)[1]),1)}
e={}
e[1]=notes(src[1], 'Introduce a task-first field guide. The main talk covers useful outputs, selection and review. Detailed vendor tables remain in a separate July 2026 reference snapshot. There is no live demo.')
e[1]=e[1].replace('July 2026</span>','Revised October 2026</span>').replace('what it can do, and what it costs','choose a useful task, tool and review')
e[2]=slide('The hook','Ask for a result you can review',cards([
 ('A paragraph','“Write a summary of this quarter’s results.”'),
 ('An editable draft','“Use these results and last quarter’s deck to build the next review. Flag missing data.”')]),
 'The useful difference is the output: a file, a working draft, or an action you can inspect.',
 'Drop the unsupported ten-percent framing. Set an achievable expectation: an editable draft with explicit gaps. The next example shows the inputs, output and human review.',theme='dark',tag='Start with the task')
e[3]=slide('Agenda','Three questions for choosing a tool',cards([
 ('What do I need?','A document, a design, a clip, an answer or a repeatable task.'),
 ('Where should I start?','The tools your team already has, then a specialist if needed.'),
 ('What must I check?','Accuracy, permissions, export, rights and the cost of iteration.')]),
 'Product and price tables are optional reference material. The main talk is about choosing a useful workflow.',
 'Twenty seconds. No six-part catalogue. Tell the audience there is a dated reference deck for product detail and sources.',tag='Our route')
e[23]=slide('One task, agent-style','Build the quarterly review from evidence',code('INPUT    results.csv + Q1 deck + brand template\nREQUEST  draft the Q2 review in the same structure\nCHECK    reconcile chart totals with the CSV\nGAPS     mark missing June data; ask for the export\nOUTPUT   editable deck + a list of unresolved points'),
 '<b>Illustrative workflow.</b> Ask it to flag gaps; verify that it actually did. Review the numbers and the story before sharing.',
 'This is a teaching example, not a captured run. Walk input to output. A model can invent missing numbers; explicitly asking for gaps and reconciling the result are checks, not guarantees. Use the same example when discussing file creation and Office editing.',theme='dark',tag='A useful first task')
e[5]=patch_note(src[5],'An agent combines a model with tools and a loop. Whether it acts safely depends on the access and checks around it.')
e[6]=patch_list(src[6],[
 '<b>Choose</b> the next action.', '<b>Run</b> a permitted tool.', '<b>Inspect</b> the result and decide what comes next.'])
e[6]=patch_note(e[6],'For the review deck: read the CSV → build a chart → reconcile the totals → revise the draft.')
e[6]=notes(e[6],'Let the animation run once. Explain the loop using the quarterly review example. Do not claim every product in the catalogue uses an identical agent architecture; this is the agentic pattern.')
e[7]=patch_list(src[7],[
 'For each step, the model needs the relevant instructions and information supplied to it.',
 'For the review deck, provide the results CSV, prior structure and brand template.',
 'Stored memories and connected files help only when the relevant information is actually retrieved.'])
e[7]=replace(e[7],'The model has <span class="o">no memory</span>','Give it the <span class="o">right material</span>')
e[7]=patch_note(e[7],'Check which files it used. A connected folder is not evidence that every document was read.')
e[7]=notes(e[7],'Use the animation for request-based context. Avoid explaining the movie analogy or introducing transformer internals. The practical consequence is that the user supplies and checks the relevant material. Product memory differs by tool.')
e[25]=slide('The human checkpoint','AI drafts. You sign.',cards([
 ('Check the facts','Reconcile numbers with the source. Open important citations.'),
 ('Check the consequence','Review more carefully when money, people or public communication are involved.'),
 ('Check the boundary','Approve publishing and external actions separately from making a draft.')]),
 'A review step reduces risk only when someone performs a relevant check.',
 'Remove the claim that human checkpoints automatically make every tool safe. Ask the room what they would check before sending the quarterly review. Keep this principle close to the worked example.',theme='dark',tag='Review')
e[22]=slide('Three everyday tasks','Start with work you already repeat',cards([
 ('Prepare a review','CSV + last deck → editable draft. Check every important number.'),
 ('Digest a report','Source documents → summary or audio. Check the claims against the originals.'),
 ('Adapt a campaign','Approved message + brand files → draft formats. Check layout and wording.')]),
 'Choose one task with a result you already know how to judge.',
 'Reduce the six-day catalogue to three outputs. These categories guide the later examples. Do not read a tool name into every tile yet.',tag='Where it helps')
e[18]=slide('Choose a starting point','Start where your work already lives',cards([
 ('Files and drafts','Try the file and agent features available in your approved assistant.'),
 ('Office or Workspace','Check the AI features your organization already provides inside its apps.'),
 ('Specialist output','Try a dedicated tool when the included option cannot produce the needed result.')]),
 'Compare one real task before buying another subscription. Check availability for your account and region.',
 'This replaces a detailed vendor price grid with a selection method. Claude, ChatGPT and Gemini examples remain in the reference snapshot. Avoid implying equal capabilities or universal plan inclusion.',theme='dark',tag='Choosing a tool')
e[14]=slide('Agents for files','Give a file agent an outcome',code('“Use this folder to draft the Q2 review.\nKeep Q1’s structure and our template.\nList missing inputs.\nAsk before changing the source files.”'),
 'Example product: Claude Cowork. Inspect the input list, changed files and unresolved questions.',
 'Discuss the file-agent workflow already described in the original deck. Keep launch dates, origin story and plan detail in reference material. The prompt is illustrative; sensitive actions require the configured approval flow.',tag='Files')
e[15]=slide('Design by iteration','Use a brief, then refine the draft',cards([
 ('Brief','Name the audience, purpose, brand references and required output.'),
 ('Refine','Change one visible thing at a time: hierarchy, wording, layout or emphasis.'),
 ('Export and inspect','Open the actual file. Check fonts, charts and editability before sharing.')]),
 'Example tools: Claude Design or Canva. Supplying a brand kit still requires a review of the result.',
 'Teach the design workflow rather than launch statistics or a guarantee that importing brand files enforces compliance. Tie the exported draft back to the quarterly review.',theme='dark',tag='Design')
e[17]=slide('Research over your documents','Use the source as the final check',cards([
 ('Ask a bounded question','“What changed in the customer study, and which pages support that?”'),
 ('Inspect the evidence','Open the cited passage. Check that it supports the summary and its qualifications.')]),
 'A source-grounded assistant such as Google’s notebook product can help you navigate documents. A citation is a starting point for verification.',
 'Avoid a product-family tour. Explain the difference between summarizing provided sources and discovering new ones. Do not promise that source restriction guarantees correctness. Product naming and plan history remain in the reference snapshot.',tag='Research')
e[4]=slide('Read the price tag','Budget for iteration, not one perfect attempt',cards([
 ('Subscription','A recurring fee with usage limits. Check what your existing plan includes.'),
 ('Credits','Each generation consumes a balance. Discarded drafts and retries count too.')]),
 'For team use, check per-seat terms, data handling and commercial rights. API integrations add metered usage.',
 'Keep two meters visible; explain team and API purchasing only if relevant to the room. No current prices are newly asserted. Historical plan tables are available separately.',theme='dark',tag='Cost')
e[20]=slide('Products change','Keep an exit route',bullets([
 'Prefer outputs your team can open and edit outside the tool.',
 'Keep the original data, prompts and approved assets.',
 'Check the current product page before promising a feature or budget.']),
 'A tool can change its name, plan or export support. Your work should remain usable.',
 'Replace six company histories with the practical consequence. One product anecdote can be spoken if helpful; do not imply that a historical price snapshot is current.',tag='Choosing a tool')
# Short task/output/review examples replace multi-vendor price catalogues.
examples={
27:('Build a small app','A prototype people can try', [('Give the brief','“Make a savings calculator with these inputs and an explanation of the result.”'),('Inspect the output','Test the calculations, empty states and forms. Review access and data handling before launch.')], 'Examples: Lovable, v0 or Replit. Budget for revisions; a working preview still needs checks.', 'Show the shape of the result and acceptance checks. Revenue figures, alternative lists and tier details belong in reference, not the teaching sequence.'),
28:('Generated video','Plan a shot before you generate it',[('Brief one shot','State the subject, action, framing and duration. Start from approved material when useful.'),('Review each take','Check continuity, text, product details, rights and the credit cost of discarded takes.')], 'Examples: Veo / Flow, Runway or Higgsfield. A good shot is one ingredient in a finished video.', 'Avoid a universal best-model claim and exact clip budgets. Keep the difference between a shot and an assembled film central.'),
29:('Templated video','Repeat a design with new data',[('Lock the template','Set layout, fonts, colours and timing once.'),('Change the content','Render another report or language version, then check text fit, data and timing.')], 'Example: HyperFrames. A reusable template improves consistency; new content still needs review.', 'Contrast templated graphics with generated footage. Remove the claim that brand compliance is solved or only one review is ever needed.'),
31:('Voice and dubbing','Change the script without a studio visit',[('Make a draft','Turn an approved script into narration or a translated voice-over.'),('Listen before release','Check names, numbers, pronunciation and meaning. Confirm rights and consent for the voice.')], 'Example: ElevenLabs. Compare a short sample before choosing a voice or buying capacity.', 'No universal popularity or commercial-license guarantee. Product prices and licensing must be checked for the specific intended use.'),
33:('Images and design','Choose by the output you need',[('Layout and brand','Use a design tool when you need controlled text, logos and repeatable formats.'),('New imagery','Use image generation for a concept or source image, then inspect and refine it.')], 'Examples: Canva, Firefly or Ideogram. Review text, rights, privacy settings and visual accuracy.', 'Remove aesthetic rankings, blanket legal assurances and price ladders. Give a concrete distinction the audience can act on.'),
37:('Repeatable automation','Put a checkpoint in the workflow',[('Trigger and draft','A form arrives → prepare a follow-up and a proposed CRM update.'),('Approve and act','A person checks the draft → send and record only the approved changes.')], 'Examples: Zapier, Make or n8n. Check the actual data flow, permissions and failure handling.', 'Self-hosting an orchestrator does not by itself keep connected AI/API data local. Do not imply otherwise. Show the review boundary in the example; no messages are sent by this deck.')}
for i,(lbl,title,cs,nt,sp) in examples.items():e[i]=slide(lbl,title,cards(cs),nt,sp,theme='dark' if i%2==0 else 'light',tag='Choose by task')
e[38]=slide('Before real use','Check the terms, access and result',cards([
 ('Rights and privacy','Can you use the output commercially? Are inputs or outputs public?'),
 ('Data and access','Where does the data go, and which actions can the tool perform?'),
 ('Cost and review','What do retries cost? Who checks the result before it is used?')]),
 'Check the actual plan and intended use. A paid tier alone does not establish permission, privacy or suitability.',
 'Keep the practical checklist and remove categorical legal recommendations. Have participants apply these grouped checks to one tool they already use, without vendor absolutes.',theme='dark',tag='Before adoption')
e[41]=slide('Story: Project Vend','An agent’s operating setup changes the result',cards([
 ('The experiment','Claude ran a snack shop: ordering stock, setting prices and talking to customers.'),
 ('The lesson','Early failures exposed weak inventory and decision controls. Later iterations added tools and operating structure.')]),
 'A bounded experiment, not evidence that an agent can run any business unattended. Source: Anthropic, Project Vend.',
 'Retain one failure-and-improvement story. Explain the mechanism rather than memorable purchase details or exact profit figures. The source links remain on the sources slide.',tag='A real-world lesson')
e[45]=slide('Story: the craft still matters','Judge the finished work',cards([
 ('One campaign choice','Anthropic’s Super Bowl campaign used human performers and a conventional production team.'),
 ('Your choice','Use AI where it helps the brief. A lower production barrier does not decide the best creative approach.')]),
 'One campaign is an example, not proof of a universal ceiling on AI-generated work. Campaign sources are in the reference list.',
 'Remove the unsupported best-ad ranking, the comparative clip count and the claim that AI has not raised a ceiling. Keep the audience-relevant decision: craft and the brief determine the production method.',theme='dark',tag='A real-world lesson')
e[53]=slide('Three integration routes','Where should the work happen?',cards([
 ('Create a new file','Upload the source material in chat and download an editable draft.'),
 ('Edit an existing file','Use an approved assistant inside the document or spreadsheet.'),
 ('Connect another system','Give access to the specific records or actions the task needs.')]),
 'Start with the route that fits the task. Check your organization’s approved tools and permissions.',
 'This decision slide now comes before the examples. Avoid repeating the vendor comparison or exact pricing. The quarterly review uses each route for a different purpose.',tag='Working in your apps')
e[49]=slide('Files from chat','For a new draft, start with the source files',code('UPLOAD   results.csv + Q1.pptx + brand template\nASK      create an editable Q2 review\nDOWNLOAD open the actual presentation file\nCHECK    chart data, layout, fonts and missing inputs'),
 'Confirm that your tool supports the required file type and that the downloaded output remains editable.',
 'A file download is not proof of correctness. Show the output inspection as part of the workflow. No add-in is needed for this route when supported by the chosen tool.',theme='dark',tag='Route 1 · create')
e[48]=slide('Edit inside the app','For an existing file, keep the review nearby',cards([
 ('Make a scoped request','“Update this chart from the new data. Preserve the formulas and template.”'),
 ('Inspect the changes','Check the affected cells or slides. Recalculate, compare with the source, and review the final file.')]),
 'Use an approved Office or Workspace integration. Availability and permissions depend on your account and organization.',
 'Do not promise formulas cannot break or conversations universally sync across apps. Teach the review workflow. Product-specific installation and plan detail remains in reference material.',tag='Route 2 · edit')
e[47]=patch_list(src[47], ['For the review deck, connect the approved source and inspect which records were retrieved.', 'MCP is one standard for tool access. Compatibility, authentication and permissions depend on the integration.', 'Expose only the records and actions needed. Review a proposed write before it happens.'])
e[47]=notes(e[47],'Use the connection diagram as a conceptual illustration. Do not claim every connector is implemented using MCP, or that every server works with every client. The practical issue is supported access to the right data, with the right permission boundary.')
e[54]=slide('Choose one task','Try one useful workflow this week',bullets([
 '<b>Choose:</b> a recurring task with a result you know how to judge.',
 '<b>Start:</b> with an approved tool you already have.',
 '<b>Review:</b> the facts, file and permissions before using the output.']),
 '<a href="ai-toolbox-reference.html">Optional reference: product tables and supporting examples</a> · <a href="index.html">All talks</a>',
 'End the spoken talk here. Ask the audience to name their task and acceptance check. Sources follow; there is no second recap. The reference deck is a dated snapshot, not a newly verified buying guide.',theme='dark',tag='Try this next')
# Important caveats in retained supporting material.
e[42]=replace(src[42],'Ten years of research. <span class="o">Two days.</span>','A hypothesis to <span class="o">test</span>') if 'Ten years of research. <span class="o">Two days.</span>' in src[42] else src[42]
e[42]=re.sub(r'<h2 class="reveal">.*?</h2>','<h2 class="reveal">AI proposed a hypothesis. Scientists supplied the evidence.</h2>',e[42],count=1,flags=re.S)
e[42]=re.sub(r'<div class="big">.*?</div>','<div class="big">Hypothesis<br>→ validation</div>',e[42],count=1,flags=re.S)
e[42]=patch_note(e[42],'The AI proposed a hypothesis; this comparison does not show that two days of generation replaced ten years of experimental work.') if '<p class="note reveal">' in e[42] else e[42]
e[42]=e[42].replace("The point: it didn't replace ten years of science — it means the <b>next</b> question might not need them.", "A generated hypothesis still needs experimental validation.")
e[42]=notes(e[42],'Keep the distinction between hypothesis generation and experimental validation explicit. The original source reports the researchers already had evidence from years of laboratory work. Do not extrapolate that future experiments can be skipped.')
e[39]=src[39].replace('Leader','Examples').replace('ElevenLabs Music (safest)','ElevenLabs Music').replace('Suno (check legal)','Suno (check rights)')
e[32]=src[32].replace('the legally safest AI music route','an option whose licence terms should be checked for the intended use')
e[35]=src[35].replace('for writing itself, the $20 general assistant is now <b>as good.</b>','for writing itself, compare your existing general assistant on a real task.')
order=[1,2,3,23,5,6,7,25,22,18,14,15,17,4,20,27,28,29,31,33,37,38,41,45,53,49,48,47,54,56,57]
refs=[8,11,12,13,16,19,24,30,32,34,35,36,39,42,43,44,50,51,52,56,57]
reasons={i:'Category detail condensed into a task/output/review example.' for i in examples}
reasons.update({9:'Use-case grid merged into original 22.',10:'Vendor section divider removed.',21:'Tasks divider removed; worked example moved to opening.',26:'Catalogue divider removed.',40:'Five-story block reduced to two integrated examples.',46:'Integration divider replaced by original 53 decision slide.',55:'Second recap merged into original 54.'})
build('ai-toolbox',order,e,refs,reasons,'July 2026')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    last=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for path,content in outputs.items():
        dest=ROOT/path
        if dest.exists():
            allowed={sha(content)}
            if path in last.get('outputs',{}):allowed.add(last['outputs'][path])
            if not path.endswith('-reference.html'):allowed.add(sha(baseline(path)))
            if sha(dest.read_text()) not in allowed:raise SystemExit('Refusing to overwrite unrecorded edits: '+path)
    print(json.dumps(metrics,indent=2))
    if args.write:
        for path,content in outputs.items():(ROOT/path).write_text(content)
        MANIFEST.write_text(json.dumps({'baseline':BASE,'outputs':{p:sha(c) for p,c in outputs.items()},'metrics':metrics},indent=2)+'\n')
        (HERE/'baseline-slides.json').write_text(json.dumps(inventories,ensure_ascii=False,indent=2)+'\n')
        (HERE/'slide-map.json').write_text(json.dumps(maps,ensure_ascii=False,indent=2)+'\n')
        rows=['# Batch 1 slide map','','Original numbers count every section. Main and reference numbers are the new positions.','']
        for deck,items in maps.items():
            rows += ['## '+deck,'','| Original | Label | Main | Reference | Disposition |','|---|---|---|---|---|']
            for s in items:rows.append(f"| {s['original']} | {s['label']} | {s['main'] or '—'} | {s['reference'] or '—'} | {s['action']}: {s['reason']} |")
            rows.append('')
        (HERE/'SLIDE-MAP.md').write_text('\n'.join(rows)+'\n')
