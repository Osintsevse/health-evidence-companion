"""Offline release state-machine checks; never access GitHub or publish during PR tests."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from release import REPO, expected_assets, notes, publish, release_tag

HEAD = 'a' * 40
VERSION = '0.2.1'
TAG = 'v' + VERSION


class FakeCommands:
    def __init__(self, root, existing=None, tag_commit=None):
        self.root = root
        self.release = copy.deepcopy(existing)
        self.tag_commit = tag_commit
        self.calls = []
        self.fail_listing = False
        self.fail_upload = None
        self.drop_upload = None
        self.reviewed = True
        self.stale_listing_after_create = False
        self.created = False

    def __call__(self, args, allowed=(0,)):
        self.calls.append(args)
        data = ''
        code = 0
        if args == ['git', 'rev-parse', 'HEAD']:
            data = HEAD
        elif args[:2] == ['git', 'merge-base']:
            if not self.reviewed:
                raise RuntimeError('Commit is not in reviewed main')
        elif args[:2] == ['git', 'show-ref']:
            code = 0 if self.tag_commit else 1
        elif args[:2] == ['git', 'rev-parse']:
            data = self.tag_commit
        elif args[:4] == ['gh', 'api', '--paginate', '--slurp']:
            if self.fail_listing:
                raise RuntimeError('GitHub lookup failed')
            visible = self.release and not (self.created and self.stale_listing_after_create)
            data = json.dumps([[{'tag_name': 'v0.0.1', 'id': 1}],
                               [self.release] if visible else []])
        elif args[:5] == ['gh', 'api', '--method', 'POST', f'repos/{REPO}/releases']:
            payload = json.loads(Path(args[args.index('--input') + 1]).read_text())
            self.release = {'id': 17, 'assets': [], **payload}
            self.created = True
            data = json.dumps(self.release)
        elif args[:3] == ['gh', 'release', 'upload']:
            path = Path(args[4])
            if path.name == self.fail_upload:
                raise RuntimeError('Upload interrupted')
            if path.name != self.drop_upload:
                self.release['assets'].append({'name': path.name, 'state': 'uploaded',
                    'digest': 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()})
        elif args[:4] == ['gh', 'api', '--method', 'PATCH']:
            self.release['draft'] = False
            self.release['html_url'] = f'https://github.com/{REPO}/releases/tag/{TAG}'
            data = json.dumps(self.release)
        elif args == ['gh', 'api', f'repos/{REPO}/releases/17']:
            data = json.dumps(self.release)
        else:
            raise AssertionError(f'Unexpected command: {args}')
        if code not in allowed:
            raise RuntimeError('Unexpected command exit')
        return subprocess.CompletedProcess(args, code, stdout=data, stderr='')

    def mutations(self):
        return [args for args in self.calls if args[:2] == ['gh', 'release']
                or args[:4] in [['gh', 'api', '--method', 'POST'],
                               ['gh', 'api', '--method', 'PATCH']]]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'plugin.json').write_text(json.dumps({'version': VERSION}))
        (self.root / 'CHANGELOG.md').write_text(f'# Changelog\n\n## {VERSION} - 2026-10-07\n\n- Delivery update.\n')
        dest = self.root / 'dist'
        dest.mkdir()
        names = [f'health-evidence-companion-{VERSION}.zip',
                 f'health-evidence-companion-{VERSION}-source.zip',
                 'health-evidence-companion.zip', 'SETUP.md', 'SETUP_PROMPT.txt']
        for name in names:
            (dest / name).write_bytes(b'synthetic plugin' if name in {names[0], names[2]}
                                     else ('synthetic ' + name).encode())
        self.hashes = {name: hashlib.sha256((dest / name).read_bytes()).hexdigest() for name in names}
        (dest / 'SHA256SUMS.txt').write_text(''.join(f'{digest}  {name}\n' for name, digest in self.hashes.items()))
        (dest / 'build-report.json').write_text(json.dumps({'version': VERSION, 'sha256': self.hashes}))
        self.env = {'GITHUB_REPOSITORY': REPO, 'GITHUB_EVENT_NAME': 'push',
                    'GITHUB_REF': 'refs/heads/main', 'GITHUB_SHA': HEAD}

    def tearDown(self):
        self.temp.cleanup()

    def draft(self, assets=None, target=HEAD):
        return {'id': 17, 'tag_name': TAG, 'draft': True, 'prerelease': False,
                'target_commitish': target, 'assets': assets or []}

    def asset(self, name, digest=None, state='uploaded'):
        hashes = expected_assets(self.root, VERSION)
        return {'name': name, 'state': state, 'digest': digest or 'sha256:' + hashes[name]}

    def test_create_then_publish_only_after_all_seven_verified_assets(self):
        fake = FakeCommands(self.root)
        result = publish(self.root, self.env, fake)
        self.assertEqual(result['action'], 'create')
        self.assertFalse(fake.release['draft'])
        self.assertEqual({a['name'] for a in fake.release['assets']}, set(expected_assets(self.root, VERSION)))
        create = next(args for args in fake.calls if args[:4] == ['gh', 'api', '--method', 'POST'])
        payload = json.loads(Path(create[create.index('--input') + 1]).read_text())
        self.assertEqual(payload['tag_name'], TAG)
        self.assertEqual(payload['target_commitish'], HEAD)
        self.assertIs(payload['draft'], True)
        self.assertEqual(fake.calls[-1][-4:], ['-F', 'draft=false', '-f', 'make_latest=legacy'])
        self.assertFalse(any('/releases/tags/' in arg for args in fake.calls for arg in args))
        self.assertFalse(any('--clobber' in args for args in fake.calls))


    def test_changelog_accepts_typographic_dashes_and_stops_at_next_version(self):
        for separator in ('-', '\u2013', '\u2014'):
            with self.subTest(separator=separator):
                (self.root / 'CHANGELOG.md').write_text(
                    f'# Changelog\n\n## {VERSION} {separator} 2026-10-08\n\n'
                    '- Current release.\n\n## 0.2.0 - 2026-10-07\n\n- Older release.\n',
                    encoding='utf-8')
                fake = FakeCommands(self.root)
                self.assertEqual(publish(self.root, self.env, fake)['action'], 'create')
                self.assertIn('Current release.', fake.release['body'])
                self.assertNotIn('Older release.', fake.release['body'])

    def test_current_manifest_has_extractable_release_notes(self):
        root = Path(__file__).resolve().parents[1]
        version = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))['version']
        result = notes(root, version, HEAD)
        self.assertIn(f'/releases/download/v{version}', result)
        self.assertIn(f'Source commit: {HEAD}', result)

    def test_published_version_is_not_overwritten_even_from_later_main(self):
        existing = self.draft()
        existing['draft'] = False
        fake = FakeCommands(self.root, existing, tag_commit='b' * 40)
        self.assertEqual(publish(self.root, self.env, fake)['action'], 'skip')
        self.assertEqual(fake.mutations(), [])

    def test_new_draft_can_publish_before_it_appears_in_release_listing(self):
        fake = FakeCommands(self.root)
        fake.stale_listing_after_create = True
        self.assertEqual(publish(self.root, self.env, fake)['action'], 'create')
        self.assertFalse(fake.release['draft'])
        listings = [args for args in fake.calls if args[:4] == ['gh', 'api', '--paginate', '--slurp']]
        self.assertEqual(len(listings), 1)

    def test_resumes_draft_and_retains_matching_existing_asset(self):
        asset = self.asset('SETUP.md')
        fake = FakeCommands(self.root, self.draft([asset]), HEAD)
        self.assertEqual(publish(self.root, self.env, fake)['action'], 'resume')
        uploads = [Path(args[4]).name for args in fake.calls if args[:3] == ['gh', 'release', 'upload']]
        self.assertNotIn('SETUP.md', uploads)
        self.assertEqual(len(uploads), 6)
        self.assertEqual(fake.release['assets'][0], asset)

    def test_interrupted_upload_stays_draft_and_retry_fills_missing_assets(self):
        fake = FakeCommands(self.root)
        fake.fail_upload = 'health-evidence-companion.zip'
        with self.assertRaisesRegex(RuntimeError, 'interrupted'):
            publish(self.root, self.env, fake)
        self.assertTrue(fake.release['draft'])
        self.assertTrue(fake.release['assets'])
        retained = copy.deepcopy(fake.release['assets'])
        fake.calls.clear()
        fake.fail_upload = None
        self.assertEqual(publish(self.root, self.env, fake)['action'], 'resume')
        uploaded = {Path(args[4]).name for args in fake.calls if args[:3] == ['gh', 'release', 'upload']}
        self.assertTrue(uploaded.isdisjoint(a['name'] for a in retained))
        self.assertFalse(fake.release['draft'])

    def test_missing_server_asset_prevents_publication(self):
        fake = FakeCommands(self.root)
        fake.drop_upload = 'SETUP_PROMPT.txt'
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            publish(self.root, self.env, fake)
        self.assertTrue(fake.release['draft'])
        self.assertFalse(any(args[:4] == ['gh', 'api', '--method', 'PATCH'] for args in fake.calls))

    def test_conflicting_or_unverifiable_draft_asset_stops_before_upload(self):
        for asset in [self.asset('SETUP.md', 'sha256:bad'),
                      self.asset('SETUP.md', state='starter'),
                      {'name': 'unexpected.zip', 'state': 'uploaded', 'digest': 'sha256:bad'}]:
            with self.subTest(asset=asset):
                fake = FakeCommands(self.root, self.draft([asset]))
                with self.assertRaises(ValueError):
                    publish(self.root, self.env, fake)
                self.assertEqual(fake.mutations(), [])

    def test_tag_or_draft_commit_conflict_never_moves_a_tag(self):
        for existing, tag_commit in [(None, 'b' * 40), (self.draft(target='main'), None),
                                     (self.draft(), 'b' * 40)]:
            with self.subTest(existing=existing, tag_commit=tag_commit):
                fake = FakeCommands(self.root, existing, tag_commit)
                with self.assertRaises(ValueError):
                    publish(self.root, self.env, fake)
                self.assertEqual(fake.mutations(), [])

    def test_lookup_failure_is_not_treated_as_a_missing_release(self):
        fake = FakeCommands(self.root)
        fake.fail_listing = True
        with self.assertRaisesRegex(RuntimeError, 'lookup failed'):
            publish(self.root, self.env, fake)
        self.assertEqual(fake.mutations(), [])

    def test_wrong_checkout_and_unreviewed_tag_are_rejected(self):
        fake = FakeCommands(self.root)
        with self.assertRaisesRegex(ValueError, 'Checked-out'):
            publish(self.root, dict(self.env, GITHUB_SHA='b' * 40), fake)
        self.assertEqual(fake.mutations(), [])
        fake = FakeCommands(self.root)
        fake.reviewed = False
        with self.assertRaises(RuntimeError):
            publish(self.root, dict(self.env, GITHUB_REF='refs/tags/' + TAG), fake)
        self.assertEqual(fake.mutations(), [])

    def test_matching_main_tag_and_main_dispatch_are_allowed(self):
        for event, ref in [('push', 'refs/tags/' + TAG), ('workflow_dispatch', 'refs/heads/main')]:
            with self.subTest(event=event, ref=ref):
                self.assertEqual(release_tag(VERSION, REPO, event, ref), TAG)

    def test_forks_pull_requests_feature_branches_and_wrong_tags_are_rejected(self):
        for repository, event, ref in [('someone/fork', 'push', 'refs/heads/main'),
                (REPO, 'pull_request', 'refs/pull/1/merge'),
                (REPO, 'push', 'refs/heads/feature'),
                (REPO, 'push', 'refs/tags/v9.0.0'),
                (REPO, 'workflow_dispatch', 'refs/tags/' + TAG)]:
            with self.subTest(repository=repository, event=event, ref=ref):
                fake = FakeCommands(self.root)
                with self.assertRaises(ValueError):
                    publish(self.root, dict(self.env, GITHUB_REPOSITORY=repository,
                                           GITHUB_EVENT_NAME=event, GITHUB_REF=ref), fake)
                self.assertEqual(fake.calls, [])

    def test_unstable_or_malformed_versions_are_rejected(self):
        for version in ['0.2.1-beta', 'v0.2.1', '00.2.1', '0.2', '']:
            with self.subTest(version=version), self.assertRaises(ValueError):
                release_tag(version, REPO, 'push', 'refs/heads/main')

    def test_corrupted_build_or_changelog_never_creates_a_draft(self):
        mutations = [(self.root / 'dist/SETUP.md', b'changed'),
                     (self.root / 'dist/SHA256SUMS.txt', b'wrong sums'),
                     (self.root / 'CHANGELOG.md', b'# Missing version\n')]
        for path, data in mutations:
            with self.subTest(path=path):
                original = path.read_bytes()
                path.write_bytes(data)
                fake = FakeCommands(self.root)
                with self.assertRaises(ValueError):
                    publish(self.root, self.env, fake)
                self.assertEqual(fake.mutations(), [])
                path.write_bytes(original)

    def test_incomplete_checksum_report_is_rejected(self):
        path = self.root / 'dist/build-report.json'
        report = json.loads(path.read_text())
        del report['sha256']['SETUP.md']
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'missing expected'):
            expected_assets(self.root, VERSION)

    def test_existing_prerelease_needs_maintainer_review(self):
        existing = self.draft()
        existing.update(draft=False, prerelease=True)
        fake = FakeCommands(self.root, existing)
        with self.assertRaisesRegex(ValueError, 'prerelease'):
            publish(self.root, self.env, fake)
        self.assertEqual(fake.mutations(), [])


if __name__ == '__main__':
    unittest.main()
