"""Regenerate source CSV/map from the English canonical JSON register."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update(root=ROOT):
    sources = json.loads((root / 'knowledge/sources.json').read_text())
    fields = ['id', 'title', 'url', 'region', 'retrieval_status', 'use', 'checked_on']
    with (root / 'knowledge/sources.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sources)
    lines = ['# Source map', '',
             'Canonical register: knowledge/sources.json. Reading status records actual scope; a link is not a completed course or live API test.', '',
             '## Verification order', '',
             'Use the current applicable guideline and exact local product label first: ALIMS for Serbia; GRLS and the clinical guideline catalogue for Russia. WHO/NICE and specialist guidance provide context. Reviews and primary studies address uncertain benefits. ICD classifies conditions; it does not choose treatment.', '',
             'Check date, version, population, setting and the section actually read. Disclose access failures. Vendor pages establish claimed features, not clinical accuracy; registration does not establish availability. Historical dosing needs current verification.', '',
             'Use MSD/NHS/MedlinePlus for explanation and verify against guidance for care decisions. Pharmacies, aggregators and other AI answers are navigation aids, not final evidence. Keep availability, registration, authorized indication and demonstrated benefit distinct. Explain differences between jurisdictions using the actual document and evidence level.', '',
             '## Search procedure', '',
             'Frame population/problem, intervention, comparator and desired outcome. Search condition names/synonyms in English, Serbian and Russian; search medicines by INN, brand, formulation and concentration. For ALIMS, use product name plus uputstvo za lek or sazetak karakteristika leka, then inspect relevant SmPC sections 4.1-4.8. For Russia, use the official guideline catalogue and GRLS; check adult scope, year and version.', '',
             'If blocked, seek the official PDF or another primary source. Label a search excerpt as an excerpt, never reconstruct a missing dose by guessing. Recheck contraindications and local applicability for each new medicine/interaction question. Save original concise notes with URL, date and limits; do not redistribute protected full texts.', '',
             'Modules 11-12 cover pharmacology/interactions, 08 covers AI/APIs and 14 covers record design. Live clinical accuracy of APIs/models was not tested; reading depth and unavailable databases remain explicit in this register.', '',
             '## Entries', '']
    for s in sources:
        lines.extend([f"### {s['id']} - {s['title']}", f"- URL: {s['url']}",
                      f"- Region: {s['region']}", f"- Reading status: {s['retrieval_status']}",
                      f"- Purpose: {s['use']}", f"- Checked: {s['checked_on']}", ''])
    (root / 'knowledge/01_SOURCE_MAP.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    update()
