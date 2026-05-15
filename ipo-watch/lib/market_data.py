#!/usr/bin/env python3
"""
Market data helper for the ipo-watch routine.

Wraps yfinance with a small JSON CLI so the routine can pull real
historical prices, options IV, and day-of-week stats instead of
guessing via WebSearch.

Usage examples:
    python3 market_data.py snapshot TSLA CBRS
    python3 market_data.py history TSLA --days 365
    python3 market_data.py options TSLA
    python3 market_data.py dow-stats TSLA --years 2
    python3 market_data.py all TSLA CBRS

Output: JSON to stdout. Errors as {"error": "..."} per ticker;
never raises uncaught exceptions so the routine can fail-soft.
"""
import sys
import json
import argparse
from datetime import datetime

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np  # noqa: F401
except ImportError:
    print(json.dumps({
        "error": "missing dependencies",
        "fix": "pip install --user --quiet yfinance pandas numpy"
    }), file=sys.stderr)
    sys.exit(2)


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def snapshot(tickers):
    """Latest close, day's change %, volume vs 20-day avg."""
    out = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="60d", auto_adjust=True)
            if hist.empty:
                out[ticker] = {"error": "no data"}
                continue
            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) >= 2 else latest
            close = float(latest["Close"])
            prev_close = float(prev["Close"])
            day_change_pct = (close / prev_close - 1) * 100 if prev_close else 0
            volume = int(latest["Volume"])
            avg_vol_20d = int(hist["Volume"].tail(20).mean())
            ratio = volume / avg_vol_20d if avg_vol_20d else 1
            label = "above avg" if ratio > 1.2 else "below avg" if ratio < 0.8 else "in-line"
            out[ticker] = {
                "close": round(close, 2),
                "prev_close": round(prev_close, 2),
                "day_change_pct": round(day_change_pct, 2),
                "volume": volume,
                "avg_volume_20d": avg_vol_20d,
                "volume_vs_avg_ratio": round(ratio, 2),
                "volume_label": label,
                "as_of_date": latest.name.strftime("%Y-%m-%d"),
            }
        except Exception as e:
            out[ticker] = {"error": str(e)}
    return out


def history_levels(ticker, days=365):
    """52-wk range, 200d MA, ATH, recent realized vol."""
    try:
        t = yf.Ticker(ticker)
        hist_1y = t.history(period="1y", auto_adjust=True)
        hist_max = t.history(period="max", auto_adjust=True)
        if hist_1y.empty:
            return {"error": "no 1y data"}
        close = hist_1y["Close"]
        returns = close.pct_change().dropna().tail(20)
        rv_daily_pct = float(returns.std() * 100) if len(returns) > 1 else None
        ma_200 = float(close.tail(200).mean()) if len(close) >= 200 else None
        ath = float(hist_max["Close"].max())
        ath_date = hist_max["Close"].idxmax().strftime("%Y-%m-%d")
        return {
            "ticker": ticker,
            "low_52w": round(float(close.min()), 2),
            "high_52w": round(float(close.max()), 2),
            "ma_200d": round(ma_200, 2) if ma_200 else None,
            "all_time_high": round(ath, 2),
            "ath_date": ath_date,
            "realized_vol_20d_daily_pct": round(rv_daily_pct, 2) if rv_daily_pct else None,
            "trading_days_in_max_history": len(hist_max),
        }
    except Exception as e:
        return {"error": str(e)}


def options_iv(ticker):
    """Implied move from nearest-expiry ATM straddle.

    Returns expected 1-σ price range for one trading day ahead, scaled
    from the front-month implied vol.
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="5d", auto_adjust=True)
        if hist.empty:
            return {"error": "no spot"}
        spot = float(hist["Close"].iloc[-1])

        expirations = t.options
        if not expirations:
            return {"error": "no options listed"}

        # Use nearest expiration that's at least 1 day out
        nearest = None
        for e in expirations:
            try:
                d = datetime.strptime(e, "%Y-%m-%d")
                if (d - datetime.now()).days >= 1:
                    nearest = e
                    break
            except Exception:
                continue
        if not nearest:
            nearest = expirations[0]

        chain = t.option_chain(nearest)
        calls = chain.calls
        puts = chain.puts
        if calls.empty or puts.empty:
            return {"error": "no chain data"}

        atm_strike = float(calls.iloc[(calls["strike"] - spot).abs().argsort()[:1]]["strike"].iloc[0])
        atm_call = calls[calls["strike"] == atm_strike].iloc[0]
        atm_put = puts[puts["strike"] == atm_strike].iloc[0]

        def _mid(row):
            bid = float(row["bid"]) if row["bid"] > 0 else 0
            ask = float(row["ask"]) if row["ask"] > 0 else 0
            if bid > 0 and ask > 0:
                return (bid + ask) / 2
            return float(row["lastPrice"])

        straddle = _mid(atm_call) + _mid(atm_put)
        period_move_pct = (straddle / spot) * 100

        days_to_expiry = (datetime.strptime(nearest, "%Y-%m-%d") - datetime.now()).days
        days_to_expiry = max(days_to_expiry, 1)
        daily_move_pct = period_move_pct / (days_to_expiry ** 0.5)

        atm_iv_call = float(atm_call.get("impliedVolatility", 0)) if pd.notna(atm_call.get("impliedVolatility")) else 0
        atm_iv_put = float(atm_put.get("impliedVolatility", 0)) if pd.notna(atm_put.get("impliedVolatility")) else 0
        atm_iv_annual = ((atm_iv_call + atm_iv_put) / 2) * 100 if (atm_iv_call or atm_iv_put) else None

        return {
            "ticker": ticker,
            "spot": round(spot, 2),
            "nearest_expiry": nearest,
            "days_to_expiry": days_to_expiry,
            "atm_strike": atm_strike,
            "straddle_mid_price": round(straddle, 2),
            "implied_move_period_pct": round(period_move_pct, 2),
            "implied_move_daily_pct": round(daily_move_pct, 3),
            "atm_iv_annualized_pct": round(atm_iv_annual, 2) if atm_iv_annual else None,
            "tomorrow_range_low": round(spot * (1 - daily_move_pct / 100), 2),
            "tomorrow_range_high": round(spot * (1 + daily_move_pct / 100), 2),
            "qualifier": "1-σ; about 2-of-3 chance of closing in this range",
        }
    except Exception as e:
        return {"error": str(e)}


def dow_stats(ticker, years=2):
    """Stock-specific day-of-week return distribution from history."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=f"{years}y", auto_adjust=True)
        if hist.empty or len(hist) < 50:
            return {"error": "insufficient history"}
        df = hist[["Close"]].copy()
        df["ret"] = df["Close"].pct_change()
        df["dow"] = df.index.dayofweek
        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        out_by_day = {}
        for i, name in enumerate(labels):
            d = df[df["dow"] == i]["ret"].dropna()
            if len(d) >= 10:
                out_by_day[name] = {
                    "count": int(len(d)),
                    "mean_return_bps": round(float(d.mean()) * 10000, 1),
                    "std_pct": round(float(d.std()) * 100, 2),
                    "pct_positive_days": round(float((d > 0).mean()) * 100, 1),
                }
        return {"ticker": ticker, "lookback_years": years, "by_day": out_by_day}
    except Exception as e:
        return {"error": str(e)}


def all_in_one(ticker):
    return {
        "snapshot": snapshot([ticker]).get(ticker, {}),
        "history": history_levels(ticker),
        "options": options_iv(ticker),
        "dow_stats": dow_stats(ticker),
    }


def main():
    p = argparse.ArgumentParser(description="Market data helper for ipo-watch routine.")
    p.add_argument("command", choices=["snapshot", "history", "options", "dow-stats", "all"])
    p.add_argument("tickers", nargs="+", help="One or more tickers")
    p.add_argument("--years", type=int, default=2)
    p.add_argument("--days", type=int, default=365)
    a = p.parse_args()

    if a.command == "snapshot":
        out = snapshot(a.tickers)
    elif a.command == "history":
        out = {t: history_levels(t, a.days) for t in a.tickers}
    elif a.command == "options":
        out = {t: options_iv(t) for t in a.tickers}
    elif a.command == "dow-stats":
        out = {t: dow_stats(t, a.years) for t in a.tickers}
    elif a.command == "all":
        out = {t: all_in_one(t) for t in a.tickers}

    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
