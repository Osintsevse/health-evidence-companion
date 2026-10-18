"""Report policy holds and reject unmarked active citations; no rights grant."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def matching_rules(url, policy):
    parsed = urlparse(url)
    hostname = (parsed.hostname or '').lower()
    return [rule for rule in policy.get('rules', [])
            if (hostname == rule['host_suffix'] or hostname.endswith('.' + rule['host_suffix']))
            and parsed.path.startswith(rule.get('path_prefix', '/'))
            and not rule.get('verified_permission_available', False)]


def source_use(source, namespace, policy):
    matches = matching_rules(source['url'], policy)
    qualified = namespace + ':' + source['id']
    # These explicit records describe a rights notice, not its clinical contents.
    rights_metadata = qualified in {'medical:S84', 'medical:S360', 'medical:S521'}
    return {'active_use': 'rights_metadata_only' if matches and rights_metadata else
            'bibliographic_only' if matches else 'not_determined',
            'source_use_rule_ids': [rule['id'] for rule in matches],
            'permission_inferred': False}


def cited_ids(text, domain):
    """Qualified IDs and bounded same-domain ranges; never mix namespaces."""
    found = set(re.findall(r'\b(?:medical|psychology):S\d+\b', text))
    found.update(domain + ':' + sid for sid in re.findall(r'(?<![:\w])S\d+\b', text))
    for left, right in re.findall(r'(?<![:\w])S(\d+)\s*[-\u2013\u2014]\s*S(\d+)\b', text):
        a, b = int(left), int(right)
        if 0 <= b - a <= 100:
            found.update(domain + ':S' + str(n).zfill(2) for n in range(a, b + 1))
    return found


def validate_active_citations(root):
    root = Path(root)
    policy = json.loads((root/'knowledge/clinical/source-use-policy.json').read_text(encoding='utf-8'))
    medical = json.loads((root/'knowledge/sources.json').read_text(encoding='utf-8'))
    psychology = json.loads((root/'knowledge/psychology/sources.json').read_text(encoding='utf-8'))['sources']
    held = {domain + ':' + item['id']
            for domain, records in [('medical', medical), ('psychology', psychology)]
            for item in records if source_use(item, domain, policy)['active_use'] == 'bibliographic_only'}
    problems = []
    for path in sorted((root/'knowledge').rglob('*.md')):
        if path.name in {'01_SOURCE_MAP.md', 'SOURCES.md', 'CHANGELOG.md', 'QUALITY_REVIEW.md'}:
            continue
        domain = 'psychology' if 'psychology' in path.relative_to(root/'knowledge').parts else 'medical'
        for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8')):
            # A URL slug/title is metadata, not a citation to a clinical claim.
            citation_text = re.sub(r'https?://\S+', '', block)
            ids = held & cited_ids(citation_text, domain)
            if not ids:
                continue
            lines = block.strip().splitlines()
            metadata_rows = all(not line.strip() or line.startswith('#') or
                                re.match(r'^- S\d+: \[', line) for line in lines)
            explicitly_passive = bool(re.search(r'bibliographic.{0,45}(?:only|pointer)|(?:only|historical).{0,30}bibliographic|not active (?:clinical )?(?:evidence|support)', block, re.I))
            if not metadata_rows and not explicitly_passive:
                problems.append({'path':path.relative_to(root).as_posix(),
                                 'source_ids':sorted(ids), 'text':block[:500]})
    for relative,key in [('knowledge/clinical/routes.json','routes'), ('evals/medical-expansion/cases.json','cases')]:
        path=root/relative
        if path.exists():
            for record in json.loads(path.read_text(encoding='utf-8')).get(key,[]):
                ids=held & {'medical:'+sid for sid in record.get('source_ids',[])}
                if ids:problems.append({'path':relative,'record_id':record['id'],'source_ids':sorted(ids)})
    if problems:
        raise ValueError('Unmarked active use of policy-held sources: ' + json.dumps(problems, ensure_ascii=True))
    return {'policy_held_records':len(held),
            'scope':'Citation/marker consistency only; a passive marker does not validate prose, rights or clinical support.'}
