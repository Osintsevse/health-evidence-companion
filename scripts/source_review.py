"""Offline review queue for public source metadata. No network or registry mutation."""
import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def review_queue(sources, as_of, interval_days=90):
    if interval_days < 1:
        raise ValueError("interval_days must be positive")
    seen = set()
    rows = []
    for source in sources:
        identifier = source["id"]
        if identifier in seen:
            raise ValueError("Duplicate source ID")
        seen.add(identifier)
        checked = dt.date.fromisoformat(source["checked_on"])
        if checked > as_of:
            raise ValueError("Check date is after requested as-of date")
        due = checked + dt.timedelta(days=interval_days)
        limited = bool(re.search(r"blocked|failed|403|429|captcha|indexed.only|index.only|abstract.only|not.*read|not.*apprais|excerpt", source["retrieval_status"], re.I))
        rows.append({
            "id": identifier, "title": source["title"], "url": source["url"],
            "region": source["region"], "last_recorded_check": checked.isoformat(),
            "reading_status": source["retrieval_status"], "purpose": source["use"],
            "planned_review_on": due.isoformat(), "due": due <= as_of,
            "limited_access_or_reading": limited
        })
    return sorted(rows, key=lambda r: (not r["due"], not r["limited_access_or_reading"], r["planned_review_on"], int(r["id"][1:])))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--interval-days", type=int, default=90)
    args = parser.parse_args()
    sources = json.loads((ROOT / "knowledge/sources.json").read_text(encoding="utf-8"))
    print(json.dumps({"as_of": args.as_of.isoformat(), "interval_days": args.interval_days,
        "scope": "Offline planning only; not live verification or a scheduled monitor",
        "sources": review_queue(sources, args.as_of, args.interval_days)}, indent=2, ensure_ascii=True))

if __name__ == "__main__":
    main()
