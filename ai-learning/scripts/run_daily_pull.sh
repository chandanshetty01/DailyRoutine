#!/bin/bash
# ai-learning daily pull wrapper — run by launchd once a day.
# Fetches @bcherny's timeline into ai-learning/raw/ and pushes if anything changed.
# Uses gh's keyring token for HTTPS push so it doesn't depend on ssh-agent under launchd.
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"

REPO="/Users/chandanshettysp/Documents/Projects/DailyRoutine"
HTTPS="https://github.com/chandanshetty01/DailyRoutine.git"
CRED='credential.helper=!gh auth git-credential'
LOG="$REPO/ai-learning/scripts/pull.log"

cd "$REPO" || exit 1

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') ai-learning daily pull ==="

  # 1) sync with remote (HTTPS via gh, autostash any stray local changes)
  git -c "$CRED" pull --rebase --autostash "$HTTPS" main || echo "WARN: pull failed, continuing"

  # 2) fetch posts into raw/
  if ! python3 ai-learning/scripts/daily_pull.py; then
    echo "ERROR: pull script failed"; echo; exit 1
  fi

  # 3) commit + push only if raw/ changed (porcelain catches untracked files too)
  if [ -z "$(git status --porcelain -- ai-learning/raw)" ]; then
    echo "no new content"
  else
    git add ai-learning/raw
    git commit -q -m "ai-learning: daily pull $(date -u +%Y-%m-%d)"
    if ! git -c "$CRED" push "$HTTPS" HEAD:main; then
      echo "push rejected; rebase + retry"
      git -c "$CRED" pull --rebase --autostash "$HTTPS" main && git -c "$CRED" push "$HTTPS" HEAD:main \
        && echo "pushed on retry" || echo "ERROR: push failed"
    else
      echo "pushed"
    fi
  fi
  echo
} >> "$LOG" 2>&1
