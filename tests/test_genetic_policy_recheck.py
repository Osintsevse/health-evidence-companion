"""Synthetic tests of identifier discordance and cheap offline policy updates."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills'/'health-record-import'/'scripts'))
import genetic_annotation as ga


class CandidatePolicyTests(unittest.TestCase):
    def info(self,rs):
        return {'CLNSIG':'Pathogenic','CLNREVSTAT':'reviewed_by_expert_panel','RS':rs,'_VCF_FILTER':'PASS'}

    def row(self,identifier='rs123'):
        return {'line':9,'rsid_raw':identifier,'alleles':['A','G'],'flags':[],'raw_row':'synthetic preserved'}

    def test_identifier_mismatch_blocks_priority(self):
        flags=ga.build_flags(self.row(),self.info('456'),9,'A','G')
        self.assertIn('marker_identifier_disagrees_with_reference',flags)
        self.assertFalse(ga.priority_for_review(self.info('456'),flags))

    def test_exact_alias_membership_not_substring(self):
        flags=ga.build_flags(self.row(),self.info('12,123|456'),9,'A','G')
        self.assertNotIn('marker_identifier_disagrees_with_reference',flags)
        self.assertTrue(ga.priority_for_review(self.info('123'),flags))
        flags=ga.build_flags(self.row(),self.info('1234'),9,'A','G')
        self.assertIn('marker_identifier_disagrees_with_reference',flags)

    def test_unknown_internal_identifier_does_not_invent_discordance(self):
        flags=ga.build_flags(self.row('iSynthetic'),self.info('123'),9,'A','G')
        self.assertNotIn('marker_identifier_disagrees_with_reference',flags)

    def test_token_metadata_does_not_infer_ploidy(self):
        match={'alternate':'G','alternate_copies':2,'chromosome':'X'}
        ga.token_metadata(match,['G','G'])
        self.assertEqual(match['alternate_token_count'],2)
        self.assertTrue(match['copy_number_not_established'])

    def test_recheck_preserves_records_recalculates_policy_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'old.sqlite'; output=Path(directory)/'new.sqlite'
            manifest={'tool_version':'1.1','operator_declarations':{'assembly':'GRCh37','strand':'forward'},
                      'counts':{'rows':20,'candidate_records':1,'priority_candidates':1},'limitations':['prior limitation']}
            record={'source_line':9,'observation':self.row(),'match':{'assembly':'GRCh37','strand':'forward','reference':'A','alternate':'G','alternate_copies':1},
                    'clinvar':{'info':self.info('456'),'source_vcf_line':77,'raw_vcf':'synthetic original VCF'},
                    'flags':[],'priority_for_manual_review':True,'interpretation':'unconfirmed'}
            with closing(sqlite3.connect(source)) as db:
                db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
                db.execute('CREATE TABLE candidates(id INTEGER PRIMARY KEY,source_line INTEGER,row_json TEXT NOT NULL)')
                db.execute('INSERT INTO metadata VALUES(?,?)',('manifest',json.dumps(manifest)))
                db.execute('INSERT INTO candidates VALUES(?,?,?)',(4,9,json.dumps(record))); db.commit()
            original_hash=ga.digest(source)
            with patch('urllib.request.build_opener',side_effect=AssertionError('network forbidden')):
                revised=ga.recheck_candidates(source,output)
            self.assertEqual(revised['derived_from']['sha256'],original_hash)
            self.assertEqual(revised['derived_from']['previous_tool_version'],'1.1')
            self.assertEqual(revised['tool_version'],'1.2')
            self.assertEqual(revised['counts']['rows'],20)
            self.assertEqual(revised['counts']['priority_candidates'],0)
            self.assertEqual(revised['counts']['identifier_disagreement_candidates'],1)
            with closing(sqlite3.connect(output)) as db:
                identifier,line,raw=db.execute('SELECT id,source_line,row_json FROM candidates').fetchone()
                self.assertEqual((identifier,line),(4,9))
                new=json.loads(raw)
                self.assertEqual(new['observation'],record['observation'])
                self.assertEqual(new['clinvar'],record['clinvar'])
                self.assertFalse(new['priority_for_manual_review'])
                self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            self.assertEqual(ga.digest(source),original_hash)
            with self.assertRaises(FileExistsError): ga.recheck_candidates(source,output)


if __name__ == '__main__': unittest.main()
