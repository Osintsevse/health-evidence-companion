"""Generate entirely blank archive import forms from the public column contract."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_TEMPLATES = {
    'source_document.template.json': 'documents',
    'lab_result.template.json': 'observations',
    'clinical_entry.template.json': 'clinical_entries',
    'medication_order.template.json': 'medication_orders',
    'medication_use_event.template.json': 'medication_use_events',
    'correction_entry.template.json': 'corrections',
}


def columns(contract, table):
    info = contract['tables'][table]
    if table == 'imports':
        return info['columns']
    return contract['common_columns'] + (contract['fact_columns'] if info['fact'] else []) + info['columns']


def expected_templates(root=ROOT):
    contract = json.loads((root / 'knowledge/archive_tables.json').read_text(encoding='utf-8'))
    forms = {name: {'is_blank_template': True, **dict.fromkeys(columns(contract, table))}
             for name, table in TABLE_TEMPLATES.items()}
    forms['archive_import.template.json'] = {
        'is_blank_template': True, 'schema_version': '1.0', 'record_id': None,
        'import_id': None, 'state': None, 'recorded_at': None,
        'tables': {table: [] for table in contract['tables'] if table != 'imports'},
    }
    forms['archive_config.template.json'] = {
        'is_blank_template': True, 'schema_version': '1.0', 'record_id': None,
        'storage_backend': None, 'root_folder_id': None, 'ledger_file_id': None,
        'folder_ids': dict.fromkeys(['originals', 'imports', 'derived', 'backups']),
        'owner_context': None, 'destination_authorization': None,
        'access_checked_at': None, 'last_verified_at': None, 'writer_policy': None,
    }
    return {Path('knowledge/templates') / name: (json.dumps(data, indent=2) + '\n').encode('utf-8')
            for name, data in forms.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for relative, content in expected_templates().items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_bytes().replace(b'\r\n', b'\n') != content:
                raise ValueError(f'Stale/missing generated blank form: {relative}')
        else:
            path.write_bytes(content)
    print('Checked blank archive forms.' if args.check else 'Generated blank archive forms; synchronize references next.')


if __name__ == '__main__':
    main()
