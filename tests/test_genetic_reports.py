import importlib.util, tempfile, pathlib, hashlib
p=pathlib.Path(__file__).parents[1]/'skills'/'health-record-import'/'scripts'/'genetic_reports.py'
spec=importlib.util.spec_from_file_location('genetic_reports',p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw=('MIME-Version: 1.0\r\nContent-Type: multipart/related; boundary=x\r\nSnapshot-Content-Location: https://example.invalid/exact?q=1\r\n\r\n--x\r\nContent-Type: text/html\r\nContent-Location: https://example.invalid/exact?q=1\r\nContent-Transfer-Encoding: base64\r\n\r\n')
import base64
body='<meta charset="utf-8"><p>\u0421\u0438\u043d\u0442\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043e\u0442\u0447\u0451\u0442</p><script>fetch("https://example.invalid")</script><p>&lt;script&gt;literal&lt;/script&gt;</p>'
with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parents[2]) as directory:
 source=pathlib.Path(directory)/'synthetic.mhtml'; payload=(raw+base64.b64encode(body.encode()).decode()+'\r\n--x--\r\n').encode();source.write_bytes(payload)
 result=m.extract_mhtml(source)
 assert result['text']=='\u0421\u0438\u043d\u0442\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043e\u0442\u0447\u0451\u0442\n<script>literal</script>'
 assert result['source']['charset_source']=='html_meta'
 assert result['source']['sha256']==hashlib.sha256(payload).hexdigest()
 assert result['source']['content_location']=='https://example.invalid/exact?q=1'
 assert result==m.extract_mhtml(source)
 output=pathlib.Path(directory)/'new'/'extracted.json'
 m.publish_extraction(source,output)
 assert output.is_file()
 try:m.publish_extraction(source,output)
 except FileExistsError:pass
 else:raise AssertionError('Existing output overwritten')
 try:m.publish_extraction(source,p.parent/'private-synthetic.json')
 except ValueError:pass
 else:raise AssertionError('Public output permitted')
 assert m.load_assessment({'genetics':{'summary':'Synthetic','reports':[]}})['summary']=='Synthetic'
 assert m.load_assessment({}) is None
print('genetic_reports: synthetic UTF-8 MHTML, escaping data, origin, hash and determinism passed')

import sqlite3,json
with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parents[2]) as directory:
 dbpath=pathlib.Path(directory)/'synthetic.sqlite'
 with sqlite3.connect(dbpath) as db:
  db.execute('CREATE TABLE metadata(key TEXT,value_json TEXT)')
  db.execute('CREATE TABLE candidates(id INTEGER PRIMARY KEY,source_line INTEGER,row_json TEXT)')
  db.execute('INSERT INTO metadata VALUES(?,?)',('manifest',json.dumps({'schema':'dtc-clinvar-candidates-v1'})))
  row={'observation':{'rsid':'rsSynthetic','alleles':['A','G']},'clinvar':{'classification':'Uncertain_significance','review_status':'synthetic_review','variation_id':'synthetic_id','info':{'GENEINFO':'SYNTHETIC:0'}},'flags':['synthetic_flag'],'priority_for_manual_review':False}
  db.execute('INSERT INTO candidates VALUES(1,9,?)',(json.dumps(row),))
 db.close()
 summary=m.candidate_summary(dbpath)
 assert summary['rows'][0]['flags']==['synthetic_flag']
 assert summary['rows'][0]['genotype']=='AG'
 assert summary['stats']['classification_counts']=={'Uncertain_significance':1}
 # Windows refuses renaming an open SQLite file: this also verifies closure.
 dbpath.rename(pathlib.Path(directory)/'closed.sqlite')
 print('candidate_summary: synthetic metadata, flags, counts and closed SQLite passed')
