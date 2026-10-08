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

def combined_review_queue(catalog, as_of, interval_days=90, domain='all'):
    if domain not in ('all','medical','psychology'):raise ValueError('Unknown source domain')
    result=[]
    for namespace in ('medical','psychology'):
        if domain not in ('all',namespace):continue
        sources=[{'id':row['id'],'title':row['title'],'url':row['url'],
                  'checked_on':row['checked_on'],'region':row['region'],
                  'retrieval_status':row['reading_status']+'; '+row['limitations'],
                  'use':row['purpose']} for row in catalog['records'] if row['namespace']==namespace]
        for row in review_queue(sources,as_of,interval_days):
            row['namespace']=namespace;row['qualified_id']=namespace+':'+row['id'];result.append(row)
    return sorted(result,key=lambda row:(not row['due'],not row['limited_access_or_reading'],row['planned_review_on'],row['qualified_id']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--interval-days", type=int, default=90)
    parser.add_argument("--domain",choices=("all","medical","psychology"),default="all")
    parser.add_argument("--catalog",type=Path,help="Public compiled catalog; defaults to bundled references or canonical knowledge")
    args = parser.parse_args()
    catalog_path=args.catalog or (ROOT/"knowledge/source-catalog.json" if (ROOT/"knowledge/source-catalog.json").is_file() else ROOT/"references/source-catalog.json")
    sources = json.loads(catalog_path.read_text(encoding="utf-8"))
    print(json.dumps({"as_of": args.as_of.isoformat(), "interval_days": args.interval_days,
        "scope": "Offline planning only; not live verification or a scheduled monitor",
        "domain":args.domain, "sources": combined_review_queue(sources, args.as_of, args.interval_days,args.domain)}, indent=2, ensure_ascii=True))

if __name__ == "__main__":
    main()
