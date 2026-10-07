"""Explicit maintainer administrative setup; dry-run by default, never handles secrets."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Osintsevse/health-evidence-companion'


def run(args):
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--protect-only', action='store_true')
    args = parser.parse_args()
    protection = {
        'required_status_checks': {'strict': True, 'contexts': ['validate-and-build']},
        'enforce_admins': False,
        'required_pull_request_reviews': {'dismiss_stale_reviews': True,
                                         'require_code_owner_reviews': True,
                                         'required_approving_review_count': 1},
        'restrictions': None, 'allow_force_pushes': False, 'allow_deletions': False,
        'required_conversation_resolution': True,
    }
    print(f'Plan: create public {REPO}, push prepared main (unless --protect-only), and apply main protection.')
    print('Owner/admin exception: enforce_admins=false permits deliberate maintainer bypass; contributor PRs require owner review.')
    print(json.dumps(protection, indent=2))
    if not args.execute:
        print('Dry run only. No network request or repository change performed.')
        return
    if not shutil.which('gh'):
        parser.error('Authenticated gh CLI is required; no credentials are collected by this script.')
    run(['gh', 'auth', 'status'])
    if not args.protect_only:
        if not (ROOT / '.git').is_dir():
            parser.error('Initialize and commit this source tree on main first; do not point this script at an unrelated repository.')
        head = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
        if head != 'main':
            parser.error('Expected main branch; inspect the checkout before executing.')
        run(['gh', 'repo', 'create', REPO, '--public', '--source', '.', '--remote', 'origin', '--push',
             '--description', 'General adult health information and evidence skills for ChatGPT'])
    with tempfile.TemporaryDirectory() as directory:
        request = Path(directory) / 'protection.json'
        request.write_text(json.dumps(protection), encoding='utf-8')
        # Close the file before gh opens it; an open NamedTemporaryFile blocks
        # ordinary readers on Windows. The directory context handles cleanup.
        run(['gh', 'api', '--method', 'PUT', f'repos/{REPO}/branches/main/protection', '--input', str(request)])
    run(['gh', 'api', f'repos/{REPO}/branches/main/protection'])


if __name__ == '__main__':
    main()
