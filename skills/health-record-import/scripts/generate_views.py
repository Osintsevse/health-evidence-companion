"""Generate private read-only views from a committed SQLite archive; no network or clinical decisions."""
import argparse
import importlib.util
import datetime
import hashlib
import json
import re
import sqlite3
from pathlib import PurePosixPath
from pathlib import Path

def helper(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


FACT_TABLES = ('observations', 'clinical_entries', 'medication_orders', 'medication_use_events')
REVIEWED = {'verified_from_source', 'user_confirmed'}


def accepted_rows(connection, table, committed):
    return [dict(r) for r in connection.execute('SELECT * FROM '+table)
            if r['import_id'] in committed and r['record_status']=='active']


def resolve_history(rows, corrections, table):
    by_id={r['entry_id']:r for r in rows}; excluded=set()
    for c in corrections:
        if c['target_table']!=table or c['review_status'] not in REVIEWED:
            continue
        replacement=c['replacement_entry_id']
        if replacement is not None and (replacement not in by_id or by_id[replacement]['review_status'] not in REVIEWED):
            continue
        excluded.add(c['target_entry_id'])
    return [r for r in rows if r['entry_id'] not in excluded]


def observation_category(row):
    method=(row.get('method_raw') or '').lower()
    specimen=(row.get('specimen_raw') or '').lower()
    if 'abpm' in method or row.get('unit_raw') in ('mmHg','bpm'):
        return 'vitals'
    if any(x in method for x in ('\u0443\u0437\u0438','ultrasound','spirom')):
        return 'investigations'
    if specimen in ('u','urine') or '\u043c\u043e\u0447' in specimen:
        return 'urine'
    if '\u043a\u0430\u043b' in specimen or 'stool' in specimen:
        return 'stool'
    return 'blood'


def build_matrix(rows,config=None,documents=None):
    """Display raw values; separate events, specimens and units; retain every cell ID."""
    columns={}; events={};config=config or {}
    labels=config.get('display_analytes',{})
    units=config.get('display_units',{})
    specimens=config.get('display_specimens',{})
    report_groups={d['entry_id']:d.get('report_group_id') or d['entry_id'] for d in (documents or [])}
    for r in rows:
        if r['review_status'] not in REVIEWED or not r['event_date']:
            continue
        if observation_category(r) not in ('blood','urine','stool'):
            continue
        # No unreviewed synonym or unit conversion. A repeated spelling is useful
        # for a display column, not proof of longitudinal clinical comparability.
        raw_name=r['analyte_name_raw'];raw_unit=r.get('unit_raw') or '';raw_specimen=r.get('specimen_raw') or ''
        display=r.get('_display');key=(raw_name,raw_unit,raw_specimen)
        col=display['row_key'] if display else json.dumps(key,ensure_ascii=False)
        columns[col]={'key':col,'name':display['label'] if display else labels.get(raw_name,raw_name),'raw_name':raw_name,
                      'unit':display['unit'] if display else raw_unit,'specimen':raw_specimen,
                      'display_unit':units.get(raw_unit,raw_unit),'display_specimen':specimens.get(raw_specimen,raw_specimen)}
        event_key=(r['event_date'],report_groups.get(r['source_document_id'],r['source_document_id']),r.get('laboratory_raw') or '',observation_category(r))
        event=events.setdefault(event_key,{'date':event_key[0],'document_id':event_key[1],
                   'laboratory':event_key[2],'specimen':'','document_ids':[],
                   'category':observation_category(r),'cells':{}})
        if r['source_document_id'] not in event['document_ids']:event['document_ids'].append(r['source_document_id'])
        event['document_id']=event['document_ids'][0]
        known_specs=set(event['specimen'].split(', ')) if event['specimen'] else set()
        if raw_specimen:known_specs.add(raw_specimen)
        event['specimen']=', '.join(sorted(known_specs))
        event['cells'].setdefault(col,[]).append(r)
    return {'columns':sorted(columns.values(),key=lambda x:(x['name'].casefold(),x['unit'],x['specimen'])),
            'events':sorted(events.values(),key=lambda x:(x['date'],x['document_id'] or '',x['specimen']))}


def read_model(db, config):
    con=sqlite3.connect('file:'+Path(db).resolve().as_posix()+'?mode=ro',uri=True)
    con.row_factory=sqlite3.Row
    names={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    imports=[dict(r) for r in con.execute('SELECT * FROM imports')]
    committed={r['import_id'] for r in imports if r['state']=='committed' and r['ledger_readback_status']=='rows_verified'}
    corrections=accepted_rows(con,'corrections',committed)
    accepted={t:accepted_rows(con,t,committed) for t in FACT_TABLES}
    tables={t:resolve_history(accepted[t],corrections,t) for t in FACT_TABLES}
    replacements={(table,r['entry_id']):r for table,rows in accepted.items() for r in rows}
    pending_corrections=[c for c in corrections if c['review_status'] not in REVIEWED or
         (c['replacement_entry_id'] is not None and
          ((c['target_table'],c['replacement_entry_id']) not in replacements or replacements[(c['target_table'],c['replacement_entry_id'])]['review_status'] not in REVIEWED))]
    documents=accepted_rows(con,'documents',committed)
    context={}
    if 'archive_context' in names:
        context={r['context_key']:json.loads(r['payload_json']) for r in con.execute('SELECT * FROM archive_context')}
    locations={r['document_id']:dict(r) for r in con.execute('SELECT * FROM storage_locations')} if 'storage_locations' in names else {}
    notes={r['document_id']:dict(r) for r in con.execute('SELECT * FROM readable_documents')} if 'readable_documents' in names else {}
    for d in documents:
        did=d['entry_id'];loc=locations.get(did,{});note=notes.get(did,{})
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}',did) or '..' in did:
            raise ValueError('Document IDs must be safe neutral filenames')
        if loc.get('relative_path'):
            relative=PurePosixPath(loc['relative_path'])
            if relative.is_absolute() or '..' in relative.parts or '\\' in loc['relative_path'] or ':' in loc['relative_path']:
                raise ValueError('Original path must remain inside the private archive')
        d.update(title=note.get('title') or d['original_filename'],body=note.get('body') or '',
                 original_path=loc.get('relative_path'),original_url=loc.get('remote_url'),
                 received_sha256=loc.get('received_sha256') or d.get('received_sha256'),
                 note_path='details/'+did+'.md')
    vaccines=[]
    clinical_ids={r['entry_id']:r for r in tables['clinical_entries']}
    if 'vaccination_details' in names:
        for r in con.execute('SELECT * FROM vaccination_details ORDER BY source_row'):
            if r['entry_id'] in clinical_ids:
                fact=clinical_ids[r['entry_id']]
                vaccines.append({**fact, 'cells':json.loads(r['cells_json']),'source_row':r['source_row']})
    else:
        vaccines=[{**r,'cells':[None,None,None,r['event_date'],None,None,r['statement_raw'],None,None]}
                  for r in tables['clinical_entries'] if r['entry_kind'] in ('vaccination_record','tuberculin_test_record','reported_disease_history')]
    saved=[]
    if 'review_questions' in names:
        for q in con.execute('SELECT * FROM review_questions'):
            q=dict(q)
            for column,key in [('document_ids_json','document_ids'),('entry_ids_json','entry_ids')]:
                if column in q:q[key]=json.loads(q.pop(column))
            saved.append(q)
    review_questions=helper('record_feedback').build_questions(tables,documents,pending_corrections,saved)
    if 'review_feedback' in names:
        for q in review_questions:
            f=con.execute('SELECT * FROM review_feedback WHERE question_id=? ORDER BY received_at DESC,feedback_id DESC LIMIT 1',(q['question_id'],)).fetchone()
            if f:
                q['last_answer']=f['answer_raw']
                if f['review_status']=='pending_review':q['status']='answered_pending'
    if 'feedback_resolutions' in names:
        outcomes={r['question_id']:dict(r) for r in con.execute('SELECT * FROM feedback_resolutions')}
        for q in review_questions:
            if q['question_id'] in outcomes:q.update(status=outcomes[q['question_id']]['status'],resolution_text=outcomes[q['question_id']]['resolution_text'])
    if config.get('display_families_enabled',True):
        for r in tables['observations']:
            if r['review_status'] in REVIEWED and observation_category(r) in ('blood','urine','stool'):r['_display']=helper('lab_identity').normalize(r)
    try:
        reconciliation,current_medications=helper('medication_reconciliation').read_reconciliation(
            con,names,tables,committed,config.get('record_id'),config.get('as_of'))
    finally:
        con.close()
    return {'format_version':'1.0','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'as_of':config.get('as_of'),'locale':config.get('locale','en'),'labels':config.get('labels',{}),
            'status_labels':config.get('status_labels',{}),
            'links':config.get('view_links',{}),
            'medication_reconciliation':reconciliation,'current_medications':current_medications,
            'imports':[{k:r.get(k) for k in ('import_id','completed_at','schema_version','state','ledger_readback_status')} for r in imports if r['import_id'] in committed],
            'tables':tables,'documents':documents,'review_questions':review_questions,'feedback_storage_key':hashlib.sha256((config.get('record_id','')+str(Path(db).resolve())).encode()).hexdigest()[:16],
            'context':context,'vaccines':vaccines,'pending_corrections':pending_corrections,
            'undated_laboratory':[{**r,'display_category':observation_category(r)} for r in tables['observations']
                                  if not r['event_date'] and r['review_status'] in REVIEWED
                                  and observation_category(r) in ('blood','urine','stool')],
            'matrix':build_matrix(tables['observations'],config,documents)}


def literal(value):
    text='' if value is None else str(value)
    return "'"+text if text.lstrip().startswith(('=','+','-','@')) else text


def workbook_data(model):
    """Portable cell matrices for the host's spreadsheet authoring adapter."""
    sheets=[]
    for category in ('blood','urine','stool'):
        events=[r for r in model['matrix']['events'] if r['category']==category]
        keys={k for r in events for k in r['cells']}
        cols=[c for c in model['matrix']['columns'] if c['key'] in keys]
        if not events:continue
        headers=['Analyte / unit / specimen']+[e['date'] for e in events]
        data=[['Laboratory']+[e['laboratory'] for e in events],['Specimen']+[e['specimen'] for e in events],['Source']+['; '.join(e['document_ids']) for e in events]]
        for c in cols:
            vals=[c['name']+(' ['+c['unit']+']' if c['unit'] else '')]
            for event in events:
                cell=event['cells'].get(c['key'],[])
                vals.append(' / '.join(r.get('_display',{}).get('display_value',r['raw_value'])+(' '+r['flag_raw'] if r.get('flag_raw') else '') for r in cell) if cell else None)
            data.append([literal(v) if isinstance(v,str) else v for v in vals])
        sheets.append({'category':category,'orientation':'analytes_in_rows','headers':[literal(v) for v in headers],'rows':data})
    detail_headers=['Date','Analyte','Raw result','Unit','Reference','Printed flag','Specimen','Laboratory','Source','Locator','Review','Uncertainty']
    detail=[]
    for r in model['tables']['observations']:
        if observation_category(r) in ('blood','urine','stool'):
            detail.append([literal(r.get(k)) for k in ('event_date','analyte_name_raw','raw_value','unit_raw','reference_range_raw','flag_raw','specimen_raw','laboratory_raw','source_document_id','source_locator','review_status','uncertainties')])
    sheets.append({'category':'source_details','headers':detail_headers,'rows':detail})
    return sheets


def generate(db, config, output, template):
    output=Path(output).resolve()
    source_root=next((p for p in Path(__file__).resolve().parents if (p/'plugin.json').is_file() and (p/'skills').is_dir()),None)
    if source_root is not None and (output==source_root or source_root in output.parents):
        raise ValueError('Private output must remain outside the plugin source tree')
    model=read_model(db,config)
    model['medication_timeline']=helper('medication_timeline').build_timeline(model['tables'],config)
    model['medication_chart']=helper('medication_chart').build_chart(model['medication_timeline'],config,model.get('as_of'))
    if config.get('embed_question_originals'):
        import importlib.util
        preview_path=Path(__file__).with_name('document_previews.py')
        spec=importlib.util.spec_from_file_location('private_previews',preview_path)
        previews=importlib.util.module_from_spec(spec);spec.loader.exec_module(previews)
        root=config.get('originals_root')
        if not root:raise ValueError('An explicit private originals_root is required for previews')
        previews.attach_previews(model,root,config)
    data=json.dumps(model,ensure_ascii=False).replace('<','\\u003c').replace('&','\\u0026')
    template=Path(template)
    text=template.read_text(encoding='utf-8').replace('__PRIVATE_MODEL__',data)
    for marker,name in [('__MEDICATION_CHART_CSS__','medication_chart.css'),('__MEDICATION_CHART_JS__','medication_chart_ui.mjs')]:
        if marker in text:text=text.replace(marker,(template.parent/name).read_text(encoding='utf-8'))
    assert '__PRIVATE_MODEL__' not in text
    output.mkdir(parents=True,exist_ok=True)
    (output/'index.html').write_text(text,encoding='utf-8')
    (output/'view_data.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'workbook_data.json').write_text(json.dumps(workbook_data(model),ensure_ascii=False,indent=2),encoding='utf-8')
    docs=output/'details';docs.mkdir(exist_ok=True)
    for d in model['documents']:
        (docs/(d['entry_id']+'.md')).write_text(d['body'],encoding='utf-8')
    return {'documents':len(model['documents']), 'observations':len(model['tables']['observations']),
            'vaccination_records':len(model['vaccines']), 'matrix_events':len(model['matrix']['events']),
            'private_output_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',required=True);parser.add_argument('--config',required=True)
    parser.add_argument('--output',required=True);parser.add_argument('--template',required=True)
    args=parser.parse_args()
    print(json.dumps(generate(args.db,json.loads(Path(args.config).read_text(encoding='utf-8')),args.output,args.template)))
