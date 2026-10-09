"""Private file intake queue. Local files only; staging never commits clinical facts."""
from contextlib import contextmanager
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
SUFFIXES = {'.json', '.md', '.txt'}
REPO = next((p for p in Path(__file__).resolve().parents if (p / 'plugin.json').exists()), None)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def private(path):
    p = Path(path).resolve()
    require(REPO is None or not p.is_relative_to(REPO), 'Private files must be outside the plugin checkout')
    require(not any((parent / 'plugin.json').is_file() and (parent / 'skills').is_dir() for parent in [p, *p.parents]), 'Private files must be outside all plugin checkouts')
    return p

def digest(data):
    return hashlib.sha256(data).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def atomic_json(p, data):
    p = Path(p)
    tmp = p.with_name(p.name + '.partial-' + os.urandom(8).hex())
    try:
        with tmp.open('x', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    finally:
        if tmp.exists():
            tmp.unlink()

@contextmanager
def lock(path):
    path = Path(path)
    with path.open('x', encoding='utf-8') as f:
        f.write(now())
    try:
        yield
    finally:
        path.unlink()

def initialize(queue, record_id):
    q = private(queue)
    require(isinstance(record_id, str) and record_id.strip(), 'An explicit owner record ID is required')
    q.mkdir(parents=True, exist_ok=True)
    cfg = q / 'queue.json'
    # Serialize configuration/staging. Do not remove another writer's lock.
    with lock(q / '.queue.lock'):
        try:
            if cfg.exists():
                require(read_json(cfg) == {'schema_version': 1, 'record_id': record_id}, 'Queue owner or schema mismatch')
            else:
                atomic_json(cfg, {'schema_version': 1, 'record_id': record_id})
            for name in ('incoming', 'packages', 'receipts'):
                (q / name).mkdir(exist_ok=True)
        finally:
            pass
    return q

def reported_manifest(q, manifest):
    receipt = q / 'receipts' / (manifest['queue_id'] + '.json')
    if not receipt.exists():
        return manifest
    result = read_json(receipt)
    require(result.get('queue_id') == manifest['queue_id'] and result.get('source_sha256') == manifest['source_sha256'] and result.get('record_id') == manifest['record_id'], 'Existing receipt binding mismatch')
    return {**manifest, 'status':result['status'], 'ledger_committed':bool(result.get('ledger_committed')), 'views_verified':bool(result.get('views_verified')), 'view_data_verified':bool(result.get('view_data_verified')), 'ui_verified':bool(result.get('ui_verified'))}

def stage(queue, source, record_id, title=None):
    q = initialize(queue, record_id)
    source = private(source)
    require(source.suffix.lower() in SUFFIXES and source.is_file(), 'Only existing JSON, Markdown or text sources are supported')
    require(source.stat().st_size <= MAX_BYTES, 'Source exceeds the bounded intake size')
    raw = source.read_bytes()
    require(0 < len(raw) <= MAX_BYTES, 'Empty or oversized source')
    text = raw.decode('utf-8-sig')
    sha = digest(raw)
    key = 'INTAKE-' + digest((record_id + '\0' + sha).encode('utf-8'))[:32].upper()
    folder = q / 'packages' / key
    with lock(q / '.queue.lock'):
        try:
            if folder.exists():
                m = read_json(folder / 'manifest.json')
                require(m['record_id'] == record_id and m['source_sha256'] == sha, 'Existing package differs')
                require(digest((folder / m['source_file']).read_bytes()) == sha, 'Existing source bytes differ')
                return reported_manifest(q, m)
            tmp = q / 'packages' / ('.partial-' + os.urandom(8).hex())
            tmp.mkdir()
            try:
                name = 'source' + source.suffix.lower()
                (tmp / name).write_bytes(raw)
                require(digest((tmp / name).read_bytes()) == sha, 'Source readback failed')
                m = {'schema_version': 1, 'queue_id': key, 'record_id': record_id,
                     'source_sha256': sha, 'source_file': name, 'original_filename': source.name,
                     'source_title': title or source.stem, 'received_at': now(),
                     'status': 'pending_review', 'source_bytes_verified': True,
                     'ledger_committed': False, 'views_verified': False}
                atomic_json(tmp / 'manifest.json', m)
                os.rename(tmp, folder)
            except BaseException:
                if tmp.exists():
                    shutil.rmtree(tmp)
                raise
        finally:
            pass
    return m

def package(queue, key):
    q = private(queue)
    require(isinstance(key, str) and re.fullmatch(r'INTAKE-[A-F0-9]{32}', key), 'Invalid queue ID')
    folder = q / 'packages' / key
    m = read_json(folder / 'manifest.json')
    require(m['queue_id'] == key and m['schema_version'] == 1, 'Package identity mismatch')
    require(m['record_id'] == read_json(q / 'queue.json')['record_id'], 'Queue owner mismatch')
    require(m['source_file'] in {'source.json', 'source.md', 'source.txt'}, 'Invalid source path')
    raw = (folder / m['source_file']).read_bytes()
    require(digest(raw) == m['source_sha256'], 'Package source hash mismatch')
    return q, folder, m, raw

def inventory(queue):
    q = private(queue)
    result = []
    for p in sorted((q / 'packages').glob('INTAKE-*')):
        _, _, m, _ = package(q, p.name)
        receipt = q / 'receipts' / (p.name + '.json')
        r = read_json(receipt) if receipt.exists() else {}
        require(not r or (r.get('queue_id') == m['queue_id'] and r.get('source_sha256') == m['source_sha256']), 'Receipt binding mismatch')
        result.append({'queue_id': m['queue_id'], 'source_title': m['source_title'],
                       'status': r.get('status', 'pending_review'), 'source_sha256': m['source_sha256'],
                       'ledger_committed': bool(r.get('ledger_committed')), 'views_verified': bool(r.get('views_verified')), 'view_data_verified': bool(r.get('view_data_verified')), 'ui_verified': bool(r.get('ui_verified'))})
    return {'packages': result, 'incoming_files': [p.name for p in sorted((q / 'incoming').iterdir()) if p.is_file()]}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--queue', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    i = sub.add_parser('init'); i.add_argument('--record-id', required=True)
    s = sub.add_parser('stage'); s.add_argument('--record-id', required=True); s.add_argument('--input', required=True); s.add_argument('--title')
    sub.add_parser('status')
    scan = sub.add_parser('scan'); scan.add_argument('--record-id', required=True)
    a = p.parse_args()
    if a.command == 'init':
        result = {'queue': str(initialize(a.queue, a.record_id)), 'ledger_committed': False}
    elif a.command == 'stage':
        result = stage(a.queue, a.input, a.record_id, a.title)
    elif a.command == 'scan':
        q = initialize(a.queue, a.record_id)
        results = []; errors = []
        for f in sorted((q / 'incoming').iterdir()):
            if f.is_file() and f.suffix.lower() in SUFFIXES:
                try: results.append(stage(q, f, a.record_id))
                except (ValueError, OSError, UnicodeError) as e: errors.append({'file': f.name, 'error': type(e).__name__})
        result = {'staged': results, 'errors': errors, 'ledger_write_performed': False}
    else:
        result = inventory(a.queue)
    print(json.dumps(result, ensure_ascii=True))

if __name__ == '__main__':
    main()