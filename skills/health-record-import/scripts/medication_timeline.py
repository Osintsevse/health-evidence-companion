"""Source-linked medication events, without inferred exposure intervals or doses."""

def build_timeline(tables, config=None):
    config = config or {}
    aliases = {k.casefold(): v for k, v in config.get('medicine_display_aliases', {}).items()}
    events = []
    for table, kind in [('medication_use_events', 'use'), ('medication_orders', 'order')]:
        for row in tables.get(table, []):
            product = row.get('product_identity_raw') if kind == 'use' else (row.get('brand_raw') or row.get('inn_raw'))
            product = product or config.get('unknown_medicine_label', 'Unspecified medicine')
            group = aliases.get(product.casefold(), product)
            events.append({'entry_id': row['entry_id'], 'date': row.get('event_date'),
                           'date_precision': row.get('event_date_precision', 'unknown'),
                           'date_role': 'reported_event_or_history' if kind == 'use' else 'prescription_date',
                           'kind': kind, 'group': group, 'product': product,
                           'event_type': row.get('event_type') if kind == 'use' else 'prescribed',
                           'dose': row.get('dose_taken_raw') if kind == 'use' else row.get('dose_raw'),
                           'regimen': row.get('regimen_reported_raw') if kind == 'use' else row.get('regimen_raw'),
                           'strength': row.get('strength_raw') if kind == 'order' else None,
                           'benefit': row.get('benefit_reported_raw'), 'adverse_effect': row.get('adverse_effect_reported_raw'),
                           'source': dict(row)})
    # Partial dates remain partial strings. No Jan 1 or end/start boundary is synthesized.
    return sorted(events, key=lambda r: (not bool(r['date']), r['date'] or '', r['entry_id']))
