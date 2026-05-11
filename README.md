# DailyRoutine

State and memory store for [Claude routines](https://code.claude.com/docs/en/routines.md).

Routines run on Anthropic's cloud and don't persist memory across runs by default. This repo gives them somewhere to read/write state between runs.

## Convention

Each routine gets its own top-level folder named after the routine (kebab-case):

```
DailyRoutine/
├── README.md
├── _template/              # copy this when adding a new routine
│   ├── README.md           # what this routine does, schedule, inputs
│   ├── state.md            # rolling state the routine reads/writes
│   └── log/                # append-only run logs (YYYY-MM-DD.md)
├── pr-triage/
│   ├── README.md
│   ├── state.md
│   └── log/
└── inbox-summary/
    └── ...
```

## How a routine should use its folder

1. **On start:** read `<routine>/state.md` for prior context.
2. **During the run:** do the work.
3. **Before exit:** update `state.md`, append a new entry to `log/YYYY-MM-DD.md`, commit, and push.

The routine's prompt should reference its folder explicitly, e.g.:

> Your state lives in `pr-triage/`. Read `pr-triage/state.md` first, then ...

## Why a separate repo

- Keeps routine state out of working repos' git history and CI triggers.
- One place to share context across multiple routines.
- Cheap to grant a routine write access here without touching production repos.
