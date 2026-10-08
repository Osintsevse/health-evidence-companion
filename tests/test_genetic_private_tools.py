"""Synthetic checks for scripts copied outside the public plugin."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PrivateToolTests(unittest.TestCase):
    def test_private_copies_do_not_misidentify_archive_as_public_root(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)/'archive'/'tools'
            folder.mkdir(parents=True)
            for name in ('genetic_staging', 'genetic_annotation', 'genetic_marker_query'):
                source = ROOT/'skills/health-record-import/scripts'/(name+'.py')
                copied = folder/source.name
                copied.write_bytes(source.read_bytes())
                spec = importlib.util.spec_from_file_location(name+'_private_copy', copied)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.assertIsNone(module.PUBLIC_ROOT)
                if hasattr(module, 'external_output'):
                    self.assertEqual(module.external_output(folder/'synthetic.sqlite'), (folder/'synthetic.sqlite').resolve())

    def test_installed_skill_is_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp)/'installed-skill'
            scripts = skill/'scripts'
            scripts.mkdir(parents=True)
            (skill/'SKILL.md').write_text('Synthetic skill', encoding='utf-8')
            copied = scripts/'genetic_annotation.py'
            copied.write_bytes((ROOT/'skills/health-record-import/scripts/genetic_annotation.py').read_bytes())
            spec = importlib.util.spec_from_file_location('annotation_installed', copied)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertEqual(module.PUBLIC_ROOT, skill.resolve())
            with self.assertRaises(ValueError):
                module.external_output(skill/'synthetic.sqlite')

if __name__ == '__main__': unittest.main()
