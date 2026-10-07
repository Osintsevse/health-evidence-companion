"""Host package contract tests; no native accounts or installation claimed."""
import io,json,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from sync_platforms import expected
from sync_references import MAP
from build import build
from release import expected_assets
class PlatformTests(unittest.TestCase):
 def test_shared_identity_and_skill_root(self):
  portable=json.loads((ROOT/'plugin.json').read_text());e=expected(ROOT)
  for name,m in e.items():self.assertEqual(json.loads((ROOT/name).read_text()),m)
  for name in ['.claude-plugin/plugin.json','.codex-plugin/plugin.json']:
   self.assertEqual(e[name]['version'],portable['version']);self.assertEqual(e[name]['name'],portable['name'])
  self.assertEqual(e['.codex-plugin/plugin.json']['skills'],'./skills/')
 def test_upload_zips_have_one_complete_named_skill(self):
  with tempfile.TemporaryDirectory() as tmp:
   report=build(ROOT,Path(tmp));self.assertEqual(set(report['platform_sha256']),{'health-evidence-companion-claude-skills.zip','PLATFORMS.md'})
   with zipfile.ZipFile(Path(tmp)/'health-evidence-companion-claude-skills.zip') as bundle:
    self.assertEqual(set(bundle.namelist()),{skill+'.zip' for skill in MAP})
    for skill in MAP:
     with zipfile.ZipFile(io.BytesIO(bundle.read(skill+'.zip'))) as z:
      self.assertIn(skill+'/SKILL.md',z.namelist());self.assertTrue(all(x.startswith(skill+'/') for x in z.namelist()));self.assertTrue(any('/references/' in x for x in z.namelist()));self.assertIsNone(z.testzip())
