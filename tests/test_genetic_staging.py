"""Entirely synthetic raw genotypes; never derived from an actual export."""
import importlib.util
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('genetic_staging', Path(__file__).resolve().parents[1] / 'skills/health-record-import/scripts/genetic_staging.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
CSV = '# Synthetic MHv1.0 build37 forward strand\nRSID,CHROMOSOME,POSITION,RESULT\nrsSynthetic,1,101,AG\n'

class GeneticStagingTests(unittest.TestCase):
    def test_csv_no_calls_symbols_and_conflicts(self):
        rows, meta = g.parse(CSV + 'rsOther,1,101,AA\nrsMissing,2,202,--\nrsIndel,3,303,ID\n')
        self.assertIn('conflicting_duplicate_locus', rows[0]['flags'])
        self.assertIn('conflicting_duplicate_locus', rows[1]['flags'])
        self.assertIn('no_call', rows[2]['flags'])
        self.assertEqual(rows[3]['alleles'], ['I', 'D'])
        self.assertIn('symbolic_allele_unexpanded', rows[3]['flags'])
        self.assertEqual(meta['assembly'], 'unknown')
        self.assertIn('build37', meta['assembly_raw'][0])

    def test_five_column_header_normalization(self):
        rows, meta = g.parse('rsID\tChromosome\tPosition\tAllele 1\tAllele_2\nx\tX\t12\tA\t-\n')
        self.assertEqual(meta['format'], 'declared_five_column_tsv')
        self.assertEqual(rows[0]['alleles'], ['A', '-'])
        self.assertIn('no_call', rows[0]['flags'])

    def test_vcf_partial_and_symbolic(self):
        vcf = '##fileformat=VCFv4.2\n##reference=synthetic-reference\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC\n'
        rows, meta = g.parse(vcf + '1\t12\tx\tA\t<DEL>\t.\tPASS\t.\tGT:DP\t1|.:8\n')
        self.assertEqual(rows[0]['alleles'], ['<DEL>', None])
        self.assertTrue(rows[0]['phased'])
        self.assertIn('no_call', rows[0]['flags'])
        with self.assertRaises(ValueError):
            g.parse(vcf.replace('SYNTHETIC', 'ONE\tTWO'))
        self.assertEqual(meta['assembly'], 'unknown')

    def test_reject_unsupported_header_and_bad_row_retained(self):
        with self.assertRaises(ValueError):
            g.parse('id,chr,pos,genotype\nx,1,1,AA\n')
        rows, _ = g.parse(CSV + 'broken,row\n')
        self.assertEqual(rows[-1]['raw_row'], 'broken,row')
        self.assertIn('invalid_column_count', rows[-1]['flags'])

    def test_invalid_tsv_alleles_remain_raw(self):
        rows, _ = g.parse('rsID\tChromosome\tPosition\tAllele1\tAllele2\nx\t1\t1\tXYZ\tA\n')
        self.assertEqual(rows[0]['alleles'], ['XYZ', 'A'])
        self.assertIn('unsupported_allele_token', rows[0]['flags'])

    def test_vcf_no_alt_invalid_gt_filter_quality(self):
        vcf = '##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC\n'
        rows, _ = g.parse(vcf + '1\t12\tx\tA\t.\t.\tLowQual\t.\tGT\t0/1\n')
        self.assertEqual(rows[0]['alt_raw'], '.')
        self.assertEqual(rows[0]['alleles'], ['A', None])
        for flag in ['invalid_gt', 'filtered_vcf_call', 'quality_unavailable']:
            self.assertIn(flag, rows[0]['flags'])
        rows, _ = g.parse(vcf + '1\t12\tx\tA\t.\t10\tPASS\t.\tGT\t0/0\n')
        self.assertNotIn('invalid_gt', rows[0]['flags'])

    def test_vcf_unapplied_filters_and_sample_field_count(self):
        vcf = '##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC\n'
        rows, _ = g.parse(vcf + '1\t12\tx\tA\tG\t10\t.\t.\tGT:DP\t0/1\n')
        self.assertIn('filters_not_applied', rows[0]['flags'])
        self.assertIn('invalid_sample_field_count', rows[0]['flags'])
        self.assertEqual(rows[0]['fields'][-1], '0/1')
        rows, _ = g.parse(vcf + '1\t12\tx\tA\tG\t10\tPASS\t.\tGT\t0/1:9\n')
        self.assertIn('invalid_sample_field_count', rows[0]['flags'])
        self.assertEqual(rows[0]['fields'][-1], '0/1:9')

    def test_excessive_duplicate_group_rejected(self):
        with self.assertRaisesRegex(ValueError, '1000'):
            g.parse(CSV + ('same,1,101,AG\n' * 1000))

    def test_private_atomic_preservation_no_overwrite(self):
        with tempfile.TemporaryDirectory(dir=g.PUBLIC_ROOT.parent) as base:
            source = Path(base) / 'synthetic.csv'
            source.write_bytes(CSV.encode())
            output = Path(base) / 'private'
            meta = g.stage(source, output)
            self.assertEqual((output / 'source.original').read_bytes(), source.read_bytes())
            with closing(sqlite3.connect(output / 'staging.sqlite')) as db:
                row = json.loads(db.execute('SELECT row_json FROM observations').fetchone()[0])
                self.assertEqual(row['line'], 3)
            self.assertEqual(meta['row_count'], 1)
            with self.assertRaises(FileExistsError):
                g.stage(source, output)
            with self.assertRaises(ValueError):
                g.stage(source, g.PUBLIC_ROOT / 'private-output-forbidden')
            bad = Path(base) / 'bad.txt'
            bad.write_text('unsupported')
            with self.assertRaises(ValueError):
                g.stage(bad, Path(base) / 'failed')
            self.assertFalse((Path(base) / 'failed').exists())

    def test_zip_allowlist_and_limits(self):
        with tempfile.TemporaryDirectory(dir=g.PUBLIC_ROOT.parent) as base:
            source = Path(base) / 'synthetic.zip'
            for names in [['../raw.csv'], ['raw.csv', 'extra.txt'], ['raw.exe']]:
                with zipfile.ZipFile(source, 'w') as z:
                    for name in names:
                        z.writestr(name, CSV)
                with self.assertRaises(ValueError):
                    g.load_source(source)
            with zipfile.ZipFile(source, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr('raw.txt', 'a' * 100000)
            with self.assertRaises(ValueError):
                g.load_source(source)
            with zipfile.ZipFile(source, 'w') as z:
                z.writestr('raw.csv', CSV)
            self.assertEqual(g.load_source(source)[3], 'raw.csv')

if __name__ == '__main__':
    unittest.main()
