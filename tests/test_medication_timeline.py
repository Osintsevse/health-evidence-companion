"""Wholly synthetic medication timeline invariants."""
import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('timeline',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/medication_timeline.py');timeline=importlib.util.module_from_spec(spec);spec.loader.exec_module(timeline)
class TimelineTests(unittest.TestCase):
 def test_prescription_cannot_become_use(self):
  data={'medication_orders':[{'entry_id':'SYN-RX','brand_raw':'Synthetic product','event_date':'2041-04-06','strength_raw':'60 synthetic units','actual_use_status':'unknown'}]}
  result=timeline.build_timeline(data);self.assertEqual(result[0]['kind'],'order');self.assertEqual(result[0]['date_role'],'prescription_date');self.assertIsNone(result[0]['dose'])
 def test_partial_and_unknown_dates_never_create_boundaries(self):
  data={'medication_use_events':[{'entry_id':'SYN-U1','product_identity_raw':'Synthetic product','event_date':'2041','event_date_precision':'year','event_type':'regimen_reported'},{'entry_id':'SYN-U2','product_identity_raw':'Synthetic product','event_date':None,'event_date_precision':'unknown','event_type':'stopped'}]}
  result=timeline.build_timeline(data);self.assertEqual([r['date'] for r in result],['2041',None]);self.assertTrue(all('end_date' not in r for r in result))
 def test_explicit_non_initiation_and_source_survive(self):
  row={'entry_id':'SYN-U','product_identity_raw':'Synthetic alternative','event_type':'not_started','event_date':'2041-08','source_document_id':'DOC-SYN','uncertainties':'Wholly synthetic uncertainty'};data={'medication_use_events':[row]};before=copy.deepcopy(data)
  result=timeline.build_timeline(data);self.assertEqual(result[0]['event_type'],'not_started');self.assertEqual(result[0]['source'],row);self.assertEqual(data,before)
 def test_aliases_do_not_merge_combined_or_similar_names(self):
  data={'medication_use_events':[{'entry_id':'SYN-1','product_identity_raw':'Synthetic brand'},{'entry_id':'SYN-2','product_identity_raw':'Synthetic brand + other'},{'entry_id':'SYN-3','product_identity_raw':'Synthetic brand extended'}]};r=timeline.build_timeline(data,{'medicine_display_aliases':{'Synthetic brand':'Synthetic ingredient'}})
  self.assertEqual([x['group'] for x in r],['Synthetic ingredient','Synthetic brand + other','Synthetic brand extended'])
