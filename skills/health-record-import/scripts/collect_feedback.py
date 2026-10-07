"""Collect an owner-exported answer file for review; never change clinical facts."""
import argparse,datetime,hashlib,json,sqlite3
from pathlib import Path

def collect(db,input_file,view_data,archive_root):
    root=Path(archive_root).resolve();db=Path(db).resolve();source=Path(input_file).resolve();view=Path(view_data).resolve()
    public=next((p for p in Path(__file__).resolve().parents if (p/'plugin.json').is_file()),None)
    if public and (root==public or public in root.parents):raise ValueError('Private archive must be outside plugin source')
    if any(root not in p.parents for p in (db,source,view)):raise ValueError('Feedback inputs and ledger must remain inside the chosen private archive')
    if source.stat().st_size>1_000_000:raise ValueError('Feedback file too large')
    payload=json.loads(source.read_text(encoding='utf-8-sig'));model=json.loads(view.read_text(encoding='utf-8'))
    if payload.get('format')!='medical-archive-feedback/1':raise ValueError('Unknown feedback format')
    known={q['question_id']:q for q in model['review_questions']};answers=payload.get('answers')
    if not isinstance(answers,list):raise ValueError('Invalid answer list')
    seen=set();prepared=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat();digest=hashlib.sha256(source.read_bytes()).hexdigest()
    for a in answers:
        qid=a.get('question_id');answer=a.get('answer')
        if qid not in known or qid in seen or not isinstance(answer,str) or not answer.strip() or len(answer)>50000:raise ValueError('Invalid, duplicate or unknown question/answer')
        seen.add(qid)
        if answer.strip()==(known[qid].get('last_answer') or '').strip():continue
        fid='FEEDBACK-'+hashlib.sha256((qid+'\0'+answer).encode()).hexdigest()[:24]
        prepared.append((fid,qid,now,answer,'owner_report','Owner export '+source.name+'; SHA-256 '+digest,'pending_review'))
    lock=root/'.archive-writer.lock';operation='FEEDBACK-'+now
    with lock.open('x',encoding='utf8') as f:f.write(operation)
    c=None
    try:
        c=sqlite3.connect(db);c.row_factory=sqlite3.Row
        names={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
        facts=[t for t in ['observations','clinical_entries','medication_orders','medication_use_events','corrections'] if t in names]
        before={t:[tuple(r) for r in c.execute('select * from '+t)] for t in facts}
        backup=root/'system'/'backups'/('feedback-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.sqlite');backup.parent.mkdir(parents=True,exist_ok=True);b=sqlite3.connect(backup);c.backup(b);b.close()
        with c:
            c.execute('create table if not exists review_feedback(feedback_id text primary key,question_id text,received_at text,answer_raw text,source_kind text,source_locator text,review_status text)')
            existing={r[0] for r in c.execute('select feedback_id from review_feedback')}
            c.executemany('insert or ignore into review_feedback values(?,?,?,?,?,?,?)',prepared)
        for r in prepared:
            got=c.execute('select question_id,answer_raw from review_feedback where feedback_id=?',(r[0],)).fetchone()
            if tuple(got)!=(r[1],r[3]):raise ValueError('Feedback readback failed')
        if before!={t:[tuple(r) for r in c.execute('select * from '+t)] for t in facts}:raise ValueError('Clinical facts changed')
        if c.execute('pragma integrity_check').fetchone()[0]!='ok':raise ValueError('Ledger integrity failed')
        return {'new_feedback_rows':sum(r[0] not in existing for r in prepared),'answers_verified':len(prepared),'status':'pending_review','clinical_facts_unchanged':True}
    finally:
        if c:c.close()
        if lock.read_text(encoding='utf8')!=operation:raise ValueError('Writer lock changed')
        lock.unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',required=True);p.add_argument('--input',required=True);p.add_argument('--view-data',required=True);p.add_argument('--archive-root',required=True);a=p.parse_args();print(json.dumps(collect(a.db,a.input,a.view_data,a.archive_root)))
