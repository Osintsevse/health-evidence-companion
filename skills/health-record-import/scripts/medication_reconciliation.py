"""Read optional owner reconciliation without promoting historical use to current use."""
import datetime
import json

REVIEWED = {'verified_from_source', 'user_confirmed'}
POSITIVE_USE = {'started', 'regimen_reported', 'dose_taken', 'changed', 'as_needed', 'resumed'}


def read_reconciliation(connection, table_names, tables, committed, record_id=None, as_of=None):
    if 'medication_reconciliations' not in table_names:
        return None, []
    candidates = [dict(r) for r in connection.execute(
        'SELECT * FROM medication_reconciliations ORDER BY recorded_at DESC, reconciliation_id DESC')
        if r['import_id'] in committed]
    if not candidates:
        return None, []
    result = candidates[0]
    if record_id and result['record_id'] != record_id:
        raise ValueError('Medication reconciliation belongs to another owner')
    confirmed = datetime.date.fromisoformat(result['confirmed_date'])
    if as_of and confirmed > datetime.date.fromisoformat(as_of):
        raise ValueError('Medication reconciliation is newer than the snapshot date')
    ids = json.loads(result['entry_ids_json'])
    if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids) or len(ids) != len(set(ids)):
        raise ValueError('Medication reconciliation needs unique row IDs')
    by_id = {r['entry_id']: r for r in tables.get('medication_use_events', [])}
    rows = []
    for eid in ids:
        row = by_id.get(eid)
        if row is None or row.get('review_status') not in REVIEWED or row.get('event_type') not in POSITIVE_USE:
            raise ValueError('Current use must link active reviewed actual-use evidence')
        rows.append(dict(row))
    return result, rows
