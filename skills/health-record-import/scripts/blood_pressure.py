"""Read-only source-local BP projection; no inferred pairing or missing values."""
import datetime as dt
import math
import re

ALIASES = {
    'sys': {'sys', 'sbp', 'systolic', 'systolic blood pressure', '\u0441\u0438\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435', '\u0441\u0438\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435', '\u0441\u0430\u0434'},
    'dia': {'dia', 'dbp', 'diastolic', 'diastolic blood pressure', '\u0434\u0438\u0430\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435', '\u0434\u0438\u0430\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435', '\u0434\u0430\u0434'},
    'pulse': {'pulse', 'pr', 'heart rate', 'hr', '\u043f\u0443\u043b\u044c\u0441', '\u0447\u0441\u0441'},
}
BP_UNITS = {'mmhg', 'mm hg', '\u043c\u043c \u0440\u0442. \u0441\u0442.', '\u043c\u043c \u0440\u0442 \u0441\u0442', '\u043c\u043c\u0440\u0442\u0441\u0442'}
PULSE_UNITS = {'bpm', 'beats/min', '/min', '1/min', '\u0443\u0434/\u043c\u0438\u043d', '\u0443\u0434./\u043c\u0438\u043d', '\u043c\u0438\u043d-1'}
VERIFIED = {'verified_from_source', 'user_confirmed'}


def component(row):
    name = str(row.get('analyte_name_raw') or '').strip().casefold()
    return next((key for key, names in ALIASES.items() if name in names), None)


def locator_key(locator):
    """Remove only an explicit terminal component label; keep measurement IDs."""
    names = sorted({n for names in ALIASES.values() for n in names}, key=len, reverse=True)
    pattern = r'\s*[;:|]\s*(?:' + '|'.join(re.escape(n) for n in names) + r')\s*$'
    return re.sub(pattern, '', str(locator or '').strip(), flags=re.I)


def exact_value(row, kind):
    if row.get('review_status') not in VERIFIED or row.get('record_status', 'active') != 'active':
        return None, 'unreviewed_or_inactive'
    if row.get('comparator') not in (None, '', '='):
        return None, 'non_exact'
    raw = str(row.get('raw_value') or '').strip().replace(',', '.')
    if not re.fullmatch(r'\d+(?:\.\d+)?', raw):
        return None, 'non_exact'
    try:
        value = float(row['numeric_value'])
    except (ValueError, TypeError, KeyError):
        return None, 'non_numeric'
    if not math.isfinite(value) or value <= 0 or value != float(raw):
        return None, 'non_exact'
    units = BP_UNITS if kind in ('sys', 'dia') else PULSE_UNITS
    if str(row.get('unit_raw') or '').strip().casefold() not in units:
        return None, 'unsupported_unit'
    return value, None


def recorded_date_time(row, as_of):
    raw = str(row.get('event_date') or '')
    date = None
    if row.get('event_date_precision', 'day') in ('day', 'datetime', 'minute', 'second'):
        try:
            parsed = dt.date.fromisoformat(raw[:10]) if re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T.*)?', raw) else None
            if parsed and (not as_of or parsed.isoformat() <= as_of):
                date = parsed.isoformat()
        except ValueError:
            pass
    match = re.search(r'T(\d{2}:\d{2})(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?$', raw)
    if not match:
        match = re.search(r'\([12]\)(\d{2}:\d{2})(?!\d)', str(row.get('source_locator') or ''))
    time = match[1] if match else None
    if time and not (0 <= int(time[:2]) < 24 and 0 <= int(time[3:]) < 60):
        time = None
    return date, time


def category(sys, dia):
    """AHA 2025 adult educational categories; low flag separately per S391."""
    if sys is None or dia is None:
        return 'unknown'
    high = 'stage2' if sys >= 140 or dia >= 90 else 'stage1' if sys >= 130 or dia >= 80 else 'elevated' if sys >= 120 else 'normal'
    if sys < 90 or dia < 60:
        return 'mixed' if high in ('stage1', 'stage2') else 'low'
    return high


def build_dashboard(model, config):
    groups, excluded = {}, []
    for row in model.get('tables', {}).get('observations', []):
        kind = component(row)
        if not kind:
            continue
        value, reason = exact_value(row, kind)
        if reason:
            excluded.append({'entry_id': row.get('entry_id'), 'reason': reason})
            continue
        locator = locator_key(row.get('source_locator'))
        # No locator means no evidence that components belong together.
        key = (row.get('source_document_id'), row.get('event_date'), locator if locator and row.get('source_document_id') else row.get('entry_id'), row.get('method_raw'), row.get('specimen_raw'))
        groups.setdefault(key, []).append((kind, value, row))
    measurements = []
    overlay = config.get('blood_pressure_categories') == 'aha_2025_adult'
    for group in groups.values():
        ambiguous = len({k for k, _, _ in group}) != len(group) or not group[0][2].get('source_document_id') or not locator_key(group[0][2].get('source_locator'))
        # Duplicates may be multiple readings; never zip them or overwrite values.
        partitions = [[item] for item in group] if ambiguous else [group]
        for partition in partitions:
            first = partition[0][2]
            date, time = recorded_date_time(first, model.get('as_of'))
            setting = 'abpm' if 'ABPM' in str(first.get('method_raw') or '').upper() else 'unspecified'
            values = {k: v for k, v, _ in partition}
            measurements.append({
                'index': len(measurements) + 1, 'date': date, 'time': time,
                'date_raw': first.get('event_date'), 'setting': setting,
                'sys': values.get('sys'), 'dia': values.get('dia'), 'pulse': values.get('pulse'),
                'category': category(values.get('sys'), values.get('dia')) if overlay and setting != 'abpm' else 'unknown',
                'ambiguous': ambiguous, 'sources': [r for _, _, r in partition],
            })
    return {'format': 'blood-pressure-v1', 'measurements': measurements,
            'excluded': excluded, 'category_scheme': 'aha_2025_adult' if overlay else None,
            'entry_ids': [r['entry_id'] for m in measurements for r in m['sources']]}
