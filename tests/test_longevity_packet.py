"""Source/measure and installed-retrieval checks; not clinical validation."""
import json
import math
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LongevityPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = json.loads((ROOT/'knowledge/longevity/statistics.json').read_text(encoding='utf-8'))
        cls.ledger = json.loads((ROOT/'knowledge/longevity/evidence-ledger.json').read_text(encoding='utf-8'))

    def test_every_statistical_source_has_reading_and_rights_provenance(self):
        known = {r['source_id']: r for r in self.ledger['records']}
        records = self.stats['prevention_panels'] + self.stats['geroscience_records'] + [self.stats['mouse_denominator_example']]
        canonical = {'medical:'+r['id'] for r in json.loads((ROOT/'knowledge/sources.json').read_text(encoding='utf-8'))}
        for record in records:
            with self.subTest(source=record['source_id']):
                self.assertIn(record['source_id'], known)
                self.assertIn(record['source_id'], canonical)
                source = known[record['source_id']]
                self.assertTrue(source['reading_scope'])
                self.assertTrue(source['rights'])
                self.assertLessEqual(source['checked_on'], self.stats['checked_on'])

    def test_intervals_are_ordered_and_not_mislabeled_iqr(self):
        def inspect(value):
            if isinstance(value, dict):
                if all(k in value for k in ['estimate','lower','upper']):
                    self.assertLessEqual(value['lower'], value['estimate'])
                    self.assertLessEqual(value['estimate'], value['upper'])
                ci=value.get('confidence_interval')
                if ci and value.get('estimate') is not None:
                    self.assertLessEqual(ci['lower'],value['estimate'])
                    self.assertLessEqual(value['estimate'],ci['upper'])
                if 'interquartile_range' in value:
                    self.assertNotIn('confidence_interval',value)
                for item in value.values(): inspect(item)
            elif isinstance(value,list):
                for item in value: inspect(item)
        inspect(self.stats)

    def test_mouse_remaining_survival_does_not_become_total_or_human(self):
        row=self.stats['mouse_denominator_example']
        remaining=row['reported_median_remaining_lifespan_weeks']
        total=row['derived_median_total_age_weeks']
        for group,value in remaining.items():
            self.assertAlmostEqual(total[group],row['treatment_start_age_weeks']+value)
        remaining_gain=(remaining['aav_osk_doxycycline']/remaining['control_doxycycline']-1)*100
        total_gain=(total['aav_osk_doxycycline']/total['control_doxycycline']-1)*100
        self.assertGreater(remaining_gain,100)
        self.assertLess(total_gain,10)
        self.assertTrue(row['not_human_data'])

    def test_adverse_events_and_affected_people_are_distinct(self):
        record=next(r for r in self.stats['geroscience_records'] if r['endpoint']=='Adverse-event count')
        counts=record['absolute']
        self.assertGreater(counts['active_event_count'],counts['active_participants_with_event'])
        self.assertEqual(counts['active_participants_with_event'],counts['placebo_participants_with_event'])
        self.assertLess(record['confidence_interval']['lower'],1)
        self.assertGreater(record['confidence_interval']['upper'],1)

    def test_absolute_percentage_points_keep_their_units_and_horizon(self):
        record=next(r for r in self.stats['prevention_panels'] if r['id']=='statin_primary_prevention_mortality')
        self.assertEqual(record['absolute_effect']['unit'],'percentage_points')
        self.assertAlmostEqual(record['absolute_effect']['estimate']*10,-3.5)
        self.assertIn('Varying',record['follow_up'])
        self.assertIn('no fixed-year NNT',record['caution'])

    def test_relevant_installed_skills_have_complete_nested_packet(self):
        for skill in ['health-explain','health-prevention','health-research','health-contribute','health-nutrition']:
            refs=ROOT/'skills'/skill/'references'
            mapping=json.loads((refs/'knowledge-search-map.json').read_text(encoding='utf-8'))
            paths={r['canonical_path']:r['local_path'] for r in mapping['entries']}
            for name in ['00_READING_PLAN.md','10_PREVENTION_EVIDENCE.md','20_GEROSCIENCE_EVIDENCE.md','30_RADICAL_EXTENSION_EVIDENCE.md','40_STATISTICS_GUIDE.md']:
                canonical='knowledge/longevity/'+name
                self.assertEqual(paths[canonical],'longevity/'+name)
                self.assertEqual((refs/paths[canonical]).read_bytes(),(ROOT/canonical).read_bytes())
            self.assertTrue((refs/'longevity/statistics.json').is_file())

    def test_installed_search_retrieves_drug_and_cessation_cards(self):
        skill=ROOT/'skills/health-prevention'
        queries=[('rapamycin RAPA', '20_GEROSCIENCE_EVIDENCE.md'),
                 ('\u043e\u0442\u043a\u0430\u0437 \u043e\u0442 \u043a\u0443\u0440\u0435\u043d\u0438\u044f', '10_PREVENTION_EVIDENCE.md')]
        for query,expected in queries:
            completed=subprocess.run([sys.executable,'-X','utf8',str(skill/'scripts/knowledge_search.py'),
                '--root',str(skill/'references'),'search',query,'--limit','5'],check=True,capture_output=True,text=True,encoding='utf-8')
            result=json.loads(completed.stdout)
            self.assertIn(expected,json.dumps(result))

    def test_no_provisional_keys_or_private_project_links_in_packet(self):
        for path in (ROOT/'knowledge/longevity').glob('*'):
            if path.is_file():
                text=path.read_text(encoding='utf-8')
                self.assertIsNone(re.search(r'L-(?:G|R|T|A|C|D|AL|S)\d{2}',text),str(path))
                self.assertNotIn('drive.google.com',text)
                self.assertNotIn('docs.google.com',text)


if __name__=='__main__':
    unittest.main()
