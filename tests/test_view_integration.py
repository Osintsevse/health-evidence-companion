"""Full generation regression using a wholly synthetic empty accepted archive."""
import hashlib,importlib.util,json,sqlite3,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('full_views',ROOT/'skills/health-record-import/scripts/generate_views.py');views=importlib.util.module_from_spec(spec);spec.loader.exec_module(views)
class FullGenerationTests(unittest.TestCase):
 def test_complete_model_and_html_generate_without_changing_ledger(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);db=root/'synthetic.sqlite';c=sqlite3.connect(db);contract=json.loads((ROOT/'knowledge/archive_tables.json').read_text())
   for name,table in contract['tables'].items():
    columns=([] if name=='imports' else contract['common_columns'])+(contract['fact_columns'] if table['fact'] else [])+table['columns'];c.execute('create table '+name+' ('+','.join(x+' TEXT' for x in columns)+')')
   c.execute("INSERT INTO imports(import_id,record_id,state,ledger_readback_status) VALUES('SYN-BASE','synthetic-owner','committed','rows_verified')");c.commit();c.close();before=hashlib.sha256(db.read_bytes()).hexdigest();out=root/'views';views.generate(db,{'record_id':'synthetic-owner'},out,ROOT/'skills/health-record-import/assets/archive-view.html');self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(),before)
   model=json.loads((out/'view_data.json').read_text());self.assertEqual(model['blood_pressure']['measurements'],[]);self.assertNotIn('__BLOOD_PRESSURE_', (out/'index.html').read_text());self.assertEqual(model['medication_timeline'],[]);self.assertEqual(model['review_questions'],[]);self.assertTrue(model['feedback_storage_key']);self.assertNotIn('__PRIVATE_MODEL__',(out/'index.html').read_text())
   first={p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in out.iterdir() if p.is_file()}
   views.generate(db,{'record_id':'synthetic-owner'},out,ROOT/'skills/health-record-import/assets/archive-view.html')
   self.assertEqual(first,{p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in out.iterdir() if p.is_file()})
   views.generate(db,{'record_id':'synthetic-owner','as_of':'2040-06-07'},out,ROOT/'skills/health-record-import/assets/archive-view.html')
   self.assertNotEqual(first['index.html'][0],(out/'index.html').read_bytes())
   self.assertEqual(first['workbook_data.json'],((out/'workbook_data.json').read_bytes(),(out/'workbook_data.json').stat().st_mtime_ns))
   self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(),before)
