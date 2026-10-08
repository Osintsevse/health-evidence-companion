"""Wholly synthetic preview tests; never reads a real archive."""
import hashlib,importlib.util,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('previews',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/document_previews.py');previews=importlib.util.module_from_spec(spec);spec.loader.exec_module(previews)
class PreviewTests(unittest.TestCase):
 def model(self,path,raw,mime='text/plain'):
  return {'documents':[{'entry_id':'DOC-SYN','original_path':path,'mime_type':mime,'received_sha256':hashlib.sha256(raw).hexdigest()}],'review_questions':[{'document_ids':['DOC-SYN']}],'tables':{}}
 def test_text_and_original_preserved(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);p=r/'synthetic.txt';raw=b'Entirely synthetic text';p.write_bytes(raw);m=self.model(p.name,raw);previews.attach_previews(m,r,{})
   self.assertEqual(m['documents'][0]['original_preview']['text'],raw.decode());self.assertEqual(p.read_bytes(),raw);self.assertFalse(m['original_preview_counts']['network_used'])
 def test_path_escape_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):previews.attach_previews(self.model('../escape',b'synthetic'),tmp,{})
 def test_checksum_required_and_verified(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);p=r/'synthetic.txt';p.write_bytes(b'Changed synthetic');m=self.model(p.name,b'Expected synthetic')
   with self.assertRaises(ValueError):previews.attach_previews(m,r,{})
   m['documents'][0]['received_sha256']=None
   with self.assertRaises(ValueError):previews.attach_previews(m,r,{})
 def test_pdf_not_fabricated(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);p=r/'synthetic.pdf';raw=b'Synthetic PDF placeholder';p.write_bytes(raw);m=self.model(p.name,raw,'application/pdf');previews.attach_previews(m,r,{})
   self.assertNotIn('original_preview',m['documents'][0]);self.assertIn('not generated',m['documents'][0]['preview_note'])
 def test_image_offline_and_immutable(self):
  try:from PIL import Image
  except ImportError:self.skipTest('Optional Pillow unavailable')
  import io,base64
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);b=io.BytesIO();Image.new('RGB',(8,12),'blue').save(b,format='PNG');raw=b.getvalue();p=r/'synthetic.png';p.write_bytes(raw);m=self.model(p.name,raw,'image/png');previews.attach_previews(m,r,{})
   v=m['documents'][0]['original_preview'];self.assertTrue(v['data_url'].startswith('data:image/jpeg;base64,'));self.assertTrue(base64.b64decode(v['data_url'].split(',')[1]).startswith(b'\xff\xd8'));self.assertEqual(p.read_bytes(),raw)
 def test_uncertain_rows_request_preview(self):
  with tempfile.TemporaryDirectory() as tmp:
   r=Path(tmp);p=r/'synthetic.txt';p.write_bytes(b'Synthetic');m=self.model(p.name,p.read_bytes());m.pop('review_questions');m['tables']={'observations':[{'review_status':'unreadable','source_document_id':'DOC-SYN'}]};previews.attach_previews(m,r,{})
   self.assertIn('original_preview',m['documents'][0])
