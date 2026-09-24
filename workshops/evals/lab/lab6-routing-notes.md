# Lab 6 notes · route by the numbers

A one-page summary of talk 07, *Measuring What Works* (`measuring-what-works.html`),
part 02, slides 19–30. Checked September 2026; the open-model field moves
monthly, so re-check before relying on any figure.

**No model wins on everything (slides 19–20).** Models trade off cost,
intelligence and taste. Cheap, fast models suit bulk mechanical work; smarter
models suit hard problems you will not supervise; the highest-taste models earn
their price where UI or copy quality is the bottleneck. The deck's placement is
illustrative: your eval numbers decide where real models sit. Lab 6 measures one
axis of that, cost per accepted task, on three tasks.

**Cursor as a harness (slide 21).** An IDE harness that routes for you. Auto
picks a model per request; on Teams and Enterprise plans the relaunched version
is Cursor Router, with Cost, Balance and Intelligence modes. Auto bills at the
routed model's list price.

**OpenRouter (slide 22).** One key and one bill over 400+ models (its public
list returned 457 entries, variants included, in September 2026). Per-token
prices pass through with no markup; card top-ups carry a 5.5 % fee, $0.80
minimum. One model is often served by several hosts and fallback is on by
default, so a request can land on a provider you did not expect. Pin or
restrict hosts with `provider.only`.

**Pi (slide 23).** Mario Zechner's minimal terminal harness, now developed at
Earendil, MIT licence. System prompt plus tool definitions come to under 1,000
tokens. 15+ providers, local models via Ollama. Using Claude through Pi means an
API key or extra-usage billing; check Anthropic's current rules on subscriptions
and third-party tools first.

**Open-weight models (slides 24–29).** The gap is closing, and it is still a
gap. NIST's CAISI rated GLM-5.2 (June 2026, about 750B MoE, MIT) about level with
OpenAI's GPT-5.2 of December 2025, roughly six months behind; GLM-5.3 moved to a
custom licence, so read licences before standardising. Gemma 4 (Apache 2.0,
April 2026) runs on laptops: the 12B (June) fits 16 GB, `ollama run gemma4:12b`.
Qwen 3.6 ships a 27B dense model and a 35B-A3B MoE (about 23 GB at 4-bit, plan
for 32 GB); Qwen3.8-27B followed in August. Colibri runs GLM-5.2 without a GPU by
streaming experts from SSD: 0.05–0.1 tokens/s cold on a 25 GB box, about 1.8
warm on a 128 GB desktop. The point is that it runs at all.

**When local makes sense (slide 30).** Go local for control: private or
air-gapped code, marginal cost near zero, latency you can wait out. Stay hosted
for capability: frontier quality, fast turnaround, no hardware or operations.

## Local models with Claude Code (optional in lab 6)

Verified 2026-09-24. Ollama documents an Anthropic-compatible Messages API and a
Claude Code integration:

```sh
ollama pull qwen3-coder
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 \
  claude --model qwen3-coder
# or: ollama launch claude
```

Ollama recommends a context of 64k or more for larger repositories, and its API
does not support prompt caching or the token-counting endpoint. Claude Code's
gateway documentation says Anthropic "doesn't support routing Claude Code to
non-Claude models through any gateway", and that while a gateway credential
(`ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY` or `apiKeyHelper`) is active, the
claude.ai subscription is not used.

So: feasible, unsupported by Anthropic, and free of subscription usage. Claude
Code's `total_cost_usd` is computed from Anthropic list prices and means nothing
for a local model; the kit exports `cost_usd` 0.0 for variant `local`. Expect
slower runs and lower pass rates on a laptop. In the lab:

```sh
LOCAL_MODEL=qwen3-coder ./lab6.sh --local
```

## Sources

- Talk 07 deck, `measuring-what-works.html`: slides 19–30; sources slide 36
  (cursor.com, openrouter.ai FAQ, blog.google Gemma 4, nist.gov CAISI on GLM-5.2,
  github.com/JustVugg/colibri).
- Ollama: docs.ollama.com/api/anthropic-compatibility,
  docs.ollama.com/integrations/claude-code
- Claude Code: code.claude.com/docs/en/llm-gateway,
  code.claude.com/docs/en/llm-gateway-connect
