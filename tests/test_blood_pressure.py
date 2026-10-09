"""Wholly invented BP fixtures, not anonymized patient records."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bp',ROOT/'skills/health-record-import/scripts/blood_pressure.py')
bp=importlib.util.module_from_spec(spec);spec.loader.exec_module(bp)


def row(component='SYS',value=108,locator='measurement[0]',**kw):
    return {'entry_id':locator+'-'+component,'analyte_name_raw':component,
            'numeric_value':str(value),'raw_value':str(value),'comparator':'=',
            'unit_raw':'bpm' if component in ('PR','\u041f\u0443\u043b\u044c\u0441') else 'mmHg',
            'event_date':'2021-02-03','event_date_precision':'day',
            'source_document_id':'SYNTHETIC-DOC','source_locator':locator+'; '+component,
            'method_raw':'synthetic cuff','review_status':'verified_from_source',
            'record_status':'active',**kw}


def readings(*rows,**config):
    return bp.build_dashboard({'as_of':'2022-01-01','tables':{'observations':list(rows)}},config)


class BloodPressureTests(unittest.TestCase):
    def test_repeat_triples_and_missing_pulse_do_not_merge(self):
        rows=[row(),row('DIA',62),row('PR',79),row(value=136,locator='measurement[1]'),row('DIA',83,locator='measurement[1]')]
        before=copy.deepcopy(rows);out=readings(*rows)
        self.assertEqual([(r['sys'],r['dia'],r['pulse']) for r in out['measurements']],[(108,62,79),(136,83,None)])
        self.assertEqual(rows,before);self.assertEqual(len(out['entry_ids']),5)
        self.assertIsNone(out['measurements'][0]['time'])

    def test_russian_labels_and_units_preserve_triple(self):
        out=readings(row('\u0421\u0438\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435',108,unit_raw='\u043c\u043c \u0440\u0442. \u0441\u0442.'),row('\u0414\u0438\u0430\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435',62,unit_raw='\u043c\u043c \u0440\u0442. \u0441\u0442.'),row('\u041f\u0443\u043b\u044c\u0441',79,unit_raw='\u0443\u0434/\u043c\u0438\u043d'))
        self.assertEqual(len(out['measurements']),1)
        self.assertEqual([out['measurements'][0][k] for k in ('sys','dia','pulse')],[108,62,79])

    def test_duplicate_components_are_not_zipped_or_overwritten(self):
        a=row();b=row(value=136,entry_id='SYNTHETIC-REPEAT');c=row('DIA',62)
        out=readings(a,b,c)['measurements']
        self.assertEqual(len(out),3);self.assertTrue(all(m['ambiguous'] for m in out))
        self.assertTrue(all(m['category']=='unknown' for m in out))

    def test_missing_locator_does_not_establish_pair(self):
        out=readings(row(source_locator=None),row('DIA',62,source_locator=None))
        self.assertEqual(len(out['measurements']),2)

    def test_distinct_sources_or_methods_are_not_paired(self):
        self.assertEqual(len(readings(row(),row('DIA',62,source_document_id='SYNTHETIC-OTHER'))['measurements']),2)
        self.assertEqual(len(readings(row(),row('DIA',62,method_raw='another synthetic method'))['measurements']),2)

    def test_unreviewed_limits_units_and_nonfinite_remain_excluded(self):
        variants=[{'review_status':'needs_review'},{'record_status':'superseded'},{'comparator':'<'},{'raw_value':'~108'},{'unit_raw':'kPa'},{'numeric_value':'NaN'},{'numeric_value':'Infinity'},{'numeric_value':'109'},{'numeric_value':'0','raw_value':'0'}]
        for variant in variants:
            with self.subTest(variant=variant):
                out=readings(row(**variant));self.assertFalse(out['measurements']);self.assertEqual(len(out['excluded']),1)

    def test_user_confirmed_and_numeric_decimal_are_accepted(self):
        self.assertEqual(readings(row(review_status='user_confirmed',value=108.5,raw_value='108,5'))['measurements'][0]['sys'],108.5)

    def test_dates_and_import_timestamps_are_not_fabricated(self):
        for date,precision in [(None,'unknown'),('2021','year'),('2021-02-30','day'),('2030-01-01','day')]:
            with self.subTest(date=date):
                out=readings(row(event_date=date,event_date_precision=precision,recorded_at='2021-02-03T08:00:00'))['measurements'][0]
                self.assertIsNone(out['date']);self.assertIsNone(out['time']);self.assertEqual(out['date_raw'],date)
        a=readings(row(event_date='2021-02-03T10:15:00',event_date_precision='datetime'))['measurements'][0]
        self.assertEqual((a['date'],a['time']),('2021-02-03','10:15'))

    def test_abpm_time_repeats_and_scheme_exclusion(self):
        a=row(locator='page 1 (1)10:15',method_raw='ABPM');b=row('DIA',62,locator='page 1 (1)10:15',method_raw='ABPM')
        c=row(locator='page 1 (2)10:15',method_raw='ABPM')
        out=readings(a,b,c,blood_pressure_categories='aha_2025_adult')['measurements']
        self.assertEqual(len(out),2);self.assertEqual(out[0]['time'],'10:15');self.assertEqual(out[0]['category'],'unknown')

    def test_category_boundaries_and_mixed_low_high(self):
        for sys,dia,result in [(119,79,'normal'),(120,79,'elevated'),(129,80,'stage1'),(130,79,'stage1'),(139,89,'stage1'),(140,79,'stage2'),(110,90,'stage2'),(89,65,'low'),(110,59,'low'),(151,54,'mixed'),(90,60,'normal'),(110,None,'unknown')]:
            self.assertEqual(bp.category(sys,dia),result)
        out=readings(row(value=151),row('DIA',54),blood_pressure_categories='aha_2025_adult')['measurements'][0]
        self.assertEqual(out['category'],'mixed')
        self.assertEqual(readings(row(),row('DIA',62))['measurements'][0]['category'],'unknown')

    def test_order_is_preserved_without_asserting_chronology(self):
        rows=[row(event_date='2021-12-01'),row(locator='measurement[1]',event_date=None)]
        out=readings(*rows)['measurements'];self.assertEqual([m['index'] for m in out],[1,2])
        self.assertEqual(out[0]['sources'][0],rows[0])

    def test_component_names_are_exact_not_substring_guesses(self):
        self.assertFalse(readings(row('SYS average',108))['measurements'])


if __name__=='__main__':unittest.main()
