# ai-learning

**What it does:** Weekly digest of what **Boris Cherny** (creator of Claude Code, [@bcherny](https://x.com/bcherny)) has been posting on X, distilled into "what to learn / try" so the user can keep up with Claude Code tips, features, and AI-coding workflow ideas.

**Schedule:** Every **Monday 09:00 SGT** (01:00 UTC). Covers the previous 7 days.

**Inputs:** `WebSearch` (primary, works in the cloud routine). Optionally an X API v2 connector for complete timeline coverage — see [`PROMPT.md`](PROMPT.md). The cloud routine has **no** access to a logged-in browser, so it relies on WebSearch.

**Output:**
- Weekly: commits a Markdown digest to `ai-learning/log/YYYY-MM-DD.md` (dated by the Monday it runs) and overwrites `ai-learning/state.md` with a rolling snapshot of what's already been covered (so the next run doesn't repeat posts).
- The first report (`2026-06-25.md`) is a one-time **30-day backfill** seeded from his timeline.

**Viewer:** Rendered alongside ipo-watch at the **AI Learning** tab of <https://chandanshetty01.github.io/DailyRoutine/>.

**Note:** Informational learning digest. Summaries are paraphrased, not full reproductions of his posts — always open the linked post for the original wording.

## Prompt

The routine prompt is committed at [`PROMPT.md`](PROMPT.md). Keep the live routine in sync with that file.
