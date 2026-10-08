import importlib.util,json,sqlite3,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('query',ROOT/'skills/health-record-import/scripts/genetic_marker_query.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class MarkerQueryTests(unittest.TestCase):
 def test_absence_and_conflicting_neighbour_retained(self):
  with tempfile.TemporaryDirectory(dir=ROOT.parent) as td:
   db=Path(td)/'s.sqlite';c=sqlite3.connect(db);c.execute('CREATE TABLE metadata(key,value_json)');c.execute('CREATE TABLE observations(source_line,row_json)')
   c.execute('INSERT INTO metadata VALUES (?,?)',('assembly',json.dumps('unknown')))
   for n,r in enumerate([{'rsid_raw':'rsSyntheticA','chromosome_raw':'1','position_raw':'100','flags':['conflicting_duplicate_locus']},{'rsid_raw':'rsSyntheticB','chromosome_raw':'1','position_raw':'100','flags':['conflicting_duplicate_locus']}],1):c.execute('INSERT INTO observations VALUES (?,?)',(n,json.dumps(r)))
   c.commit();c.close();r=m.marker_query(db,['rsSyntheticMissing','rsSyntheticA'])
   self.assertEqual(r['markers'][1]['status'],'absent_from_export');self.assertEqual(r['markers'][0]['observations'][0]['flags'],['conflicting_duplicate_locus']);self.assertEqual(len(r['other_observations_at_selected_loci']),1)
 def test_public_output_and_overwrite_refused(self):
  with self.assertRaises(ValueError):m.write_private(ROOT/'sample.json',{})
  with tempfile.TemporaryDirectory(dir=ROOT.parent) as td:
   p=Path(td)/'query.json';m.write_private(p,{'safe':'fixture'})
   with self.assertRaises(FileExistsError):m.write_private(p,{})
   self.assertEqual(json.loads(p.read_text())['safe'],'fixture')
