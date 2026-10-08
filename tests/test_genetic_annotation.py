"""Synthetic fixtures only; tests do not download or access patient records."""
import gzip
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from contextlib import closing
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts'))
import genetic_annotation as ga


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.vcf = self.root / 'fixture.vcf.gz'
        self.index = self.root / 'reference.sqlite'
        self.staging = self.root / 'staging.sqlite'
        self.output = self.root / 'candidates.sqlite'

    def tearDown(self):
        self.temp.cleanup()

    def reference(self, assembly='GRCh37'):
        records = [
            '1\t100\t11\tA\tG\t.\tPASS\tCLNSIG=Pathogenic;CLNREVSTAT=reviewed_by_expert_panel;MC=SO:0001583|missense_variant',
            '1\t100\t12\tA\tG\t.\tPASS\tCLNSIG=Conflicting_classifications_of_pathogenicity;CLNREVSTAT=criteria_provided,_conflicting_classifications;CLNSIGCONF=Pathogenic(1),Benign(1)',
            '1\t100\t13\tA\tT\t.\tPASS\tCLNSIG=Pathogenic;CLNREVSTAT=practice_guideline',
            '1\t101\t14\tA\tC,G\t.\tPASS\tCLNSIG=Pathogenic',
            '1\t102\t15\tA\tAT\t.\tPASS\tCLNSIG=Pathogenic',
        ]
        with gzip.open(self.vcf, 'wt') as stream:
            stream.write('##fileformat=VCFv4.2\n##reference=' + assembly + '\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n' + '\n'.join(records) + '\n')
        return ga.build_index(self.vcf, self.index)

    def calls(self, rows, metadata=None):
        db = sqlite3.connect(self.staging)
        db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
        db.execute('CREATE TABLE observations(source_line INTEGER PRIMARY KEY,row_json TEXT NOT NULL)')
        for key, value in (metadata or {'assembly': 'unknown', 'strand':'unknown'}).items():
            db.execute('INSERT INTO metadata VALUES(?,?)', (key,json.dumps(value)))
        for i, (alleles, flags) in enumerate(rows, 1):
            row = {'chromosome_raw':'1','position_raw':'100','alleles':alleles,'flags':flags,'rsid_raw':'rsSynthetic'}
            db.execute('INSERT INTO observations VALUES(?,?)',(i,json.dumps(row)))
        db.commit(); db.close()

    def run_annotation(self):
        with patch('urllib.request.build_opener', side_effect=AssertionError('Network forbidden')):
            return ga.annotate(self.staging,self.index,self.output,'GRCh37','forward')

    def candidates(self):
        with closing(sqlite3.connect(self.output)) as db:
            return [json.loads(raw) for (raw,) in db.execute('SELECT row_json FROM candidates')]

    def test_preserves_all_exact_candidates_and_separates_conflict(self):
        manifest = self.reference()
        self.assertEqual(manifest['counts']['indexed_snps'],3)
        self.calls([(['A','G'],[])])
        result=self.run_annotation(); rows=self.candidates()
        self.assertEqual(result['counts']['candidate_records'],2)
        self.assertEqual(result['counts']['priority_candidates'],1)
        self.assertEqual(rows[0]['clinvar']['info']['MC'],'SO:0001583|missense_variant')
        self.assertIn('conflicting_classifications',rows[1]['flags'])
        self.assertEqual(rows[0]['match']['alternate_copies'],1)
        self.assertIn('source_vcf_line',rows[0]['clinvar'])

    def test_flags_and_outside_record_allele_preserved_not_prioritized(self):
        self.reference(); self.calls([(['G','T'],[]),(['A','G'],['duplicate_rsid'])])
        self.run_annotation(); rows=self.candidates()
        self.assertTrue(all(not r['priority_for_manual_review'] for r in rows))
        self.assertTrue(any('genotype_contains_allele_outside_record' in r['flags'] for r in rows))
        self.assertTrue(any('duplicate_rsid' in r['flags'] for r in rows))

    def test_reference_only_nocall_and_complement_do_not_match(self):
        self.reference(); self.calls([(['A','A'],[]),([],[]),(['C','C'],[]),(['N'],[])])
        result=self.run_annotation()
        self.assertEqual(result['counts']['candidate_records'],0)

    def test_wrong_reference_assembly_fails_and_removes_partial_index(self):
        with self.assertRaises(ValueError): self.reference('GRCh38')
        self.assertFalse(self.index.exists())

    def test_known_incompatible_staging_cannot_be_overridden(self):
        self.reference(); self.calls([(['A','G'],[])],{'assembly':'GRCh38','strand':'forward'})
        with self.assertRaises(ValueError): self.run_annotation()
        self.assertFalse(self.output.exists())

    def test_raw_build_contradiction_cannot_be_overridden(self):
        self.reference(); self.calls([(['A','G'],[])],{'assembly':'unknown','strand':'unknown','assembly_raw':'##reference=build38'})
        with self.assertRaises(ValueError): self.run_annotation()
        self.assertFalse(self.output.exists())

    def test_existing_manifest_not_overwritten(self):
        self.reference(); self.calls([(['A','G'],[])])
        sidecar=Path(str(self.output)+'.manifest.json'); sidecar.write_text('preserved',encoding='utf-8')
        with self.assertRaises(FileExistsError): self.run_annotation()
        self.assertEqual(sidecar.read_text(encoding='utf-8'),'preserved')

    def test_two_star_no_conflicts_is_not_a_conflict(self):
        info={'CLNSIG':'Pathogenic','CLNREVSTAT':'criteria_provided,_multiple_submitters,_no_conflicts'}
        self.assertEqual(ga.candidate_flags(info,[]),[])
        info['CLNSIGCONF']='Pathogenic(1),Benign(1)'
        self.assertIn('conflicting_classifications',ga.candidate_flags(info,[]))

    def test_no_ambiguous_mitochondrial_alias(self):
        self.assertEqual(ga.chromosome('25'),'25')
        self.assertEqual(ga.chromosome('26'),'26')
        self.assertEqual(ga.chromosome('M'),'MT')

    def test_public_repo_output_guard(self):
        with self.assertRaises(ValueError):
            ga.external_output(ga.PUBLIC_ROOT/'synthetic-private.sqlite')

    def test_explicit_declarations_required(self):
        with self.assertRaises(ValueError):
            ga.annotate(self.staging,self.index,self.output,'GRCh38','forward')
        with self.assertRaises(ValueError):
            ga.annotate(self.staging,self.index,self.output,'GRCh37','unknown')

    def test_existing_partial_download_is_preserved(self):
        from io import BytesIO
        partial = self.root / 'download.gz.part'
        partial.write_bytes(b'existing work')
        checksum = b'00000000000000000000000000000000  clinvar_20260101.vcf.gz\n'
        class Opener:
            def open(self, url, timeout):
                return BytesIO(checksum)
        with patch('urllib.request.build_opener', return_value=Opener()):
            with self.assertRaises(FileExistsError):
                ga.download(ga.BASE+'clinvar_20260101.vcf.gz', self.root/'download.gz')
        self.assertEqual(partial.read_bytes(), b'existing work')

    def test_public_download_rejects_arbitrary_and_latest_urls(self):
        for url in ('https://example.org/data.vcf.gz',ga.BASE+'clinvar.vcf.gz',ga.BASE+'clinvar_20261004.vcf.gz?query=rsSynthetic'):
            with self.assertRaises(ValueError): ga.download(url,self.root/'download.gz')


if __name__ == '__main__': unittest.main()
