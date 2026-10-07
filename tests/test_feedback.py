"""Wholly synthetic feedback collection and stable identity checks."""
import importlib.util,json,sqlite3,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts'
def load(name):
 s=importlib.util.spec_from_file_location(name,R/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
questions=load('record_feedback');collector=load('collect_feedback')
class FeedbackTests(unittest.TestCase):
 def test_stable_group_and_accepted_unknown(self):
  rows=[{'entry_id':'SYN-A','source_document_id':'DOC-SYN','review_status':'needs_review','uncertainties':'Synthetic unclear unit'},{'entry_id':'SYN-B','source_document_id':'DOC-SYN','review_status':'unreadable','source_text':'Synthetic fragment'}]
  a=questions.build_questions({'observations':rows},[]);b=questions.build_questions({'observations':list(reversed(rows))},[]);self.assertEqual(a[0]['question_id'],b[0]['question_id']);a[0]['status']='accepted_unknown';c=questions.build_questions({'observations':rows},[],saved=a);self.assertEqual(len(c),1);self.assertEqual(c[0]['status'],'accepted_unknown')
 def fixture(self,root):
  db=root/'ledger.sqlite';c=sqlite3.connect(db);c.execute('create table observations(entry_id text,value text)');c.execute("insert into observations values('SYN','unchanged synthetic fact')");c.commit();c.close();view=root/'view_data.json';view.write_text(json.dumps({'review_questions':[{'question_id':'Q-SYN','last_answer':None}]}));answer=root/'answers.json';answer.write_text(json.dumps({'format':'medical-archive-feedback/1','answers':[{'question_id':'Q-SYN','answer':'Wholly synthetic unknown'}]}));return db,answer,view
 def test_retry_is_idempotent_and_facts_unchanged(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);db,a,v=self.fixture(r);first=collector.collect(db,a,v,r);second=collector.collect(db,a,v,r);self.assertEqual(first['new_feedback_rows'],1);self.assertEqual(second['new_feedback_rows'],0);self.assertTrue(first['clinical_facts_unchanged']);c=sqlite3.connect(db);self.assertEqual(c.execute('select value from observations').fetchone()[0],'unchanged synthetic fact');c.close()
 def test_unknown_and_duplicate_answers_are_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);db,a,v=self.fixture(r)
   for entries in [[{'question_id':'Q-UNKNOWN','answer':'Synthetic'}],[{'question_id':'Q-SYN','answer':'Synthetic'},{'question_id':'Q-SYN','answer':'Synthetic again'}]]:
    a.write_text(json.dumps({'format':'medical-archive-feedback/1','answers':entries}))
    with self.assertRaises(ValueError):collector.collect(db,a,v,r)
   self.assertFalse((r/'.archive-writer.lock').exists())
 def test_private_paths_cannot_escape_archive(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);db,a,v=self.fixture(r);inner=r/'inner';inner.mkdir()
   with self.assertRaises(ValueError):collector.collect(db,a,v,inner)
