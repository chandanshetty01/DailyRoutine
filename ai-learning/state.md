# State — ai-learning

Rolling state for the ai-learning routine. Read on start, rewritten before exit.

## Last run
2026-08-10T00:00:00Z — weekly run, window 2026-08-03 → 2026-08-10.

## Covered posts (dedupe list — prune entries older than ~60 days)

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
- **Prompt injection defense** is his anchor topic: Jul 24 Opus 5 announcement → Aug 7 confirmation of ~0 success rate → Aug 9 detailed public explanation of stacked defenses. Watch for any follow-up blog post or system card addendum.
- **Auto Mode** going default; he and the team have used it exclusively for months.
- **Autonomy playbook**: /loop, /batch, dynamic workflows, worktree isolation, self-verification — consistent framework across weeks.
- **Domain knowledge as infrastructure**: CLAUDE.md, skills, REVIEW.md encoding tribal knowledge; newer models need leaner versions.

### @simonw (Simon Willison)
- **Independent empirical tester**: writes up experiments and publishes counter-takes to announcements (e.g., auto-mode skepticism this week).
- **Security tracker**: self-appointed chronicler of the "accidental cyberattacks" phenomenon; now at 4–5 incidents.
- **Game dev with AI**: multi-week thread on vibe-coding games; consistent finding that aesthetics is solved, game feel is not.

### @emollick (Ethan Mollick)
- **Evidence-based skeptic** on AI benchmarks and hype; consistently surfaces the harness/evaluation quality gap.
- **Cybersecurity alarm**: most vocal this week about the implications of open-weight frontier-level models for autonomous hacking.
- **Practical prompting**: shares concrete prompts and techniques for getting better results from coding agents.

### @swyx
- **AI tooling ecosystem** trends: skills hygiene, forge, hackathons.
- **Competitive AI development** experiments: Kill My SaaS is his most concrete test of AI-first product velocity.
- **Infrastructure for agents**: papercuts, agent-native git (Smol Forge), eval frameworks.

### @rasbt (Sebastian Raschka)
- **Open-source LLM education**: LLMs-from-scratch is his flagship resource; steadily adds new material.
- **Architecture deep-dives**: weekly analyses of new open-weight model releases (Kimi K3, Laguna, etc.).
- **Harness/token efficiency** observations: Claude Code uses 2–3x more tokens than other harnesses at similar success rates.

### @levelsio (Pieter Levels)
- **Indie builder shipping with AI**: vibe-codes tools (calorie tracker, Photo AI video editor) and reflects on AI changing professional services.
- **AI in professional services**: accountant-as-AI-relay observation this week; recurring theme of when humans add value vs. when AI suffices.

### @_catwu, @alexalbert__, @karpathy
- All quiet for 2+ weeks. _catwu and alexalbert__ newest posts Jul 24; karpathy newest Aug 2.
- Watch karpathy for Anthropic R&D posts; _catwu for Claude Code PM previews.

## Open threads to watch

- **Auto Mode as default** — ships "next week" per Aug 7 bcherny post; watch for announcement and user reports on whether it changes workflows meaningfully.
- **simonw vs. bcherny on prompt injection** — simonw's Aug 8 blog explicitly says he isn't persuaded; watch for bcherny response or a more detailed Anthropic write-up to address the skepticism.
- **Kill My SaaS results** — swyx's $10k hackathon; watch for final evaluation and which SaaS categories proved hard to clone.
- **rasbt's custom small LLM project** — teased Aug 7 as "keeping me super busy this month"; likely ships August/September.
- **Open-weight frontier models + cybersecurity** — emollick explicitly asked "what's the plan" for open-weight Mythos/Astra-level models; no institutional answer yet.
- **Claude Security plugin** — still in beta; watch for GA announcement.
- **"More surfaces coming soon" for Claude Tag** — June 23 promise still open.
- **Artifacts + MCP on publicly-shared artifacts** — still unavailable on public shares.

## Notes for next run

- Window: 2026-08-10 → 2026-08-17.
- **Full 9-account roster is active and populated.** All stores are fresh (pulled 2026-08-10T00:00Z).
- This week was rich: bcherny/simonw/emollick/swyx all had substantive posts; _catwu/alexalbert__/karpathy were quiet. Keep the multi-person structure.
- The auto-mode announcement + simonw counterpoint is the most important thread to follow up next week — look for bcherny's response or a community reaction.
- emollick's cybersecurity alarm posts were numerous and high-signal; filter carefully next week if the Black Hat fallout continues.
- swyx's Kill My SaaS hackathon closes Wednesday Aug 12 — results may appear next week.
