# Deck 09 — AI Graph Engineering — fact sheet

Research pass: 9 August 2026 (four parallel web sweeps + Claude Code docs pass).
Companion to the user's own research note `graph-engineering-ai-llms.md` (7 Aug 2026).
Every claim below carries its source. Items marked ⚠ are single-source or vendor-sourced — verify or caveat on stage.

## The buzzword

- Peter Steinberger (@steipete), **July 18, 2026**: "Are we still talking loops or did we shift to graphs yet?" — 2.9M views. Within 48h: three competing definitions, copycat posts, and a **fabricated study citing a non-existent $3.1M Stanford grant**. (digg.com/tech/7ifyvmb9, theaioperator.io/p/what-is-graph-engineering-a-field)
- Community lineage: prompt engineering (2023) → context engineering (mid-2025) → loop engineering (June 2026) → graph engineering (July 2026).
- LangChain's rebuttal, "3 Years of Graph Engineering with LangGraph" (Runkle & Chase, **July 22, 2026**): "loops are just simple graphs"; production agents need cycles, not DAGs; 65M+ monthly downloads. (langchain.com/blog/3-years-of-graph-engineering-with-langgraph)
- Four distinct meanings of "graph" (user's note, confirmed by research): knowledge graph (what the system knows) · retrieval graph / GraphRAG (how it finds evidence) · workflow graph (what the app does) · GNN (learned model on graph data — research-stage outside Kumo's relational-prediction niche; skip for this talk).

## GraphRAG mechanics

- Microsoft GraphRAG (arXiv:2404.16130, Edge et al.): chunk → LLM entity/relation extraction → hierarchical **Leiden** community detection → LLM community summaries. Query modes: **local** (entity neighborhood), **global** (map-reduce over community summaries), **DRIFT** (global entry + local refinement). (microsoft.github.io/graphrag)
- Extraction cost driver: ~4–6 LLM calls per source chunk → indexing 20–100× more expensive than embedding-only.
- Microsoft's own estimate: graph extraction ≈ **75% of standard indexing cost** (microsoft.github.io/graphrag/index/methods/ — cited in user's note).
- ⚠ Cost-collapse story: ~5GB corpus cost **$33,000 to index in early 2024 → ~$33 by mid-2025** (~1000×). Single source: medium.com/graph-praxis "The GraphRAG Cost Cliff" (Mar 2026). LazyGraphRAG numbers below are Microsoft-official.
- **LazyGraphRAG** (Microsoft Research blog): defers all LLM summarization to query time; index-time uses noun-phrase extraction + co-occurrence stats. Indexing cost = **0.1% of full GraphRAG** (≈ vector-RAG cost); at mid budget outperforms Global Search at **4% of its query cost**; comparable quality at 700× lower query cost at low budget. (microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)
- Extraction quality: audit found **2.4% anomalous triples** of 6,014 (0.65% pure hallucination). Structural risk: downstream LLMs **trust graph output over source prose** even when the graph contradicts the text.
- Schema-free vs ontology: converged 2025/26 pattern — start schema-free to explore, fold discoveries into a canonical ontology once "precision" is defined for the domain.

## Honest benchmarks (graphs-as-knowledge)

Primary source: "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (arXiv:2502.11371); GraphRAG-Bench (ICLR 2026).
- Simple fact retrieval: **tie** (60.9 chunk vs 60.1 graph, GraphRAG-Bench).
- Complex reasoning: graph wins **53.4 vs 42.9**; contextual summarization: **64.4 vs 51.3**.
- Multi-hop Recall@5 avg **73.4% → 87.8%** (MuSiQue/HotpotQA/2Wiki); temporal queries **49–59% vs 30.7%** (MultiHop-RAG) — biggest documented graph advantage.
- **Null-query collapse**: on questions with no answer in corpus, plain RAG correctly abstains **96%**; Community-GraphRAG Global scores **19.27%** — it hallucinates an answer ~4 times out of 5.
- Latency: KG-GraphRAG retrieval ~**8× slower** than plain RAG (14,434s vs 1,724s, MultiHop-RAG); construction 5,560–7,702s vs 135s.
- Graphs help up to ~**2 hops**; increasingly fail at 3–4 hops (paths not captured in retrieved subgraph).
- ⚠ ICLR 2026 lead (arXiv:2506.05690): "GraphRAG frequently underperforms vanilla RAG on many real-world tasks" — read before quoting.
- Text-to-Cypher: best model **61.58%** execution accuracy on CypherBench (Claude 3.5 Sonnet); GPT-4o 60.18%; sub-10B <20%. (arXiv:2412.18702) → use Cypher **templates** (LlamaIndex CypherTemplateRetriever pattern), not free-form generation.

## Memory graphs

- Zep/Graphiti (arXiv:2501.13956): **bi-temporal edges** — four timestamps (t_created/t_expired system-time; t_valid/t_invalid event-time). Contradicted facts get their validity window **closed, not deleted** → "what's true now" and "what was true in March" from the same graph.
- Benchmark theatre timeline (all documented):
  - Apr 2025: Mem0 paper claims SOTA over Zep on LoCoMo.
  - May 2025: Zep rebuttal "Lies, Damn Lies, & Statistics" claims 84% — then is caught in an arithmetic error (Cat-5 in numerator, not denominator), corrects to 75.14%. (blog.getzep.com, github.com/getzep/zep-papers/issues/5)
  - Mem0 re-runs Zep's fixed pipeline: 58.44% — *below* Mem0. (blog.continua.ai/p/the-locomo-fair-fight)
  - **Aug 2025, Letta**: GPT-4o-mini + plain filesystem tools (grep/open/search) scores **74.0%** on LoCoMo — beating both specialized memory systems.
  - 2026 audits: **6.4% of LoCoMo's answer key is wrong** (99/1,540, Penfield Labs); LLM judge accepts 62.8% of intentionally-wrong answers; ⚠ MemPalace "100% on LoCoMo" → 5,400 GitHub stars in 24h → caught tuning on dev set within 48h → retracted (essays.bloo-mind.ai/posts/2026-05-20-mem-eval/).
  - Tsinghua MemoryBench (20k cases): "none of the advanced memory systems consistently outperform RAG baselines using full task context."

## Workflow graphs (control flow)

- LangGraph model: StateGraph — nodes (work), conditional edges (router functions), shared typed state + reducers, checkpointing at every super-step (pause/resume/HITL via interrupt()), Send API for map-reduce fan-out, time-travel via get_state_history + fork.
- 1.0 GA Oct 22, 2025. ⚠ Adoption (vendor): ~400 companies on LangGraph Platform incl. Klarna, Uber, LinkedIn, Replit.
- The debate, in three quotes:
  - "Loops are just simple graphs." — LangChain, Jul 2026.
  - "Graph-based systems become debugging nightmares in production." — CrewAI, "Lessons from 2 Billion Agentic Workflows" (DocuSign switched off a graph framework: **14× less code**, 75% faster lead-time). (blog.crewai.com)
  - "Find the simplest solution possible, and only increase complexity when needed." — Anthropic, "Building Effective Agents" (Dec 2024).
- Convergent decision rule (HackerNoon/Backbase framing): **control, repeatability, or compliance → deterministic workflow/graph; ill-defined problem where the path doesn't matter → autonomous loop.**
- Anthropic multi-agent research system: orchestrator + 3–5 parallel subagents beat single-agent Opus 4 by **90.2%** on internal eval at **~15× token cost**.
- ⚠ Production numbers (all vendor blogs): Klarna 80% resolution-time cut; Uber ~21k dev-hours saved; LinkedIn recruiter agent + SQL bot.
- Per-hop math: at 85% per-hop accuracy, a 5-hop chain ≈ **0.85⁵ ≈ 44%** end-to-end.
- "A graph of weak nodes is just slop produced in parallel." — aibuilderclub.com/blog/graph-engineering-with-claude-code.

## Production receipt (verified, peer-reviewed)

- **LinkedIn customer-service KG-RAG** (SIGIR 2024, arXiv:2404.17723): intra-ticket trees + inter-ticket graph, Neo4j + Qdrant/E5, GPT-4. Six months in production: **median resolution time −28.6%; mean 40h → 15h; p90 87h → 47h**; retrieval MRR 0.522 → 0.927.

## Implementing in Claude Code

### Graph DBs via MCP
- Neo4j official MCP (github.com/neo4j/mcp): 3 tools — `get-schema`, `read-cypher`, `write-cypher`. Registration (May 2026 walkthrough, gaetanopiazzolla.github.io):
  `claude mcp add --transport stdio -e NEO4J_URI=bolt://127.0.0.1:7687 -e NEO4J_USERNAME=neo4j -e NEO4J_PASSWORD=… -e NEO4J_READ_ONLY=true -- neo4j-mcp neo4j-mcp`
- Separate **Neo4j Data Modeling MCP**: validates LLM-proposed models, renders Mermaid schema diagrams. (medium.com/neo4j/explore-the-neo4j-data-modeling-mcp-server)
- Memgraph MCP: `run_query` + `get_schema`. FalkorDB MCP: `@falkordb/mcpserver`, HTTP :3000, read-only mode.
- **Kuzu archived Oct 10, 2025** — repo frozen at v1.4.1; community forks Bighorn (Kineviz) + Ladybug within days. Vendor-risk lesson. (theregister.com/software/2025/10/14/kuzudb-graph-database-abandoned-community-mulls-options)
- GraphRAG building: realistic pattern = Claude Code **drives** `neo4j-graphrag-python` (pipeline incl. entity-resolution stage) or LightRAG — not running microsoft/graphrag directly.
- Entity resolution, not extraction, is the production bottleneck (recurring practitioner finding).

### Memory spectrum (cheap → heavy)
1. **CLAUDE.md** — static, cache-friendly, paid every turn.
2. **Auto memory** — `~/.claude/projects/<project>/memory/`, MEMORY.md index loaded (first 200 lines / 25KB), topic files on demand.
3. **Official memory MCP** (`@modelcontextprotocol/server-memory`): entities/relations/observations in a **JSONL file**; 8 tools; string search only, no time, no semantic search.
4. **Graphiti MCP** (Zep): temporal edges, `search_memory_facts` with time filters; FalkorDB (default) or Neo4j backend; HTTP at :8000/mcp/.
5. **Cognee plugin**: `claude plugin install cognee-memory@cognee`; exposes 3 verbs (remember/recall/forget) + **5 lifecycle hooks** (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) that build the graph automatically while you work; auto-distill every 150 tool calls / 60s idle; per-client dataset isolation. ⚠ Cognee's extraction/embedding LLM calls bill against its own configured provider — separate from the Claude plan. (docs.cognee.ai/integrations/claude-code)
- MCP token tax: tool schemas historically loaded every turn; **deferred tool loading** (Claude Code v2.1.220+, default) withholds schemas until needed; `alwaysLoad: true` opts out.

### Code graphs
- House philosophy — Boris Cherny: "Early versions of Claude Code used RAG + a local vector db, but we found pretty quickly that agentic search generally works better. It is also simpler and doesn't have the same issues around security, privacy, staleness, and reliability." (x.com/bcherny; elaborated: "it outperformed everything. By a lot.") Formalized in Anthropic "Effective context engineering for AI agents" (Sept 29, 2025) — just-in-time context via glob/grep.
- ⚠ Counter-evidence (single-author but unusually honest benchmarks, dev.to code-review-graph writeup): tree-sitter+SQLite code-graph MCP → avg **8.2× token reduction** across 6 repos; **Next.js monorepo 739,352 → 15,049 tokens (49×)**; FastAPI 3.7×; **Express.js <1× (graph overhead lost to plain reading)**. One-endpoint FastAPI change: ~800 tokens expected, 5,500 actual without graph (6.9× overspend). Break-even guidance: ~500+ files or >$20/mo spend.
- Rigorous head-to-head (Codebase-Memory, arXiv:2603.27277): graph agent ~**1,000 vs ~10,000 tokens/query (10×)**, 2.3 vs 4.8 tool calls, <1ms vs 10–30s — but quality **83% vs 92%** (graph slightly worse on holistic comprehension). Indexes Django (49K nodes) in 6s; Linux kernel in 3 min.
- Industry hybrids: Sourcegraph (SCIP graph + embeddings + text), Cursor (semantic+lexical lifts agent evals up to **23.5%** over grep alone — cursor.com/blog/semsearch), GitHub semantic indexing GA Mar 2025. Aider repo map = tree-sitter + **PageRank** over def/ref graph (aider.chat/2023/10/22/repomap.html).

### Control flow with native primitives
- Mapping (aibuilderclub framing + docs): **subagents = nodes** (`.claude/agents/*.md`: name/description/model/tools frontmatter), **hooks = gates** (PreToolUse can block/modify; Stop can refuse turn end; 12 events), **orchestrator routing = conditional edges**, **`claude -p` = composable DAG nodes** (json/stream-json output; `--resume <id>`), **checkpointing = sessions + /rewind** (file snapshots per prompt, last 100; session JSONL; SDK `forkSession: true` = branch = time travel).
- **Workflows** (v2.1.154+; "ultracode"): JS orchestration script — `agent()` spawns a subagent, `pipeline(items, stages…)` fans out (no barrier), `parallel()` with barrier; max 16 concurrent; resumable — unchanged prefix of agent() calls returns cached results. This is the closest native thing to a scripted LangGraph.
- Claude Agent SDK has **no graph engine by design**; 2026 consensus hybrid: LangGraph as outer state machine, SDK agents inside nodes.
- Cheaper-first alternative: API **memory tool** (GA, client-side file ops) + **context editing** — Anthropic 100-turn benchmark: **84% token savings, 39% performance improvement** combined. Managed Agents memory (public beta Apr 2026) adds audit trails + rollback; ⚠ Rakuten 97% error-rate reduction (vendor claim).

## Agentic-retrieval counter-trend (closing)

- Amazon, AAAI 2026: "Keyword search is all you need" — agentic keyword search hits **94.5% of RAG faithfulness with zero vector store**. (amazon.science, arXiv:2602.23368)
- Net framing: graphs are becoming **one tool among several** (grep, SQL, vectors) that an agent picks per query — not the retrieval backbone. Durable niches: multi-hop relationship reasoning, temporal/audit requirements, entity-centric domains (fraud, dependencies, org structures, support).

## Worked example (from user's note, `graph-engineering-ai-llms.md`)

Bank IT incident copilot — "what caused the card-payment outage, what's affected, what next?"
- Knowledge graph: Service/Database/Deployment/Incident/Runbook nodes; DEPENDS_ON / DEPLOYED_TO / AFFECTS / OWNED_BY / APPLIES_TO typed edges; provenance + time validity; entity resolution (payments-prod = PAY-SVC = CMDB id).
- Retrieval: embed question → entry entities → bounded typed traversal (Incident→AFFECTS→Service→DEPENDS_ON→Database…) + vector search for similar past incidents; deterministic access-control + depth/size caps.
- Workflow: identify → traverse ∥ similar-incidents → join/rank → provenance/access check (loop if insufficient) → draft → **human approval gate** → publish.
- LLM does extraction/interpretation/drafting; deterministic code owns access control, traversal, thresholds, stop rules. Evaluate layers separately "so a fluent answer cannot hide a bad graph."
