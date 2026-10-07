"""Publish a checked main snapshot once per version; never replace released assets."""
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Osintsevse/health-evidence-companion'


def run(args, root=ROOT, allowed=(0,)):
    result = subprocess.run(args, cwd=root, capture_output=True, text=True)
    if result.returncode not in allowed:
        # A failed lookup is not a missing release; do not log token/error bodies.
        raise RuntimeError(f'{args[0]} command failed (exit {result.returncode})')
    return result


def release_tag(version, repository, event, ref):
    if repository != REPO:
        raise ValueError('Release publication is restricted to the maintainer repository')
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version):
        raise ValueError('Expected a stable X.Y.Z manifest version')
    tag = 'v' + version
    if not ((event in {'push', 'workflow_dispatch'} and ref == 'refs/heads/main')
            or (event == 'push' and ref == 'refs/tags/' + tag)):
        raise ValueError('Expected main or a pushed tag matching the manifest version')
    return tag


def disposition(existing, head, tag_commit):
    if existing and not existing['draft']:
        if existing.get('prerelease'):
            raise ValueError('Existing prerelease needs explicit maintainer review')
        return 'skip'
    if tag_commit and tag_commit != head:
        raise ValueError('Version tag points elsewhere; bump the version rather than move it')
    if existing and not tag_commit and existing.get('target_commitish') != head:
        raise ValueError('Draft targets a different commit; do not reuse its version')
    return 'resume' if existing else 'create'


def expected_assets(root, version):
    names = [f'health-evidence-companion-{version}.zip',
             f'health-evidence-companion-{version}-source.zip',
             'health-evidence-companion.zip', 'SETUP.md', 'SETUP_PROMPT.txt',
             'SHA256SUMS.txt', 'build-report.json']
    report = json.loads((root / 'dist/build-report.json').read_text())
    if report['version'] != version:
        raise ValueError('Build report and manifest version differ')
    platform_hashes=report.get('platform_sha256',{})
    if platform_hashes and set(platform_hashes)!={'health-evidence-companion-claude-skills.zip','PLATFORMS.md'}:
        raise ValueError('Unexpected platform assets')
    names+=list(platform_hashes)
    hashes = {name: hashlib.sha256((root / 'dist' / name).read_bytes()).hexdigest()
              for name in names}
    if set(report['sha256']) != set(names[:5]):
        raise ValueError('Build report is missing expected asset checksums')
    if any(hashes.get(name) != digest for name, digest in report['sha256'].items()):
        raise ValueError('Built asset differs from its recorded checksum')
    if any(hashes[name]!=digest for name,digest in platform_hashes.items()):
        raise ValueError('Platform asset differs from its recorded checksum')
    sums = ''.join(f'{hashes[name]}  {name}\n' for name in names[:5]+list(platform_hashes))
    if (root / 'dist/SHA256SUMS.txt').read_text() != sums:
        raise ValueError('Checksum file differs from the built assets')
    if hashes[names[0]] != hashes['health-evidence-companion.zip']:
        raise ValueError('Stable ZIP differs from the versioned plugin ZIP')
    return hashes


def missing_assets(existing, hashes):
    assets = {asset['name']: asset for asset in existing.get('assets', [])}
    if set(assets) - set(hashes):
        raise ValueError('Unexpected assets in the draft; inspect it before publication')
    for name, asset in assets.items():
        if asset.get('state') != 'uploaded' or asset.get('digest') != 'sha256:' + hashes[name]:
            raise ValueError('Existing draft asset differs or is unverifiable; do not overwrite')
    return sorted(set(hashes) - set(assets))


def find_release(command, tag):
    # Listing with publisher permissions includes drafts; lookup by tag may not.
    pages = json.loads(command(['gh', 'api', '--paginate', '--slurp',
                                f'repos/{REPO}/releases']).stdout)
    return next((item for page in pages for item in page if item['tag_name'] == tag), None)


def notes(root, version, head):
    text = (root / 'CHANGELOG.md').read_text()
    match = re.search(r'^## ' + re.escape(version) + r' - .*?\n(.*?)(?=^## |\Z)',
                      text, flags=re.M | re.S)
    if not match:
        raise ValueError('Missing changelog section for the release version')
    url = f'https://github.com/{REPO}/releases/download/v{version}'
    return (f'Download the [plugin ZIP]({url}/health-evidence-companion.zip). '
            f'Read [browser setup]({url}/SETUP.md) and the '
            f'[copy-and-paste setup prompt]({url}/SETUP_PROMPT.txt).\n\n'
            'The versioned plugin ZIP has the same bytes as the stable download. '
            'The -source.zip asset is for contributors. [Codex/Claude setup]('+url+'/PLATFORMS.md) and [Claude skill uploads]('+url+'/health-evidence-companion-claude-skills.zip) are separate assets. SHA256SUMS.txt and '
            'build-report.json accompany the downloads.\n\n'
            'This GitHub release does not publish the plugin in the ChatGPT directory. '
            'Browser creation/install options depend on account permissions.\n\n'
            f'Source commit: {head}\n\n' + match.group(1).strip() + '\n')


def publish(root=ROOT, env=None, command=None):
    env = os.environ if env is None else env
    command = (lambda args, allowed=(0,): run(args, root, allowed)) if command is None else command
    version = json.loads((root / 'plugin.json').read_text())['version']
    tag = release_tag(version, env.get('GITHUB_REPOSITORY'), env.get('GITHUB_EVENT_NAME'),
                      env.get('GITHUB_REF'))
    head = command(['git', 'rev-parse', 'HEAD']).stdout.strip()
    if head != env.get('GITHUB_SHA'):
        raise ValueError('Checked-out commit differs from the workflow commit')
    command(['git', 'merge-base', '--is-ancestor', head, 'origin/main'])
    existing = find_release(command, tag)
    has_tag = command(['git', 'show-ref', '--verify', '--quiet', 'refs/tags/' + tag],
                      allowed=(0, 1)).returncode == 0
    tag_commit = (command(['git', 'rev-parse', 'refs/tags/' + tag + '^{commit}']).stdout.strip()
                  if has_tag else None)
    action = disposition(existing, head, tag_commit)
    if action == 'skip':
        print(f'Published {tag} already exists; its tag and assets are retained. Bump the version for new contents.')
        return {'action': action, 'tag': tag}
    hashes = expected_assets(root, version)
    release_notes = root / 'dist/RELEASE_NOTES.md'
    release_notes.write_text(notes(root, version, head), encoding='utf-8')
    if action == 'create':
        request = root / 'dist/RELEASE_REQUEST.json'
        request.write_text(json.dumps({'tag_name': tag, 'target_commitish': head,
                                      'name': 'Health Evidence Companion ' + tag,
                                      'body': release_notes.read_text(), 'draft': True,
                                      'prerelease': False}), encoding='utf-8')
        # The creation response identifies this draft even if the release listing
        # has not updated yet. Never create twice or guess a release ID.
        existing = json.loads(command(['gh', 'api', '--method', 'POST',
                                       f'repos/{REPO}/releases', '--input', str(request)]).stdout)
    if not isinstance(existing, dict) or type(existing.get('id')) is not int or existing['id'] <= 0:
        raise ValueError('GitHub did not return a valid release ID; inspect its state')
    endpoint = f'repos/{REPO}/releases/{existing["id"]}'
    draft = json.loads(command(['gh', 'api', endpoint]).stdout)
    if not draft['draft'] or draft['tag_name'] != tag:
        raise ValueError('Release changed during publication; inspect its state')
    disposition(draft, head, tag_commit)
    # Validate all existing assets before any upload, then fill only missing ones.
    for name in missing_assets(draft, hashes):
        command(['gh', 'release', 'upload', tag, str(root / 'dist' / name)])
    uploaded = json.loads(command(['gh', 'api', endpoint]).stdout)
    if missing_assets(uploaded, hashes):
        raise ValueError('Release assets are incomplete; leave the release as a draft')
    published = json.loads(command(['gh', 'api', '--method', 'PATCH',
                                    f'repos/{REPO}/releases/{draft["id"]}',
                                    '-F', 'draft=false', '-f', 'make_latest=legacy']).stdout)
    if published['draft']:
        raise ValueError('GitHub did not confirm publication')
    print(published['html_url'])
    if env.get('GITHUB_STEP_SUMMARY'):
        with Path(env['GITHUB_STEP_SUMMARY']).open('a') as summary:
            summary.write(f'Published [{tag}]({published["html_url"]}).\n\n'
                          f'[Download latest ZIP](https://github.com/{REPO}/releases/latest/download/health-evidence-companion.zip).\n')
    return {'action': action, 'tag': tag, 'url': published['html_url']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if not args.execute:
        print('No changes made. GitHub Actions uses --execute after main validation/build.')
        return
    publish()


if __name__ == '__main__':
    main()
