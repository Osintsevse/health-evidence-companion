"""Offline, owner-selected summaries only. Never discover or read a private diary."""
import argparse
import json
import os
import re
import tempfile
from pathlib import Path

SCHEMA = 'psychology-sharing-summary-v1'
MAX_BYTES = 2 * 1024 * 1024


def _string(value, name, limit, required=True):
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()):
        raise ValueError('Invalid ' + name)
    if any(ord(c) < 32 and c not in '\n\r\t' for c in value):
        raise ValueError('Control characters in ' + name)
    return value


def _id(value, name):
    _string(value, name, 128)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value) or '..' in value:
        raise ValueError('Invalid ' + name)
    return value


def project_summary(data, owner_key):
    """Validate and copy only allowed summary fields; discard all extra fields."""
    owner_key = _id(owner_key, 'owner_key')
    if not isinstance(data, dict) or data.get('schema') != SCHEMA:
        raise ValueError('Unsupported psychology summary schema')
    if data.get('selection_scope') != 'owner_selected_summary':
        raise ValueError('Explicit owner selection is required')
    if _id(data.get('owner_key'), 'owner_key') != owner_key:
        raise ValueError('Psychology summary owner mismatch')
    rows = data.get('summaries')
    if not isinstance(rows, list) or len(rows) > 1000:
        raise ValueError('Invalid summaries list')
    output = {'schema': SCHEMA, 'owner_key': owner_key,
              'selection_scope': 'owner_selected_summary', 'summaries': []}
    if 'label' in data:
        output['label'] = _string(data['label'], 'label', 256)
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Invalid summary record')
        record_id = _id(row.get('record_id'), 'record_id')
        if record_id in seen:
            raise ValueError('Duplicate summary record_id')
        seen.add(record_id)
        projected = {'record_id': record_id,
                     'title': _string(row.get('title'), 'title', 512),
                     'text': _string(row.get('text'), 'text', 100000)}
        for key, limit in [('source_ref', 2048), ('as_of', 128)]:
            if key in row:
                projected[key] = _string(row[key], key, limit)
        output['summaries'].append(projected)
    if len(json.dumps(output, ensure_ascii=True).encode('utf-8')) > MAX_BYTES:
        raise ValueError('Summary exceeds 2 MiB limit')
    return output


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field')
        result[key] = value
    return result


def read_summary(path, owner_key):
    """Read exactly the explicit local JSON file, bounded even if it changes."""
    owner_key = _id(owner_key, 'owner_key')
    path = Path(path)
    if not path.is_file():
        raise ValueError('Summary must be an explicitly selected local file')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Summary exceeds 2 MiB limit')
    return project_summary(json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object), owner_key)


def load_summary(config):
    settings = config.get('psychology')
    if settings is None:
        return None
    if not isinstance(settings, dict):
        raise ValueError('Invalid psychology configuration')
    # No inline summary, diary fallback, account lookup or guessed owner identity.
    if not isinstance(settings.get('summary_path'), str) or not settings['summary_path'].strip():
        raise ValueError('Explicit psychology.summary_path is required')
    return read_summary(settings['summary_path'], settings.get('owner_key'))


def share_summary(data, output, owner_key):
    """Publish an already selected summary locally, atomically without overwrite."""
    selected = project_summary(data, owner_key)
    destination = Path(output).resolve()
    source_root = next((p for p in Path(__file__).resolve().parents
                        if (p / 'plugin.json').is_file() and (p / 'skills').is_dir()), None)
    if source_root is None:
        source_root = next((p for p in Path(__file__).resolve().parents
                            if (p / 'SKILL.md').is_file() and (p / 'scripts').is_dir()), None)
    if source_root is not None and (destination == source_root or source_root in destination.parents):
        raise ValueError('Private summary must remain outside the public plugin source tree')
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(selected, ensure_ascii=True, indent=2).encode('utf-8')
    if len(payload) > MAX_BYTES:
        raise ValueError('Summary exceeds 2 MiB limit')
    fd, temporary = tempfile.mkstemp(prefix='.psychology-summary-', dir=destination.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        # Windows rename refuses overwrite; POSIX hard-link creation does too.
        if os.name == 'nt':
            os.rename(temporary, destination)
        else:
            os.link(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return selected


def ui_labels(locale):
    if locale.startswith('ru'):
        return {'psychology': '\u041f\u0441\u0438\u0445\u043e\u043b\u043e\u0433\u0438\u044f',
                'psychologyNotice': '\u0422\u043e\u043b\u044c\u043a\u043e \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0435 \u0432\u043b\u0430\u0434\u0435\u043b\u044c\u0446\u0435\u043c \u0441\u0432\u043e\u0434\u043a\u0438. \u0418\u0441\u0445\u043e\u0434\u043d\u044b\u0439 \u0434\u043d\u0435\u0432\u043d\u0438\u043a \u0445\u0440\u0430\u043d\u0438\u0442\u0441\u044f \u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e.',
                'psychologySource': '\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a',
                'psychologyAsOf': '\u041f\u043e \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044e \u043d\u0430'}
    return {'psychology': 'Psychology',
            'psychologyNotice': 'Only owner-selected summaries. The original diary is stored separately.',
            'psychologySource': 'Source reference', 'psychologyAsOf': 'As of'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='Already owner-selected summary JSON, never a diary')
    parser.add_argument('--output', required=True)
    parser.add_argument('--owner-key', required=True)
    args = parser.parse_args()
    share_summary(read_summary(args.input, args.owner_key), args.output, args.owner_key)
