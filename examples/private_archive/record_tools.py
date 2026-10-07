"""Offline staging helpers. No OCR, network, storage connector or clinical decisions."""
import argparse
import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads((ROOT / 'knowledge/archive_tables.json').read_text(encoding='utf-8'))
TABLES = set(CONTRACT['tables']) - {'imports'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def columns(table):
    info = CONTRACT['tables'][table]
    if table == 'imports':
        return info['columns']
    return CONTRACT['common_columns'] + (CONTRACT['fact_columns'] if info['fact'] else []) + info['columns']


def empty_row(table):
    return dict.fromkeys(columns(table))


def validate_date(value, precision):
    require(precision in CONTRACT['enums']['date_precision'], 'Unknown date precision')
    if precision == 'unknown':
        require(value is None, 'Unknown date must remain null')
        return
    require(isinstance(value, str), 'Date must be a string')
    if precision == 'year':
        require(re.fullmatch(r'[0-9]{4}', value) and 1 <= int(value) <= 9999, 'Invalid year')
    elif precision == 'month':
        require(re.fullmatch(r'[0-9]{4}-[0-9]{2}', value), 'Invalid month precision')
        date.fromisoformat(value + '-01')  # Validation only; never stored as a fabricated day.
    elif precision == 'day':
        require(re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value), 'Invalid day precision')
        date.fromisoformat(value)
    else:
        require('T' in value, 'Datetime requires a time')
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        require(parsed.tzinfo is not None, 'Datetime timezone is unknown')


def decimal_value(value):
    require(isinstance(value, str) and re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)', value),
            'Expected a finite decimal string')
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        raise ValueError('Invalid decimal representation') from None
    require(parsed.is_finite(), 'Expected finite decimal value')
    return parsed


def parse_numeric_result(raw, decimal_separator):
    """Parse an already readable token with an established separator; never guess OCR."""
    require(isinstance(raw, str), 'Raw result must be literal text')
    require(decimal_separator in {'.', ','}, 'Establish decimal separator before normalization')
    normalized = raw.strip().replace('\u2264', '<=').replace('\u2265', '>=')
    match = re.fullmatch(r'(<=|>=|<|>|=)?\s*([+-]?(?:[0-9]+(?:[.,][0-9]+)?|[.,][0-9]+))', normalized)
    require(match is not None, 'Not an unambiguous numeric token')
    token = match.group(2)
    other = ',' if decimal_separator == '.' else '.'
    require(other not in token, 'Result separator conflicts with established source format')
    value = token.replace(',', '.')
    decimal_value(value)
    return {'raw_value': raw, 'numeric_value': value, 'comparator': match.group(1) or '='}


def validate_bundle(bundle, expected_record_id, known_ids=None):
    """Check staging invariants; receipt fields must still be verified by real storage tools."""
    known_ids = known_ids or {}
    required_keys = {'schema_version', 'record_id', 'import_id', 'state', 'recorded_at', 'tables'}
    require(isinstance(bundle, dict) and required_keys <= set(bundle)
            and set(bundle) <= required_keys | {'is_synthetic'}, 'Unexpected/missing bundle field')
    if 'is_synthetic' in bundle:
        require(type(bundle['is_synthetic']) is bool, 'Invalid synthetic marker')
    require(bundle.get('schema_version') == '1.0', 'Unsupported row contract')
    require(bundle.get('record_id') == expected_record_id and bool(expected_record_id), 'Archive owner mismatch')
    require(isinstance(bundle.get('import_id'), str) and bundle['import_id'], 'Missing import ID')
    require(bundle.get('state') in CONTRACT['enums']['import_state'], 'Invalid import state')
    validate_date(bundle.get('recorded_at'), 'datetime')
    tables = bundle.get('tables')
    require(isinstance(tables, dict) and set(tables) == TABLES, 'Unexpected/missing table')
    require(all(isinstance(rows, list) for rows in tables.values()), 'Tables must contain row lists')
    ids = {}
    all_ids = set()
    for table, rows in tables.items():
        ids[table] = set(known_ids.get(table, ()))
        for row in rows:
            require(isinstance(row, dict) and set(row) == set(columns(table)), 'Unexpected/missing row column')
            for field, value in row.items():
                if field in {'size_bytes', 'page_order'}:
                    require(value is None or (type(value) is int and value >= 0), 'Invalid count/size field')
                else:
                    require(value is None or isinstance(value, str), 'Non-scalar/non-text row field')
            entry = row['entry_id']
            require(isinstance(entry, str) and entry and entry not in all_ids and entry not in ids[table], 'Duplicate/missing row ID')
            require(row['import_id'] == bundle['import_id'], 'Row belongs to another import')
            require(row['record_status'] in CONTRACT['enums']['record_status'], 'Invalid record status')
            validate_date(row['recorded_at'], 'datetime')
            all_ids.add(entry)
            ids[table].add(entry)
    hashes = set()
    for document in tables['documents']:
        validate_date(document['document_date'], document['document_date_precision'])
        digest = document['received_sha256']
        if digest is not None:
            require(isinstance(digest, str) and re.fullmatch(r'[a-f0-9]{64}', digest), 'Invalid received-byte hash')
            require(digest not in hashes, 'Duplicate source bytes: reuse a source instead of importing twice')
            hashes.add(digest)
        require(document['storage_readback_status'] in CONTRACT['enums']['storage_readback_status'], 'Invalid source readback state')
        if document['size_bytes'] is not None:
            require(type(document['size_bytes']) is int and document['size_bytes'] >= 0, 'Invalid original byte size')
        if bundle['state'] == 'committed':
            require(document['remote_file_id'] and document['storage_readback_status'] in {'metadata_verified', 'bytes_verified'},
                    'Original storage has not been verified')
    for table, rows in tables.items():
        for row in rows:
            if row['supersedes_entry_id'] is not None:
                require(row['supersedes_entry_id'] in ids[table] and row['supersedes_entry_id'] != row['entry_id'],
                        'Invalid same-table predecessor')
            if not CONTRACT['tables'][table]['fact']:
                continue
            require(row['source_kind'] in CONTRACT['enums']['source_kind'], 'Missing/invalid fact source kind')
            require(isinstance(row['source_locator'], str) and row['source_locator'].strip(), 'Missing source locator')
            if row['source_kind'] != 'owner_report':
                require(row['source_document_id'] in ids['documents'], 'Unknown source document')
            elif row['source_document_id'] is not None:
                require(row['source_document_id'] in ids['documents'], 'Unknown owner-report source document')
            validate_date(row['event_date'], row['event_date_precision'])
            require(row['review_status'] in CONTRACT['enums']['review_status'], 'Invalid transcription review status')
            if row['review_status'] in {'verified_from_source', 'user_confirmed'}:
                require(isinstance(row['source_text'], str) and row['source_text'].strip(), 'Verified fact lacks source text')
            if table == 'observations':
                validate_date(row['issued_date'], row['issued_date_precision'])
                for field in ['analyte_mapping_status', 'unit_mapping_status', 'comparability_status']:
                    require(row[field] in CONTRACT['enums']['mapping_status'], 'Unknown observation mapping status')
                if row['numeric_value'] is not None:
                    require(row['review_status'] in {'verified_from_source', 'user_confirmed'}, 'Ambiguous result must remain untyped')
                    parsed = parse_numeric_result(row['raw_value'], row['decimal_separator'])
                    require(decimal_value(row['numeric_value']) == decimal_value(parsed['numeric_value'])
                            and row['comparator'] == parsed['comparator'], 'Normalized result differs from raw token')
                    require(row['qualitative_value'] is None, 'Numeric and qualitative results conflict')
                else:
                    require(row['comparator'] is None, 'Missing result cannot have a numeric comparator')
                for field in ['reference_low', 'reference_high']:
                    if row[field] is not None:
                        decimal_value(row[field])
                if row['reference_low'] is not None and row['reference_high'] is not None:
                    require(decimal_value(row['reference_low']) <= decimal_value(row['reference_high']), 'Reference interval is reversed')
            elif table == 'medication_orders':
                require(row['actual_use_status'] == 'unknown', 'A prescription cannot establish actual use')
            elif table == 'medication_use_events':
                require(row['event_type'] in CONTRACT['enums']['medication_event_type'], 'Unknown medication event type')
                require(row['use_evidence'] in CONTRACT['enums']['use_evidence'], 'Actual-use evidence is missing')
                if row['order_entry_id'] is not None:
                    require(row['order_entry_id'] in ids['medication_orders'], 'Unknown prescription link')
                if row['use_evidence'] == 'explicit_owner_report':
                    require(row['source_kind'] == 'owner_report', 'Owner use report has a different source kind')
                elif row['use_evidence'] == 'administration_record':
                    require(row['source_kind'] == 'administration_record', 'Administration evidence has a different source kind')
                else:
                    require(row['source_kind'] == 'medical_document', 'Documented use has a different source kind')
            elif table == 'corrections':
                target = row['target_table']
                require(target in TABLES and target != 'corrections', 'Unknown correction target table')
                require(row['target_entry_id'] in ids[target], 'Unknown correction target')
                if row['replacement_entry_id'] is not None:
                    require(row['replacement_entry_id'] in ids[target] and row['replacement_entry_id'] != row['target_entry_id'],
                            'Invalid correction replacement')
                require(bool(row['reason_raw']) and bool(row['correction_authority']), 'Missing correction reason/authority')
    return {'import_id': bundle['import_id'], 'state': bundle['state'],
            'counts': {table: len(rows) for table, rows in tables.items()}}


def chart_candidates(rows, committed_import_ids, excluded_entry_ids):
    """Return exact numeric points grouped conservatively; the caller resolves corrections."""
    groups, excluded, seen = {}, {}, {}
    for row in rows:
        if row['entry_id'] in seen:
            require(row == seen[row['entry_id']], 'Conflicting chart rows share an ID')
            continue
        seen[row['entry_id']] = row
        reason = None
        if row['import_id'] not in committed_import_ids:
            reason = 'uncommitted_import'
        elif row['entry_id'] in excluded_entry_ids or row['record_status'] != 'active':
            reason = 'historical_or_erroneous_version'
        elif row['review_status'] not in {'verified_from_source', 'user_confirmed'}:
            reason = 'transcription_not_verified'
        elif row['numeric_value'] is None:
            reason = 'not_numeric'
        elif row['comparator'] != '=':
            reason = 'censored_limit_not_exact_value'
        elif row['event_date_precision'] not in {'day', 'datetime'}:
            reason = 'partial_date'
        elif any(row[field] != 'verified' for field in ['analyte_mapping_status', 'unit_mapping_status', 'comparability_status']):
            reason = 'comparability_not_verified'
        elif not all(row[field] for field in ['analyte_id', 'unit_code', 'specimen_raw', 'method_raw', 'laboratory_raw']):
            reason = 'missing_series_context'
        if reason:
            excluded[row['entry_id']] = reason
        else:
            validate_date(row['event_date'], row['event_date_precision'])
            key = tuple(row[field] for field in ['analyte_id', 'unit_code', 'specimen_raw', 'method_raw', 'laboratory_raw'])
            groups.setdefault(key, []).append({'entry_id': row['entry_id'], 'event_date': row['event_date'],
                                              'numeric_value': decimal_value(row['numeric_value'])})
    return groups, excluded


def literal_csv(value):
    if value is None:
        return ''
    text = str(value)
    # Quotes alone do not stop spreadsheet formula interpretation. Preserve raw
    # text in the private JSON; this escaped cell is only an import staging view.
    if text.lstrip().startswith(('=', '+', '-', '@')) or text.startswith(('\t', '\r', '\n')):
        return "'" + text
    return text


def outside_repository(path):
    resolved = Path(path).resolve()
    require(not resolved.is_relative_to(ROOT), 'Actual records/exports must stay outside the source repository')
    return resolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Already extracted private bundle outside the repository')
    parser.add_argument('--record-id', required=True, help='Expected private archive owner ID')
    parser.add_argument('--export-dir', help='Optional private CSV staging destination outside the repository')
    args = parser.parse_args()
    source = outside_repository(args.input)
    output = outside_repository(args.export_dir) if args.export_dir else None
    bundle = json.loads(source.read_text(encoding='utf-8'))
    report = validate_bundle(bundle, args.record_id)
    if output:
        require(not any((output / (table + '.csv')).exists() for table in bundle['tables']),
                'Staging destination already contains export files; choose a new snapshot directory')
        output.mkdir(parents=True, exist_ok=True)
        for table, rows in bundle['tables'].items():
            target = output / (table + '.csv')
            # New snapshots only: never overwrite an existing staging export.
            with target.open('x', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=columns(table), lineterminator='\n')
                writer.writeheader()
                writer.writerows({key: literal_csv(value) for key, value in row.items()} for row in rows)
    # Deliberately print counts/states, not raw clinical fields, links or content.
    print(json.dumps({'state': report['state'], 'counts': report['counts'],
                      'archive_commit_performed': False, 'staging_csv_written': bool(output),
                      'ocr_performed': False}, indent=2))


if __name__ == '__main__':
    main()
