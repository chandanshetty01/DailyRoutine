#!/usr/bin/env python3
"""
ai-learning daily pull — fetch @bcherny's timeline from a Nitter RSS feed and
merge it into a durable local store the cloud weekly routine can summarize from.

Why this exists: Nitter blocks Anthropic's cloud IPs (HTTP 403) but works fine
from a residential IP, and X itself returns 402 to unauthenticated fetches. So
the user's Mac captures the raw posts daily; the cloud routine just reads the
committed JSONL. No browser, no login, stdlib only.

Store: ai-learning/raw/bcherny.jsonl  (one JSON object per line, newest first,
deduped by tweet id). Also writes raw/_meta.json with last-pull info.
"""
import json, re, sys, os, urllib.request
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET
from datetime import datetime, timezone

FEEDS = [
    "https://nitter.net/bcherny/rss",
    "https://nitter.privacydev.net/bcherny/rss",
    "https://lightbrd.com/bcherny/rss",
]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
DC = "{http://purl.org/dc/elements/1.1/}"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(ROOT, "raw")
STORE = os.path.join(RAW_DIR, "bcherny.jsonl")
META = os.path.join(RAW_DIR, "_meta.json")


def fetch():
    last_err = None
    for url in FEEDS:
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
    raise SystemExit(f"all feeds failed; last error: {last_err}")


def parse(body):
    root = ET.fromstring(body)
    out = {}
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        m = re.search(r"status/(\d+)", link) or re.search(r"status/(\d+)", guid)
        if not m:
            continue
        tid = m.group(1)
        author = (item.findtext(DC + "creator") or "").lstrip("@").strip() or "bcherny"
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
            "is_repost": author.lower() != "bcherny",
            "is_reply": is_reply,
            "text": text,
            "url": f"https://x.com/{author}/status/{tid}",
        }
    return out


def load_store():
    store = {}
    if os.path.exists(STORE):
        with open(STORE) as f:
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


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    used_url, body = fetch()
    fresh = parse(body)
    store = load_store()
    before = len(store)
    added = [tid for tid in fresh if tid not in store]
    store.update(fresh)  # refresh text/date for existing too
    rows = sorted(store.values(), key=lambda o: (o["date"], o["id"]), reverse=True)
    with open(STORE, "w") as f:
        for o in rows:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    meta = {
        "last_pull_utc": datetime.now(timezone.utc).isoformat(),
        "source": used_url,
        "total_posts": len(rows),
        "new_this_pull": len(added),
        "newest_date": rows[0]["date"] if rows else "",
    }
    with open(META, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"OK source={used_url} total={len(rows)} (+{len(added)} new, was {before})")


if __name__ == "__main__":
    main()
