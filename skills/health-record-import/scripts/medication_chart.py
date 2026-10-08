"""Build source-linked display annotations; never infer intervals from event gaps."""
import datetime
import re


def valid_date(value):
    if value is None:
        return
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?', value):
        raise ValueError('Invalid chart date precision')
    first=datetime.date.fromisoformat(value + ('-01-01' if len(value) == 4 else '-01' if len(value) == 7 else ''))
    if len(value)==4:last=datetime.date(first.year,12,31)
    elif len(value)==7:last=datetime.date(first.year+(first.month==12),first.month%12+1,1)-datetime.timedelta(days=1)
    else:last=first
    return first,last


def build_chart(events, config, as_of=None):
    by_id = {e['entry_id']: e for e in events}
    if len(by_id) != len(events):raise ValueError('Medication chart needs unique event IDs')
    valid_date(as_of)
    definitions = config.get('medication_timeline_themes', [])
    themes = []
    used = set()
    for theme in definitions:
        if not isinstance(theme.get('id'),str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',theme['id']) or theme['id'] in used or not isinstance(theme.get('label'),str) or not theme['label'].strip():
            raise ValueError('Invalid or duplicate medicine theme')
        used.add(theme['id'])
        for field in ('groups', 'entry_ids', 'source_document_ids'):
            members=theme.get(field, [])
            if not isinstance(members, list) or any(not isinstance(v, str) for v in members):
                raise ValueError('Topic membership requires explicit string lists')
        themes.append({'id': theme['id'], 'label': theme['label'], 'note': theme.get('note', '')})
    display_events = []
    for event in events:
        memberships = [t['id'] for t in definitions if
                       event['group'] in t.get('groups', []) or event['entry_id'] in t.get('entry_ids', []) or
                       event['source'].get('source_document_id') in t.get('source_document_ids', [])]
        display_events.append({**event, 'themes': memberships})
    intervals = []
    interval_ids = set()
    for raw in config.get('medication_timeline_periods', []):
        annotation = dict(raw)
        if annotation['id'] in interval_ids or annotation['kind'] not in ('period', 'duration_only', 'ongoing'):
            raise ValueError('Invalid or duplicate interval annotation')
        interval_ids.add(annotation['id'])
        evidence = annotation.get('evidence_entry_ids', [])
        if not isinstance(evidence, list) or not evidence or any(not isinstance(e, str) for e in evidence) or len(evidence)!=len(set(evidence)) or any(e not in by_id for e in evidence):
            raise ValueError('Period evidence is unavailable in the accepted snapshot')
        for eid in evidence:
            row = by_id[eid]
            allowed = ('verified_from_source', 'user_confirmed', 'needs_review') if annotation['kind'] == 'duration_only' and annotation.get('note') else ('verified_from_source', 'user_confirmed')
            if row['kind'] != 'use' or row['event_type'] in ('not_started','benefit_reported','adverse_effect_reported') or row['source'].get('review_status') not in allowed:
                raise ValueError('Interval annotations require reviewed actual-use evidence')
            if row['group'] != annotation['group']:
                raise ValueError('Interval evidence belongs to another medicine')
        for field in ('start', 'end', 'anchor_date', 'confirmed_until'):
            valid_date(annotation.get(field))
        if annotation['kind'] == 'period':
            if not annotation.get('start') or not annotation.get('end') or valid_date(annotation['start'])[0] > valid_date(annotation['end'])[1]:
                raise ValueError('A bounded period needs ordered source-supported boundaries')
        elif annotation['kind'] == 'duration_only':
            if annotation.get('start') or annotation.get('end'):
                raise ValueError('Duration-only annotations cannot manufacture boundaries')
        elif not annotation.get('confirmed_until'):
            raise ValueError('Ongoing use needs a dated reconciliation')
        if annotation['kind']=='ongoing' and annotation.get('end'):
            raise ValueError('Ongoing use cannot include a forecast stop date')
        valid_date(as_of)
        if as_of and annotation.get('confirmed_until') and annotation['confirmed_until'] > as_of:
            raise ValueError('Future use cannot be asserted')
        annotation['evidence'] = [dict(by_id[e]) for e in evidence]
        annotation['themes'] = sorted({t for e in display_events if e['entry_id'] in evidence for t in e['themes']})
        intervals.append(annotation)
    default = config.get('medication_timeline_default_theme', '')
    if default and default not in used:
        raise ValueError('Default medication theme is unavailable')
    return {'events': display_events, 'intervals': intervals, 'themes': themes,
            'default_theme': default, 'labels': config.get('medication_timeline_labels', {}),
            'as_of': as_of, 'theme_group_order': config.get('medication_timeline_group_order', [])}
