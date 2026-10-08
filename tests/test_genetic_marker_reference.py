"""Synthetic public-reference aliases; no actual genomic records."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills'/'health-record-import'/'scripts'))
from genetic_marker_query import marker_query


class MarkerReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.staging=self.root/'staging.sqlite'; self.reference=self.root/'reference.sqlite'
        with closing(sqlite3.connect(self.staging)) as db:
            db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
            db.execute('CREATE TABLE observations(source_line INTEGER PRIMARY KEY,row_json TEXT NOT NULL)')
            db.execute('INSERT INTO metadata VALUES(?,?)',('assembly',json.dumps('unknown')))
            for n,identifier in enumerate(('rsAlias','iSynthetic'),1):
                db.execute('INSERT INTO observations VALUES(?,?)',(n,json.dumps({'line':n,'rsid_raw':identifier,'chromosome_raw':'1','position_raw':'100','alleles':['A','G'],'flags':['synthetic_flag']})))
            db.commit()
        with closing(sqlite3.connect(self.reference)) as db:
            db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
            db.execute('INSERT INTO metadata VALUES(?,?)',('manifest',json.dumps({'assembly':'GRCh37','sha256':'synthetic'})))
            db.execute('CREATE TABLE variants(chrom TEXT,pos INTEGER,ref TEXT,alt TEXT,variation_id TEXT,source_line INTEGER,info_json TEXT)')
            db.execute('INSERT INTO variants VALUES(?,?,?,?,?,?,?)',('1',100,'A','G','synthetic',5,json.dumps({'RS':'123,456'})))
            db.commit()

    def tearDown(self): self.temp.cleanup()

    def test_identifier_absent_locus_present_preserves_all_raw_rows(self):
        result=marker_query(self.staging,['rs123'],self.reference,'GRCh37','forward')
        marker=result['markers'][0]
        self.assertEqual(marker['status'],'identifier_absent_locus_observed')
        self.assertEqual(marker['observations'],[])
        self.assertEqual(len(marker['observations_at_reference_loci']),2)
        self.assertEqual(marker['observations_at_reference_loci'][0]['flags'],['synthetic_flag'])
        self.assertEqual(marker['reference_records'][0]['source_vcf_line'],5)

    def test_without_reference_literal_status_remains_absent(self):
        marker=marker_query(self.staging,['rs123'])['markers'][0]
        self.assertEqual(marker['status'],'absent_from_export')
        self.assertEqual(marker['observations_at_reference_loci'],[])

    def test_wrong_reference_assembly_rejected(self):
        with closing(sqlite3.connect(self.reference)) as db:
            db.execute('UPDATE metadata SET value_json=?',(json.dumps({'assembly':'GRCh38'}),)); db.commit()
        with self.assertRaises(ValueError): marker_query(self.staging,['rs123'],self.reference,'GRCh37','forward')

    def test_reference_requires_explicit_declarations(self):
        with self.assertRaises(ValueError): marker_query(self.staging,['rs123'],self.reference)

    def test_raw_old_build_cannot_be_overridden(self):
        with closing(sqlite3.connect(self.staging)) as db:
            db.execute('INSERT INTO metadata VALUES(?,?)',('comments_raw',json.dumps(['##reference=build36']))); db.commit()
        with self.assertRaises(ValueError): marker_query(self.staging,['rs123'],self.reference,'GRCh37','forward')


if __name__ == '__main__': unittest.main()
