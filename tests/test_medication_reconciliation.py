"""Wholly fictional current-use reconciliation and rejected source states."""
import importlib.util,json,sqlite3,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('reconciliation',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/medication_reconciliation.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:');self.db.row_factory=sqlite3.Row
        self.db.execute('CREATE TABLE medication_reconciliations(reconciliation_id TEXT,import_id TEXT,record_id TEXT,confirmed_date TEXT,recorded_at TEXT,entry_ids_json TEXT,scope_note TEXT)')
        self.rows={'medication_use_events':[{'entry_id':'FAKE-USE','review_status':'user_confirmed','event_type':'regimen_reported'}]}
    def tearDown(self):self.db.close()
    def add(self,ids=None,owner='fictional-owner',operation='FAKE-IMPORT',date='2049-06-02'):
        self.db.execute('INSERT INTO medication_reconciliations VALUES(?,?,?,?,?,?,?)',('FAKE-RECONCILIATION',operation,owner,date,'2049-06-03T10:00:00Z',json.dumps(ids or ['FAKE-USE']),'Only the selected synthetic medicine was reconciled.'))
    def read(self):return mod.read_reconciliation(self.db,{'medication_reconciliations'},self.rows,{'FAKE-IMPORT'},'fictional-owner','2049-07-01')
    def test_explicit_committed_owner_confirmation_links_reviewed_use(self):
        self.add();rec,rows=self.read();self.assertEqual(rec['confirmed_date'],'2049-06-02');self.assertEqual(rows,self.rows['medication_use_events']);self.assertIn('Only',rec['scope_note'])
    def test_no_confirmation_or_uncommitted_confirmation_establishes_no_current_use(self):
        self.assertEqual(self.read(),(None,[]));self.add(operation='STAGED-ONLY');self.assertEqual(self.read(),(None,[]))
    def test_stopped_nonuse_effect_or_unreviewed_is_rejected(self):
        self.add()
        for field,value in [('event_type','stopped'),('event_type','not_started'),('event_type','benefit_reported'),('review_status','needs_review')]:
            original=self.rows['medication_use_events'][0][field];self.rows['medication_use_events'][0][field]=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.read()
            self.rows['medication_use_events'][0][field]=original
    def test_wrong_owner_future_and_duplicate_or_excluded_ids_are_rejected(self):
        for kwargs in [{'owner':'another-fictional-owner'},{'date':'2050-01-01'},{'ids':['FAKE-USE','FAKE-USE']},{'ids':['EXCLUDED-OLD-ROW']}]:
            self.db.execute('DELETE FROM medication_reconciliations');self.add(**kwargs)
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):self.read()
