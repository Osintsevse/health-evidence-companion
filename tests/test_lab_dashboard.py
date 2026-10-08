import importlib.util,copy,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('dashboard',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/lab_dashboard.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
def row(id='SYN-A',value='2',date='2040-01-01',**kw):
 return {'entry_id':id,'analyte_name_raw':'Synthetic measurement','numeric_value':value,'raw_value':value,'comparator':'=','event_date':date,'event_date_precision':'day','review_status':'verified_from_source','record_status':'active','unit_raw':'example','specimen_raw':'synthetic sample','method_raw':'synthetic method','laboratory_raw':'synthetic lab','source_document_id':'SYNTHETIC-DOC','reference_range_raw':'1-3',**kw}
def model(*rows):return {'as_of':'2041-01-01','tables':{'observations':list(rows)}}
class DashboardTests(unittest.TestCase):
 def test_points_preserve_sources_and_input(self):
  m=model(row());before=copy.deepcopy(m);o=lab.build_dashboard(m,{})
  self.assertEqual(o['point_count'],1);self.assertEqual(o['series'][0]['latest']['source'],m['tables']['observations'][0]);self.assertEqual(m,before)
 def test_non_exact_unreviewed_partial_invalid_future_nonfinite_excluded(self):
  rows=[row('X1',comparator='<'),row('X2',review_status='needs_review'),row('X3',date='2040',event_date_precision='year'),row('X4',date='2040-02-30'),row('X5',date='2042-01-01'),row('X6',value='NaN'),row('X7',value='1e999')]
  o=lab.build_dashboard(model(*rows),{});self.assertEqual(o['point_count'],0);self.assertEqual(len(o['excluded']),7)
 def test_each_original_reference_is_used(self):
  a=row('A',value='4',reference_range_raw='<3');b=row('B',value='4',date='2040-02-01',reference_range_raw='1-5');o=lab.build_dashboard(model(a,b),{});self.assertEqual([p['reference_status'] for p in o['series'][0]['points']],['above','within'])
 def test_reference_inequality_boundary(self):
  self.assertEqual(lab.flag(lab.D('3'),lab.reference(row(reference_range_raw='<3'),{})),'above');self.assertEqual(lab.flag(lab.D('3'),lab.reference(row(reference_range_raw='<=3'),{})),'within')
 def test_ambiguous_source_reference_not_guessed(self):
  o=lab.build_dashboard(model(row(reference_range_raw='desired <2; borderline 2-3; high >3')),{});self.assertEqual(o['series'][0]['latest']['reference_status'],'unknown')
 def test_exact_source_override_guard(self):
  c={'lab_reference_overrides':{'SYN-A':{'raw':'1-3','low':'1','high':'3'}}};self.assertEqual(lab.build_dashboard(model(row()),c)['point_count'],1)
  with self.assertRaises(ValueError):lab.build_dashboard(model(row(reference_range_raw='1-4')),c)
 def test_conversion_applies_to_reference_without_mutating_raw(self):
  r=row(value='.4',unit_raw='fraction',reference_range_raw='0.2-0.5',_display={'row_key':'SYN-K','label':'Synthetic fraction','unit':'%','factor':'100','display_numeric_value':'40','category':'blood'})
  p=lab.build_dashboard(model(r),{})['series'][0]['latest'];self.assertEqual(p['value'],40);self.assertEqual(p['reference']['high'],50);self.assertEqual(p['reference_status'],'within');self.assertEqual(p['raw_unit'],'fraction')
 def test_context_delta_and_duplicates(self):
  a=row();b=row('B',value='3',date='2040-02-01');o=lab.build_dashboard(model(a,b),{});self.assertEqual(o['series'][0]['trend']['delta'],1)
  b['laboratory_raw']='another synthetic lab';self.assertIsNone(lab.build_dashboard(model(a,b),{})['series'][0]['trend'])
  b['laboratory_raw']=a['laboratory_raw'];c=row('C',value='4',date=b['event_date']);self.assertIsNone(lab.build_dashboard(model(a,b,c),{})['series'][0]['trend'])
 def test_units_and_specimens_do_not_merge(self):
  o=lab.build_dashboard(model(row(),row('B',unit_raw='other'),row('C',specimen_raw='other specimen')),{});self.assertEqual(len(o['series']),3)
 def test_saved_review_staleness(self):
  m=model(row());c={'health_review':{'source_fingerprint':lab.review_fingerprint(m),'items':[{'entry_ids':['SYN-A']} ]}}
  lab.attach_assessment(m,c);self.assertFalse(m['health_review']['stale']);m['tables']['observations'][0]['numeric_value']='4';lab.attach_assessment(m,c);self.assertTrue(m['health_review']['stale'])
 def test_context_reconciliation_alone_invalidates_review(self):
  m=model(row());c={'health_review':{'source_fingerprint':lab.review_fingerprint(m),'items':[]}};m['medication_reconciliation']={'synthetic_change':True};lab.attach_assessment(m,c);self.assertTrue(m['health_review']['stale'])
 def test_reference_unit_mismatch_and_inverted_interval_unassessed(self):
  for r in [row(reference_unit_raw='other'),row(reference_low='5',reference_high='1')]:self.assertEqual(lab.build_dashboard(model(r),{})['series'][0]['latest']['reference_status'],'unknown')
 def test_imaging_separate_and_zero_preserved(self):
  o=lab.build_dashboard(model(row(value='0',method_raw='Ultrasound')),{});self.assertEqual(o['series'][0]['category'],'investigations');self.assertEqual(o['series'][0]['latest']['value'],0)
if __name__=='__main__':unittest.main()
