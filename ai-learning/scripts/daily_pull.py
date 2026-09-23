#!/usr/bin/env python3
"""
ai-learning daily pull — fetch tracked accounts' X timelines (twitterapi.io) and
blog feeds, and merge them into durable per-account stores the cloud weekly
routine summarizes.

History: originally Nitter RSS (free), which died for good on 2026-08-21. X
itself returns 402 to unauthenticated fetches. Since 2026-09-23 X posts come
from twitterapi.io (pay-per-use, ~$1/mo at this volume); first-party blog feeds
supplement five accounts.

API key: env TWITTERAPI_KEY, else ~/.config/ai-learning/twitterapi.key. The key
is a secret and must NEVER be committed — this repo backs a public site.

Stores: ai-learning/raw/<handle>.jsonl (one JSON object per line, newest first,
deduped by tweet id / blog URL). ai-learning/raw/_meta.json holds per-account
pull info.
"""
import json, re, sys, os, time, urllib.request, urllib.parse
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET
from datetime import datetime, timezone, timedelta

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

# First-party blog/newsletter feeds (verified live 2026-09-03). Normal websites —
# reliable and cloud-fetchable. Long-form content is often higher signal than
# the same person's tweets.
BLOG_FEEDS = {
    "simonw": "https://simonwillison.net/atom/everything/",
    "karpathy": "https://karpathy.bearblog.dev/feed/",
    "emollick": "https://www.oneusefulthing.org/feed",
    "rasbt": "https://magazine.sebastianraschka.com/feed",
    "swyx": "https://www.latent.space/feed",
}

TWITTERAPI_URL = "https://api.twitterapi.io/twitter/user/last_tweets"
KEY_FILE = os.path.expanduser("~/.config/ai-learning/twitterapi.key")
MAX_PAGES = 6            # 20 tweets/page; caps cost if an account goes wild
BACKFILL_DAYS = 45       # never page further back than this
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
FETCH_DELAY_S = 1

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.dirname(ROOT)
RAW_DIR = os.path.join(ROOT, "raw")
META = os.path.join(RAW_DIR, "_meta.json")

# Report folders listed in docs/manifest.json. The web viewer reads the manifest
# from raw.githubusercontent.com (CDN, no rate limit) instead of depending on
# api.github.com's 60 req/hr unauthenticated cap.
MANIFEST_DIRS = ["ipo-watch/log", "ipo-watch/monthly", "ai-learning/log"]
MANIFEST = os.path.join(REPO_ROOT, "docs", "manifest.json")


def api_key():
    k = os.environ.get("TWITTERAPI_KEY", "").strip()
    if not k and os.path.exists(KEY_FILE):
        k = open(KEY_FILE).read().strip()
    return k


def _tweet_row(t, handle):
    """Normalize a twitterapi.io tweet object into a store row."""
    rt = t.get("retweeted_tweet")
    src = rt if rt else t
    author = ((src.get("author") or {}).get("userName") or handle)
    tid = str(src.get("id") or t.get("id"))
    try:
        date_iso = datetime.strptime(src.get("createdAt", ""), "%a %b %d %H:%M:%S %z %Y") \
            .astimezone(timezone.utc).isoformat()
    except Exception:
        date_iso = ""
    text = re.sub(r"\s+", " ", src.get("text") or "").strip()
    return tid, {
        "id": tid,
        "date": date_iso,
        "author": author,
        "is_repost": bool(rt) or author.lower() != handle.lower(),
        "is_reply": bool(src.get("isReply")),
        "source": "x",
        "text": text,
        "url": f"https://x.com/{author}/status/{tid}",
    }


def fetch_x(handle, known_ids, key):
    """Page through the user's recent tweets until we reach already-stored ids
    or BACKFILL_DAYS. Returns {id: row}."""
    out, cursor = {}, ""
    cutoff = datetime.now(timezone.utc) - timedelta(days=BACKFILL_DAYS)
    for _ in range(MAX_PAGES):
        q = {"userName": handle}
        if cursor:
            q["cursor"] = cursor
        req = urllib.request.Request(
            f"{TWITTERAPI_URL}?{urllib.parse.urlencode(q)}",
            headers={"X-API-Key": key, "User-Agent": UA},
        )
        # twitterapi.io latency varies wildly (10-50s observed): long timeout + 1 retry.
        for attempt in (1, 2):
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    data = json.load(r)
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(5)
        if data.get("status") != "success":
            raise RuntimeError(f"twitterapi: {data.get('msg') or data}")
        tweets = (data.get("data") or {}).get("tweets") or data.get("tweets") or []
        reached_known = reached_cutoff = False
        for t in tweets:
            tid, row = _tweet_row(t, handle)
            if tid in known_ids:
                reached_known = True
            if row["date"] and datetime.fromisoformat(row["date"]) < cutoff:
                reached_cutoff = True
                continue
            out[tid] = row
        cursor = data.get("next_cursor") or ""
        if reached_known or reached_cutoff or not data.get("has_next_page") or not cursor:
            break
    return out


def _iso_date(raw):
    if not raw:
        return ""
    raw = raw.strip()
    try:  # RFC822 (RSS pubDate)
        return parsedate_to_datetime(raw).astimezone(timezone.utc).isoformat()
    except Exception:
        pass
    try:  # ISO 8601 (Atom published/updated)
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
    except Exception:
        return ""


def _strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def parse_blog(body, handle):
    """Parse an RSS <item> or Atom <entry> feed into store rows keyed by link."""
    root = ET.fromstring(body)
    out = {}
    entries = [e for e in root.iter() if e.tag.split("}")[-1] in ("item", "entry")]
    for e in entries:
        fields = {}
        for c in e:
            tag = c.tag.split("}")[-1]
            if tag == "link":
                # Atom: <link href="..."/>; RSS: <link>text</link>
                href = c.get("href") or (c.text or "")
                rel = c.get("rel", "alternate")
                if href and (tag not in fields or rel == "alternate"):
                    fields["link"] = href.strip()
            elif tag in ("title", "pubDate", "published", "updated", "description", "summary", "content"):
                fields.setdefault(tag, "".join(c.itertext()) if tag in ("content", "summary", "description") else (c.text or ""))
        link = fields.get("link", "")
        if not link:
            continue
        title = _strip_html(fields.get("title", ""))
        snippet = _strip_html(fields.get("description") or fields.get("summary") or fields.get("content") or "")[:220]
        text = f"{title} — {snippet}" if snippet else title
        date_iso = _iso_date(fields.get("pubDate") or fields.get("published") or fields.get("updated"))
        out[link] = {
            "id": link,
            "date": date_iso,
            "author": handle,
            "is_repost": False,
            "is_reply": False,
            "source": "blog",
            "text": text,
            "url": link,
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


def pull_account(handle, key):
    store_path = os.path.join(RAW_DIR, f"{handle}.jsonl")
    store = load_store(store_path)
    fresh, sources, errors = {}, [], []

    # X timeline via twitterapi.io
    if key:
        try:
            fresh.update(fetch_x(handle, set(store), key))
            sources.append("twitterapi.io")
        except Exception as e:
            errors.append(f"x: {e}")
    else:
        errors.append("x: no TWITTERAPI_KEY / key file")

    # First-party blog feed (primary live source for handles that have one)
    if handle in BLOG_FEEDS:
        url = BLOG_FEEDS[handle]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                fresh.update(parse_blog(r.read(), handle))
            sources.append(url)
        except Exception as e:
            errors.append(f"blog: {e}")

    if not sources:
        raise RuntimeError("; ".join(errors) or "no sources configured")

    added = [k for k in fresh if k not in store]
    store.update(fresh)  # refresh text/date for existing too
    rows = sorted(store.values(), key=lambda o: (o["date"], o["id"]), reverse=True)
    with open(store_path, "w") as f:
        for o in rows:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    return {
        "source": ", ".join(sources),
        "errors": errors or None,
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
    key = api_key()
    meta = {"last_pull_utc": datetime.now(timezone.utc).isoformat(), "accounts": {}}
    failures = 0
    for i, handle in enumerate(ACCOUNTS):
        if i:
            time.sleep(FETCH_DELAY_S)
        try:
            info = pull_account(handle, key)
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
