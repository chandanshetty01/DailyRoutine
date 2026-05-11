# ipo-watch

**What it does:** Daily morning briefing on AI + quantum-computing IPOs and on the IPO status of three private companies the user is tracking (OpenAI, Anthropic, SpaceX). Includes links to source news for any AI/quantum stock moves worth a closer look.

**Schedule:** Every day at 09:00 IST (03:30 UTC).

**Output:** Commits a Markdown report to `ipo-watch/log/YYYY-MM-DD.md` and overwrites `ipo-watch/state.md` with the latest tracked-company snapshot.

**Disclaimer:** Informational only. Not investment advice. Always verify with primary sources (SEC filings, exchange announcements, company press releases) before acting.

## Prompt

The routine prompt is committed at [`PROMPT.md`](PROMPT.md). Keep the live routine in sync with that file.
