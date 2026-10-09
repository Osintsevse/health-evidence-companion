import importlib.util
import contextlib
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).parents[1]
SCRIPT = ROOT / 'skills/health-record-import/scripts/psychology_records.py'
spec = importlib.util.spec_from_file_location('psychology_records', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def summary():
    return {'schema': m.SCHEMA, 'owner_key': 'synthetic-owner',
            'selection_scope': 'owner_selected_summary',
            'summaries': [{'record_id': 'summary-1', 'title': 'Selected note',
                           'text': '<script>literal text</script>'}]}


class SummaryTests(unittest.TestCase):
    def test_no_config(self):
        self.assertIsNone(m.load_summary({}))
        for config in [{'psychology': {}}, {'psychology': []},
                       {'psychology': {'summary_path': 'missing'}}]:
            with self.assertRaises(ValueError):
                m.load_summary(config)

    def test_validation(self):
        for field, value in [('schema', 'diary'), ('owner_key', 'other-owner'),
                             ('selection_scope', 'whole_diary'), ('summaries', 'text')]:
            data = summary(); data[field] = value
            with self.assertRaises(ValueError):
                m.project_summary(data, 'synthetic-owner')
        for field, value in [('record_id', '../file'), ('title', []), ('text', None),
                             ('source_ref', {}), ('as_of', 2)]:
            data = summary(); data['summaries'][0][field] = value
            with self.assertRaises(ValueError):
                m.project_summary(data, 'synthetic-owner')
        data = summary(); data['summaries'] *= 2
        with self.assertRaises(ValueError):
            m.project_summary(data, 'synthetic-owner')
        with self.assertRaises(ValueError):
            m.project_summary(summary(), None)

    def test_strict_projection(self):
        data = summary(); data['private_diary'] = 'never export'
        data['summaries'][0]['full_conversation'] = 'never export'
        selected = m.project_summary(data, 'synthetic-owner')
        self.assertEqual(selected, summary())

    def test_bounded_loading_and_atomic_export(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            source = pathlib.Path(directory) / 'chosen.json'
            source.write_text(json.dumps(summary()), encoding='utf-8')
            config = {'psychology': {'summary_path': str(source), 'owner_key': 'synthetic-owner'}}
            self.assertEqual(m.load_summary(config), summary())
            config['psychology']['owner_key'] = 'wrong'
            with self.assertRaises(ValueError): m.load_summary(config)
            source.write_text('{bad', encoding='utf-8')
            with self.assertRaises(ValueError): m.read_summary(source, 'synthetic-owner')
            source.write_bytes(b' ' * (m.MAX_BYTES + 1))
            with self.assertRaises(ValueError): m.read_summary(source, 'synthetic-owner')
            source.write_text('{"schema":"a","schema":"b"}', encoding='utf-8')
            with self.assertRaises(ValueError): m.read_summary(source, 'synthetic-owner')
            output = pathlib.Path(directory) / 'summary.json'
            m.share_summary(summary(), output, 'synthetic-owner')
            self.assertEqual(m.read_summary(output, 'synthetic-owner'), summary())
            with self.assertRaises(FileExistsError):
                m.share_summary(summary(), output, 'synthetic-owner')
            with self.assertRaises(ValueError):
                m.share_summary(summary(), SCRIPT.parent / 'private.json', 'synthetic-owner')
            self.assertEqual(list(pathlib.Path(directory).glob('.psychology-summary-*')), [])

    def test_copied_helper_and_installed_skill_boundary(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            base = pathlib.Path(directory)
            copied = base / 'private' / 'scripts' / 'psychology_records.py'
            copied.parent.mkdir(parents=True); copied.write_bytes(SCRIPT.read_bytes())
            spec = importlib.util.spec_from_file_location('copied_psychology', copied)
            local = importlib.util.module_from_spec(spec); spec.loader.exec_module(local)
            output = base / 'private' / 'selected.json'
            local.share_summary(summary(), output, 'synthetic-owner')
            self.assertTrue(output.is_file())
            (copied.parent.parent / 'SKILL.md').write_text('Synthetic installed skill')
            with self.assertRaises(ValueError):
                local.share_summary(summary(), base / 'private' / 'another.json', 'synthetic-owner')

    def test_optional_generation(self):
        import sqlite3
        spec = importlib.util.spec_from_file_location('summary_views', SCRIPT.with_name('generate_views.py'))
        views = importlib.util.module_from_spec(spec); spec.loader.exec_module(views)
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            base = pathlib.Path(directory); db = base / 'synthetic.sqlite'
            contract = json.loads((ROOT / 'knowledge/archive_tables.json').read_text())
            with contextlib.closing(sqlite3.connect(db)) as connection:
                for name, table in contract['tables'].items():
                    columns = ([] if name == 'imports' else contract['common_columns']) + (contract['fact_columns'] if table['fact'] else []) + table['columns']
                    connection.execute('create table ' + name + ' (' + ','.join(x + ' TEXT' for x in columns) + ')')
                connection.execute("INSERT INTO imports(import_id,record_id,state,ledger_readback_status) VALUES('SYN-BASE','synthetic-owner','committed','rows_verified')")
                connection.commit()
            template = ROOT / 'skills/health-record-import/assets/archive-view.html'
            out = base / 'view'
            views.generate(db, {'record_id':'synthetic-owner'}, out, template)
            self.assertNotIn('psychology', json.loads((out / 'view_data.json').read_text()))
            source = base / 'selected.json'; source.write_text(json.dumps(summary()))
            config = {'record_id':'synthetic-owner','locale': 'ru', 'psychology': {'summary_path': str(source), 'owner_key': 'synthetic-owner'}}
            views.generate(db, config, out, template)
            model = json.loads((out / 'view_data.json').read_text(encoding='utf-8'))
            self.assertEqual(model['psychology'], summary())
            html = (out / 'index.html').read_text(encoding='utf-8')
            self.assertNotIn('<script>literal text</script>', html)
            self.assertIn('literal text', html)
            self.assertEqual(model['labels']['psychology'], m.ui_labels('ru')['psychology'])

    def test_projection_preserves_original_and_has_independent_rows(self):
        import copy
        original=summary()
        original['private_diary']='Synthetic excluded text'
        before=copy.deepcopy(original)
        selected=m.project_summary(original,'synthetic-owner')
        self.assertEqual(original,before)
        selected['summaries'][0]['text']='Modified exported copy'
        self.assertEqual(original,before)


if __name__ == '__main__':
    unittest.main()
