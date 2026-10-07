"""Offline mutation tests for actual packaging/privacy rejection paths."""
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import build
from validate import check_blank, privacy_check, validate, validate_zip


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__', '.venv'))

    def tearDown(self):
        self.temp.cleanup()

    def test_real_tree_validates(self):
        self.assertEqual(validate(self.root)['sources'], len(json.loads((self.root / 'knowledge/sources.json').read_text())))

    def test_build_is_reproducible(self):
        a = build(self.root, Path(self.temp.name) / 'a')
        b = build(self.root, Path(self.temp.name) / 'b')
        self.assertEqual(a['sha256'], b['sha256'])

    def test_runtime_archive_excludes_developer_code(self):
        report = build(self.root)
        stable = self.root / 'dist/health-evidence-companion.zip'
        versioned = self.root / f"dist/health-evidence-companion-{report['version']}.zip"
        self.assertEqual(stable.read_bytes(), versioned.read_bytes())
        self.assertEqual((self.root / 'dist/SETUP.md').read_bytes(),
                         (self.root / 'docs/quick-start.md').read_bytes())
        self.assertEqual((self.root / 'dist/SETUP_PROMPT.txt').read_bytes(),
                         (self.root / 'docs/setup-prompt.txt').read_bytes())
        with zipfile.ZipFile(self.root / f"dist/health-evidence-companion-{report['version']}.zip") as z:
            names = z.namelist()
            self.assertIn('plugin.json', names)
            self.assertFalse(any(n.startswith(('examples/', 'scripts/', '.github/', 'tests/')) for n in names))
            self.assertTrue(any(n.endswith('14_PATIENT_RECORD_RULES.md') for n in names))

    def test_stale_reference_is_rejected(self):
        (self.root / 'knowledge/03_RESPIRATORY.md').write_text('changed general knowledge')
        with self.assertRaisesRegex(ValueError, 'Stale/missing'):
            validate(self.root)

    def test_unknown_reference_is_rejected(self):
        (self.root / 'skills/health-explain/references/extra.md').write_text('unmapped content')
        with self.assertRaisesRegex(ValueError, 'Unexpected reference'):
            validate(self.root)

    def test_missing_relative_link_is_rejected(self):
        path = self.root / 'skills/health-explain/SKILL.md'
        path.write_text(path.read_text() + '\n[Missing](references/no-such-file.md)\n')
        with self.assertRaisesRegex(ValueError, 'Missing relative link'):
            validate(self.root)

    def test_unknown_source_id_is_rejected(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\nUnsupported claim [S999].\n')
        with self.assertRaisesRegex(ValueError, 'Unknown source ID'):
            validate(self.root)

    def test_private_link_is_rejected_without_echo(self):
        private_link = 'https://' + 'drive.google.com/file/d/' + 'synthetic-private-id/view'
        with self.assertRaises(ValueError) as error:
            privacy_check(private_link, 'fixture.md')
        self.assertNotIn('synthetic-private-id', str(error.exception))

    def test_filled_template_is_rejected(self):
        data = json.loads((self.root / 'knowledge/templates/patient_record.template.json').read_text())
        data['owner']['display_name'] = 'Synthetic Person'
        with self.assertRaisesRegex(ValueError, 'Populated template'):
            check_blank(data, 'synthetic-fixture')

    def test_nonempty_template_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Nonempty template'):
            check_blank({'is_blank_template': True, 'conditions': ['Synthetic condition']}, 'fixture')

    def test_unknown_status_is_not_negative(self):
        data = json.loads((self.root / 'knowledge/templates/patient_record.template.json').read_text())
        check_blank(data, 'fixture')
        self.assertEqual(data['allergies']['information_status'], 'unknown')
        self.assertEqual(data['medications']['reconciliation_status'], 'unknown')

    def test_cyrillic_content_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Non-English'):
            privacy_check('\u043c\u0435\u0434\u0438\u0446\u0438\u043d\u0430', 'fixture')

    def test_overlong_metadata_is_rejected(self):
        path = self.root / 'plugin.json'
        data = json.loads(path.read_text())
        data['extensions']['com.openai']['interface']['displayName'] = 'x' * 31
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Invalid listing'):
            validate(self.root)

    def test_unknown_portable_field_is_rejected(self):
        path = self.root / 'plugin.json'
        data = json.loads(path.read_text())
        data['unsupportedField'] = True
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Unknown portable'):
            validate(self.root)

    def test_lifecycle_extension_is_rejected(self):
        path = self.root / 'plugin.json'
        data = json.loads(path.read_text())
        data['extensions']['com.openai']['hooks'] = './hooks.json'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Unexpected extension'):
            validate(self.root)

    def test_archive_path_traversal_is_rejected(self):
        path = Path(self.temp.name) / 'bad.zip'
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr('plugin.json', (ROOT / 'plugin.json').read_bytes())
            z.writestr('../outside.md', 'synthetic')
        with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
            validate_zip(path)

    def test_duplicate_archive_member_is_rejected(self):
        path = Path(self.temp.name) / 'bad.zip'
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('plugin.json', '{}')
                z.writestr('plugin.json', '{}')
        with self.assertRaisesRegex(ValueError, 'Duplicate archive'):
            validate_zip(path)

    def test_unexpected_archive_member_is_rejected(self):
        path = Path(self.temp.name) / 'bad.zip'
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr('plugin.json', (ROOT / 'plugin.json').read_bytes())
            z.writestr('patient-data/record.json', '{}')
        with self.assertRaisesRegex(ValueError, 'Unexpected archive'):
            validate_zip(path)

    def test_symlink_is_rejected(self):
        (self.root / 'knowledge/linked.md').symlink_to(self.root / 'README.md')
        with self.assertRaisesRegex(ValueError, 'Symlink forbidden'):
            validate(self.root)


if __name__ == '__main__':
    unittest.main()
