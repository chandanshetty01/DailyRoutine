# ai-learning

**What it does:** Weekly digest of what **Boris Cherny** (creator of Claude Code, [@bcherny](https://x.com/bcherny)) has been posting on X, distilled into "what to learn / try" so the user can keep up with Claude Code tips, features, and AI-coding workflow ideas.

**Schedule:** Every **Monday 09:00 SGT** (01:00 UTC). Covers the previous 7 days.

**How data flows (two jobs):**

```
Local daily pull (launchd, your Mac)         Cloud weekly routine (Anthropic cloud)
  scripts/run_daily_pull.sh                     reads raw/bcherny.jsonl from the repo,
  → curl nitter.net/bcherny/rss                 filters last 7 days, summarizes
  → merge into raw/bcherny.jsonl (dedup)    →   → writes log/YYYY-MM-DD.md + state.md
  → commit + push                               → commits + pushes
```

Why split: Nitter (the free X mirror) returns **403 from Anthropic's cloud** but **200 from a residential IP**, and X itself blocks unauthenticated fetches (402). So your Mac captures the raw posts daily into `raw/`, and the cloud routine just summarizes from the committed file — no X access needed in the cloud, works even on weeks your Mac is mostly off (the next successful pull backfills the gap).

**Inputs:**
- **Local daily pull:** `scripts/daily_pull.py` (stdlib Python) + `scripts/run_daily_pull.sh` (git wrapper), scheduled by `~/Library/LaunchAgents/com.chandanshetty.ai-learning-pull.plist`. Source: Nitter RSS. No login, no browser, no API key.
- **Cloud weekly digest:** reads `raw/bcherny.jsonl` → Nitter (usually 403 in cloud) → WebSearch, in that order. See [`PROMPT.md`](PROMPT.md).

**Output:**
- Daily: updates `ai-learning/raw/bcherny.jsonl` (+ `raw/_meta.json`).
- Weekly: commits a digest to `ai-learning/log/YYYY-MM-DD.md` (dated by the Monday) and overwrites `ai-learning/state.md` with a rolling covered-posts snapshot (so the next run doesn't repeat posts).
- The first report (`2026-06-25.md`) is a one-time **30-day backfill** seeded from a high-fidelity Chrome pull of his timeline.

**Viewer:** Rendered alongside ipo-watch at the **AI Learning** tab of <https://chandanshetty01.github.io/DailyRoutine/>.

**Note:** Informational learning digest. Summaries are paraphrased, not full reproductions of his posts — always open the linked post for the original wording.

## Prompt

The routine prompt is committed at [`PROMPT.md`](PROMPT.md). Keep the live routine in sync with that file.
