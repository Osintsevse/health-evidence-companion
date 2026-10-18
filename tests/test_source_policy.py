import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import source_policy


class SourcePolicyTests(unittest.TestCase):
    def test_exact_host_path_and_permission_do_not_become_blanket_clearance(self):
        policy={'rules':[{'id':'hold','host_suffix':'restricted.example','path_prefix':'/clinical/','verified_permission_available':False}]}
        source={'id':'S25','url':'https://restricted.example/clinical/a'}
        self.assertEqual(source_policy.source_use(source,'medical',policy)['active_use'],'bibliographic_only')
        for url in ['https://notrestricted.example/clinical/a','https://restricted.example/about','https://restricted.example.evil.test/clinical/a']:
            self.assertEqual(source_policy.matching_rules(url,policy),[])
        self.assertFalse(source_policy.source_use({'id':'S99','url':'https://independent.example/'},'medical',policy)['permission_inferred'])

    def test_citation_ranges_and_namespaces_preserve_distinct_sources(self):
        found=source_policy.cited_ids('[S07-S09] and psychology:S25','medical')
        self.assertTrue({'medical:S07','medical:S08','medical:S09','psychology:S25'}<=found)
        self.assertNotIn('medical:S25',found)

    def test_clinical_claim_rejected_but_historical_metadata_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'knowledge/clinical').mkdir(parents=True);(root/'knowledge/psychology').mkdir()
            (root/'knowledge/clinical/source-use-policy.json').write_text(json.dumps({'rules':[{'id':'hold','host_suffix':'restricted.example','path_prefix':'/'}]}))
            (root/'knowledge/sources.json').write_text(json.dumps([{'id':'S25','url':'https://restricted.example/'}]))
            (root/'knowledge/psychology/sources.json').write_text(json.dumps({'sources':[]}))
            note=root/'knowledge/clinical/NOTE.md'
            note.write_text('# Topic\n\nUse this as first-line treatment. S25\n')
            with self.assertRaisesRegex(ValueError,'Unmarked active use'):
                source_policy.validate_active_citations(root)
            note.write_text('# Topic\n\nHistorical source S25 is a bibliographic pointer only; no active claim relies on it.\n')
            self.assertEqual(source_policy.validate_active_citations(root)['policy_held_records'],1)
            for relative,key in [('knowledge/clinical/routes.json','routes'), ('evals/medical-expansion/cases.json','cases')]:
                target=root/relative
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(json.dumps({key:[{'id':'synthetic-record','source_ids':['S25']}]}))
                with self.assertRaisesRegex(ValueError,'synthetic-record'):
                    source_policy.validate_active_citations(root)
                target.write_text(json.dumps({key:[]}))


    def test_current_canonical_notes_follow_declared_policy(self):
        source_policy.validate_active_citations(ROOT)


if __name__=='__main__':unittest.main()
