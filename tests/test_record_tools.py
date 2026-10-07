"""Wholly synthetic offline archive checks; no patient or connector access."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('record_tools', ROOT / 'examples/private_archive/record_tools.py')
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_archive_templates import expected_templates


def row(table, entry):
    data = rt.empty_row(table)
    data.update(entry_id=entry, import_id='imp_demo', recorded_at='2026-01-02T12:00:00Z', record_status='active')
    if rt.CONTRACT['tables'][table]['fact']:
        data.update(source_kind='medical_document', source_document_id='doc_demo', source_locator='page 1, row A',
                    source_text='WHOLLY SYNTHETIC EXAMPLE', event_date='2024-03-18', event_date_precision='day',
                    review_status='verified_from_source')
    return data


def observation(entry='obs_demo'):
    data = row('observations', entry)
    data.update(analyte_name_raw='Example analyte A', analyte_id='local_example_A', analyte_mapping_status='verified',
                raw_value='1,20', decimal_separator=',', numeric_value='1.20', comparator='=', unit_raw='mg/L',
                unit_code='mg/L', unit_mapping_status='verified', specimen_raw='serum', method_raw='assay A',
                laboratory_raw='fictional lab A', issued_date='2024-03-20', issued_date_precision='day',
                comparability_status='verified')
    return data


def bundle():
    data = {'schema_version': '1.0', 'record_id': 'synthetic_owner', 'import_id': 'imp_demo', 'state': 'staged',
            'recorded_at': '2026-01-02T12:00:00Z', 'is_synthetic': True, 'tables': {t: [] for t in rt.TABLES}}
    doc = row('documents', 'doc_demo')
    doc.update(document_date='2024-03-20', document_date_precision='day', received_sha256='a' * 64,
               storage_readback_status='pending', size_bytes=100, page_order=1)
    data['tables']['documents'].append(doc)
    data['tables']['observations'].append(observation())
    return data


class ArchiveChecks(unittest.TestCase):
    def test_canonical_blank_templates(self):
        for relative, expected in expected_templates(ROOT).items():
            actual = (ROOT / relative).read_bytes().replace(b'\r\n', b'\n')
            self.assertEqual(actual, expected, relative)
            value = json.loads(actual)
            self.assertTrue(value['is_blank_template'])

    def test_decimal_comma_and_threshold_preserved(self):
        result = rt.parse_numeric_result(' <0,10 ', ',')
        self.assertEqual(result, {'raw_value': ' <0,10 ', 'numeric_value': '0.10', 'comparator': '<'})
        self.assertEqual(rt.parse_numeric_result('\u22640.10', '.')['comparator'], '<=')

    def test_ambiguous_tokens_and_separators_rejected(self):
        for raw, separator in [('1,200.5', ','), ('1,20', '.'), ('O.10', '.'), ('negative', '.'), ('1.20', None)]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                rt.parse_numeric_result(raw, separator)

    def test_numeric_boolean_nonfinite_rejected(self):
        for value in [True, 1.2, 'NaN', 'Infinity', '1e3', None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                rt.decimal_value(value)

    def test_date_precision_is_preserved(self):
        for value, precision in [(None, 'unknown'), ('2024', 'year'), ('2024-03', 'month'),
                                 ('2024-02-29', 'day'), ('2024-03-18T12:00:00+01:00', 'datetime')]:
            rt.validate_date(value, precision)
        for value, precision in [('2024-03-01', 'month'), ('2024-13', 'month'), ('2023-02-29', 'day'),
                                 ('2024', 'unknown'), ('2024-03-18T12:00:00', 'datetime')]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                rt.validate_date(value, precision)

    def test_valid_staged_bundle(self):
        self.assertEqual(rt.validate_bundle(bundle(), 'synthetic_owner')['counts']['observations'], 1)

    def test_owner_and_row_import_mismatch(self):
        with self.assertRaises(ValueError):
            rt.validate_bundle(bundle(), 'different_owner')
        data = bundle()
        data['tables']['observations'][0]['import_id'] = 'wrong_import'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_duplicate_ids_and_unknown_columns(self):
        for change in ['duplicate', 'column']:
            data = bundle()
            if change == 'duplicate':
                data['tables']['observations'].append(copy.deepcopy(data['tables']['observations'][0]))
            else:
                data['tables']['observations'][0]['unexpected'] = 'text'
            with self.subTest(change=change), self.assertRaises(ValueError):
                rt.validate_bundle(data, 'synthetic_owner')

    def test_source_foreign_key_required(self):
        data = bundle()
        data['tables']['observations'][0]['source_document_id'] = 'missing'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_duplicate_original_bytes_rejected(self):
        data = bundle()
        duplicate = copy.deepcopy(data['tables']['documents'][0])
        duplicate['entry_id'] = 'another_photo_id'
        data['tables']['documents'].append(duplicate)
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_committed_original_needs_storage_readback(self):
        data = bundle()
        data['state'] = 'committed'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')
        data['tables']['documents'][0].update(remote_file_id='mock_original', storage_readback_status='metadata_verified')
        self.assertEqual(rt.validate_bundle(data, 'synthetic_owner')['state'], 'committed')

    def test_unreadable_results_remain_untyped(self):
        for status in ['needs_review', 'unreadable']:
            data = bundle()
            obs = data['tables']['observations'][0]
            obs['review_status'] = status
            with self.subTest(status=status), self.assertRaises(ValueError):
                rt.validate_bundle(data, 'synthetic_owner')
            obs.update(numeric_value=None, comparator=None)
            rt.validate_bundle(data, 'synthetic_owner')

    def test_normalization_must_match_source(self):
        data = bundle()
        data['tables']['observations'][0]['numeric_value'] = '12.0'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_verified_fact_needs_source_text(self):
        data = bundle()
        data['tables']['observations'][0]['source_text'] = None
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_orders_and_actual_use_are_separate(self):
        data = bundle()
        order = row('medication_orders', 'order_demo')
        order.update(brand_raw='ExampleMed', actual_use_status='unknown')
        data['tables']['medication_orders'].append(order)
        use = row('medication_use_events', 'use_demo')
        use.update(source_kind='owner_report', source_document_id=None, source_locator='owner statement in this import',
                   order_entry_id='order_demo', event_type='not_started', use_evidence='explicit_owner_report',
                   regimen_reported_raw='Owner says: never started ExampleMed')
        data['tables']['medication_use_events'].append(use)
        rt.validate_bundle(data, 'synthetic_owner')
        order['actual_use_status'] = 'currently_taking'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_actual_use_evidence_kind_matches(self):
        data = bundle()
        use = row('medication_use_events', 'use_demo')
        use.update(event_type='dose_taken', use_evidence='explicit_owner_report')
        data['tables']['medication_use_events'].append(use)
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_correction_requires_target_and_keeps_old_row(self):
        data = bundle()
        replacement = observation('obs_corrected')
        replacement.update(raw_value='1,02', numeric_value='1.02', supersedes_entry_id='obs_demo')
        correction = row('corrections', 'correction_demo')
        correction.update(target_table='observations', target_entry_id='obs_demo', replacement_entry_id='obs_corrected',
                          reason_raw='Synthetic transcription correction', correction_authority='source page review')
        data['tables']['observations'].append(replacement)
        data['tables']['corrections'].append(correction)
        rt.validate_bundle(data, 'synthetic_owner')
        self.assertEqual(len(data['tables']['observations']), 2)
        correction['target_entry_id'] = 'absent'
        with self.assertRaises(ValueError):
            rt.validate_bundle(data, 'synthetic_owner')

    def test_chart_excludes_threshold_partial_date_and_staged(self):
        rows = [observation('exact'), observation('limit'), observation('month'), observation('staged')]
        rows[1].update(raw_value='<0,10', numeric_value='0.10', comparator='<')
        rows[2].update(event_date='2024-03', event_date_precision='month')
        rows[3]['import_id'] = 'unfinished'
        groups, excluded = rt.chart_candidates(rows, {'imp_demo'}, set())
        self.assertEqual(sum(map(len, groups.values())), 1)
        self.assertEqual(excluded, {'limit': 'censored_limit_not_exact_value', 'month': 'partial_date', 'staged': 'uncommitted_import'})

    def test_chart_separates_assays_labs_and_units(self):
        rows = [observation(str(i)) for i in range(4)]
        rows[1]['method_raw'] = 'assay B'
        rows[2]['laboratory_raw'] = 'fictional lab B'
        rows[3]['unit_code'] = 'g/L'
        groups, excluded = rt.chart_candidates(rows, {'imp_demo'}, set())
        self.assertEqual(len(groups), 4)
        self.assertEqual(excluded, {})

    def test_chart_resolves_corrections_and_duplicate_ids(self):
        rows = [observation('old'), observation('current')]
        groups, excluded = rt.chart_candidates(rows + [copy.deepcopy(rows[1])], {'imp_demo'}, {'old'})
        self.assertEqual(sum(map(len, groups.values())), 1)
        self.assertEqual(excluded['old'], 'historical_or_erroneous_version')
        conflict = copy.deepcopy(rows[1])
        conflict['numeric_value'] = '99'
        with self.assertRaises(ValueError):
            rt.chart_candidates(rows + [conflict], {'imp_demo'}, set())

    def test_literal_csv_does_not_evaluate_document_formulas(self):
        for value in ['=1+1', ' +SUM(A1:A2)', '-1.2', '@cmd', '\tcell', '\n=2']:
            self.assertEqual(rt.literal_csv(value), "'" + value)
        self.assertEqual(rt.literal_csv('ordinary text'), 'ordinary text')
        self.assertEqual(rt.literal_csv(None), '')

    def test_repository_is_not_an_archive_destination(self):
        with self.assertRaises(ValueError):
            rt.outside_repository(ROOT / 'dist' / 'private.json')

    def test_offline_cli_exports_staging_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'synthetic.json'
            output = Path(directory) / 'staging'
            data = bundle()
            data['tables']['observations'][0]['analyte_name_raw'] = '=1+1'
            source.write_text(json.dumps(data), encoding='utf-8')
            command = [sys.executable, str(ROOT / 'examples/private_archive/record_tools.py'), str(source),
                       '--record-id', 'synthetic_owner', '--export-dir', str(output)]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            receipt = json.loads(result.stdout)
            self.assertFalse(receipt['archive_commit_performed'])
            self.assertFalse(receipt['ocr_performed'])
            with (output / 'observations.csv').open(encoding='utf-8', newline='') as stream:
                self.assertEqual(next(csv.DictReader(stream))['analyte_name_raw'], "'=1+1")
            before = (output / 'observations.csv').read_bytes()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual((output / 'observations.csv').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
