# Review: decks 01 & 02 — accuracy and currency

**Decks reviewed:** `ai-toolbox.html` (*The AI Toolbox*, 59 slides) and `agentic-ai.html`
(*Intro to Agentic AI*, 43 slides).
**Decks dated:** July 2026. **Review date:** 21 September 2026.

## Verdict

Both decks are structurally sound and most core facts held up. The problem is drift:
the decks are a July 2026 snapshot and the market moved a lot in ten weeks. Every
"July 2026" label is now stale, and roughly a third of the product/model claims need
a touch. A handful of claims were already wrong in July.

| | Deck 01 · AI Toolbox | Deck 02 · Intro to Agentic AI |
|---|---|---|
| Must fix (wrong today, or wrong in July) | 19 | 9 |
| Should update (drifted since July) | 14 | 6 |
| Nice to have (attribution, nuance) | 9 | 5 |
| Verified correct, no change | ~45 claims | ~25 claims |

**The biggest single changes since July 2026:**

- Anthropic: Claude **Fable 5.1** shipped 1 Sep (Fable 5 → legacy). **Cowork merged into
  the main Claude app** on 16 Sep (with new Claude Docs & Claude Slides). Claude in
  Chrome went **GA on all paid plans** 26 Aug. Claude Code's **`auto` permission mode
  became the default** on Pro/Max/Team on 14 Aug.
- OpenAI: **GPT‑6 Astra** shipped 3 Sep. **Agent mode was retired** (Aug) in favour of
  **ChatGPT Work** (9 Jul). **Custom GPTs are being retired** (announced 11 Sep, off
  11 Dec). **Atlas actually shut down** 9 Aug. **Images 2.5** replaced 2.0 (8 Sep).
  Pro $200 new sign‑ups paused 10 Sep. Sora API ends 24 Sep.
- Google: **Gemini 3.7 Flash** (13 Aug) and **3.8 Flash** (2 Sep) shipped; **3.5 Pro is
  still unreleased** after three missed targets. Gemini CLI was **replaced by
  Antigravity CLI** for consumers (18 Jun, so already stale in July).
- Stories: **IMO 2026** (July) produced the first **perfect 42/42 AI scores**, so the
  "5 of 6" gold is now a 2025 milestone. **UMG & Sony filed a fresh suit against Suno**
  on 18 Sep 2026.
- Harnesses: **Windsurf is now Devin Desktop**; **Aider is dormant** (last release Aug 2025).

## Method and caveats

- Five parallel research passes (~200 web searches) against primary sources
  (vendor docs and pricing pages, official blogs) and reputable press.
- The sandbox blocks direct fetches of anthropic.com, claude.com, openai.com,
  blog.google, most vendor pricing pages and most news sites, so several verdicts
  rest on search‑index snippets of those pages rather than a full read. These are
  marked **verify** below; do a 10‑minute browser pass on them before presenting.
- Slide references below use the **position of the `<section>` in the file** (§1 = title)
  plus the slide's `data-label`, because on‑slide numbers skip dividers.

---

## Cross‑cutting changes (both decks)

1. **Re‑stamp the date.** "July 2026" appears on the title of both decks and in ~20
   "Prices as of July 2026" footers in deck 01 and 4 in deck 02. After applying the
   fixes below, search/replace to **"September 2026"** (and README "verified as of
   July 2026" → September 2026). Speaker notes that say "this month" about the
   NotebookLM rename must become "in July".
2. **Model lineup table** (deck 01 §11, deck 02 §18) — identical table in both decks:
   - Anthropic: `Claude Fable 5.1 · Opus 5 · Sonnet 5 · Haiku 4.5` (Fable 5.1 shipped
     1 Sep 2026; Fable 5 is legacy; no Haiku 5 yet).
   - OpenAI: `GPT‑6 Astra (Sep 2026) · GPT‑5.6 Sol · Terra · Luna` (Astra shows as
     "GPT‑6 Pro" on Pro/Business/Enterprise; the 5.6 family remains as the tiered lineup).
   - Google: `Gemini 3.8 Flash · 3.5 Flash‑Lite (3.5 Pro still unreleased)`.
   - Add a one‑line footnote: *Fable = generally available Mythos‑class model with
     safety classifiers; Mythos itself is restricted (Project Glasswing). On Claude
     Pro, Fable is billed through usage credits.*
3. **Codex model**: "on GPT‑5.6" → "on GPT‑6 Astra (Sep 2026)" (deck 01 §13, §16;
   deck 02 §20).
4. **"Agent mode"** → **"ChatGPT Work"** everywhere (deck 01 §16, §18, §22, §35, §56, §57).
   Agent mode was removed in Aug 2026; Work launched 9 Jul 2026 and is included on
   all plans (Free/Go limited; usage shared with Codex).
5. **Sora**: keep as a churn example, but it is no longer just "gone" — app/web closed
   26 Apr 2026, API ends 24 Sep 2026. Remove Sora from any "same category" list
   (deck 02 §23).
6. **MCP server count**: "10,000+" / "thousands" → "10,000+ active servers (Dec 2025
   figure)" (deck 01 §48, deck 02 §39).
7. **Deep research plan inclusion** ("included from the ~$20 tiers"): free tiers do get
   a handful of runs (Gemini ~5/month, ChatGPT Free/Go "limited", Perplexity 5/day);
   Anthropic's feature is called **Research** and needs Pro+. Reword to "a few free
   runs on most free tiers; full access from ~$20" (deck 01 §24; touches §18 table).
8. **Speaker‑note leak**: deck 01 speaker notes say "the kcard" three times (§14, §24,
   §37). `kcard` is a CSS class name; presenter‑facing text should say "the callout".

---

## Deck 01 — `ai-toolbox.html` (*The AI Toolbox*)

### Must fix

| § | Slide | What's wrong | Change to |
|---|---|---|---|
| 11 | Today's models | Lineup stale (Fable 5, GPT‑5.6 flagship, Gemini 3.6 Flash). | See cross‑cutting #2. |
| 12 | The Claude family | Cowork is no longer a separate product tab; Claude in Chrome status; "free tier = chat only" imprecise. | Add "Since 16 Sep 2026 Cowork's capabilities live inside the main Claude app (plus Claude Docs & Claude Slides)". Claude in Chrome: "GA on all paid plans since 26 Aug 2026 (Chrome desktop; not on Free)". Footer: "free tier = chat, Projects, Artifacts — no Code, Cowork or Design". |
| 13 | Claude Code & Codex | Codex "on GPT‑5.6"; "full access from Plus". | "Codex on GPT‑6 Astra (Sep 2026) — CLI, IDE, cloud and inside the ChatGPT desktop app; included on every ChatGPT plan (Free/Go limited; Plus and up for real work)". Cite the 80% figure: *Anthropic Institute, "When AI builds itself", June 2026 — >80% of merged production code as of May 2026*. |
| 14 | Claude Cowork | Product merged into Claude; "runs on a schedule" implies local folder. | Add the 16 Sep merge line (as §12). Reword schedule: "scheduled tasks run in the cloud (not against a local folder)". Update the speaker note accordingly. |
| 15 | Claude Design | "research preview" is stale. | "Launched 17 Apr 2026 (Anthropic Labs); 1M+ users in week one. Now **beta on paid plans**, and since Sep 2026 works inside any Claude conversation and in Claude Code. Design‑system import rebuilt June 2026." |
| 16 | The ChatGPT family | Agent mode retired; Images 2.0 superseded; Custom GPTs being retired; ads footprint grew. | Tiles: **"ChatGPT Work** (Jul 2026, successor to agent mode) — multi‑step tasks → finished decks, sheets, docs, sites"; **"Images 2.5** (Sep 2026; 2.0 in Apr introduced native 2K + batch consistency)"; **"Custom GPTs — being retired** (announced 11 Sep 2026; stop 11 Dec) → Plugins / Workspace Agents". Warning tile: "Ads on Free & Go: US since Feb 2026, UK Jun, 31 European countries Aug 2026. Sora app closed Apr 2026. Pro $200 new sign‑ups paused since 10 Sep 2026." |
| 17 | The Gemini family | Workspace "no separate add‑on" is misleading; Veo/Flow line missing Omni; rename date vague. | Notebook: "renamed **16 July 2026**; same product plus code execution and Gemini‑app sync; free tier still gets Audio Overviews, but limits are compute‑based since 2 Sep 2026". Video: "Veo 3.1 + **Gemini Omni Flash** in Flow — 1,000 credits/mo on Pro ≈ 10 Veo Quality clips". Workspace: "core Gemini bundled in paid plans — full suite from Business Standard ~$14/user; Starter ($7) gets limited Gemini; higher AI limits via optional **AI Expanded Access** add‑on (Feb 2026)". Speaker note: "until this month called NotebookLM" → "renamed from NotebookLM in July". |
| 18 | The $20 question | "Agent mode", "Images 2.0" cells. | "ChatGPT Work"; "Images 2.5". |
| 20 | Products churn fast | Sora dates/figures imprecise; Atlas is past tense; 3.5 Pro delay longer; rename date. | Sora: "shutdown announced 24 Mar 2026; app closed 26 Apr; API ends 24 Sep 2026 — WSJ: ~$1M/day running cost vs ~$2.1M lifetime revenue (a Cantor Fitzgerald estimate put peak inference at up to $15M/day)". Atlas: "launched Oct 2025 — **shut down 9 Aug 2026**; folded into ChatGPT desktop browser mode". Gemini 3.5 Pro: "announced for June 2026 — **missed June, July and August targets**, still unreleased". NotebookLM: "16 Jul 2026". Tome: add "team pivoted to Lightfield (CRM)". Consider swapping one weaker row for a stronger 2026 example: agent mode retired (Aug), Custom GPTs retirement (Sep), Gemini CLI shut for consumers 18 Jun → Antigravity CLI, Windsurf → Devin Desktop (Jun). Rewrite the speaker note to past tense for Atlas. |
| 22 | A week of tasks | "(Cowork / agent mode)". | "(Claude / ChatGPT Work)". |
| 29 | AI video generation | **Already wrong in July:** Veo was not "the only one with synced dialogue" (Sora 2 Sep 2025, Kling 2.6 Dec 2025 / 3.0 Feb 2026, Runway Gen‑4.5 Mar 2026). Higgsfield tiers $15/$39/$99 match no 2026 price list; "15+ models" unverified. Luma entry price. | Veo: "among the first with native synced dialogue — Kling 3.0 and Runway Gen‑4.5 now do too". Higgsfield: "Basic $9 · Pro $29 · Max $79/mo (Sep 2026 — tiers renamed twice this year); dozens of third‑party models". Runway: top tier is now "Max" ($95). Luma: "Dream Machine Lite ~$10 · Luma Agents from $30". Fix the speaker note ("only one generating synchronised dialogue"). |
| 32 | ElevenLabs | Dubbing "29+ languages" was stale in July; Starter price; 1,000‑credit rule overstated. | "Dubbing into **90+ languages**". "Starter ~$5/mo (annual) / $6 monthly". Rule of thumb: "~1,000 credits ≈ 1 min of **speech**; dubbing costs 2–10k credits/min". Speaker note: "twenty‑nine‑plus" → "ninety‑plus". |
| 33 | Music & editing | Suno litigation status moved; Udio missed its target. | Suno: "Warner (Nov 2025), BMG (Aug 2026) and Believe (Sep 2026) now license; **UMG & Sony filed a fresh suit 18 Sep 2026** against Suno's licensed v6 models — legal check still mandatory". Udio: add "Q2 2026 launch target missed; downloads still disabled per latest reports". ElevenLabs Music: "opt‑in licensing deals with Merlin & Kobalt (50/50 royalty split)". |
| 35 | Presentations | **Beautiful.ai pricing wrong**: it has a $12/mo Pro tier; $40 is the Team seat. "ChatGPT's agent mode". | "Beautiful.ai — Pro $12/mo (annual, $45 month‑to‑month) · Team $40/user; no free tier (14‑day card‑required trial)". Soften the speaker note ("enterprise‑priced… hard to justify"). "Also in this race: Claude Design, **Claude Slides (Sep 2026)** and ChatGPT Work". Gamma: "paid ~$8–18/mo (Ultra $100)". Tome → "dead Apr 2025 → team pivoted to Lightfield". |
| 36 | Copy platforms | Jasper "$39–69" — no $39 tier on the 2026 list; Copy.ai has a $49 Starter. | Jasper: "Pro $69/mo ($59 annual) + Business custom". Copy.ai: "Starter $49; agents from ~$249". |
| 38 | Automation glue | Zapier "8,000+ apps" (now 9,000+); Make price band; "3–5× cheaper" unverified. | "Zapier — 9,000+ apps; Free 100 tasks · Professional ~$20 annual / $30 monthly". Make: "~$9–34/mo ('operations' are now 'credits'); cheaper per step — steeper curve" (drop the 3–5× unless you can source it). Lindy price: **verify**. |
| 44 | Story 3 · The exams | IMO story superseded; CFA citation imprecise. | Label the IMO tile **"IMO 2025"** and add: "**July 2026:** at IMO 2026 several AI systems scored a perfect 42/42 (two officially graded); three humans did too". Keep "~1 in 10" (72 of 630 = 11.4%). CFA: "best 79.1% (OpenAI o4‑mini, of 23 models tested by Goodfin/NYU Stern; CNBC, **Sep 2025**)"; attribute "~300 h per level" to CFA Institute. Speaker note: "The same summer" → "Summer 2025". |
| 52 | The ChatGPT side | OpenAI renamed connectors → apps → plugins; individual synced connectors shut off. | "**Plugins** (ex‑connectors/apps; Plugin Directory since Jul 2026) — Drive, Gmail, SharePoint, Slack… Enterprise‑grade ones need Business+. Individual‑user *synced* connectors were switched off 14 Aug 2026." Excel/Sheets add‑in: "ChatGPT for Excel / Google Sheets — GA on all plans May 2026". Apps: "third‑party plugins (Canva, Booking.com…) — **not available in EEA/UK/CH** on consumer plans". Region tile: spell out "EEA/UK: no third‑party plugins and no deep‑research connectors on consumer plans; Business/Enterprise admins can enable more". |
| 53 | The built‑ins | "The Office agents run on Anthropic's models" is overstated. | "Fun fact: parts of Copilot — Researcher, **Copilot Cowork** (built with Anthropic, GA Jul 2026) and optionally the Office agents — run on Claude; Microsoft is now multi‑model, OpenAI still default." Prices fine: "$21 (Business) / $30 (Enterprise) per user/mo". Workspace line: same nuance as §17. |
| 54 | The universal adapter | Zapier MCP counts and billing. | "~30,000 actions across **9,000+** apps"; add "each MCP call draws 2 tasks from your Zapier plan (since Jun 2026)". |
| 58 | Sources 1/2 | `learn.chatgpt.com/docs/pricing` — one research pass found it indexed, another found no trace; either way it is not OpenAI's canonical page. | Replace with `https://openai.com/chatgpt/pricing/` (or `chatgpt.com/pricing`). Add sources for GPT‑6 Astra and Claude Fable 5.1 (`platform.claude.com/docs/en/models/overview`). |

### Should update

| § | Slide | Change |
|---|---|---|
| 1 | Title | "July 2026" → "September 2026". |
| 4 | Reading a price tag | Footer date. |
| 19 | The plan ladder | ChatGPT Team row: "Business $20–25/seat (Standard) · **Premium seat $100–125** (Aug 2026)". Claude Team: "$20–25/seat (Standard) · Premium $100–125; min 2 seats". Add footnote "ChatGPT Pro $200 (20×) new sign‑ups paused since 10 Sep 2026". Google Ultra: "$99.99 / $199.99". |
| 24 | Deep research | See cross‑cutting #7. |
| 28 | Prompt‑to‑app | Lovable figures hold ($500M ARR, 9 Jun 2026). One tracker reports a pricing change in Aug 2026 — **verify** `lovable.dev/pricing` before presenting. |
| 30 | HyperFrames | "billed per minute by HeyGen" — no published per‑minute rate found. Say "optional managed cloud rendering from HeyGen (paid)". |
| 31 | AI avatars | Synthesia: add annual prices ($18 / $64). D‑ID "~$16/mo" — no such monthly tier found; likely Pro billed annually. Suggest "from ~$6/mo (Lite, watermarked, personal use); commercial from Pro (~$16/mo annual)" — **verify** on d‑id.com. |
| 34 | Images & design | Canva Pro "~$10–18/mo depending on billing/region". Ideogram "paid from ~$7–8" — legacy Basic may be closed to new subscribers, **verify**. Firefly: note indemnity excludes third‑party partner models. Magnific entry price "€6" doubtful — likely "Premium from ~€9/mo", **verify**. |
| 37 | Perplexity | Optionally add "Enterprise Max $325/seat". Prompt‑injection tile: optionally add "follow‑on exploits in ChatGPT Atlas (Oct 2025) and Comet calendar invites (2026)". |
| 40 | Cheat sheet | Decks entry price "free → ~$8/mo"; Automation "free → ~$20–30/mo"; otherwise fine. |
| 48 | MCP | "10,000+ active servers (Dec 2025 figure)". |
| 50 | Claude inside Office | All verified except "needs a work/school Microsoft 365 account" (support article blocked) — **verify**. Outlook still beta as of Sep 2026 ✅. |
| 51 | Files straight from chat | Attribute the ChatGPT side to "ChatGPT Work". |
| 56–57 | Three things / Summary | "agent mode" → "ChatGPT Work"; date stamp. |
| 59 | Sources 2/2 | Add: IMO 2026 coverage; Variety on the Sony/UMG v Suno suit (18 Sep 2026). |

### Nice to have

| § | Slide | Change |
|---|---|---|
| 14 | Claude Cowork | Speaker note: cite Boris Cherny (~10 days, code "pretty much all" by Claude Code). |
| 42 | Story 1 · Project Vend | "hallucinated inventory" is not a documented finding — the documented ones are hallucinating a Venmo account and claiming to be a human in a blue blazer. Dates: phase 1 spring 2025, phase 2 published Dec 2025. Net worth ~$1,000 → <$800 (so "−$200" is right). |
| 43 | Story 2 | Add "Feb 2025; later published in Cell (Sep 2025)". |
| 45 | Story 4 | Add "July 2025, CVE‑2025‑6965". |
| 46 | Story 5 | Coca‑Cola: two studios (Secret Level and Silverside); the 70k‑clip figure is Silverside's spot. Optionally credit agency Mother / director Jeff Low for the Anthropic ad and Similarweb for the +11%. |
| 48 | MCP | Adoption dates (OpenAI Mar, Google Apr, Microsoft May 2025) are widely reported but were not re‑fetched. |
| 17 | Gemini family | Speaker note: "Nearly every core feature works on the free tier" — still true, but limits are now compute‑based. |
| 8 | Glossary | "Token ≈ ¾ of a word" — true for OpenAI; current Claude tokenizer is ≈ 0.55 word/token. Consider "≈ ½–¾ of a word". |
| 27 | Landscape map | Leaders still hold; no change needed. |

### Verified correct — no change needed

Claude plan prices (Pro $20, Max $100/$200, Team $20–25) · Cowork GA 9 Apr 2026, built in ~10 days · Claude Design 1M+ users week one, exports · >80% of Anthropic production code by Claude · Claude for M365 feature list, Marketplace distribution, Outlook beta · ChatGPT Go $8 / Plus $20 / Pro $100 & $200 · Ads on Free & Go · Google AI Plus $4.99 / Pro $19.99 / Ultra $99.99 & $199.99 · Veo 3.1 Quality = 100 credits, 1,000 credits on Pro · `=AI()` in Sheets · Antigravity & Jules · Lovable $500M ARR & prices · v0, Bolt, Replit, Figma Make · Runway $15/$35/$95 · Kling ~$7, Pika ~$10 · HyperFrames Apache 2.0, skill install · Synthesia & HeyGen prices · Descript · Midjourney tiers & Stealth‑only‑on‑Pro · Firefly licensing · Freepik → Magnific 28 Apr 2026 · Tome dead 30 Apr 2025 · Writer, Notion AI · Perplexity Pro $20 / 20 deep research/day / Enterprise $40 / Comet free 2 Oct 2025 · Brave's Comet prompt‑injection disclosure (20 Aug 2025) · Zapier free tier & Professional price · Relay.app $19 · Project Vend arc · AI co‑scientist superbug story · Big Sleep SQLite · Anthropic espionage disclosure (Nov 2025, 80–90%) · Super Bowl ad, +11% DAU, top‑10 App Store · Coca‑Cola 70k clips / ~100 people · MCP Nov 2024 → AAIF Dec 2025 · M365 Copilot $21/$30 · admins can block add‑ins · ChatGPT for Excel/Sheets features · Codex approval modes (read‑only / auto / full access).

---

## Deck 02 — `agentic-ai.html` (*Intro to Agentic AI*)

### Must fix

| § | Slide | What's wrong | Change to |
|---|---|---|---|
| 18 | Today's models | Lineup stale. | See cross‑cutting #2. Speaker note: "Claude Fable 5" → "Fable 5.1". Stat tiles hold (96.0% SWE‑bench Verified; 30.2% ARC‑AGI‑3 — "3×" is conservative, the gap to GPT‑5.6 Sol at 7.8% is nearer 4×). |
| 20 | Today's harnesses | Codex model; Windsurf renamed; Aider dormant. | Codex: "on GPT‑6 Astra (Sep 2026) — terminal, IDE, cloud". "Windsurf" → "**Devin Desktop** (ex‑Windsurf, Cognition, Jun 2026)". "Aider" → replace with "**OpenCode** — open‑source terminal agent" (Aider's last release was Aug 2025). Consider adding a "…and many more" tile: Kiro (AWS), Amp, Jules (Google), GitHub Copilot coding agent / CLI. |
| 21 | Front doors | "Gemini CLI" no longer serves consumer/Pro/Ultra users; "Claude Code app"; Windsurf; Aider. | Terminal: "Claude Code · Codex · **Antigravity CLI** (replaced Gemini CLI for consumers, Jun 2026) · OpenCode". Desktop: "**Claude Desktop app** (Claude Code Desktop) · Codex inside the ChatGPT desktop app". IDE: "…· **Devin Desktop** · Antigravity · Copilot". |
| 23 | Higgsfield | "Same category: Sora, Veo, Runway" — Sora app closed Apr 2026, API ends 24 Sep 2026. | "Same category: Veo, Kling, Runway". |
| 27 | Smarter can be cheaper | "~1⁄7 thinking — Opus 5 hit its best score with a seventh of its predecessor's thinking" is a **customer quote from a trading benchmark** (vs Opus 4.8), not an Anthropic headline benchmark. | Either rephrase the tile: "~1⁄7 thinking — on one customer's trading benchmark Opus 5 beat Opus 4.8 on a seventh of the reasoning tokens", or replace it. Sonnet 5 tile: name it — "matches Opus 4.8 on **BrowseComp** (web research) at ~⅓ the tokens". Fix the same line in the speaker note. Footnote: Fable 5.1 is 10× Haiku per token; Opus 5 is 5×. |
| 28 | What context is | "1M ≈ 2,500 pages" assumes 750k words/1M tokens; the current Claude tokenizer (since Opus 4.7) yields ≈ 555k words per 1M. | "1M tokens ≈ 550–750k words ≈ **1,800–2,500 pages**, depending on tokenizer". Speaker note: "roughly two and a half thousand pages" → "roughly two thousand pages". |
| 29 | Context rot | "40% threshold of stupidity" — no source uses this phrase; the idea is Dex Horthy's (HumanLayer) **"dumb zone"**, and deck 03 already uses that name. | Rename the on‑slide label and body to "the 40% **'dumb zone'** (Dex Horthy, HumanLayer)" and keep the caveat: a practitioner heuristic backed by gradual‑degradation studies, not a hard threshold. Add the talk to Sources 2/2. |
| 33 | Permissions | **Mode names are wrong.** The slide equates "Auto" with "accept edits". In Claude Code, `auto` is a separate, classifier‑reviewed mode and has been the **default on Pro/Max/Team since 14 Aug 2026**. Documented modes: `default` (UI: "Manual"), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. | Rewrite the three tiles as a five‑step ladder or keep three and label them correctly: **Manual** (asks before every action) · **Accept edits** (file edits pre‑approved, commands still ask) · **Auto** (a classifier approves routine actions, blocks risky ones — the default on paid plans since Aug 2026) · **Bypass / "YOLO"** (asks for nothing — sandbox only). Update the LIVE callout to match whichever mode the demo actually runs in. Codex names (read‑only / auto / full access) are correct. README's "auto / accept‑edits" wording should be adjusted to match. |
| 37 | Skills & plugins | "Plugins bundle skills, **commands** and MCP servers" — the `commands/` directory is legacy; docs say use skills. | "Plugins bundle skills, subagents, hooks and MCP servers for a team" (diagram label too). |
| 42 | Sources 1/2 | Sources predate Astra and Fable 5.1. | Add GPT‑6 Astra announcement and Fable 5.1 what's‑new (`platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1`). The Gemini 3.5 blog link is fine as a "still unreleased Pro" pointer but consider the 3.8 Flash post. |

### Should update

| § | Slide | Change |
|---|---|---|
| 1 | Title | "Internal talk · July 2026" → "September 2026". |
| 7 | Glossary | "Token ≈ ¾ of a word (un·believ·able = 3)" → "≈ ½–¾ of a word depending on the model (OpenAI ≈ ¾, current Claude ≈ ½)". |
| 14 | Thinking | "Newer Claude models decide adaptively" ✅ — strengthen: "Claude 5‑series models think adaptively by default; you steer with an effort dial (low → max). Haiku 4.5 still uses a fixed thinking budget." |
| 25 | Subscriptions | Both columns verified (ChatGPT really does sell Pro 5× $100 and Pro 20× $200). Add footnote: "ChatGPT Pro 20× new sign‑ups paused since 10 Sep 2026." Claude Free now includes Sonnet 5 chat but not Claude Code. |
| 36 | CLAUDE.md & memory | "some harnesses do this automatically" → state it: "Claude Code does this automatically — **auto memory** (on by default) writes notes to a per‑project memory folder with a `MEMORY.md` index loaded every session; toggle with `/memory`." |
| 39 | MCP | "Thousands now exist" → "10,000+ active servers (Dec 2025)". Add "governed since Dec 2025 by the Linux Foundation's Agentic AI Foundation" for consistency with deck 01. |

### Nice to have

| § | Slide | Change |
|---|---|---|
| 10 | Model in the cloud | "Claude Opus 5" in the diagram is fine; if the live demo runs Fable 5.1, match it. |
| 15 | Thinking in the loop | Specify the model: "Claude 3.7 Sonnet mentioned the hint 25% of the time; DeepSeek R1 39%". |
| 19 | Which tier when | Add a fourth line or footnote for the frontier tier (Fable: 10× Haiku per token; reserved for the hardest work). |
| 30 | Keep it lean | Status‑line example is fine; if you re‑stamp, consider `claude-fable-5-1` or keep `claude-opus-5`. |
| 43 | Sources 2/2 | Add Dex Horthy's "Context Engineering for Complex Codebases" (AI Engineer 2025) if you adopt the "dumb zone" naming. Consider `https://arxiv.org/abs/2505.05410` as the paper link for CoT faithfulness. |

### Verified correct — no change needed

Hook & loop worked example · three building blocks · no‑memory framing · what one turn sends · thinking as scratchpad, billed as output · CoT faithfulness ~25% · Opus 5 96% SWE‑bench Verified, 30% ARC‑AGI‑3 · Opus 4.5 −76% tokens vs Sonnet 4.5 · Opus = 5× Haiku per token · 1M context on Fable/Opus/Sonnet, 200K on Haiku 4.5 · Claude/ChatGPT subscription tiers · subscription vs API · Chroma context‑rot (18 models) · Lost in the Middle (Liu et al.; Stanford lead) · caching & compaction · sub‑agents · bypass‑mode guidance & prompt‑injection warning · CLAUDE.md · skills load on demand (SKILL.md) · MCP Nov 2024 · all `code.claude.com` and `platform.claude.com` source URLs resolve (models overview now redirects to `/docs/en/models/overview`).

---

## README and landing page

- `README.md`: "Facts … verified as of July 2026" → September 2026; deck 01 bullet
  "Pricing … (July 2026 snapshot)"; "agent mode" in the *What's covered* paragraph →
  "ChatGPT Work"; live‑demo note "start Claude Code … in auto / accept‑edits mode" →
  "in Auto mode (the default on paid plans) or Accept‑edits".
- `index.html`: deck 01/02 copy is generic and needs no change.

## Items to spot‑check in a browser (blocked from the sandbox)

1. `claude.com/claude-for-microsoft-365` and the support article — does the add‑in
   still require a work/school Microsoft 365 account? (deck 01 §50)
2. `lovable.dev/pricing` — reported Aug 2026 pricing change. (§28)
3. `d-id.com/pricing` — current entry and commercial tiers. (§31)
4. `ideogram.ai/pricing` and `magnific.com` — entry tiers. (§34)
5. Suno Pro price (~$10) and Lindy paid price. (§33, §38)
6. Whether Udio's licensed platform has launched since July. (§33)
7. `learn.chatgpt.com/docs/pricing` — conflicting evidence on whether it exists; use
   the canonical OpenAI pricing URL regardless. (§58)
8. `hyperframes.video/pricing` — any published per‑minute cloud rate. (§30)

## Key sources consulted

- Anthropic: `platform.claude.com/docs/en/models/overview`; Fable 5.1 what's‑new;
  `code.claude.com/docs/en/permission-modes`, `/memory`, `/plugins`, `/chrome`,
  `/whats-new/2026-w32`; `claude.com/blog/cowork-is-now-claude`; Anthropic Institute
  "When AI builds itself" (Jun 2026); Opus 5 / Sonnet 5 announcements.
- OpenAI: `openai.com/index/gpt-5-6/`; CNBC 3 Sep 2026 (GPT‑6 Astra); help‑center
  articles on Pro tiers, Sora discontinuation, Atlas, ChatGPT agent, ChatGPT Work,
  Custom GPT retirement, ChatGPT for Excel/Sheets; Images 2.0 / 2.5 posts.
- Google: blog.google posts on Gemini 3.6/3.7/3.8 Flash and Gemini Notebook rename;
  9to5Google on 3.5 Pro delays and AI plan prices; developers.googleblog.com on
  Gemini CLI → Antigravity CLI; Workspace Updates blog (AI Expanded Access, `=AI()`).
- Microsoft: M365 blog (model choice Sep 2025; Copilot Cowork Mar 2026); pricing pages.
- Stories: deepmind.google IMO 2025 post; imo‑official.org 2025 results; IMO 2026
  coverage (TechXplore, SCMP); CNBC 24 Sep 2025 (CFA); Google Research / Imperial
  (co‑scientist); The Hacker News (Big Sleep, CVE‑2025‑6965); CNBC 13 Feb 2026 and
  TechCrunch (Super Bowl); Hollywood Reporter / TheWrap (Coca‑Cola).
- Tools: vendor pricing pages where reachable plus 2026 price trackers; TechCrunch
  9 Jun 2026 (Lovable); Variety 18 Sep 2026 (Sony/UMG v Suno); Brave blog
  (Comet prompt injection); `zapier.com/mcp`; Chroma context‑rot repo;
  arXiv 2307.03172; Dex Horthy, AI Engineer 2025.
