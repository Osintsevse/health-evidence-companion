"""Plan changed private files only. No network, upload, deletion or locking."""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


def managed_path(root, name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Managed paths must be relative POSIX paths')
    parts = name.split('/')
    rel = PurePosixPath(name)
    if rel.is_absolute() or any(p in ('', '.', '..') or ':' in p for p in parts):
        raise ValueError('Unsafe managed path')
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('Symlink in managed path')
    if not path.resolve().is_relative_to(root):
        raise ValueError('Managed path escapes root')
    if not path.is_file():
        raise ValueError('Managed file missing; no deletion is planned')
    return path


def build_plan(root, managed, state, archive_key, operation_id):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Root must be a directory')
    if not archive_key or not operation_id:
        raise ValueError('Archive key and stable operation ID required')
    if not isinstance(managed, list) or any(not isinstance(p, str) for p in managed):
        raise ValueError('Managed files must be a list of paths')
    if len(managed) != len(set(managed)):
        raise ValueError('Duplicate managed path')
    if state.get('archive_key') != archive_key or not isinstance(state.get('files'), dict):
        raise ValueError('Sync state belongs to a different archive or is invalid')
    actions = []
    for name in sorted(managed):
        path = managed_path(root, name)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        old = state['files'].get(name)
        if old is None:
            action, reason = 'create_candidate', 'No prior target; discover by operation/path before creation'
        else:
            if not isinstance(old, dict):
                raise ValueError('Invalid sync entry')
            verified = (old.get('status') == 'verified' and
                        isinstance(old.get('sha256'), str) and
                        re.fullmatch('[0-9a-f]{64}', old['sha256']) and
                        bool(old.get('file_id')) and old.get('remote_version') is not None)
            if not verified:
                action, reason = 'inspect_remote', 'Prior outcome or remote version is unverified'
            elif old['sha256'] == digest:
                action, reason = 'skip_candidate', 'Bytes match last readback; confirm remote version before skipping'
            else:
                action, reason = 'update_candidate', 'Bytes changed; reconcile if the remote base changed'
        actions.append({'path': name, 'sha256': digest, 'size_bytes': len(data),
                        'action': action, 'reason': reason,
                        'file_id': old.get('file_id') if old else None,
                        'expected_remote_version': old.get('remote_version') if old else None})
    return {'format': 'private_archive_sync_plan', 'schema_version': '1.0',
            'archive_key': archive_key, 'operation_id': operation_id,
            'root': str(root), 'actions': actions,
            'uploaded': False, 'verified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--managed', required=True, help='Private JSON list of managed relative paths')
    parser.add_argument('--state', required=True, help='Private JSON sync state from remote readback')
    parser.add_argument('--archive-key', required=True)
    parser.add_argument('--operation-id', required=True)
    parser.add_argument('--output', required=True, help='Private output JSON plan')
    args = parser.parse_args()
    plan = build_plan(args.root, json.loads(Path(args.managed).read_text(encoding='utf-8')),
                      json.loads(Path(args.state).read_text(encoding='utf-8')),
                      args.archive_key, args.operation_id)
    output = Path(args.output).resolve()
    source_root = next((p for p in Path(__file__).resolve().parents
                        if (p / 'plugin.json').is_file() and (p / 'skills').is_dir()), None)
    if source_root is not None and output.is_relative_to(source_root):
        raise ValueError('Private plan must remain outside plugin source')
    inputs = {Path(args.managed).resolve(), Path(args.state).resolve()}
    inputs.update(Path(plan['root']) / a['path'] for a in plan['actions'])
    if output in inputs:
        raise ValueError('Output cannot overwrite an input or managed file')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    print('Plan staged; no archive files uploaded or verified.')


if __name__ == '__main__':
    main()
