"""Accept manually reviewed owner statements into an existing project SQLite ledger.
No OCR, clinical interpretation, schema migration, cloud upload or automatic scheduler.
"""
from contextlib import closing
import re
import argparse
import datetime
import hashlib
import json
import sqlite3
from pathlib import Path
from sqlite_snapshot import check_owner, fingerprint, current_fingerprint, snapshot
from intake_queue import private, package, require, digest, atomic_json, now, read_json, lock

CLINICAL = ['entry_id','import_id','recorded_at','record_status','supersedes_entry_id','source_kind','source_document_id','source_locator','source_text','event_date','event_date_precision','review_status','uncertainties','entry_kind','statement_raw','diagnostic_certainty_raw','clinician_raw','organization_raw','followup_raw','completion_status_raw','coding_system','code','coding_status']
KINDS = {'owner_reported_symptom', 'owner_reported_history', 'family_history_report', 'record_reconciliation'}

def validate_review(m, raw, review):
    require(review.get('record_id') == m['record_id'], 'Review owner mismatch')
    require(review.get('source_sha256') == m['source_sha256'], 'Review source hash mismatch')
    require(review.get('review_status') == 'reviewed_from_source', 'Explicit source review is required')
    require(isinstance(review.get('coverage_note'), str) and review['coverage_note'].strip(), 'State the reviewed source coverage and omissions')
    facts = review.get('facts')
    require(isinstance(facts, list) and 0 < len(facts) <= 200, 'A bounded nonempty list of reviewed statements is required')
    source = raw.decode('utf-8-sig')
    # JSON transcripts preserve escaped newlines; inspect only user-authored text.
    if m['source_file'] == 'source.json':
        payload = json.loads(source)
        require(isinstance(payload, dict) and isinstance(payload.get('turns'), list), 'JSON intake needs turns/items/role/text')
        texts = {f'turns[{ti}].items[{ii}]': item.get('text') for ti, t in enumerate(payload['turns']) for ii, item in enumerate(t.get('items', [])) if item.get('role') == 'user'}
    else:
        texts = {'source': source}
    for f in facts:
        require(isinstance(f, dict) and set(f) == {'statement_raw','source_text','source_locator','event_date','event_date_precision','uncertainties','entry_kind'}, 'Unexpected or missing review fields')
        require(all(isinstance(f[k], str) and f[k].strip() for k in ['statement_raw','source_text','source_locator','entry_kind']), 'Missing statement or provenance')
        require(f['source_locator'] in texts and isinstance(texts[f['source_locator']], str) and f['source_text'] in texts[f['source_locator']], 'Evidence must be a literal excerpt of the located user source')
        require(f['entry_kind'] in KINDS, 'Only reported statements are accepted; diagnoses/orders/measurements need their dedicated workflow')
        require(f['uncertainties'] is None or isinstance(f['uncertainties'], str), 'Invalid uncertainty')
        value = f['event_date']; precision = f['event_date_precision']
        if value is None:
            require(precision == 'unknown', 'Unknown date needs unknown precision')
        else:
            require(isinstance(value, str), 'Date must be text')
            if precision == 'day': require(datetime.date.fromisoformat(value).isoformat() == value, 'Invalid day')
            elif precision == 'month': require(len(value) == 7 and datetime.date.fromisoformat(value + '-01').strftime('%Y-%m') == value, 'Invalid month')
            elif precision == 'year': require(len(value) == 4 and value.isdigit() and 1 <= int(value) <= 9999, 'Invalid year')
            else: raise ValueError('Unsupported date precision')
    require(len({json.dumps(f, sort_keys=True, ensure_ascii=False) for f in facts}) == len(facts), 'Duplicate statement in review')
    return facts

def columns(c, table):
    return [r[1] for r in c.execute('PRAGMA table_info(' + table + ')')]

def insert(c, table, data):
    cols = columns(c, table)
    require(set(data) <= set(cols), 'Existing database schema is incompatible: ' + table)
    c.execute('INSERT INTO ' + table + ' (' + ','.join(cols) + ') VALUES (' + ','.join('?' for _ in cols) + ')', [data.get(k) for k in cols])

def check_rows(c, table, key, expected):
    row = c.execute('SELECT * FROM ' + table + ' WHERE ' + key + '=?', (expected[key],)).fetchone()
    require(row is not None, 'Missing readback row')
    require(all(row[k] == v for k, v in expected.items()), 'Material row readback mismatch: ' + table)

def check_base(connection, db, review):
    expected=review.get('expected_ledger_fingerprint')
    if expected is not None:
        require(expected==fingerprint(connection), 'Ledger version changed; review against the current base')
    else:
        # Legacy reviews are supported only where the main file contains committed data.
        require(connection.execute('PRAGMA journal_mode').fetchone()[0].lower()!='wal',
                'WAL ledger requires expected_ledger_fingerprint')
        require(review.get('expected_db_sha256')==digest(db.read_bytes()),
                'Ledger version changed; review against the current base')


def accept(queue, key, review_path, archive_root, db_path, system_root=None):
    q, folder, m, raw = package(queue, key)
    review_path = private(review_path); review_raw = review_path.read_bytes(); review = json.loads(review_raw.decode('utf-8-sig'))
    facts = validate_review(m, raw, review)
    root = private(archive_root); db = private(db_path)
    require(root.is_dir() and db.is_file() and db.is_relative_to(root), 'Resolve an existing ledger inside the selected archive')
    receipt_path = q / 'receipts' / (key + '.json')
    review_sha = digest(review_raw)
    operation = 'IMPORT-' + key
    document = 'DOC-' + key
    service = private(system_root) if system_root else root
    require(service.is_dir() and (service == root or service.is_relative_to(root)), 'System directory must be inside the archive')
    originals = service / 'intake_sources' / key
    with lock(root / '.archive-writer.lock'):
        c = sqlite3.connect(db, timeout=5); c.row_factory = sqlite3.Row
        try:
            require(set(columns(c, 'clinical_entries')) == set(CLINICAL), 'Existing clinical row contract differs; no migration performed')
            require(c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'Database integrity failed')
            require(c.execute('PRAGMA foreign_key_check').fetchone() is None, 'Foreign key check failed')
            check_owner(c,m['record_id'])
            prev = c.execute('SELECT * FROM imports WHERE import_id=?', (operation,)).fetchone()
            if receipt_path.exists():
                previous = read_json(receipt_path)
                require(previous['review_sha256'] == review_sha, 'Completed review differs; use an explicit correction workflow')
            if not prev:
                with c:
                    c.execute('BEGIN')
                    check_base(c,db,review)
            # Originals and exact review survive transaction/retry; never overwrite.
            originals.mkdir(parents=True, exist_ok=True)
            for name, content in [(m['source_file'], raw), ('review.json', review_raw)]:
                target = originals / name
                if target.exists(): require(target.read_bytes() == content, 'Existing archived source/review differs')
                else:
                    with target.open('xb') as f: f.write(content)
                require(target.read_bytes() == content, 'Original byte readback failed')
            timestamp = prev['recorded_at'] if prev else now()
            rows = [{**dict.fromkeys(CLINICAL), **f, 'entry_id': 'CE-' + key + '-' + str(i + 1).zfill(3), 'import_id': operation,
                     'recorded_at': timestamp, 'record_status': 'active', 'source_kind': 'owner_report', 'source_document_id': document,
                     'review_status': 'verified_from_source', 'diagnostic_certainty_raw': 'Owner report; transcription reviewed, clinical claims not confirmed',
                     'completion_status_raw': 'reported', 'coding_status': 'not_coded'} for i, f in enumerate(facts)]
            doc = {'entry_id': document, 'import_id': operation, 'recorded_at': timestamp, 'record_status': 'active',
                   'document_kind': 'owner_report', 'original_filename': m['original_filename'],
                   'mime_type': {'source.json':'application/json','source.md':'text/markdown','source.txt':'text/plain'}[m['source_file']],
                   'size_bytes': len(raw), 'received_sha256': m['source_sha256'], 'storage_readback_status': 'bytes_verified',
                   'document_date': m['received_at'], 'document_date_precision':'datetime', 'source_language': review.get('source_language')}
            location = {'document_id': document, 'relative_path': (originals / m['source_file']).relative_to(root).as_posix(),
                        'received_sha256': m['source_sha256'], 'readback_status': 'bytes_verified'}
            body = '# ' + m['source_title'] + '\n\n' + review['coverage_note'] + '\n\n' + '\n\n'.join('- ' + f['statement_raw'] + '\n  Uncertainty: ' + (f['uncertainties'] or 'None recorded') for f in facts)
            readable = {'document_id':document,'title':m['source_title'],'body':body}
            if not prev:
                backup = service / 'intake_backups' / (key + '.before.sqlite')
                backup.parent.mkdir(parents=True, exist_ok=True)
                require(not backup.exists(), 'Backup already exists without a recorded import; inspect recovery before retry')
                with closing(sqlite3.connect(backup)) as b: c.backup(b)
                with c:
                    c.execute('BEGIN IMMEDIATE')
                    check_owner(c,m['record_id'])
                    check_base(c,db,review)
                    insert(c, 'imports', {'import_id':operation,'record_id':m['record_id'],'schema_version':'1.0','state':'staged',
                                         'recorded_at':timestamp,'original_count':1,'fact_count':len(rows),
                                         'unresolved_count':sum(bool(x['uncertainties']) for x in rows),'ledger_readback_status':'pending'})
                    insert(c, 'documents', doc); insert(c, 'storage_locations', location); insert(c, 'readable_documents', readable)
                    for row in rows: insert(c, 'clinical_entries', row)
            for t, field, data in [('documents','entry_id',doc),('storage_locations','document_id',location),('readable_documents','document_id',readable)]: check_rows(c,t,field,data)
            for row in rows: check_rows(c,'clinical_entries','entry_id',row)
            actual = c.execute('SELECT count(*) FROM clinical_entries WHERE import_id=?', (operation,)).fetchone()[0]
            require(actual == len(rows), 'Unexpected rows in this import')
            with c:
                c.execute("UPDATE imports SET state='committed', ledger_readback_status='rows_verified', completed_at=COALESCE(completed_at,?) WHERE import_id=?", (now(),operation))
            require(tuple(c.execute('SELECT state,ledger_readback_status,fact_count FROM imports WHERE import_id=?',(operation,)).fetchone()) == ('committed','rows_verified',len(rows)), 'Commit marker readback failed')
            for row in rows: check_rows(c,'clinical_entries','entry_id',row)
            with c:
                c.execute('BEGIN')
                ledger_fingerprint=fingerprint(c)
            require(c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'Final integrity failed')
            require(c.execute('PRAGMA foreign_key_check').fetchone() is None, 'Final foreign key check failed')
        finally:
            c.close()
        receipt = {'schema_version':1,'queue_id':key,'record_id':m['record_id'],'source_sha256':m['source_sha256'],
                   'review_sha256':review_sha,'import_id':operation,'document_id':document,'row_ids':[r['entry_id'] for r in rows],
                   'ledger_committed':True,'ledger_readback':'rows_verified','source_bytes_verified':True,
                   'db_sha256':digest(db.read_bytes()),'ledger_fingerprint':ledger_fingerprint,
                   'db_path':str(db),'views_verified':False,'view_data_verified':False,'ui_verified':False,
                   'cloud_status':'not_verified','status':'ledger_verified_views_pending','coverage_note':review['coverage_note']}
        if receipt_path.exists():
            old = read_json(receipt_path)
            if old.get('view_data_verified') and old.get('ledger_fingerprint') == ledger_fingerprint:
                return old
        atomic_json(receipt_path, receipt)
        require(read_json(receipt_path) == receipt, 'Receipt readback failed')
        return receipt

def verify_views(queue, key, model_path, view_paths):
    model_path=private(model_path)
    with lock(model_path.parent/'.view-generator.lock'):
        return _verify_views(queue,key,model_path,view_paths)


def _verify_views(queue, key, model_path, view_paths):
    q, _, m, _ = package(queue, key)
    p=q/'receipts'/(key+'.json'); r=read_json(p)
    require(r['queue_id']==key and r['record_id']==m['record_id'] and
            r['source_sha256']==m['source_sha256'] and r['ledger_committed'], 'Ledger receipt mismatch')
    model_path=private(model_path); model=read_json(model_path)
    db=private(r['db_path'])
    with snapshot(db,m['record_id']) as c:
        current=fingerprint(c)
        require(model.get('record_id')==m['record_id'] and model.get('input_ledger_fingerprint')==current,
                'View model owner or ledger fingerprint mismatch')
        rows={x['entry_id']:x for x in model['tables']['clinical_entries']}
        require(set(r['row_ids'])<=set(rows), 'Requested facts missing from view model')
        for eid in r['row_ids']:
            require(rows[eid]['source_document_id']==r['document_id'], 'View provenance mismatch')
            actual=c.execute('SELECT * FROM clinical_entries WHERE entry_id=?',(eid,)).fetchone()
            require(actual is not None and all(rows[eid].get(k)==v for k,v in dict(actual).items()),
                    'View material value mismatch')
    manifest=read_json(model_path.parent/'generation.json')
    require(manifest.get('format')=='archive-view-generation-v1' and
            manifest.get('record_id')==m['record_id'] and
            manifest.get('input_ledger_fingerprint')==current, 'Generation manifest mismatch')
    expected_files={'index.html',model_path.name,'workbook_data.json'} | {
        'details/'+d['entry_id']+'.md' for d in model['documents']}
    require(set(manifest['files'])==expected_files, 'Incomplete generation manifest')
    for name,sha in manifest['files'].items():
        relative=Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts and ':' not in name and '\\' not in name,
                'Unsafe generation path')
        target=(model_path.parent/relative).resolve()
        require(target.is_relative_to(model_path.parent) and digest(target.read_bytes())==sha,
                'Interrupted or changed view generation')
    require(manifest['files'].get(model_path.name)==digest(model_path.read_bytes()),
            'View model is not a member of this generation')
    require(view_paths, 'Provide inspected reader outputs')
    views=[]; embedded=[]
    for v in view_paths:
        v=private(v)
        require(v.parent==model_path.parent and v.suffix in {'.html','.md'} and
                manifest['files'].get(v.name)==digest(v.read_bytes()), 'Reader output generation mismatch')
        text=v.read_text(encoding='utf-8')
        marker=re.search(r'const\s+DATA\s*=\s*',text) if v.suffix=='.html' else None
        if marker:
            data,_=json.JSONDecoder().raw_decode(text[marker.end():])
            require(data==model, 'Embedded reader model differs from the verified model')
            embedded.append(data)
        views.append({'path':str(v),'sha256':digest(v.read_bytes())})
    require(embedded, 'No reader HTML contains the verified model')
    require(current_fingerprint(db,m['record_id'])==current, 'Ledger changed during view verification')
    # Data readback cannot certify JavaScript execution, visible UI or source navigation.
    r.update({'ledger_fingerprint':current,'views_verified':False,'view_data_verified':True,
              'ui_verified':False,'status':'ledger_verified_reader_data_verified_ui_pending',
              'view_model_sha256':digest(model_path.read_bytes()),'reader_files':views})
    atomic_json(p,r); require(read_json(p)==r, 'View receipt readback failed')
    return r

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--queue',required=True); p.add_argument('--queue-id',required=True)
    sub = p.add_subparsers(dest='command',required=True)
    a = sub.add_parser('accept'); a.add_argument('--review',required=True); a.add_argument('--archive-root',required=True); a.add_argument('--db',required=True); a.add_argument('--system-root')
    v = sub.add_parser('verify-views'); v.add_argument('--model',required=True); v.add_argument('--view',action='append',required=True)
    args = p.parse_args()
    if args.command == 'accept': result = accept(args.queue,args.queue_id,args.review,args.archive_root,args.db,args.system_root)
    else: result = verify_views(args.queue,args.queue_id,args.model,args.view)
    print(json.dumps(result,ensure_ascii=True))

if __name__ == '__main__': main()