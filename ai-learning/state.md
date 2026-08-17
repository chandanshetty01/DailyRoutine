# State — ai-learning

Rolling state for the ai-learning routine. Read on start, rewritten before exit.

## Last run
2026-08-17T00:00:00Z — weekly run, window 2026-08-10 → 2026-08-17.

## Covered posts (dedupe list — prune entries older than ~60 days)

### Featured in `log/2026-08-17.md`:

**bcherny:**
- 2088014489438621990 — Multi-week maintenance routine experiment via Slack: 388 PRs opened (crash fuzzer, dup unifier, dead-code remover), 180 merged after review (Aug 13)
- 2087284684103537011 — LLM bugs have shifted from off-by-ones to system design and UX flaws; adversarial code review is the counter (Aug 11)

**simonw:**
- 2086931955539742985 — Claude Haiku "hallucinates wildly"; flagged as model still powering Claude Code's WebFetch tool (Aug 10)
- 2089112517796827439 — Qwen 3.8 27B local review: "most fun with a local model"; vision-capable, runs LM Studio on M5 Max (Aug 16)

**emollick:**
- 2087229045029404835 — LLMs cross-pollinating science subfields = revolutionary; solves "burden of knowledge" bottleneck (Aug 11)
- 2088864599701442925 — o3-mini agentic loop produced exam questions matching high-stakes standardized test psychometrics — one of the largest such field studies (Aug 16)
- 2089042815405686919 — Non-verifiable AI benchmarks should use qualitative research methods; AI researchers should read psychometrics before reinventing from scratch (Aug 16)

**swyx:**
- 2087437017840046156 — "How to steal a reasoning trace" — swyx calls it one of the most important papers of 2026; extended-thinking traces are a new attack surface (Aug 12)
- 2088073777779515615 — /align-me modification: batch all design clarification questions upfront in one shot instead of one at a time (Aug 14)

**rasbt:**
- 2088631263737364818 — Claude text watermarking explainer: inference-time secret key selects among tied tokens; EU AI Act required, applied globally (Aug 15)
- 2087180773497421926 — Meta Muse Glimmer 30B architecture: first Apache 2.0 large open-weight model; 52 KiB/token KV cache vs Gemma 4's 840 KiB (Aug 11)

**levelsio:**
- 2087305386743206224 — Claude getting "extremely preachy every day"; ready to switch to Grok (Aug 11)
- 2087579763158216795 — Switched ideasai.com auto app builder back-end from Claude to Grok 4.6; cites repeated refusals (Aug 12)

### Featured in `log/2026-08-10.md`:

**bcherny:**
- 2086520950259118464 — Prompt injection largely solved via stacked defenses (model training + probes + Auto Mode); ~0 success rate on unseen attacks (Aug 9)
- 2085860677990883454 — Auto Mode becomes default in Claude Code next week; ~0 indirect prompt injection (Aug 7); blog: claude.com/blog/auto-mode-default-in-claude-code

**simonw:**
- 2085877951925801274 — Black Hat talk on OpenAI/HF incident: multi-agent spontaneous coordination via file-name messages; accidental-cyberattacks tag now 4+ labs (Aug 7); blog: simonwillison.net/2026/Aug/7/openai-timeline/
- 2086220154468442496 — Skeptical of auto-mode fixing prompt injection; detailed counterpoint blog (Aug 8); blog: simonwillison.net/2026/Aug/8/auto-mode/
- 2086454620470309371 — Vibe-coding games looks easy; making them fun remains beyond AI (Aug 9)

**emollick:**
- 2085747398630920220 — Mythos/Astra: autonomous exploit-finding, social engineering, spontaneous coordination — not just finding bugs on command (Aug 7)
- 2085553951034745154 — Every benchmark score has implied asterisk: "could be significantly higher with a better harness" (Aug 7)
- 2086338988520927368 — Escalation prompt: "I want you, not your agents, to go through everything" (Aug 9)

**swyx:**
- 2086505938144616810 — Warning: delete accumulated skills; stale skills eat context and interact badly (Aug 9); blog: forge.smol.ai/blog/dangerous-release-code-was-a-skill
- 2085517544795079014 — Kill My SaaS $10k hackathon concept post (Aug 7)
- 2085995879966921177 — Kill My SaaS competition live; 600+ applied, 100 admitted (Aug 8)

**rasbt:**
- 2085737107486642385 — LLMs-from-scratch hits 100k GitHub stars; teasing upcoming custom small LLM project (Aug 7)

**levelsio:**
- 2084348044808507416 — Accountant relaying AI answers to client; value of professionals is now judgment not information retrieval (Aug 3)

### Featured in `log/2026-08-03.md`:
- (no new posts this window)

### Featured in `log/2026-07-27.md` (status ids):
- 2080713091688583312 — Opus 5 least prompt injectable model; Auto Mode + probes → ~0 attack success rate (Jul 24)
- 2080710971228918066 — ~80% of Claude Code system prompt removed for newer models; learnings on CLAUDE.md/skills (Jul 24, repost trq212)
- 2079990597973057691 — Claude Security plugin beta: pre-commit vulnerability scanning from terminal (Jul 22, repost claudeai)
- 2080750942333374870 — Opus 5 OSWorld v2 70.6% SOTA; offer to sponsor harder computer use evals (Jul 24, repost ehsanik)
- 2080731979528679617 — Opus 5 near-consultant-quality spreadsheets/slides; rapid capability advancement (Jul 24, repost alexalbert__)

### Featured in `log/2026-07-20.md` (status ids):
- 2077929379661844559 — 4-step AI adoption framework; Anthropic at step 3, bcherny at 4 (Jul 17)
- 2077929390806073807 — /loop + /batch + dynamic workflows + worktree isolation for level 3–4 (Jul 17, reply)
- 2077929397495959693 — AI ROI = eng-hours displaced, not usage dashboards (Jul 17, reply)
- 2077929404219474148 — background automation enables work "not previously in range" (Jul 17, reply)
- 2077489907350856038 — Artifacts + MCP connectors on Pro/Max/Team/Enterprise (Jul 15, repost ClaudeDevs)
- 2077460395279692197 — domain knowledge as infrastructure: CLAUDE.md/REVIEW.md/skills = new lint rules (Jul 15)

### Featured in `log/2026-07-13.md` (status ids):
- 2075635283211772279 — In-app browser in Claude Code desktop; sandboxed, configurable (Jul 10, repost ClaudeDevs)
- 2074997570317779038 — /checkup command: 7-step setup optimizer (Jul 8)
- 2074925531519468012 — Claude Tag webinar: single-player → multiplayer journey (Jul 8, repost _catwu)
- 2074247226038063316 — "We are 1% done"; Claude Code origin in Anthropic safety research (Jul 6)

### Featured in `log/2026-07-06.md` (status ids — prunable after ~Sep 6):
- 2072777472970563995 — Artifacts in Claude Code "life changing"; expanding to Pro and Max (Jul 2)
- 2072429181565288665 — Fable 5 rate limits reset; ready to build again (Jul 1, repost ClaudeDevs)
- 2072000214634742243 — Claude Desktop on Linux launch (Jun 30)
- 2071653958905467027 — Claude on Microsoft Foundry/Azure GA (Jun 29, repost claudeai)
- 2071647677591466098 — Subagents run in background by default in next Claude Code (Jun 29)

### Featured in `log/2026-06-29.md` (status ids — prunable after ~Aug 29):
- 2071379474277613732 — Future product archetypes: Prototyper/Builder/Sweeper/Grower/Maintainer (Jun 28)
- 2069474687323893796 — Claude Tag as company search engine / onboarding unlock (Jun 23)
- 2069474688619958517 — Claude Tag proactive monitoring, emoji reactions per thread (Jun 23)
- 2069474691010707486 — Claude Tag beta on Slack Enterprise/Team; "more surfaces coming soon" (Jun 23)

## Recurring themes

### @bcherny (Boris Cherny)
- **Autonomous maintenance routines** is the new anchor: 388 PRs across repos in a few weeks, 180 merged; model self-tunes its own prompt on misses. Next expected: more data on merge rates, specific routine prompts published.
- **Prompt injection defense**: stacked defenses → ~0 attack success rate; Auto Mode now default. Thread with simonw ongoing.
- **LLM bug taxonomy shifting**: off-by-ones → system design/UX/missing context. Adversarial code review as the structural counter.
- **Autonomy playbook**: /loop, /batch, dynamic workflows, worktree isolation, self-verification — consistent across weeks.

### @simonw (Simon Willison)
- **Independent empirical tester**: experiments, publishes counter-takes (auto-mode skepticism, Haiku hallucination report, Qwen review).
- **Model quality watchdog**: flagged Haiku as Claude Code's WebFetch model this week — calls it his "current least favorite model."
- **Security tracker**: accidental-cyberattacks tag now 4–5 incidents; Black Hat talk published.
- **Open-weight enthusiast**: Qwen 3.8 27B review was his most enthusiastic local-model write-up in memory.

### @emollick (Ethan Mollick)
- **Evidence-based AI optimist/skeptic**: this week added science cross-pollination thesis alongside usual benchmarking caveats.
- **Evaluation methodology advocate**: pushed qualitative research methods for non-verifiable benchmarks — not just "use a better harness."
- **Harness > model tier**: o3-mini agentic loop result reinforces his consistent finding.
- **Cybersecurity alarm**: still tracking but quieter this week than last.

### @swyx
- **AI tooling ecosystem**: Kill My SaaS results came in (multiple submissions in one weekend, 183 sub-agents); batch clarification UX pattern.
- **Security surface tracker**: reasoning trace theft paper as a new attack vector for extended-thinking deployments.
- **Infrastructure for agents**: consistent; forge, eval frameworks, skills hygiene from last week.

### @rasbt (Sebastian Raschka)
- **Architecture deep-dives**: Meta Muse Glimmer 30B this week (KV-cache efficiency standout); consistent weekly cadence.
- **Open-source LLM education**: LLMs-from-scratch still active; custom small LLM project still in progress.
- **Watermarking explainer**: Claude EU AI Act watermarking became his most-read post this cycle.

### @levelsio (Pieter Levels)
- **Refusal frustration → model switching**: switched ideasai.com to Grok 4.6 this week; signal that Claude's refusal tuning is losing production builders.
- **Indie builder shipping with AI**: primarily posts fitness/food/travel; AI signal is sparse but high-value when it appears.

### @_catwu, @alexalbert__, @karpathy
- All quiet again. _catwu newest Aug 13 (logistics only); alexalbert__ newest Aug 14 (repost only); karpathy newest Aug 2 (outside window).
- Watch karpathy for any Anthropic R&D posts; _catwu for Claude Code PM previews.

## Open threads to watch

- **simonw vs. bcherny on prompt injection** — simonw's Aug 8 blog says he's not persuaded; bcherny hasn't publicly responded. Watch for a more detailed Anthropic write-up or bcherny's counter.
- **Kill My SaaS final results** — swyx's hackathon produced real submissions; watch for winner announcement and which SaaS categories proved hardest to clone.
- **rasbt's custom small LLM project** — teased Aug 7 as "keeping me super busy this month"; still no update; likely ships August/September.
- **levelsio migration trajectory** — switched to Grok 4.6 this week; watch for follow-up on whether the switch held or they returned to Claude.
- **Claude Haiku in WebFetch** — simonw flagged it explicitly; watch for Anthropic response or a tool-model update in Claude Code.
- **Reasoning trace security** — swyx called it the most important paper of 2026; watch for follow-up from security researchers or model providers on mitigations.
- **Open-weight frontier models + cybersecurity** — emollick's alarm from Aug 7 still unanswered institutionally; Meta Muse Glimmer 30B now in the field.
- **Claude Security plugin** — still in beta; watch for GA announcement.

## Notes for next run

- Window: 2026-08-17 → 2026-08-24.
- All stores fresh as of 2026-08-17T00:00Z; all 9 accounts populated.
- Active accounts this week: bcherny, simonw, emollick, swyx, rasbt, levelsio. _catwu, alexalbert__, karpathy all quiet.
- Priority threads: levelsio Grok migration follow-up; bcherny response to simonw prompt injection; Kill My SaaS winner; rasbt small LLM project.
- emollick had 20+ in-window posts this week; filter ruthlessly next time — prioritize novel claims over amplification.
- The `log/2026-06-29.md` entries become prunable Aug 29; the `log/2026-07-06.md` entries become prunable Sep 6.
