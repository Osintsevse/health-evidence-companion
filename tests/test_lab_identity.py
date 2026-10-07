"""Wholly synthetic examples; no personal facts, dates or identifiers."""
import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('lab_identity',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/lab_identity.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
def row(name='Glukoza',unit='mmol/L',sample='S',value='4.321',comparator='=',review='verified_from_source'):
 return {'analyte_name_raw':name,'unit_raw':unit,'specimen_raw':sample,'raw_value':value,'numeric_value':value.lstrip('<>='),'comparator':comparator,'review_status':review,'method_raw':'synthetic_method'}
class LabIdentityTests(unittest.TestCase):
 def test_bilingual_source_unchanged(self):
  r=row(name='\u0413\u043b\u044e\u043a\u043e\u0437\u0430',unit='\u043c\u043c\u043e\u043b\u044c/\u043b');old=copy.deepcopy(r);n=lab.normalize(r);self.assertEqual(n['row_key'],lab.normalize(row())['row_key']);self.assertEqual(r,old);self.assertIsNone(n['loinc_code'])
 def test_blood_vs_urine(self):self.assertNotEqual(lab.normalize(row())['row_key'],lab.normalize(row(sample='U',unit='arb.jed.',value='1+'))['row_key'])
 def test_percent_vs_absolute(self):self.assertNotEqual(lab.normalize(row('Neutrofili','%','eK'))['row_key'],lab.normalize(row('Neutrofili aps.','10*9/L','eK'))['row_key'])
 def test_mass_transform(self):
  n=lab.normalize(row('Hemoglobin','g/dL','eK','12.6'));self.assertEqual((n['display_numeric_value'],n['display_value'],n['unit'],n['factor']),('126.0','126','g/L','10'))
 def test_fraction_transform(self):
  n=lab.normalize(row('Hematokrit','L/L','eK','0.417'));self.assertEqual((n['display_value'],n['unit']),('41.7','%'))
 def test_count_unit_aliases(self):self.assertEqual(lab.normalize(row('WBC','10^9/L','eK'))['row_key'],lab.normalize(row('Leukociti','10*9/L','cK'))['row_key'])
 def test_detection_limit(self):self.assertEqual(lab.normalize(row('Hemoglobin','g/dL','eK','<12.6','<'))['display_value'],'<126')
 def test_unknown_specimen_display_only(self):
  n=lab.normalize(row(sample=None));self.assertEqual(n['mapping_status'],'display_group_only');self.assertIn('not recorded',n['note']);self.assertEqual(n['comparability_status'],'not_established')
 def test_no_fuzzy_name_match(self):self.assertNotEqual(lab.normalize(row('Glukoz?'))['row_key'],lab.normalize(row())['row_key'])
 def test_unreviewed_not_converted(self):
  n=lab.normalize(row('Hemoglobin','g/dL','eK','12.6',review='needs_review'));self.assertIsNone(n['display_numeric_value']);self.assertEqual(n['display_value'],'12.6')
 def test_slash_preserved(self):
  r=row('Glukoza','arb.jed.','U','/');r['numeric_value']=None;n=lab.normalize(r);self.assertEqual(n['display_value'],'/');self.assertIsNone(n['display_numeric_value'])
 def test_no_global_unit_lowercasing(self):self.assertNotEqual(lab.normalize(row(unit='ML/L'))['row_key'],lab.normalize(row(unit='mL/L'))['row_key'])
if __name__=='__main__':unittest.main()
