# State — ai-learning

Rolling state for the ai-learning routine. Read on start, rewritten before exit.

## Last run
2026-09-14T00:00:00Z — weekly run, window 2026-09-07 → 2026-09-14. **Data gap: all raw stores still stale (newest data Aug 19–20); 4th consecutive missed digest from the Mac daily pull. Content sourced via WebSearch last resort: 1 confirmed in-window X post (bcherny Sep 11) + 3 simonw blog posts (Sep 8, 11, 12). Dominant story: OpenAI Navier-Stokes claim (Sep 8).**

## Covered posts (dedupe list — prune entries older than ~60 days)

### Featured in `log/2026-09-14.md`:

**bcherny:**
- 2098217573276131577 — Production vs. prototype code quality bar: production Claude code needs higher bar + lint/tests/fuzzers/auto-review (Sep 11)

**simonw:**
- simonwillison.net/2026/Sep/8/on-navier-stokes/ — OpenAI Navier-Stokes claim, 10,000 agents, $40M, Anthropic credit controversy (Sep 8, blog post)
- simonwillison.net/2026/Sep/11/boris-cherny/ — amplification of bcherny Sep 11 post (Sep 11, blog post)
- simonwillison.net/2026/Sep/12/astra-running-routes/ — GPT-6 Astra running routes 27-min agent run (Sep 12, blog post)

### Featured in `log/2026-09-07.md`:
_(No posts — full data gap. Mac daily pull did not cover Aug 20 – Sep 7.)_

### Featured in `log/2026-08-31.md`:
_(No posts — full data gap. Mac daily pull did not cover Aug 20–31.)_

### Featured in `log/2026-08-24.md`:

**bcherny:**
- 2089756371570900999 — Cowork now on mobile and web for all paid plans (Aug 18, repost claudeai)
- 2089842387845804246 — Claude designed protein binders 14/15 targets (Aug 18, repost AnthropicAI)
- 2089924199804711410 — Claude Code Desktop startup latency under active improvement (Aug 19)

**_catwu:**
- 2089470636796059754 — /design command early preview in Claude Code (Aug 17, repost nateparrott)

**emollick:**
- 2089488934082363397 — AI creative variance problem (Aug 17)
- 2089351996016918825 — AI-generated analyses need multiverse-style reporting (Aug 17)
- 2089819700033102273 — OpenAI 20% compute on CoT monitoring = alignment concern signal (Aug 18)

**swyx:**
- 2089518027956158716 — Kill My SaaS: 69 unique submissions (Aug 18, repost)
- 2089726272448422040 — Context engineering workshop: 90% token cost cut via caching (Aug 18, repost)

**rasbt:**
- 2089527404138033497 — Watermarking detection clarification (Aug 18)

### Featured in `log/2026-08-17.md`:

**bcherny:**
- 2088014489438621990 — Multi-week maintenance routine: 388 PRs opened, 180 merged (Aug 13)
- 2087284684103537011 — LLM bugs shifted from off-by-ones to system design/UX flaws (Aug 11)

**simonw:**
- 2086931955539742985 — Claude Haiku hallucination concern in WebFetch (Aug 10)
- 2089112517796827439 — Qwen 3.8 27B local review (Aug 16)

**emollick:**
- 2087229045029404835 — LLMs cross-pollinating science subfields (Aug 11)
- 2088864599701442925 — o3-mini loop produced exam questions matching psychometrics (Aug 16)
- 2089042815405686919 — Non-verifiable AI benchmarks need qualitative methods (Aug 16)

**swyx:**
- 2087437017840046156 — "How to steal a reasoning trace" — extended-thinking as attack surface (Aug 12)
- 2088073777779515615 — /align-me modification: batch design clarifications upfront (Aug 14)

**rasbt:**
- 2088631263737364818 — Claude text watermarking explainer (Aug 15)
- 2087180773497421926 — Meta Muse Glimmer 30B architecture (Aug 11)

**levelsio:**
- 2087305386743206224 — Claude getting "extremely preachy"; ready to switch to Grok (Aug 11)
- 2087579763158216795 — Switched ideasai.com back-end from Claude to Grok 4.6 (Aug 12)

### Featured in `log/2026-08-10.md`:

**bcherny:**
- 2086520950259118464 — Prompt injection largely solved via stacked defenses (Aug 9)
- 2085860677990883454 — Auto Mode becomes default in Claude Code (Aug 7)

**simonw:**
- 2085877951925801274 — Black Hat talk on OpenAI/HF incident (Aug 7)
- 2086220154468442496 — Skeptical of auto-mode fixing prompt injection (Aug 8)
- 2086454620470309371 — Vibe-coding games looks easy; making them fun remains hard (Aug 9)

**emollick:**
- 2085747398630920220 — Mythos/Astra: autonomous exploit-finding, spontaneous coordination (Aug 7)
- 2085553951034745154 — Every benchmark score has implied asterisk (Aug 7)
- 2086338988520927368 — Escalation prompt: "I want you, not your agents" (Aug 9)

**swyx:**
- 2086505938144616810 — Warning: delete accumulated stale skills (Aug 9)
- 2085517544795079014 — Kill My SaaS hackathon concept post (Aug 7)
- 2085995879966921177 — Kill My SaaS competition live (Aug 8)

**rasbt:**
- 2085737107486642385 — LLMs-from-scratch hits 100k GitHub stars (Aug 7)

**levelsio:**
- 2084348044808507416 — AI as judgment not information retrieval (Aug 3)

### Featured in `log/2026-07-27.md` (prunable after ~Sep 27):
- 2080713091688583312, 2080710971228918066, 2079990597973057691, 2080750942333374870, 2080731979528679617

### Featured in `log/2026-07-20.md` (PRUNABLE — Sep 20 passed):
- 2077929379661844559, 2077929390806073807, 2077929397495959693, 2077929404219474148, 2077489907350856038, 2077460395279692197

## Recurring themes

### @bcherny (Boris Cherny)
- **Production code quality**: Sep 11 post establishes clear two-tier framework: prototype = black box OK; production Claude code = HIGHER bar than human code (lint + e2e + daily fuzzers + auto-review + security review). Landmark practical post.
- **Autonomous maintenance routines**: 388 PRs/180 merged remains the landmark data point. Cowork expansion signals broader access.
- **Claude Code extensibility**: Sep 3 post (just outside window) previewed major extensibility features — watch for follow-up.
- **Store still stale since Aug 20** — 4 weeks without Mac pull data; Sep 11 post found only via WebSearch.

### @simonw (Simon Willison)
- **OpenAI math claim critic**: Sep 8 Navier-Stokes post is his most important piece of the month — balanced, covers technical + ethical dimensions.
- **Agent-era experiments**: Sep 12 running routes demo shows simonw's hands-on approach to testing new models immediately on release.
- **May be using Bluesky over X**: bsky.app/profile/simonwillison.net found in search — may explain difficulty finding X post IDs. Raw store had 403 error since Aug 20.
- **Blog active**: posts consistently throughout the window. Consider blog as primary source when raw store is stale.

### @emollick (Ethan Mollick)
- **Satirical Navier-Stokes post confirmed via secondary sources**: "Quick, spread some rumors about other really hard problems that Anthropic is on the verge of solving" — multiple sources describe this but no X URL found. Confirms he was active this week.
- **Book "Co-Existence" releasing Oct 20** — promotion period has started; watch for posts.
- **Store stale since Aug 20** — 4 weeks without data.

### @_catwu (Cat Wu)
- **Store stale since Aug 17** — 4 weeks without data. Last known: /design command preview.

### @swyx
- **Latent Space AINews covered Navier-Stokes Sep 7-8**: https://www.latent.space/p/ainews-openai-reports-navier-stokes
- **Store 403 error since Aug 20** — 4 weeks. Newsletter is active.

### @rasbt (Sebastian Raschka)
- **Custom small LLM project still unannounced**: teased Aug 7; 6+ weeks without update. Book club Q&A for "Build a Reasoning Model From Scratch" was Sep 3. Likely ships Sep–Oct.
- **Store stale since Aug 18** — 4 weeks.

### @levelsio (Pieter Levels)
- **Still on Grok 4.6** (switched Aug 12). No Claude return signals.
- **Made nomads.com free** (~early Sep, unconfirmed date). Store stale since Aug 19.

### @alexalbert__, @karpathy
- Both stale for 5+ weeks. karpathy joined Anthropic pretraining team per search results (late 2025/2026). alexalbert__ last Aug 14.

## Open threads to watch

- **⚠️ Mac daily pull failure (CRITICAL — 4th week)**: raw stores have a 25-day gap (Aug 20 → Sep 14). Four consecutive digests missed. Check launchd job, Nitter source availability, and whether the RSS URLs have changed. Recovery essential.
- **Navier-Stokes credit controversy**: Levent Alpöge (Anthropic) + Tristan Buckmaster (NYU) alleged credit-stripping by OpenAI — watch for resolution, response from Anthropic, or Clay Institute decision.
- **emollick book "Co-Existence"** (Oct 20): pre-release promotion period has started. Watch for teaching/framework posts.
- **bcherny Claude Code extensibility**: Sep 3 post previewed major extension features — follow-up posts expected.
- **rasbt custom small LLM project**: teased Aug 7; 6+ weeks; likely ships Sep–Oct.
- **Kill My SaaS winner**: 69 final submissions; no winner announced. Watch for swyx post-mortem.
- **simonw vs. bcherny on prompt injection**: simonw's Aug 8 blog skeptical; no bcherny counter. Stale.
- **Claude Haiku in WebFetch**: simonw flagged Aug 10; no Anthropic response yet.
- **levelsio migration trajectory**: still on Grok 4.6; watch for return to Claude.
- **/design command GA**: early preview Aug 17; watch for wider release.
- **Reasoning trace security**: swyx's Aug 12 paper; no public mitigation.
- **Claude Security plugin**: still in beta.
- **karpathy at Anthropic pretraining**: reportedly joined; watch for first post from inside the team.
- **swyx "simulation as scaling law"**: late-Aug post; unconfirmed status.

## Notes for next run

- Window: 2026-09-21 → 2026-09-28.
- **CRITICAL**: Mac launchd pull has now missed 25 days. Check `ai-learning/raw/_meta.json` immediately.
- Prune `log/2026-07-20.md` entries (Sep 20 prune date has passed).
- `log/2026-07-27.md` entries prunable after Sep 27.
- simonw may primarily use Bluesky (bsky.app/profile/simonwillison.net) — if raw store remains 403, try WebFetching the blog directly or checking bsky.
- emollick: "Co-Existence" book releases Oct 20 — watch for teaching framework posts in next window.
- rasbt: check for custom small LLM project announcement (6+ weeks since tease).
- karpathy: check for first "inside Anthropic pretraining" posts.
- bcherny: check for extensibility feature follow-up (Sep 3 preview post was outside window).
- Watch for Navier-Stokes credit dispute resolution (Clay Institute deliberating).
