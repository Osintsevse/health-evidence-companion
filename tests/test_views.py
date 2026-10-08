"""Wholly synthetic view tests; never reads a real patient archive."""
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/health-record-import/scripts/generate_views.py'
spec=importlib.util.spec_from_file_location('view_helpers',SCRIPT)
views=importlib.util.module_from_spec(spec);spec.loader.exec_module(views)


def observation(entry,**changes):
    row={'entry_id':entry,'import_id':'SYN-IMPORT','record_status':'active','review_status':'verified_from_source',
         'source_document_id':'DOC-SYN','source_kind':'medical_document','source_locator':'synthetic row',
         'source_text':'Wholly synthetic result','event_date':'2040-05-06','event_date_precision':'day',
         'analyte_name_raw':'Synthetic analyte','unit_raw':'mg/L','specimen_raw':'synthetic serum',
         'method_raw':'synthetic method','laboratory_raw':'Synthetic laboratory','raw_value':'0',
         'numeric_value':'0','comparator':'=','flag_raw':None,'uncertainties':None}
    row.update(changes);return row


class ReadableViewsTests(unittest.TestCase):
    def test_same_day_distinct_reports_and_repeat_results_survive(self):
        rows=[observation('SYN-A'),observation('SYN-B'),observation('SYN-C',source_document_id='DOC-SYN-OTHER')]
        result=views.build_matrix(rows)
        self.assertEqual(len(result['events']),2)
        self.assertEqual(sum(len(c) for e in result['events'] for c in e['cells'].values()),3)

    def test_report_pages_group_but_categories_stay_separate(self):
        docs=[{'entry_id':'DOC-SYN','report_group_id':'SYN-REPORT'},{'entry_id':'DOC-SYN-OTHER','report_group_id':'SYN-REPORT'}]
        rows=[observation('SYN-A'),observation('SYN-B',source_document_id='DOC-SYN-OTHER',analyte_name_raw='Another synthetic analyte'),observation('SYN-U',specimen_raw='U')]
        result=views.build_matrix(rows,documents=docs)
        self.assertEqual({r['category'] for r in result['events']},{'blood','urine'})
        self.assertEqual(len(result['events']),2)

    def test_display_alias_cannot_merge_raw_units_or_analytes(self):
        rows=[observation('SYN-A'),observation('SYN-B',unit_raw='g/L'),observation('SYN-C',analyte_name_raw='Other synthetic analyte')]
        result=views.build_matrix(rows,{'display_units':{'mg/L':'same label','g/L':'same label'},'display_analytes':{'Other synthetic analyte':'Synthetic analyte'}})
        self.assertEqual(len(result['columns']),3)

    def test_owner_report_without_document_id(self):
        result=views.build_matrix([observation('SYN-A'),observation('SYN-B',source_kind='owner_report',source_document_id=None)])
        self.assertEqual(len(result['events']),2)

    def test_unreviewed_and_undated_not_fabricated(self):
        result=views.build_matrix([observation('SYN-A',review_status='needs_review',numeric_value=None,comparator=None),observation('SYN-B',event_date=None,event_date_precision='unknown')])
        self.assertEqual(result['events'],[])

    def test_pending_replacement_does_not_hide_accepted_value(self):
        rows=[observation('SYN-A'),observation('SYN-B',review_status='needs_review')]
        corr={'target_table':'observations','review_status':'verified_from_source','target_entry_id':'SYN-A','replacement_entry_id':'SYN-B'}
        self.assertEqual(len(views.resolve_history(rows,[corr],'observations')),2)
        rows[1]['review_status']='user_confirmed'
        self.assertEqual([r['entry_id'] for r in views.resolve_history(rows,[corr],'observations')],['SYN-B'])

    def test_literal_headers_and_limit_values(self):
        row=observation('SYN-A',analyte_name_raw='=synthetic()',raw_value='<2.0',numeric_value='2.0',comparator='<')
        model={'matrix':views.build_matrix([row]),'tables':{'observations':[row]}}
        export=views.workbook_data(model)
        self.assertEqual(export[0]['orientation'],'analytes_in_rows')
        self.assertTrue(export[0]['rows'][-1][0].startswith("'="))
        self.assertEqual(export[0]['rows'][-1][-1],'<2.0')

    def test_no_private_output_inside_public_source(self):
        with self.assertRaises(ValueError):
            views.generate('unused',{},ROOT/'private-output',ROOT/'skills/health-record-import/assets/archive-view.html')


if __name__=='__main__':unittest.main()
