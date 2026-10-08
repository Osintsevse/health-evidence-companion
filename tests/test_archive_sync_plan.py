"""Wholly synthetic sync planning; no live archive or connector."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/health-record-import/scripts/plan_archive_sync.py'
SPEC = importlib.util.spec_from_file_location('sync_plan', SCRIPT)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class SyncPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'summary.md').write_bytes(b'Synthetic summary\n')
        self.state = {'archive_key': 'synthetic-archive', 'files': {}}

    def plan(self, managed=None, state=None):
        return SYNC.build_plan(self.root, managed or ['summary.md'],
                               state or self.state, 'synthetic-archive', 'synthetic-operation')

    def verified(self):
        return {'status': 'verified', 'sha256': hashlib.sha256(b'Synthetic summary\n').hexdigest(),
                'file_id': 'synthetic-file', 'remote_version': 'v1'}

    def test_verified_unchanged_is_conditional_skip(self):
        self.state['files']['summary.md'] = self.verified()
        plan = self.plan()
        self.assertEqual(plan['actions'][0]['action'], 'skip_candidate')
        self.assertEqual(plan['actions'][0]['expected_remote_version'], 'v1')
        self.assertFalse(plan['verified'])
        self.assertFalse(plan['uploaded'])
        self.assertEqual(plan, self.plan())

    def test_changed_file_preserves_remote_base(self):
        self.state['files']['summary.md'] = self.verified()
        (self.root / 'summary.md').write_bytes(b'Synthetic correction\n')
        item = self.plan()['actions'][0]
        self.assertEqual(item['action'], 'update_candidate')
        self.assertEqual(item['file_id'], 'synthetic-file')
        self.assertEqual(self.state['files']['summary.md']['remote_version'], 'v1')

    def test_unknown_outcome_is_inspected_even_if_hash_matches(self):
        for status in ('unknown', 'failed', 'uploaded'):
            entry = self.verified()
            entry['status'] = status
            self.state['files']['summary.md'] = entry
            self.assertEqual(self.plan()['actions'][0]['action'], 'inspect_remote')

    def test_no_verified_version_cannot_skip(self):
        entry = self.verified()
        del entry['remote_version']
        self.state['files']['summary.md'] = entry
        self.assertEqual(self.plan()['actions'][0]['action'], 'inspect_remote')

    def test_new_file_is_only_a_creation_candidate(self):
        self.assertEqual(self.plan()['actions'][0]['action'], 'create_candidate')
        self.assertEqual((self.root / 'summary.md').read_bytes(), b'Synthetic summary\n')

    def test_other_archive_and_duplicate_paths_rejected(self):
        with self.assertRaises(ValueError):
            self.plan(state={'archive_key': 'other', 'files': {}})
        with self.assertRaises(ValueError):
            self.plan(managed=['summary.md', 'summary.md'])

    def test_unsafe_or_missing_paths_do_not_become_deletions(self):
        for name in ('../summary.md', '/summary.md', 'C:/summary.md', 'a\\summary.md',
                     './summary.md', 'a//summary.md', 'missing.md', 'summary.md:stream'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.plan(managed=[name])

    def test_unmanaged_files_excluded(self):
        (self.root / 'owner-answers.txt').write_bytes(b'Synthetic private answers')
        self.assertEqual([a['path'] for a in self.plan()['actions']], ['summary.md'])

    def test_symlink_rejected(self):
        try:
            (self.root / 'link.md').symlink_to(self.root / 'summary.md')
        except OSError:
            self.skipTest('Symlink creation unavailable on host')
        with self.assertRaises(ValueError):
            self.plan(managed=['link.md'])


if __name__ == '__main__':
    unittest.main()
