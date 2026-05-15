#!/usr/bin/env python3
"""
Forecast accuracy tracking + self-audit for the ipo-watch routine.

Every Tomorrow-range prediction is logged. Each subsequent run looks up
the actual close on the predicted-for date and scores the prediction
(hit / miss + how far). After ~10 predictions per ticker, the routine
can surface systematic biases (ranges too narrow, asymmetric skew,
weak catalyst handling) so the prompt can be improved deliberately by
the user — not auto-modified by the routine.

Storage: `ipo-watch/lib/forecast-log.jsonl` (one JSON record per line,
append-only, committed to the repo for full transparency).

Usage:
    # Log a new prediction (call this after building today's Tomorrow bullet):
    python3 forecast_audit.py log TSLA --low 307.42 --high 324.18 \\
        --for-date 2026-05-15 --method options_iv --skew "Wed FOMC"

    # Fill in actuals for predictions whose target date is past:
    python3 forecast_audit.py evaluate

    # Get rolling 30-day accuracy stats per ticker:
    python3 forecast_audit.py stats --days 30

    # Surface systematic biases (run weekly):
    python3 forecast_audit.py audit
"""
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

LOG_FILE = Path(__file__).parent / "forecast-log.jsonl"

try:
    import yfinance as yf
except ImportError:
    yf = None


def _read_log():
    if not LOG_FILE.exists():
        return []
    out = []
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _write_log(records):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def log_prediction(ticker, low, high, for_date, method="options_iv", skew_factors=None):
    """Append a new prediction record."""
    rec = {
        "predicted_on": datetime.utcnow().strftime("%Y-%m-%d"),
        "predicted_for_close": for_date,
        "ticker": ticker.upper(),
        "range_low": float(low),
        "range_high": float(high),
        "midpoint": round((float(low) + float(high)) / 2, 2),
        "method": method,
        "skew_factors": skew_factors or [],
        "actual_close": None,
        "hit": None,
        "close_position_in_range": None,
        "miss_pct": None,
    }
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def evaluate_pending():
    """For each unfilled prediction whose target date is past (and US market traded),
    look up actual close and score the prediction. Weekend/holiday targets roll
    to the next trading day automatically (yfinance returns first available bar)."""
    if yf is None:
        return {"error": "yfinance not installed; cannot evaluate"}
    records = _read_log()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    updated = 0
    skipped = 0
    for r in records:
        if r.get("actual_close") is not None:
            continue
        for_date = r.get("predicted_for_close")
        if not for_date or for_date >= today:
            continue
        try:
            t = yf.Ticker(r["ticker"])
            end = (datetime.strptime(for_date, "%Y-%m-%d") + timedelta(days=5)).strftime("%Y-%m-%d")
            hist = t.history(start=for_date, end=end, auto_adjust=True)
            if hist.empty:
                skipped += 1
                continue
            actual_close = float(hist["Close"].iloc[0])
            r["actual_close"] = round(actual_close, 2)
            r["hit"] = (r["range_low"] <= actual_close <= r["range_high"])
            range_size = r["range_high"] - r["range_low"]
            if range_size > 0:
                r["close_position_in_range"] = round((actual_close - r["range_low"]) / range_size, 2)
            if r["hit"]:
                r["miss_pct"] = 0.0
            else:
                if actual_close > r["range_high"]:
                    r["miss_pct"] = round((actual_close - r["range_high"]) / r["range_high"] * 100, 2)
                else:
                    r["miss_pct"] = round((r["range_low"] - actual_close) / r["range_low"] * 100, 2)
            updated += 1
        except Exception:
            skipped += 1
            continue
    _write_log(records)
    return {"evaluated": updated, "skipped": skipped, "total_records": len(records)}


def latest_for(ticker):
    """Get the most recent evaluated prediction for a ticker. Used by the routine
    to surface 'Yesterday's call' in the Buying Window block."""
    records = _read_log()
    evaluated = [r for r in records if r.get("ticker") == ticker.upper() and r.get("actual_close") is not None]
    if not evaluated:
        return {"info": "no evaluated predictions yet"}
    evaluated.sort(key=lambda r: r.get("predicted_for_close", ""), reverse=True)
    return evaluated[0]


def rolling_stats(days=30):
    """Hit rate + miss-magnitude stats over last N days, per ticker."""
    records = _read_log()
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    evaluated = [r for r in records
                 if r.get("actual_close") is not None and r.get("predicted_on", "") >= cutoff]
    if not evaluated:
        return {"window_days": days, "info": "no evaluated predictions in window"}
    by_ticker = {}
    for r in evaluated:
        t = r["ticker"]
        by_ticker.setdefault(t, {"hits": 0, "misses": 0, "miss_pcts": [], "positions": []})
        if r["hit"]:
            by_ticker[t]["hits"] += 1
        else:
            by_ticker[t]["misses"] += 1
        if r.get("miss_pct") is not None:
            by_ticker[t]["miss_pcts"].append(r["miss_pct"])
        if r.get("close_position_in_range") is not None:
            by_ticker[t]["positions"].append(r["close_position_in_range"])
    stats = {"window_days": days, "by_ticker": {}}
    for t, d in by_ticker.items():
        total = d["hits"] + d["misses"]
        hr = d["hits"] / total if total else 0
        avg_miss = sum(d["miss_pcts"]) / len(d["miss_pcts"]) if d["miss_pcts"] else 0
        avg_pos = (sum(d["positions"]) / len(d["positions"])) if d["positions"] else None
        cal = "insufficient samples"
        if total >= 5:
            if abs(hr - 0.68) < 0.10:
                cal = "well-calibrated"
            elif hr < 0.58:
                cal = "ranges too narrow (more misses than expected)"
            elif hr > 0.78:
                cal = "ranges too wide (fewer misses than expected)"
            else:
                cal = "borderline"
        stats["by_ticker"][t] = {
            "samples": total,
            "hit_rate_pct": round(hr * 100, 1),
            "expected_hit_rate_pct": 68.0,
            "avg_miss_when_outside_pct": round(avg_miss, 2),
            "avg_close_position_when_inside": round(avg_pos, 2) if avg_pos is not None else None,
            "calibration": cal,
        }
    return stats


def audit_patterns():
    """Surface systematic biases — INFORMATIONAL ONLY. Routine should NEVER
    auto-modify the prompt; surface findings to the user instead."""
    records = _read_log()
    evaluated = [r for r in records if r.get("actual_close") is not None]
    if len(evaluated) < 10:
        return {"info": f"only {len(evaluated)} evaluated predictions; need ~10+ before audit is meaningful"}

    findings = []

    # Pattern 1: overall hit rate too low / too high
    hits = sum(1 for r in evaluated if r["hit"])
    hr = hits / len(evaluated)
    if hr < 0.55:
        findings.append({
            "pattern": "ranges_too_narrow",
            "evidence": f"Hit rate {hr:.1%} on {len(evaluated)} predictions (expected ~68% for 1-σ).",
            "suggestion": "Widen base 1-σ multiplier or improve skew adjustment.",
        })
    elif hr > 0.80:
        findings.append({
            "pattern": "ranges_too_wide",
            "evidence": f"Hit rate {hr:.1%} on {len(evaluated)} predictions (expected ~68% for 1-σ).",
            "suggestion": "Tighten ranges by 10-20% or remove redundant skew widening.",
        })

    # Pattern 2: asymmetric position-in-range
    inside = [r for r in evaluated if r["hit"] and r.get("close_position_in_range") is not None]
    if len(inside) >= 10:
        avg_pos = sum(r["close_position_in_range"] for r in inside) / len(inside)
        if avg_pos > 0.65:
            findings.append({
                "pattern": "upward_skew_undermodeled",
                "evidence": f"Avg position-in-range = {avg_pos:.2f} on {len(inside)} hits (expected ~0.50).",
                "suggestion": "Methodology is under-estimating upside; consider asymmetric skew when bullish catalysts present.",
            })
        elif avg_pos < 0.35:
            findings.append({
                "pattern": "downward_skew_undermodeled",
                "evidence": f"Avg position-in-range = {avg_pos:.2f} on {len(inside)} hits.",
                "suggestion": "Methodology is under-estimating downside; add downside-skew on negative-catalyst days.",
            })

    # Pattern 3: catalyst-day handling
    cat = [r for r in evaluated if r.get("skew_factors")]
    quiet = [r for r in evaluated if not r.get("skew_factors")]
    if len(cat) >= 5 and len(quiet) >= 5:
        cat_hr = sum(1 for r in cat if r["hit"]) / len(cat)
        quiet_hr = sum(1 for r in quiet if r["hit"]) / len(quiet)
        if quiet_hr - cat_hr > 0.15:
            findings.append({
                "pattern": "catalyst_widening_too_small",
                "evidence": f"Catalyst-day hit rate {cat_hr:.1%} vs quiet-day {quiet_hr:.1%}; catalyst widening insufficient.",
                "suggestion": "Widen ranges more aggressively on flagged-catalyst days (e.g., 1.5× base on FOMC/earnings).",
            })

    # Pattern 4: per-ticker calibration drift
    by_t = {}
    for r in evaluated:
        by_t.setdefault(r["ticker"], []).append(r)
    per_ticker_issues = []
    for t, recs in by_t.items():
        if len(recs) >= 8:
            tickr = sum(1 for r in recs if r["hit"]) / len(recs)
            if tickr < 0.50:
                per_ticker_issues.append(f"{t}: {tickr:.0%} hit rate on {len(recs)} samples")
    if per_ticker_issues:
        findings.append({
            "pattern": "per_ticker_underperformance",
            "evidence": "; ".join(per_ticker_issues),
            "suggestion": "Specific ticker(s) need separate calibration — possibly switch methodology (e.g. options→realized-vol or vice versa).",
        })

    return {
        "evaluated_total": len(evaluated),
        "overall_hit_rate_pct": round(hr * 100, 1),
        "findings": findings if findings else [{"info": "No systematic biases detected. Routine is well-calibrated."}],
        "next_review": "weekly Monday audit; trigger prompt edits only on persistent patterns (4+ weeks).",
    }


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    pl = sub.add_parser("log", help="Append a new prediction")
    pl.add_argument("ticker")
    pl.add_argument("--low", type=float, required=True)
    pl.add_argument("--high", type=float, required=True)
    pl.add_argument("--for-date", required=True, help="YYYY-MM-DD (next trading day)")
    pl.add_argument("--method", default="options_iv")
    pl.add_argument("--skew", action="append", default=[])

    sub.add_parser("evaluate", help="Fill in actuals for past predictions")
    sub.add_parser("audit", help="Surface systematic biases (run weekly)")

    pf = sub.add_parser("latest", help="Latest evaluated prediction for a ticker")
    pf.add_argument("ticker")

    ps = sub.add_parser("stats", help="Rolling accuracy stats")
    ps.add_argument("--days", type=int, default=30)

    a = p.parse_args()

    if a.command == "log":
        out = log_prediction(a.ticker, a.low, a.high, a.for_date, a.method, a.skew)
    elif a.command == "evaluate":
        out = evaluate_pending()
    elif a.command == "latest":
        out = latest_for(a.ticker)
    elif a.command == "stats":
        out = rolling_stats(a.days)
    elif a.command == "audit":
        out = audit_patterns()

    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
