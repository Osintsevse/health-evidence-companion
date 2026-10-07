"""Stable, source-linked clarification groups; no clinical decisions."""
import hashlib
import json

CLOSED = {'accepted', 'accepted_with_uncertainty', 'accepted_unknown', 'excluded_by_owner', 'resolved_from_sources'}

def build_questions(tables, documents, pending_corrections=(), saved=()):
    groups = {}
    for table, rows in tables.items():
        for row in rows:
            if row.get('review_status') not in ('needs_review', 'unreadable'):
                continue
            did = row.get('source_document_id')
            key = (did, 'uncertain_source')
            group = groups.setdefault(key, {'document_ids': [did] if did else [], 'entry_ids': [], 'notes': []})
            group['entry_ids'].append(row['entry_id'])
            text = row.get('uncertainties') or row.get('source_text') or 'Unclear source field'
            if text not in group['notes']:group['notes'].append(text)
    for d in documents:
        if d.get('missing_pages'):
            key = (d.get('report_group_id') or d['entry_id'], 'missing_pages')
            g = groups.setdefault(key, {'document_ids': [], 'entry_ids': [], 'notes': []})
            g['document_ids'].append(d['entry_id'])
            if d['missing_pages'] not in g['notes']:g['notes'].append(d['missing_pages'])
    for row in pending_corrections:
        key = (row.get('source_document_id'), 'correction')
        g = groups.setdefault(key, {'document_ids': [], 'entry_ids': [], 'notes': []})
        if row.get('source_document_id'):g['document_ids'].append(row['source_document_id'])
        g['entry_ids'].append(row['entry_id']);g['notes'].append(row.get('reason_raw') or 'Source disagreement')
    prior = {q['question_id']:dict(q) for q in saved}
    for key, group in groups.items():
        ids = sorted(set(group['entry_ids']));docs = sorted(set(group['document_ids']))
        identity = json.dumps([key,ids,docs],ensure_ascii=True,separators=(',',':'))
        qid = 'Q-'+hashlib.sha256(identity.encode()).hexdigest()[:12].upper()
        if qid in prior:continue
        prior[qid] = {'question_id':qid,'title':'Clarify source '+str(key[0] or 'owner report'),
                      'question':'\n'.join(group['notes'])+'\nPlease add only what you know. Unknown details may remain unknown.',
                      'document_ids':docs,'entry_ids':ids,'status':'needs_answer','last_answer':None}
    return list(prior.values())
