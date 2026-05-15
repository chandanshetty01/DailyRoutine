#!/usr/bin/env python3
"""
SEC EDGAR filings helper for the ipo-watch routine.

Hits the public EDGAR full-text search and company-submission APIs
directly via requests (no SDK install needed beyond `requests`). SEC
requires a real User-Agent string with contact info per their fair-
access policy.

Usage examples:
    python3 sec_filings.py recent --forms S-1 F-1 --days 2
    python3 sec_filings.py recent --forms 8-K --days 1
    python3 sec_filings.py company TSLA --forms 8-K --days 30
    python3 sec_filings.py ai-quantum --days 3

Output: JSON to stdout. Errors fail-soft.
"""
import sys
import json
import argparse
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "missing dependency",
        "fix": "pip install --user --quiet requests"
    }), file=sys.stderr)
    sys.exit(2)


# SEC requires a contact-bearing UA string; replace if you fork
SEC_UA = "ipo-watch routine chandanshetty01@gmail.com"
HEADERS = {"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}

EDGAR_SEARCH = "https://efts.sec.gov/LATEST/search-index"
COMPANY_TICKERS = "https://www.sec.gov/files/company_tickers.json"
COMPANY_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"


def _date_str(d):
    return d.strftime("%Y-%m-%d")


def recent(forms, days_back=2, q=""):
    """Recent filings of given form types within the last N days."""
    end = datetime.utcnow().date()
    start = end - timedelta(days=days_back)
    out = []
    for form in forms:
        try:
            params = {
                "forms": form,
                "dateRange": "custom",
                "startdt": _date_str(start),
                "enddt": _date_str(end),
            }
            if q:
                params["q"] = q
            r = requests.get(EDGAR_SEARCH, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            for hit in data.get("hits", {}).get("hits", []):
                src = hit.get("_source", {})
                adsh = hit.get("_id", "").split(":")[0]
                cik = src.get("ciks", [None])[0]
                out.append({
                    "form": form,
                    "company": ", ".join(src.get("display_names", [])),
                    "filed_date": src.get("file_date"),
                    "accession": adsh,
                    "link": _filing_index_url(cik, adsh) if cik and adsh else None,
                })
        except Exception as e:
            out.append({"form": form, "error": str(e)})
    return out


def _filing_index_url(cik, accession):
    try:
        cik_int = int(cik)
        no_dashes = accession.replace("-", "")
        return f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_int}&type=&dateb=&owner=include&count=40"
    except Exception:
        return None


def ticker_to_cik(ticker):
    try:
        r = requests.get(COMPANY_TICKERS, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        for v in data.values():
            if v.get("ticker", "").upper() == ticker.upper():
                return f"{v['cik_str']:010d}"
        return None
    except Exception:
        return None


def company(ticker, forms, days_back=30):
    """All recent filings for one company (by ticker)."""
    cik = ticker_to_cik(ticker)
    if not cik:
        return {"error": f"no CIK for ticker {ticker}"}
    try:
        url = COMPANY_SUBMISSIONS.format(cik=cik)
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        data = r.json()
        filings = data.get("filings", {}).get("recent", {})
        cutoff = (datetime.utcnow().date() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        out = []
        for i, form in enumerate(filings.get("form", [])):
            if form not in forms:
                continue
            filing_date = filings.get("filingDate", [None])[i]
            if not filing_date or filing_date < cutoff:
                continue
            accession = filings.get("accessionNumber", [None])[i]
            primary_doc = filings.get("primaryDocument", [""])[i]
            no_dashes = accession.replace("-", "") if accession else ""
            link = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{no_dashes}/{primary_doc}"
                    if accession and primary_doc else None)
            out.append({
                "form": form,
                "filing_date": filing_date,
                "accession": accession,
                "link": link,
            })
        return {"ticker": ticker.upper(), "cik": cik, "filings": out}
    except Exception as e:
        return {"error": str(e)}


def ai_quantum(days_back=3):
    """Recent S-1/F-1 filings whose company name suggests AI / quantum / robotics."""
    keywords = [
        "AI", "ARTIFICIAL INTELLIGENCE", "QUANTUM", "QBIT", "QUBIT",
        "MACHINE LEARNING", "DEEP LEARNING", "NEURAL", "ROBOTICS",
        "AUTONOMOUS", "LLM", "GENAI", "GEN-AI"
    ]
    all_filings = recent(["S-1", "F-1", "S-1/A", "F-1/A", "DRSLTR", "424B"], days_back=days_back)
    matched = []
    for f in all_filings:
        if f.get("error"):
            continue
        name_upper = (f.get("company") or "").upper()
        if any(kw in name_upper for kw in keywords):
            matched.append(f)
    return matched


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    pr = sub.add_parser("recent")
    pr.add_argument("--forms", nargs="+", default=["S-1", "F-1", "8-K"])
    pr.add_argument("--days", type=int, default=2)
    pr.add_argument("--query", default="")

    pc = sub.add_parser("company")
    pc.add_argument("ticker")
    pc.add_argument("--forms", nargs="+", default=["8-K", "10-Q", "10-K", "S-1", "F-1"])
    pc.add_argument("--days", type=int, default=30)

    pa = sub.add_parser("ai-quantum")
    pa.add_argument("--days", type=int, default=3)

    a = p.parse_args()

    if a.command == "recent":
        out = recent(a.forms, a.days, a.query)
    elif a.command == "company":
        out = company(a.ticker, a.forms, a.days)
    elif a.command == "ai-quantum":
        out = ai_quantum(a.days)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
