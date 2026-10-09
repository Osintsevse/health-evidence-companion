"""Wholly synthetic owner, WAL and interrupted-generation regressions."""
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import test_intake_queue as fixtures
import generate_views as views
import sqlite_snapshot as ledger
import accept_owner_report as accept


class SnapshotSafetyTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.IntakeTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.f=self.fixture
        self.template=fixtures.SCRIPTS.parent/'assets/archive-view.html'
        self.config={'record_id':'synthetic-owner'}

    def generate(self):
        output=self.f.root/'views'
        views.generate(self.f.db,self.config,output,self.template)
        return output

    def test_missing_wrong_or_mixed_owner_rejected_without_reader(self):
        for config in ({},{'record_id':'other-owner'}):
            with self.assertRaises(ValueError):
                views.generate(self.f.db,config,self.f.root/'rejected',self.template)
            self.assertFalse((self.f.root/'rejected/index.html').exists())
        with sqlite3.connect(self.f.db) as c:
            c.execute("INSERT INTO imports(import_id,record_id) VALUES('SYN-OTHER','other-owner')")
        with self.assertRaises(ValueError): self.generate()

    def wal_writer(self):
        c=sqlite3.connect(self.f.db)
        c.execute('PRAGMA journal_mode=WAL')
        c.execute('PRAGMA wal_autocheckpoint=0')
        self.addCleanup(c.close)
        return c

    def test_wal_commit_changes_logical_fingerprint_without_changing_main_file(self):
        writer=self.wal_writer()
        before=ledger.current_fingerprint(self.f.db,'synthetic-owner')
        raw=hashlib.sha256(self.f.db.read_bytes()).hexdigest()
        writer.execute("UPDATE imports SET error_note='Wholly synthetic WAL update'");writer.commit()
        self.assertEqual(raw,hashlib.sha256(self.f.db.read_bytes()).hexdigest())
        self.assertNotEqual(before,ledger.current_fingerprint(self.f.db,'synthetic-owner'))
        self.f.review_data['expected_ledger_fingerprint']=before;self.f.save_review()
        with self.assertRaises(ValueError): self.f.commit()
        self.assertEqual(self.f.count(),0)

    def test_wal_accept_requires_logical_base_and_reader_has_current_fingerprint(self):
        self.wal_writer()
        with self.assertRaisesRegex(ValueError,'WAL ledger requires'): self.f.commit()
        self.f.review_data['expected_ledger_fingerprint']=ledger.current_fingerprint(self.f.db,'synthetic-owner')
        self.f.save_review()
        receipt=self.f.commit()
        output=self.generate()
        model=json.loads((output/'view_data.json').read_text())
        self.assertEqual(receipt['ledger_fingerprint'],model['input_ledger_fingerprint'])
        result=accept.verify_views(self.f.q,self.f.m['queue_id'],output/'view_data.json',[output/'index.html'])
        self.assertTrue(result['view_data_verified']);self.assertFalse(result['ui_verified'])

    def test_read_transaction_retains_snapshot_across_external_commit(self):
        writer=self.wal_writer()
        with ledger.snapshot(self.f.db,'synthetic-owner') as reader:
            before=ledger.fingerprint(reader)
            writer.execute("UPDATE imports SET error_note='Another fictional update'");writer.commit()
            self.assertEqual(before,ledger.fingerprint(reader))
        self.assertNotEqual(before,ledger.current_fingerprint(self.f.db,'synthetic-owner'))

    def test_atomic_replace_failure_keeps_old_file_and_cleans_temp(self):
        output=self.generate();target=output/'index.html'
        old=target.read_bytes()
        with patch.object(views.os,'replace',side_effect=OSError('Synthetic replacement failure')):
            with self.assertRaises(OSError): views.write_changed(target,'New fictional content')
        self.assertEqual(old,target.read_bytes())
        self.assertEqual(list(output.glob('.view-partial-*')),[])

    def test_interrupted_set_is_rejected_by_generation_manifest(self):
        self.f.commit();output=self.generate()
        original=views.write_changed
        def fail_second(path,text):
            if Path(path).name=='view_data.json':
                raise OSError('Synthetic publication interruption')
            original(path,text)
        with patch.object(views,'write_changed',side_effect=fail_second):
            with self.assertRaises(OSError):
                views.generate(self.f.db,{**self.config,'as_of':'2040-01-02'},output,self.template)
        with self.assertRaisesRegex(ValueError,'Interrupted or changed'):
            accept.verify_views(self.f.q,self.f.m['queue_id'],output/'view_data.json',[output/'index.html'])
        self.assertFalse((output/'.view-generator.lock').exists())
        self.generate()
        self.assertTrue(accept.verify_views(self.f.q,self.f.m['queue_id'],output/'view_data.json',[output/'index.html'])['view_data_verified'])

    def test_raw_data_script_cannot_claim_full_ui_verification(self):
        self.f.commit();output=self.generate()
        result=accept.verify_views(self.f.q,self.f.m['queue_id'],output/'view_data.json',[output/'index.html'])
        self.assertFalse(result['views_verified'])
        self.assertFalse(result['ui_verified'])
        self.assertNotEqual(result['status'],'processed')

    def test_uri_reserved_filename_is_supported(self):
        renamed=self.f.root/'synthetic # ledger.sqlite'
        self.f.db.rename(renamed)
        self.assertEqual(len(ledger.current_fingerprint(renamed,'synthetic-owner')),64)
