"""Synthetic domain/citation isolation and canonical-source preservation checks."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source_catalog import catalog
from source_review import combined_review_queue
from validate import check_psychology_blank, check_source_citations, PSYCHOLOGY_BLANK_FORMS

class CatalogTests(unittest.TestCase):
    def fixture(self, folder):
        (folder/'knowledge/psychology').mkdir(parents=True)
        medical={'id':'S01','title':'Synthetic medical source','url':'https://example.org/shared','checked_on':'2026-01-01','retrieval_status':'selected section read','region':'Synthetic','use':'Synthetic medical question'}
        psychological={'id':'S01','title':'Synthetic psychological source','url':medical['url'],'checked_at':'2026-02-01','access':'indexed_excerpt','limitations':'Full text not read','use':'Synthetic psychological question'}
        (folder/'knowledge/sources.json').write_text(json.dumps([medical]),encoding='utf-8')
        (folder/'knowledge/psychology/sources.json').write_text(json.dumps({'sources':[psychological]}),encoding='utf-8')
        return medical,psychological

    def test_overlapping_ids_and_urls_do_not_merge_reading_histories(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);medical,psychological=self.fixture(folder)
            before={p:p.read_bytes() for p in folder.rglob('*.json')}
            result=catalog(folder)
            self.assertEqual(result['record_count'],2)
            self.assertEqual(result['unique_url_count'],1)
            self.assertEqual([r['qualified_id'] for r in result['records']],['medical:S01','psychology:S01'])
            self.assertEqual(result['records'][1]['limitations'],psychological['limitations'])
            self.assertEqual([r['checked_on'] for r in result['records']],['2026-01-01','2026-02-01'])
            self.assertEqual(before,{p:p.read_bytes() for p in folder.rglob('*.json')})
            queue=combined_review_queue(result,dt.date(2026,3,1),30)
            self.assertEqual(len(queue),2)
            self.assertEqual({r['qualified_id'] for r in queue},{'medical:S01','psychology:S01'})
            self.assertEqual(len(combined_review_queue(result,dt.date(2026,3,1),30,'psychology')),1)

    def test_citation_namespace_is_checked_before_acceptance(self):
        check_source_citations('S150','knowledge/02_PRIMARY_CARE.md',{'S150'},{'S01'})
        with self.assertRaises(ValueError):
            check_source_citations('S150','knowledge/psychology/02_ETHICS_AND_DIALOGUE.md',{'S150'},{'S01'})
        with self.assertRaises(ValueError):
            check_source_citations('S150','skills/psyops-dialogue/references/psychology/02_ETHICS_AND_DIALOGUE.md',{'S150'},{'S01'})

    def test_filled_psychological_forms_are_rejected(self):
        for name,blank in PSYCHOLOGY_BLANK_FORMS.items():
            check_psychology_blank(blank,name)
            changed=copy.deepcopy(blank);changed['recording_authorization']='Synthetic filled field'
            with self.assertRaises(ValueError):check_psychology_blank(changed,name)
            changed=copy.deepcopy(blank);changed['unexpected']='Synthetic extra field'
            with self.assertRaises(ValueError):check_psychology_blank(changed,name)

    def test_imported_knowledge_and_source_bytes_are_preserved(self):
        root=Path(__file__).resolve().parents[1]
        provenance=json.loads((root/'docs/psychology/import-provenance.json').read_text(encoding='utf-8'))
        for entry in provenance['files']:
            if not entry['destination_path'].startswith('skills/'):
                self.assertEqual(hashlib.sha256((root/entry['destination_path']).read_bytes()).hexdigest(),entry['sha256'],entry['destination_path'])

if __name__=='__main__':unittest.main()
