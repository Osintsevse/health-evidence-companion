"""Compile public source metadata without changing canonical IDs or review dates."""
import datetime
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

def catalog(root=ROOT):
    medical=json.loads((root/'knowledge/sources.json').read_text(encoding='utf-8'))
    psychological=json.loads((root/'knowledge/psychology/sources.json').read_text(encoding='utf-8'))
    from source_policy import source_use
    policy=json.loads((root/'knowledge/clinical/source-use-policy.json').read_text(encoding='utf-8'))
    records=[]
    for source in medical:
        records.append({'namespace':'medical','id':source['id'], 'qualified_id':'medical:'+source['id'],
            'title':source['title'],'url':source['url'],'checked_on':source['checked_on'],
            'reading_status':source['retrieval_status'],'limitations':source['retrieval_status'],
            'purpose':source['use'],'region':source['region'], 'canonical_path':'knowledge/sources.json', **source_use(source,'medical',policy)})
    for source in psychological['sources']:
        records.append({'namespace':'psychology','id':source['id'],'qualified_id':'psychology:'+source['id'],
            'title':source['title'],'url':source['url'],'checked_on':source['checked_at'],
            'reading_status':source['access'],'limitations':source['limitations'],
            'purpose':source['use'],'region':'Original psychological source applicability; inspect canonical record',
            'canonical_path':'knowledge/psychology/sources.json', **source_use(source,'psychology',policy)})
    identities=[row['qualified_id'] for row in records]
    if len(set(identities))!=len(identities):raise ValueError('Duplicate qualified source identifier')
    groups=defaultdict(list)
    for row in records:groups[row['url']].append(row['qualified_id'])
    return {'schema':'unified-source-catalog-v1','record_count':len(records),
        'unique_url_count':len(groups), 'records':records,
        'shared_urls':[{'url':url,'qualified_ids':ids} for url,ids in sorted(groups.items()) if len(ids)>1],
        'limitations':'Record and URL counts are not independent study counts. Import preserves historical reading scope, not a new literature review.'}


def validate_import_amendments(root=ROOT):
    """Preserve import pins; allow only exact, documented post-import byte changes."""
    root = Path(root).resolve()

    def check(condition, message):
        if not condition:
            raise ValueError(message)

    def relative_path(value):
        check(isinstance(value, str) and value, 'Invalid provenance path')
        path = PurePosixPath(value)
        check(path.parts and not path.is_absolute() and path.as_posix() == value
              and '..' not in path.parts and '\\' not in value and ':' not in value,
              f'Invalid provenance path: {value}')
        return path

    def checked_file(value):
        relative_path(value)
        path = (root / value).resolve()
        check(path.is_relative_to(root) and path.is_file(),
              f'Missing or unsafe provenance file: {value}')
        return path

    provenance = json.loads(checked_file('docs/psychology/import-provenance.json').read_text(encoding='utf-8'))
    originals = {}
    seen = set()
    for entry in provenance['files']:
        path = entry['destination_path']
        relative_path(path)
        check(path not in seen, f'Duplicate import provenance path: {path}')
        seen.add(path)
        check(isinstance(entry.get('sha256'), str) and re.fullmatch(r'[a-f0-9]{64}', entry['sha256']),
              f'Invalid original import hash: {path}')
        # Generated skill copies are checked against canonical files by reference synchronization.
        if not path.startswith('skills/'):
            originals[path] = entry['sha256']

    ledger_path = root / 'docs/psychology/post-import-amendments.json'
    ledger = (json.loads(checked_file('docs/psychology/post-import-amendments.json').read_text(encoding='utf-8'))
              if ledger_path.exists() else {'schema': 'psychology-post-import-amendments-v1', 'amendments': []})
    check(isinstance(ledger, dict) and set(ledger) == {'schema', 'amendments'}
          and ledger['schema'] == 'psychology-post-import-amendments-v1'
          and isinstance(ledger['amendments'], list), 'Invalid post-import amendment ledger')
    amendments = {}
    fields = {'path', 'original_import_sha256', 'current_sha256', 'date', 'reason', 'review_document'}
    for entry in ledger['amendments']:
        check(isinstance(entry, dict) and set(entry) == fields, 'Invalid amendment fields')
        path = entry['path']
        relative_path(path)
        check(path in originals, f'Unknown amendment path: {path}')
        check(path not in amendments, f'Duplicate amendment path: {path}')
        check(entry['original_import_sha256'] == originals[path], f'Original import hash mismatch: {path}')
        check(isinstance(entry['current_sha256'], str) and re.fullmatch(r'[a-f0-9]{64}', entry['current_sha256']),
              f'Invalid current amendment hash: {path}')
        check(entry['current_sha256'] != originals[path], f'Redundant amendment for unchanged import: {path}')
        check(isinstance(entry['date'], str), f'Invalid amendment date: {path}')
        try:
            date = datetime.date.fromisoformat(entry['date'])
        except ValueError as error:
            raise ValueError(f'Invalid amendment date: {path}') from error
        check(date.isoformat() == entry['date'], f'Invalid amendment date: {path}')
        check(isinstance(entry['reason'], str) and entry['reason'].strip(), f'Missing amendment reason: {path}')
        review = relative_path(entry['review_document'])
        check(review.parts[0] == 'docs' and review.suffix == '.md', f'Invalid amendment review document: {path}')
        checked_file(entry['review_document'])
        amendments[path] = entry

    for path, original in originals.items():
        actual = hashlib.sha256(checked_file(path).read_bytes()).hexdigest()
        if path in amendments:
            check(actual == amendments[path]['current_sha256'], f'Current amendment hash mismatch: {path}')
        else:
            check(actual == original, f'Undocumented imported source change: {path}')
    return {'imported_files': len(originals), 'amended_files': len(amendments),
            'unchanged_files': len(originals) - len(amendments)}


def update(root=ROOT):
    result=catalog(root)
    (root/'knowledge/source-catalog.json').write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n',encoding='utf-8',newline='\n')
    return result

if __name__=='__main__':
    result=update()
    print(json.dumps({'records':result['record_count'],'unique_urls':result['unique_url_count']}))
