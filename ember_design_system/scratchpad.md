# Deck: Subagents & Prompt Caching
Audience: developers + IT admins · 30 min · Direction C (Bold dev-tool)

## Visual system
- Light slide: bg #f4efe6, ink #16130e, muted #5c5446, faint #a39684, accent #ff5c35
- Dark slide:  bg #16130e, text #f4efe6, muted #8a7f6d, lines #2c281f/#3a342a, accent #ff5c35
- Section headers: DARK, big number, coral accent. All section headers parallel.
- Fonts: Space Grotesk (headings/display 600-700), IBM Plex Sans (body 400-500), IBM Plex Mono (eyebrows/labels/code)
- Type @1920: eyebrow 22 mono · title 72 · subtitle 40 · body 32 · small 26 · big-number 200
- Padding: x 110 · top 96 · bottom 84

## Rhythm
- Light body slides; dark for section headers + a few hero diagram/quote slides for contrast.
- Max 1-2 bg colors → using the light/dark pair only.

## Title sequence (the ToC)
01  Subagents & Prompt Caching            [title, dark]
02  What We'll Cover                       [agenda, light]
03  01 · Subagents                         [section, dark]
04  The Core Mental Model                  [light]
05  Context Isolation — Why It Matters     [dark hero diagram: with/without]
06  How Context Travels: Four Crossings    [light]
07  The Spawn: A Self-Contained Task       [light, failure-mode callout]
08  The Return: Many Turns, One Block      [light]
09  Parallel Fan-Out                       [dark hero diagram]
10  The Integration Constraint             [light]
11  Token Economics                        [light, tradeoff]
12  When to Reach for a Subagent           [light, two-col yes/no]
13  In Code: Just Another Call             [dark, trimmed snippet + callouts]
14  02 · Prompt Caching                    [section, dark]
15  The Core Idea: Reuse the Prefix        [light, cold vs warm]
16  What Actually Gets Cached              [light]
17  The Exact-Match Requirement            [dark hero diagram: divergence]
18  Ordering: Stable Front, Volatile Back  [light]
19  The Cache Lookup Path                  [light flow diagram]
20  The Pricing Model                      [light, three rates]
21  Where Caching Pays Off                 [dark, break-even curve]
22  TTL & Eviction                         [light]
23  Multiple Breakpoints                   [light, nested segments]
24  In Code: Marking the Breakpoint        [dark, trimmed snippet + usage callout]
25  Where They Reinforce                   [light, shared prefix across fan-out]
26  03 · Running It Under a Subscription   [section, dark]
27  OAuth & Subscriptions: Allowed vs Not  [light, decision table]
28  What to Do Instead                     [light, two paths]
29  Key Takeaways                          [dark]
30  Close                                  [dark]

## Copy rules
- Trimmed code snippets, callout the key lines (cache_control placement; resp.content[0].text crossing back)
- Diagrams redrawn polished (not ASCII)
- Compliance = clean allowed/not-allowed decision table
- No emoji, no AI-ism punchline titles
