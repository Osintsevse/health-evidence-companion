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
from validate import SOURCE_MANIFEST, check_blank, check_blank_markdown, privacy_check, source_files, validate, validate_zip
from sync_references import sync


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__', '.venv'))

    def tearDown(self):
        self.temp.cleanup()

    def allow_source(self, name):
        manifest = self.root / SOURCE_MANIFEST
        manifest.write_text(manifest.read_text(encoding='utf-8') + name + '\n', encoding='utf-8')

    def rewrite_plugin(self, name, replacement=None):
        report = build(self.root)
        source = self.root / 'dist' / f"health-evidence-companion-{report['version']}.zip"
        target = Path(self.temp.name) / 'modified.zip'
        with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, 'w') as modified:
            for member in original.infolist():
                if member.filename != name:
                    modified.writestr(member, original.read(member))
                elif replacement is not None:
                    modified.writestr(member, replacement)
        return target

    def test_unlisted_local_file_prevents_build_before_output(self):
        (self.root / 'local-note.txt').write_text('Wholly synthetic local note.', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unexpected source file'):
            build(self.root)
        self.assertFalse((self.root / 'dist').exists())

    def test_gitignored_private_directory_is_rejected(self):
        directory = self.root / 'private-records'
        directory.mkdir()
        (directory / 'synthetic.txt').write_text('Wholly fictional fixture.', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unexpected source file'):
            build(self.root)

    def test_source_archive_matches_reviewed_manifest(self):
        report = build(self.root)
        with zipfile.ZipFile(self.root / 'dist' / f"health-evidence-companion-{report['version']}-source.zip") as archive:
            self.assertEqual(set(archive.namelist()),
                             {'health-evidence-companion/' + p.as_posix() for p in source_files(self.root)})

    def test_invalid_source_manifests_are_rejected(self):
        manifest = self.root / SOURCE_MANIFEST
        original = manifest.read_text(encoding='utf-8')
        for extra in ['../outside.txt', '/outside.txt', 'C:/outside.txt', 'docs\\outside.txt',
                      'docs/../outside.txt', 'dist/output.txt', 'README.md', '']:
            with self.subTest(entry=extra):
                manifest.write_text(original + extra + '\n', encoding='utf-8')
                with self.assertRaises(ValueError):
                    source_files(self.root)
        manifest.write_text(original, encoding='utf-8')

    def test_missing_allowlisted_file_is_rejected(self):
        (self.root / 'README.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing allowlisted'):
            source_files(self.root)

    def test_filled_markdown_template_is_rejected_after_sync(self):
        card = self.root / 'knowledge/templates/patient_card.template.md'
        original = card.read_text(encoding='utf-8')
        for mutated in [original.replace('[not entered]', 'Synthetic Person', 1),
                        original + '\nPatient name: Synthetic Example\n',
                        original.replace('|---|---|---|---|', '|---|---|---|---|\n| Fictional | Reported | Synthetic | Unknown |', 1)]:
            with self.subTest():
                card.write_text(mutated, encoding='utf-8')
                sync(self.root)
                with self.assertRaisesRegex(ValueError, 'Populated or changed Markdown template'):
                    validate(self.root)

    def test_reviewed_blank_markdown_accepts_crlf(self):
        text = (self.root / 'knowledge/templates/patient_card.template.md').read_text(encoding='utf-8')
        check_blank_markdown(text.replace('\n', '\r\n'), 'patient_card.template.md')

    def test_unreviewed_markdown_template_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unreviewed Markdown template'):
            check_blank_markdown('[not entered]', 'new.template.md')

    def test_filled_markdown_archive_member_is_rejected(self):
        name = 'skills/health-record-design/references/templates/patient_card.template.md'
        original = (self.root / name).read_text(encoding='utf-8')
        archive = self.rewrite_plugin(name, original + '\nPatient: Synthetic Example\n')
        with self.assertRaisesRegex(ValueError, 'Populated or changed Markdown template'):
            validate_zip(archive)

    def test_missing_runtime_member_is_rejected(self):
        archive = self.rewrite_plugin('skills/health-explain/agents/openai.yaml')
        with self.assertRaisesRegex(ValueError, 'Missing plugin archive member'):
            validate_zip(archive)

    def test_extra_code_in_runtime_archive_is_rejected(self):
        report = build(self.root)
        archive = self.root / 'dist' / f"health-evidence-companion-{report['version']}.zip"
        with zipfile.ZipFile(archive, 'a') as modified:
            modified.writestr('assets/local.py', '# Wholly synthetic unexpected runtime code.\n')
        with self.assertRaisesRegex(ValueError, 'Unexpected archive member'):
            validate_zip(archive)

    def test_extra_runtime_code_is_rejected_even_if_source_allowlisted(self):
        name = 'skills/health-explain/agents/local.py'
        (self.root / name).write_text('# Wholly synthetic unexpected runtime code.\n', encoding='utf-8')
        self.allow_source(name)
        with self.assertRaisesRegex(ValueError, 'Unexpected plugin file'):
            build(self.root)

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
        self.allow_source('skills/health-explain/references/extra.md')
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
        try:
            (self.root / 'knowledge/linked.md').symlink_to(self.root / 'README.md')
        except OSError as exc:
            if sys.platform == 'win32' and getattr(exc, 'winerror', None) == 1314:
                self.skipTest('Windows symlink privilege is unavailable; Linux CI must run this check.')
            raise
        with self.assertRaisesRegex(ValueError, 'Symlink forbidden'):
            validate(self.root)

    def test_archive_symlink_is_rejected_without_os_privileges(self):
        path = Path(self.temp.name) / 'symlink.zip'
        member = zipfile.ZipInfo('assets/link.txt')
        member.create_system = 3
        member.external_attr = 0o120777 << 16
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('plugin.json', (ROOT / 'plugin.json').read_bytes())
            archive.writestr(member, 'synthetic-target')
        with self.assertRaisesRegex(ValueError, 'Archive symlink'):
            validate_zip(path)


if __name__ == '__main__':
    unittest.main()
