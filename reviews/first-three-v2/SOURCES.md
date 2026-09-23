# Source and claim review — first three decks v2

Reviewed 22 September 2026. This is the evidence record for the revised content, not a blanket certification of every product or of the preserved original decks.

## What changed in the claims

- Removed model leaderboards, exact subscription prices, market-share claims, product-churn anecdotes and model-specific routing defaults. They consumed talk time without helping the revised learning objectives.
- Removed universal context-percentage thresholds, unconditional statements about resending every token, and contradictory claims about retaining thinking tokens.
- Replaced guaranteed completion/correctness language with observable outputs and checks. A prompt is not an enforcement mechanism; a passing command is not complete acceptance evidence.
- Kept current product examples at the capability/category level. Features, plan access and administrator settings still vary.
- Historical experiments remain dated historical experiments. The co-scientist example no longer equates generating a hypothesis with replacing years of laboratory validation.

## Primary sources checked

| Revised material | Source | What it supports / boundary |
|---|---|---|
| Toolbox: general assistants | [Claude overview](https://claude.com/product/overview), [ChatGPT overview](https://chatgpt.com/overview/), [Gemini overview](https://gemini.google/overview/) | General assistant and document/data work examples. Does not establish parity across plans or vendors. |
| Toolbox: supplied documents and audio | [Gemini Notebook](https://notebook.google/), [Google: NotebookLM is now Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/), [Workspace Updates, 16 July 2026](https://workspaceupdates.googleblog.com/2026/07/notebooklm-now-gemini-notebook.html), [Generate Audio Overview in Gemini Notebook](https://support.google.com/gemininotebook/answer/16212820), [Google's Audio Overviews announcement](https://blog.google/innovation-and-ai/products/notebooklm-audio-overviews/) | Google renamed NotebookLM to Gemini Notebook on 16 July 2026. Checked 23 September 2026: notebooklm.google redirects to notebook.google, whose page title is "Gemini Notebook", and Google's help centre still documents Audio Overviews. |
| Toolbox: presentations/design | [Gamma](https://gamma.app/), [Canva AI](https://www.canva.com/canva-ai/) | Presentation/design creation as example categories. No ranking or guaranteed layout fidelity retained. |
| Toolbox: voice | [ElevenLabs text-to-speech](https://elevenlabs.io/text-to-speech) | Text-to-speech capability. No licensing or cloned-voice entitlement claims made. |
| Toolbox: app prototypes and automation | [Lovable](https://lovable.dev/), [Zapier](https://zapier.com/) | Prompt-driven app creation and connected workflow examples. No deployed automation or production security claim. |
| Toolbox: in-app assistance | [Microsoft 365 Copilot](https://www.microsoft.com/en-us/microsoft-365-copilot/business), [Gemini in Workspace](https://workspace.google.com/solutions/ai/) | Assistance alongside existing work apps; user must check actual licence and administrator controls. |
| Toolbox: shop experiment | [Project Vend, phase 1](https://www.anthropic.com/research/project-vend-1), [Project Vend: phase two](https://www.anthropic.com/research/project-vend-2) | June 2025 report: supplier research and stock changes, but below-cost sales and invented payment details. We do not claim literal bankruptcy or generalise to all agents. The 18 December 2025 phase two report (Claude Sonnet 4.0, then Sonnet 4.5, with new tools) says weeks with a negative profit margin were "largely eliminated", but the agent was "still vulnerable in lots of important ways" to manipulation by staff. |
| Toolbox: research experiment | [Google Research AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) | February 2025 hypothesis-generation system with researcher evaluation and experimental validation. No “ten years replaced in two days” claim. |
| Intro: loop and context | [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | Model/harness/tool loop and the information available to the session. Product architecture, not a universal wire-protocol specification. |
| Intro: permissions | [Claude Code permissions](https://code.claude.com/docs/en/permissions) | Permissions are configurable. The deck avoids claims about a universal default mode or a folder being a sandbox. |
| Intro: durable instructions and procedures | [Memory](https://code.claude.com/docs/en/memory), [Skills](https://code.claude.com/docs/en/skills) | Project instructions, persistent notes and task-specific procedures; exact loading is product-specific. |
| Intro: reasoning text | [Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think) | Reported reasoning is not a complete proof of the causes of a model's decision. No benchmark percentage retained. |
| Intro/engineering: context | [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Curating context, summaries and delegated investigation. No universal fill-percentage boundary or simplistic attention formula. |
| Intro/toolbox: external tools | [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | Standardised connection to tools/data. Authentication and authorisation remain distinct concerns. |
| Engineering: workflows and agents | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Distinction between predetermined workflow structure and agent-directed decisions; start simple and add complexity when needed. |
| Engineering: verification/evaluation | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Observable checks, realistic tasks, evidence and evaluating more than a final answer. The retry policy and worked contract are our proposed teaching designs. |

## Local evidence and illustrative material

- `examples/v2/review-data.csv` contains synthetic monthly values. The report calculates `(120 − 80) / 80 = 50%` and explicitly withholds a Q2 total because June is missing. The HTML artifact is authored for this talk; it does not establish a vendor's performance.
- `examples/v2/invoice/before/` reproduces the intended two failures. `after/` contains a reference fix plus CSV exporter and tests. `fixture-results.json` records the actual test runs. Slide output is abbreviated prepared fixture evidence, not an autonomous-agent transcript.
- `examples/v2/invoices.csv` is generated by the reference exporter. Round-trip tests cover commas, quotes, newlines, known totals and empty input. The fixture assumes validated rows and does not claim to be production billing software.
- The model-cost comparison is explicitly hypothetical. No vendor measurements are implied.
- The loop and subagent videos are retained Remotion assets. Their production source is `remotion/src/`; static posters are new SVG diagrams. No new video was represented as a vendor-generated result. Commit `9c96fc4` (23 July 2026), which added the agent-loop composition, is co-authored by Claude; that supports toolbox slide 14's claim that an agent wrote the code.

## Browser guidance

Used `frontend-slides` in enhancement mode and `modern-web-guidance`'s CSS guide. Preserved the existing fixed 1920×1080 deck-stage contract, scoped new styles to v2 slides, retained visible base states and added reduced-motion-aware video playback. Fonts use the existing local WOFF2 files. Browser QA is recorded separately in VALIDATION.md.
