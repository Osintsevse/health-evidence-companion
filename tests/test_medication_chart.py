"""Wholly synthetic evidence/date/filter invariants for the graphic model."""
import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('chart',Path(__file__).resolve().parents[1]/'skills/health-record-import/scripts/medication_chart.py');chart=importlib.util.module_from_spec(spec);spec.loader.exec_module(chart)

def event(eid='FAKE-A',kind='use',event_type='regimen_reported',review='user_confirmed',group='Synthetic Alpha'):
    return {'entry_id':eid,'kind':kind,'event_type':event_type,'group':group,'date':'2048-02','source':{'review_status':review,'source_document_id':'FICTIONAL-SOURCE'}}

class ChartTests(unittest.TestCase):
    def test_disconnected_reports_never_generate_a_course(self):
        events=[event(),event('FAKE-B')];events[1]['date']='2052-10-13';before=copy.deepcopy(events)
        result=chart.build_chart(events,{},'2053-01-01');self.assertEqual(result['intervals'],[]);self.assertEqual(events,before)
    def test_contextual_topics_and_multiple_memberships(self):
        cfg={'medication_timeline_themes':[{'id':'context-a','label':'Synthetic context A','groups':['Synthetic Alpha']},{'id':'context-b','label':'Synthetic context B','entry_ids':['FAKE-A']}],'medication_timeline_default_theme':'context-a'}
        result=chart.build_chart([event()],cfg);self.assertEqual(result['events'][0]['themes'],['context-a','context-b']);self.assertEqual(result['default_theme'],'context-a')
    def test_supported_partial_period_preserves_precision(self):
        item={'id':'FAKE-PERIOD','kind':'period','group':'Synthetic Alpha','start':'2048-02','end':'2048','evidence_entry_ids':['FAKE-A']}
        result=chart.build_chart([event()],{'medication_timeline_periods':[item]},'2049-01-01');self.assertEqual(result['intervals'][0]['start'],'2048-02');self.assertEqual(result['intervals'][0]['end'],'2048')
    def test_prescription_nonuse_and_unreviewed_cannot_support_band(self):
        cfg={'medication_timeline_periods':[{'id':'FAKE-PERIOD','kind':'period','group':'Synthetic Alpha','start':'2048-02','end':'2048-03','evidence_entry_ids':['FAKE-A']}]}
        for row in [event(kind='order'),event(event_type='not_started'),event(event_type='benefit_reported'),event(event_type='adverse_effect_reported'),event(review='needs_review'),event(group='Synthetic Beta')]:
            with self.subTest(row=row),self.assertRaises(ValueError):chart.build_chart([row],cfg)
    def test_unknown_start_and_duration_only_stay_unknown(self):
        cfg={'medication_timeline_periods':[{'id':'FAKE-CURRENT','kind':'ongoing','group':'Synthetic Alpha','confirmed_until':'2048-11-03','evidence_entry_ids':['FAKE-A']},{'id':'FAKE-DURATION','kind':'duration_only','group':'Synthetic Alpha','duration_text':'seven weeks','anchor_date':'2048-02','evidence_entry_ids':['FAKE-A']}]}
        result=chart.build_chart([event()],cfg,'2048-12-01')
        for row in result['intervals']:self.assertIsNone(row.get('start'));self.assertIsNone(row.get('end'))
        cfg['medication_timeline_periods'][1]['start']='2048-02-01'
        with self.assertRaises(ValueError):chart.build_chart([event()],cfg,'2048-12-01')
    def test_bad_dates_missing_evidence_duplicates_and_future_confirmation(self):
        base={'id':'FAKE-CURRENT','kind':'ongoing','group':'Synthetic Alpha','confirmed_until':'2048-11-03','evidence_entry_ids':['FAKE-A']}
        for update in [{'confirmed_until':'2048-02-30'},{'confirmed_until':'2050-01-01'},{'evidence_entry_ids':['MISSING']}]:
            with self.subTest(update=update),self.assertRaises(ValueError):chart.build_chart([event()],{'medication_timeline_periods':[{**base,**update}]},'2049-01-01')
        with self.assertRaises(ValueError):chart.build_chart([event(),event()],{})
        with self.assertRaises(ValueError):chart.build_chart([event()],{'medication_timeline_themes':[{'id':'x','label':'X'},{'id':'x','label':'Y'}]})
        with self.assertRaises(ValueError):chart.build_chart([event()],{'medication_timeline_themes':[{'id':'x','label':'X','groups':'Synthetic Alpha'}]})
        with self.assertRaises(ValueError):chart.build_chart([event()],{'medication_timeline_periods':[{**base,'end':'2050-01-01'}]},'2049-01-01')
