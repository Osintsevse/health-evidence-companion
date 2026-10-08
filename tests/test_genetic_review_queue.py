"""Bounded summaries from entirely synthetic classifications."""
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts'))
import genetic_reports as reports

class QueueTests(unittest.TestCase):
    def test_limits_do_not_hide_aggregate_counts_or_flags(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'fixture.sqlite'
            with closing(sqlite3.connect(path)) as db:
                db.execute('CREATE TABLE metadata(key TEXT,value_json TEXT)')
                db.execute('INSERT INTO metadata VALUES(?,?)', ('manifest', json.dumps({'schema':'dtc-clinvar-candidates-v1'})))
                db.execute('CREATE TABLE candidates(id INTEGER,source_line INTEGER,row_json TEXT)')
                for i, classification in enumerate(('Pathogenic', 'Benign', 'Likely_pathogenic', 'Pathogenic'), 1):
                    row = {'observation':{'alleles':['A','G'], 'chromosome_raw':'X'}, 'clinvar':{'classification':classification, 'variation_id':str(i)}, 'flags':['synthetic_unresolved'], 'priority_for_manual_review':i==4}
                    db.execute('INSERT INTO candidates VALUES(?,?,?)', (i,i,json.dumps(row)))
                db.commit()
            summary=reports.candidate_overview(path, 1)
            self.assertEqual(summary['stats']['candidate_records'], 4)
            self.assertEqual(summary['review_queue_total'], 3)
            self.assertEqual(summary['omitted_review_rows'], 2)
            self.assertEqual(summary['rows'][0]['variation_id'], '4')
            self.assertIn('synthetic_unresolved',summary['rows'][0]['flags'])
            self.assertIn('sex_chromosome_ploidy_not_established',summary['rows'][0]['context_flags'])
            self.assertIn('heterozygous_x_call_requires_ploidy_context',summary['rows'][0]['context_flags'])
            self.assertTrue(summary['rows'][0]['priority'])
            for limit in (0,501,True):
                with self.assertRaises(ValueError): reports.candidate_overview(path,limit)

if __name__ == '__main__': unittest.main()
