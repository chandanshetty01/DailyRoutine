#!/usr/bin/env python3
"""
ai-learning daily pull — fetch tracked accounts' timelines from Nitter RSS and
merge them into durable per-account stores the cloud weekly routine summarizes.

Why this exists: Nitter blocks Anthropic's cloud IPs (HTTP 403) but works fine
from a residential IP, and X itself returns 402 to unauthenticated fetches. So
the user's Mac captures the raw posts daily; the cloud routine just reads the
committed JSONL. No browser, no login, stdlib only.

Stores: ai-learning/raw/<handle>.jsonl (one JSON object per line, newest first,
deduped by tweet id). ai-learning/raw/_meta.json holds per-account pull info.
"""
import json, re, sys, os, time, urllib.request
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET
from datetime import datetime, timezone

# Tracked accounts. Boris anchors the digest; the rest were chosen with the user
# (tier 1 + tier 2, 2026-08-08).
ACCOUNTS = [
    "bcherny",       # Claude Code creator — anchor
    "_catwu",        # Claude Code PM
    "alexalbert__",  # Anthropic, Claude Relations
    "simonw",        # hands-on LLM experiments
    "karpathy",      # deep takes on LLMs/agents
    "emollick",      # evidence-based AI-at-work advice
    "swyx",          # AI-engineering ecosystem
    "rasbt",         # LLM research explainers
    "levelsio",      # indie shipping with AI
]
FEED_HOSTS = [
    "https://nitter.net",
    "https://nitter.privacydev.net",
    "https://lightbrd.com",
]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
DC = "{http://purl.org/dc/elements/1.1/}"
FETCH_DELAY_S = 2  # be polite to the Nitter instance between account fetches

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.dirname(ROOT)
RAW_DIR = os.path.join(ROOT, "raw")
META = os.path.join(RAW_DIR, "_meta.json")

# Report folders listed in docs/manifest.json. The web viewer reads the manifest
# from raw.githubusercontent.com (CDN, no rate limit) instead of depending on
# api.github.com's 60 req/hr unauthenticated cap.
MANIFEST_DIRS = ["ipo-watch/log", "ipo-watch/monthly", "ai-learning/log"]
MANIFEST = os.path.join(REPO_ROOT, "docs", "manifest.json")


def fetch(handle):
    last_err = None
    for host in FEED_HOSTS:
        url = f"{host}/{handle}/rss"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status == 200:
                    body = r.read()
                    if b"<item>" in body:
                        return url, body
                    last_err = f"{url}: 200 but no items"
                else:
                    last_err = f"{url}: HTTP {r.status}"
        except Exception as e:
            last_err = f"{url}: {e}"
    raise RuntimeError(last_err)


def parse(body, handle):
    root = ET.fromstring(body)
    out = {}
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        m = re.search(r"status/(\d+)", link) or re.search(r"status/(\d+)", guid)
        if not m:
            continue
        tid = m.group(1)
        author = (item.findtext(DC + "creator") or "").lstrip("@").strip() or handle
        text = re.sub(r"\s+", " ", (item.findtext("title") or "")).strip()
        # Nitter prefixes replies/thread continuations with "R to @handle: "
        reply_m = re.match(r"^R to @[\w]+:\s*", text)
        is_reply = bool(reply_m)
        if reply_m:
            text = text[reply_m.end():]
        pub = item.findtext("pubDate")
        try:
            date_iso = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except Exception:
            date_iso = ""
        out[tid] = {
            "id": tid,
            "date": date_iso,
            "author": author,
            "is_repost": author.lower() != handle.lower(),
            "is_reply": is_reply,
            "text": text,
            "url": f"https://x.com/{author}/status/{tid}",
        }
    return out


def load_store(path):
    store = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                    store[o["id"]] = o
                except Exception:
                    pass
    return store


def pull_account(handle):
    store_path = os.path.join(RAW_DIR, f"{handle}.jsonl")
    used_url, body = fetch(handle)
    fresh = parse(body, handle)
    store = load_store(store_path)
    added = [tid for tid in fresh if tid not in store]
    store.update(fresh)  # refresh text/date for existing too
    rows = sorted(store.values(), key=lambda o: (o["date"], o["id"]), reverse=True)
    with open(store_path, "w") as f:
        for o in rows:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    return {
        "source": used_url,
        "total_posts": len(rows),
        "new_this_pull": len(added),
        "newest_date": rows[0]["date"] if rows else "",
    }


def build_manifest():
    listing = {}
    for rel in MANIFEST_DIRS:
        d = os.path.join(REPO_ROOT, rel)
        if os.path.isdir(d):
            listing[rel] = sorted(
                f for f in os.listdir(d) if f.endswith(".md") and not f.startswith(".")
            )
        else:
            listing[rel] = []
    with open(MANIFEST, "w") as f:
        json.dump(
            {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "reports": listing},
            f, indent=1,
        )
    total = sum(len(v) for v in listing.values())
    print(f"manifest: {total} reports across {len(listing)} folders")


def main():
    if "--manifest-only" in sys.argv:
        build_manifest()
        return
    os.makedirs(RAW_DIR, exist_ok=True)
    meta = {"last_pull_utc": datetime.now(timezone.utc).isoformat(), "accounts": {}}
    failures = 0
    for i, handle in enumerate(ACCOUNTS):
        if i:
            time.sleep(FETCH_DELAY_S)
        try:
            info = pull_account(handle)
            meta["accounts"][handle] = info
            print(f"OK  {handle}: total={info['total_posts']} (+{info['new_this_pull']} new)")
        except Exception as e:
            failures += 1
            meta["accounts"][handle] = {"error": str(e)}
            print(f"ERR {handle}: {e}")
    with open(META, "w") as f:
        json.dump(meta, f, indent=2)
    build_manifest()
    # Only fail the run if EVERY account failed — partial data is still useful.
    if failures == len(ACCOUNTS):
        raise SystemExit("all accounts failed")


if __name__ == "__main__":
    main()
