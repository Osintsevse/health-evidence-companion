"""Wholly fictional intake and SQLite acceptance tests. No actual histories or accounts."""
from contextlib import closing
import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/health-record-import/scripts'
sys.path.insert(0, str(SCRIPTS))
import intake_queue as queue
import accept_owner_report as accept

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.archive = self.root / 'archive'; self.archive.mkdir()
        self.q = self.archive / 'queue'; self.source = self.root / 'source.json'
        self.text = 'Synthetic user reports a misplaced appointment note.'
        self.source.write_text(json.dumps({'turns':[{'items':[{'role':'assistant','text':'An invented claim must not become user evidence.'},{'role':'user','text':self.text}]}]}), encoding='utf8')
        self.m = queue.stage(self.q,self.source,'synthetic-owner','Synthetic note')
        self.db = self.archive / 'ledger.sqlite'
        contract = json.loads((ROOT/'knowledge/archive_tables.json').read_text())
        with closing(sqlite3.connect(self.db)) as c, c:
            for t, rules in contract['tables'].items():
                cols = ([] if t=='imports' else contract['common_columns']) + (contract['fact_columns'] if rules['fact'] else []) + rules['columns']
                cols = list(dict.fromkeys(cols)); pk = 'import_id' if t=='imports' else 'entry_id'
                c.execute('CREATE TABLE '+t+' ('+','.join(k+' '+('INTEGER' if k in {'size_bytes','fact_count','original_count','unresolved_count'} else 'TEXT')+(' PRIMARY KEY' if k==pk else '') for k in cols)+')')
            c.execute('CREATE TABLE storage_locations (document_id TEXT PRIMARY KEY,relative_path TEXT,remote_url TEXT,received_sha256 TEXT,readback_status TEXT)')
            c.execute('CREATE TABLE readable_documents (document_id TEXT PRIMARY KEY,title TEXT,body TEXT)')
            c.execute("INSERT INTO imports(import_id,record_id,state,ledger_readback_status) VALUES('SYN-BASE','synthetic-owner','committed','rows_verified')")
        self.review = self.root / 'review.json'
        self.review_data = {'record_id':'synthetic-owner','source_sha256':self.m['source_sha256'],'review_status':'reviewed_from_source',
              'coverage_note':'One fictional user statement; assistant text excluded.', 'expected_db_sha256':queue.digest(self.db.read_bytes()),'source_language':'en',
              'facts':[{'statement_raw':self.text,'source_text':self.text,'source_locator':'turns[0].items[1]','event_date':None,'event_date_precision':'unknown','uncertainties':'Date not supplied.','entry_kind':'owner_reported_history'}]}
        self.save_review()
    def save_review(self): self.review.write_text(json.dumps(self.review_data),encoding='utf8')
    def commit(self): return accept.accept(self.q,self.m['queue_id'],self.review,self.archive,self.db)
    def count(self):
        with closing(sqlite3.connect(self.db)) as c, c: return c.execute('SELECT count(*) FROM clinical_entries').fetchone()[0]
    def test_staging_keeps_exact_bytes_and_no_ledger_write(self):
        self.assertEqual(self.count(),0); self.assertFalse(self.m['ledger_committed'])
        self.assertEqual((self.q/'packages'/self.m['queue_id']/self.m['source_file']).read_bytes(),self.source.read_bytes())
    def test_repeated_input_is_one_package(self):
        duplicate = self.root / 'renamed.json'; duplicate.write_bytes(self.source.read_bytes())
        self.assertEqual(queue.stage(self.q,duplicate,'synthetic-owner')['queue_id'],self.m['queue_id'])
        self.assertEqual(len(queue.inventory(self.q)['packages']),1)
    def test_owners_and_paths_checked(self):
        with self.assertRaises(ValueError): queue.stage(self.q,self.source,'other-owner')
        with self.assertRaises(ValueError): queue.package(self.q,'../escape')
        with self.assertRaises(ValueError): queue.private(ROOT/'actual.json')
    def test_modified_source_cannot_be_accepted(self):
        (self.q/'packages'/self.m['queue_id']/self.m['source_file']).write_text('changed')
        with self.assertRaises(ValueError): self.commit()
        self.assertEqual(self.count(),0)
    def test_assistant_claim_and_inexact_quote_rejected(self):
        for locator, text in [('turns[0].items[0]','An invented claim'),('turns[0].items[1]','unsupported quote')]:
            self.review_data['facts'][0].update(source_locator=locator,source_text=text);self.save_review()
            with self.assertRaises(ValueError):self.commit()
        self.assertEqual(self.count(),0)
    def test_ledger_change_rejected(self):
        with closing(sqlite3.connect(self.db)) as c, c:c.execute("UPDATE imports SET error_note='Synthetic changed base'")
        with self.assertRaises(ValueError):self.commit()
        self.assertEqual(self.count(),0)
    def test_lock_and_no_schema_creation(self):
        (self.archive/'.archive-writer.lock').write_text('other writer')
        with self.assertRaises(FileExistsError):self.commit()
        self.assertEqual((self.archive/'.archive-writer.lock').read_text(),'other writer')
        (self.archive/'.archive-writer.lock').unlink()
        with closing(sqlite3.connect(self.db)) as c, c:c.execute('DROP TABLE clinical_entries')
        self.review_data['expected_db_sha256']=queue.digest(self.db.read_bytes());self.save_review()
        with self.assertRaises(ValueError):self.commit()
    def test_accept_is_read_back_and_idempotent(self):
        first=self.commit();second=self.commit()
        self.assertEqual(self.count(),1);self.assertEqual(first['import_id'],second['import_id']);self.assertTrue(first['ledger_committed']);self.assertFalse(first['views_verified'])
        self.assertEqual(queue.inventory(self.q)['packages'][0]['status'],'ledger_verified_views_pending')
        with closing(sqlite3.connect(self.db)) as c, c:
            self.assertEqual(c.execute('SELECT event_date,event_date_precision,review_status FROM clinical_entries').fetchone(),(None,'unknown','verified_from_source'))
    def test_changed_review_requires_correction(self):
        self.commit(); self.review_data['facts'][0]['statement_raw']='Changed fictional summary';self.save_review()
        with self.assertRaises(ValueError):self.commit()
        self.assertEqual(self.count(),1)
    def test_staged_import_can_finalize_after_unknown_outcome(self):
        r=self.commit();(self.q/'receipts'/(self.m['queue_id']+'.json')).unlink()
        with closing(sqlite3.connect(self.db)) as c, c:c.execute("UPDATE imports SET state='staged',ledger_readback_status='pending' WHERE import_id=?",(r['import_id'],))
        self.assertTrue(self.commit()['ledger_committed']);self.assertEqual(self.count(),1)
    def test_invalid_dates_and_unreviewed_facts_rejected(self):
        self.review_data['facts'][0].update(event_date='2040-02-31',event_date_precision='day');self.save_review()
        with self.assertRaises(ValueError):self.commit()
        self.review_data['review_status']='pending';self.save_review()
        with self.assertRaises(ValueError):self.commit()
    def test_view_verification_requires_matching_material_rows(self):
        r=self.commit(); model=self.root/'model.json'; view=self.root/'index.html';view.write_text('Synthetic inspected view')
        with closing(sqlite3.connect(self.db)) as c, c:
            c.row_factory=sqlite3.Row;rows=[dict(x) for x in c.execute('SELECT * FROM clinical_entries')]
        model.write_text(json.dumps({'input_database_sha256':queue.digest(self.db.read_bytes()),'tables':{'clinical_entries':rows}}))
        rows[0]['statement_raw']='Wrong fictional value';model.write_text(json.dumps({'input_database_sha256':queue.digest(self.db.read_bytes()),'tables':{'clinical_entries':rows}}))
        with self.assertRaises(ValueError):accept.verify_views(self.q,self.m['queue_id'],model,[view])
        rows[0]['statement_raw']=self.text;model.write_text(json.dumps({'input_database_sha256':queue.digest(self.db.read_bytes()),'tables':{'clinical_entries':rows}}));view.write_text('const DATA='+json.dumps({'input_database_sha256':queue.digest(self.db.read_bytes()),'tables':{'clinical_entries':rows}})+';')
        r=accept.verify_views(self.q,self.m['queue_id'],model,[view]);self.assertTrue(r['views_verified']);self.assertEqual(r['status'],'processed')
        self.assertTrue(self.commit()['views_verified'])

if __name__=='__main__':unittest.main()