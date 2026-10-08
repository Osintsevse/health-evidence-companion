import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('localized_genetics',ROOT/'skills/health-record-import/scripts/genetic_reports.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class LocalizationTests(unittest.TestCase):
 def test_localization_preserves_source_codes(self):
  source={'candidates':{'rows':[{'classification':'Benign|association'}]}}
  result=m.localize_assessment(source,'ru')
  self.assertEqual(result['candidates']['rows'][0]['classification'],'Benign|association')
  self.assertNotEqual(result['classification_labels']['Benign|association'],'Benign|association')
  self.assertNotIn('classification_labels',source)
  self.assertEqual(m.ui_labels('ru')['genetics'],'\u0413\u0435\u043d\u0435\u0442\u0438\u043a\u0430')
 def test_unknown_locale_and_code_remain_literal(self):
  result=m.localize_assessment({'candidates':{'rows':[{'classification':'synthetic_unknown'}]}},'xx')
  self.assertEqual(result['classification_labels']['synthetic_unknown'],'synthetic_unknown')
