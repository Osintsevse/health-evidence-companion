"""Regenerate source CSV/map from the English canonical JSON register."""
import csv
import json
from pathlib import Path
from source_policy import source_use

ROOT = Path(__file__).resolve().parents[1]


def update(root=ROOT):
    sources = json.loads((root / 'knowledge/sources.json').read_text(encoding='utf-8'))
    policy = json.loads((root / 'knowledge/clinical/source-use-policy.json').read_text(encoding='utf-8'))
    fields = ['id', 'title', 'url', 'region', 'retrieval_status', 'use', 'checked_on']
    with (root / 'knowledge/sources.csv').open('w', newline='', encoding='utf-8') as f:
        # Keep generated text files LF-normalized so `git diff --check` does not
        # treat csv.writer's platform-independent CRLF terminator as whitespace.
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(sources)
    lines = ['# Source map', '',
             'Canonical register: knowledge/sources.json. Reading status records actual scope; a link is not a completed course or live API test.', '',
             '## Verification order', '',
             'Use the current applicable guideline and exact local product label first: ALIMS for Serbia; GRLS and the clinical guideline catalogue for Russia. Use WHO and specialist guidance within the source-use policy. Policy-held NICE works remain bibliographic pointers only pending matching permission. Reviews and primary studies address uncertain benefits. ICD classifies conditions; it does not choose treatment.', '',
             'Check date, version, population, setting and the section actually read. Disclose access failures. Vendor pages establish claimed features, not clinical accuracy; registration does not establish availability. Historical dosing needs current verification.', '',
             'Use MSD/NHS/MedlinePlus for explanation and verify against guidance for care decisions. Pharmacies, aggregators and other AI answers are navigation aids, not final evidence. Keep availability, registration, authorized indication and demonstrated benefit distinct. Explain differences between jurisdictions using the actual document and evidence level.', '',
             '## Search procedure', '',
             'Frame population/problem, intervention, comparator and desired outcome. Search condition names/synonyms in English, Serbian and Russian; search medicines by INN, brand, formulation and concentration. For ALIMS, use product name plus uputstvo za lek or sazetak karakteristika leka, then inspect relevant SmPC sections 4.1-4.8. For Russia, use the official guideline catalogue and GRLS; check adult scope, year and version.', '',
             'For a technical access failure, record it and use an independently permitted primary source. A rights restriction is not bypassed through another format, mirror or search excerpt. Label a search excerpt as an excerpt, never reconstruct a missing dose by guessing. Recheck contraindications and local applicability for each new medicine/interaction question. Save original concise notes with URL, date and limits; do not redistribute protected full texts.', '',
             'Modules 11-12 cover pharmacology/interactions, 08 covers AI/APIs and 14 covers record design. Modules 15-18 expand allergy, laboratory literacy, vaccination and treatment evidence. Secondary discovery lists are marked and do not support final efficacy classifications. Live clinical accuracy of APIs/models was not tested; reading depth and unavailable databases remain explicit in this register.', '',
             'The clinical navigation extension has additional reading records in knowledge/clinical/source-review.json, distributed as source-review.json in medical skill references. It preserves later section reviews and rights limits without rewriting historical IDs or claiming entire guidelines/textbooks were read. CLINICAL_INDEX.md connects topic, route and evidence scope; a navigation class atlas requires current exact-label retrieval before personal application.', '',
             '## Entries', '']
    for s in sources:
        lines.extend([f"### {s['id']} - {s['title']}", f"- URL: {s['url']}",
                      f"- Region: {s['region']}", f"- Reading status: {s['retrieval_status']}",
                      f"- Purpose: {s['use']}", f"- Checked: {s['checked_on']}",
                      f"- Active-use disposition: {source_use(s, 'medical', policy)['active_use']} (not a permission grant)", ''])
    (root / 'knowledge/01_SOURCE_MAP.md').write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8', newline='\n')
    from source_catalog import update as update_catalog
    update_catalog(root)


if __name__ == '__main__':
    update()
