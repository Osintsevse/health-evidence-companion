"""Optional real-browser regression; all fixture rows are wholly invented.

Set BP_BROWSER_NODE and optionally BP_PLAYWRIGHT_MODULE/BP_BROWSER_CHANNEL.
The core model/integration suite needs only Python's standard library.
"""
import contextlib
import hashlib
import importlib.util
import json
import os
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bp_fixture',ROOT/'tests/test_blood_pressure.py')
fixtures=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixtures)
spec=importlib.util.spec_from_file_location('bp_views',ROOT/'skills/health-record-import/scripts/generate_views.py')
views=importlib.util.module_from_spec(spec);spec.loader.exec_module(views)


def create_fixture(output,locale):
    with tempfile.TemporaryDirectory() as tmp:
        db=Path(tmp)/'synthetic.sqlite'
        with contextlib.closing(sqlite3.connect(db)) as c:
            contract=json.loads((ROOT/'knowledge/archive_tables.json').read_text())
            for name,table in contract['tables'].items():
                columns=([] if name=='imports' else contract['common_columns'])+(contract['fact_columns'] if table['fact'] else [])+table['columns']
                c.execute('create table '+name+' ('+','.join(x+' TEXT' for x in columns)+')')
            c.execute("INSERT INTO imports(import_id,record_id,state,ledger_readback_status) VALUES('SYNTHETIC-IMPORT','synthetic-owner','committed','rows_verified')")
            row=fixtures.row
            names=['SYS','DIA','PR'] if locale=='en' else ['\u0421\u0438\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435','\u0414\u0438\u0430\u0441\u0442\u043e\u043b\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435','\u041f\u0443\u043b\u044c\u0441']
            rows=[]
            for index,values in enumerate([(108,62,79),(136,83,None),(151,54,72),(112,68,75),(118,71,80)]):
                for name,value,unit in zip(names,values,['mmHg','mmHg','bpm']):
                    if value is None:continue
                    rows.append(row(name,value,locator='measurement['+str(index)+']',unit_raw=unit,
                        event_date=None if index==3 else '2021-02-03',
                        method_raw='ABPM' if index==4 else 'synthetic cuff',
                        source_locator=('page 1 (1)10:15' if index==4 else 'measurement['+str(index)+']')+'; '+name))
            rows.append(row(value=999,locator='measurement[5]',review_status='needs_review'))
            rows.append(row('MAP',81,locator='measurement[6]'))
            for r in rows:
                r.update(import_id='SYNTHETIC-IMPORT',source_kind='owner_report')
                columns=list(r);c.execute('INSERT INTO observations('+','.join(columns)+') VALUES('+','.join('?' for _ in columns)+')',list(r.values()))
            c.commit()
        before=hashlib.sha256(db.read_bytes()).hexdigest()
        views.generate(db,{'record_id':'synthetic-owner','locale':locale,'as_of':'2022-01-01','blood_pressure_categories':'aha_2025_adult'},output,ROOT/'skills/health-record-import/assets/archive-view.html')
        if hashlib.sha256(db.read_bytes()).hexdigest()!=before:raise AssertionError('View generation mutated the synthetic ledger')


class BloodPressureBrowserTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('BP_BROWSER_NODE'),'Optional Node/Playwright browser runtime not configured')
    def test_complete_offline_bp_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            for locale in ['en','ru']:create_fixture(Path(tmp)/locale,locale)
            result=subprocess.run([os.environ['BP_BROWSER_NODE'],str(ROOT/'tests/blood_pressure_browser.mjs'),tmp],capture_output=True,text=True,timeout=90)
            self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)
            receipt=json.loads(result.stdout);self.assertEqual(receipt['locales'],['en','ru']);self.assertEqual(receipt['network_requests'],0)


if __name__=='__main__':unittest.main()
