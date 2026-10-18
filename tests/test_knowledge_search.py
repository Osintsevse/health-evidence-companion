"""Failure-oriented tests of bounded packaged-note retrieval."""
import importlib.util
from contextlib import closing
import json
import sqlite3
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('knowledge_search', Path(__file__).resolve().parents[1] / 'scripts/knowledge_search.py')
searcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(searcher)


class KnowledgeSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'plugin'
        (self.root / 'knowledge/clinical').mkdir(parents=True)
        self.write('00_KNOWLEDGE_POLICY.md', '# Policy\nOriginal notes only.\n')
        self.write('42_NOTES.md', '# Asthma\nChild asthma education [medical:S01].\n```md\n## False heading\n```\n## Follow-up\nContinue assessment.\n')
        self.save('knowledge/search-aliases.json', {'schema': 'knowledge-search-aliases-v1', 'groups': [['asthma', '\u0430\u0441\u0442\u043c\u0430'], ['child', '\u0434\u0435\u0442\u0441\u043a\u0430\u044f']]})
        self.save('knowledge/source-catalog.json', {'records': [{'qualified_id': 'medical:S01', 'title': 'Source', 'url': 'https://restricted.example/page', 'reading_status': 'description only'}]})
        self.save('knowledge/clinical/source-use-policy.json', {'rules': [{'id': 'restricted', 'host_suffix': 'restricted.example', 'path_prefix': '/', 'action': 'bibliographic_pointer_only'}]})

    def write(self, name, text):
        (self.root / 'knowledge' / name).write_text(text, encoding='utf-8')

    def save(self, name, data):
        (self.root / name).write_text(json.dumps(data), encoding='utf-8')

    def test_aliases_fences_exact_locator_and_provenance(self):
        result = searcher.search(self.root, '\u0434\u0435\u0442\u0441\u043a\u0430\u044f \u0430\u0441\u0442\u043c\u0430')['results'][0]
        self.assertEqual(result['heading'], 'Asthma')
        self.assertEqual((result['line_start'], result['line_end']), (1, 5))
        source = result['sources'][0]
        self.assertEqual(source['qualified_id'], 'medical:S01')
        self.assertEqual(source['reading_status'], 'description only')
        self.assertEqual(source['rights_rules'][0]['id'], 'restricted')
        self.assertFalse(source['permission_inferred'])
        fetched = searcher.fetch(self.root, result['section_id'])
        self.assertIn('## False heading', fetched['text'])
        self.assertNotIn('Follow-up', fetched['text'])
        self.assertFalse(fetched['truncated'])

    def test_bounds_no_raw_fts_or_paths(self):
        for query in ['', 'a ' * 25, 'a' * 501]:
            with self.assertRaises(ValueError):
                searcher.search(self.root, query)
        self.assertEqual(searcher.search(self.root, '" OR NOT *')['results'], [])
        with self.assertRaises(ValueError):
            searcher.fetch(self.root, '../../secret')
        with self.assertRaises(ValueError):
            searcher.fetch(self.root, '0' * 24)
        sid = searcher.search(self.root, 'asthma')['results'][0]['section_id']
        first = searcher.fetch(self.root, sid, max_chars=5)
        self.assertTrue(first['truncated'])
        self.assertEqual(first['next_offset'], 5)
        self.assertEqual(searcher.fetch(self.root, sid, offset=5, max_chars=5)['offset'], 5)
        with self.assertRaises(ValueError):
            searcher.fetch(self.root, sid, offset=100000)
        with self.assertRaises(ValueError):
            searcher.search(self.root, 'asthma', limit=21)

    def test_explicit_stale_index_requires_rebuild(self):
        index = Path(self.temp.name) / 'cache.sqlite'
        searcher.build_index(self.root, index)
        original = searcher.search(self.root, 'asthma', index_path=index)['results'][0]
        self.write('42_NOTES.md', '# Asthma\nUpdated child asthma.\n')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            searcher.search(self.root, 'asthma', index_path=index)
        searcher.build_index(self.root, index)
        updated = searcher.search(self.root, 'asthma', index_path=index)['results'][0]
        self.assertEqual(original['section_id'], updated['section_id'])
        self.assertNotEqual(original['content_sha256'], updated['content_sha256'])
        with self.assertRaises(ValueError):
            searcher.build_index(self.root, self.root / 'knowledge/cache.sqlite')

    def test_installed_map_has_no_repository_dependency(self):
        installed = Path(self.temp.name) / 'references'
        installed.mkdir()
        (installed / 'note.md').write_text('# Topic\nAsthma standalone note.\n', encoding='utf-8')
        (installed / 'knowledge-search-map.json').write_text(json.dumps({'entries': [{'canonical_path': 'knowledge/42_NOTES.md', 'local_path': 'note.md'}]}), encoding='utf-8')
        found = searcher.search(installed, 'asthma')['results'][0]
        self.assertEqual(found['canonical_path'], 'knowledge/42_NOTES.md')
        self.assertEqual(found['sources'], [])
        self.assertEqual(searcher.status(installed)['notes'], 1)
        with self.assertRaises(ValueError):
            searcher.build_index(installed, installed / 'cache.sqlite')
        (installed / 'knowledge-search-map.json').write_text(json.dumps({'entries': [{'canonical_path': 'knowledge/x.md', 'local_path': '../outside.md'}]}), encoding='utf-8')
        with self.assertRaises(ValueError):
            searcher.status(installed)

    def test_long_sections_have_bounded_chunks_and_parent_fetch(self):
        self.write('43_LONG.md', '# Long\n' + ('Asthma context. ' * 80 + '\n') * 20 + '\nSource medical:S01.\n')
        result = next(r for r in searcher.search(self.root, 'context', limit=20)['results'] if r['kind'] == 'chunk')
        self.assertLessEqual(len(searcher.fetch(self.root, result['section_id'])['text']), 6000)
        parent = searcher.fetch(self.root, result['parent_section_id'], max_chars=1000)
        self.assertTrue(parent['truncated'])
        self.assertEqual(parent['kind'], 'section')
        self.assertEqual(result['sources'][0]['qualified_id'], 'medical:S01')
        self.assertEqual(parent['sources'][0]['qualified_id'], 'medical:S01')
        self.assertEqual(parent['text_range']['char_end'], 1000)
        self.assertEqual(parent['evidence_status'], 'not_appraised_by_search')

    def test_natural_question_phrase_and_curated_russian_inflection(self):
        found = searcher.search(self.root, 'How should I interpret child asthma?')['results'][0]
        self.assertEqual(found['heading'], 'Asthma')
        query = '\u041a\u0430\u043a \u043f\u043e\u043d\u044f\u0442\u044c \u0434\u0435\u0442\u0441\u043a\u043e\u0439 \u0430\u0441\u0442\u043c\u044b'
        found = searcher.search(self.root, query)['results'][0]
        self.assertEqual(found['heading'], 'Asthma')
        self.assertTrue(found['unmatched_terms'])
        self.write('44_INTERVAL.md', '# Uncertainty\nA confidence interval has a sampling interpretation.\n')
        self.save('knowledge/search-aliases.json', {'groups': [['confidence interval', '\u0434\u043e\u0432\u0435\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b']]})
        query = '\u041a\u0430\u043a \u043f\u043e\u043d\u044f\u0442\u044c \u0434\u043e\u0432\u0435\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b?'
        self.assertEqual(searcher.search(self.root, query)['results'][0]['canonical_path'], 'knowledge/44_INTERVAL.md')

    def test_bibliography_is_distinct_and_source_lookup_never_fetches_content(self):
        self.write('45_SOURCE_LIST.md', '# Source register\nChild asthma asthma asthma source title.\n')
        rows = searcher.search(self.root, 'child asthma', limit=20)['results']
        self.assertEqual(rows[0]['result_type'], 'project_note')
        self.assertEqual(next(x for x in rows if x['heading']=='Source register')['result_type'], 'bibliographic_navigation')
        record = searcher.lookup_source(self.root, 'medical:S01')
        self.assertEqual(record['result_type'], 'bibliographic_metadata')
        self.assertFalse(record['external_content_fetched'])
        self.assertEqual(record['source']['rights_status'], 'restricted')
        with self.assertRaises(ValueError):
            searcher.lookup_source(self.root, 'S01')
        with self.assertRaises(ValueError):
            searcher.lookup_source(self.root, 'psychology:S01')

    def test_foreign_database_never_modified_and_bad_map_rejected(self):
        index = Path(self.temp.name) / 'unrelated.sqlite'
        with closing(sqlite3.connect(index)) as conn:
            conn.execute('CREATE TABLE sections(id TEXT)')
            conn.execute('INSERT INTO sections VALUES ("keep")')
            conn.commit()
        original = index.read_bytes()
        for operation in [searcher.build_index, searcher.status]:
            with self.assertRaisesRegex(ValueError, 'unrelated'):
                operation(self.root, index)
        self.assertEqual(index.read_bytes(), original)
        with closing(sqlite3.connect(index)) as conn:
            self.assertEqual(conn.execute('SELECT id FROM sections').fetchone(), ('keep',))
        installed = Path(self.temp.name) / 'mapped'
        installed.mkdir()
        (installed / 'note.md').write_text('# Safe\nText', encoding='utf-8')
        for canonical in ['knowledge/../bad.md', 'knowledge/part\\bad.md', 'knowledge/C:bad.md', '/knowledge/bad.md']:
            (installed / 'knowledge-search-map.json').write_text(json.dumps({'entries': [{'canonical_path': canonical, 'local_path': 'note.md'}]}), encoding='utf-8')
            with self.assertRaises(ValueError):
                searcher.status(installed)

    def test_host_translation_fusion_preserves_queries_and_bounds(self):
        query = '\u043d\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u0430\u044f \u0444\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u043e\u0432\u043a\u0430'
        result = searcher.search(self.root, query, alternate_queries=['child asthma'])
        self.assertEqual(result['queries'], [query, 'child asthma'])
        self.assertFalse(result['translation_generated_by_helper'])
        self.assertEqual(result['results'][0]['heading'], 'Asthma')
        self.assertEqual(result['results'][0]['matched_query_indices'], [1])
        self.assertLessEqual(len(result['results']), 5)
        with self.assertRaises(ValueError):
            searcher.search(self.root, query, limit=21, alternate_queries=['child asthma'])
        with self.assertRaises(ValueError):
            searcher.search(self.root, query, alternate_queries=['a', 'b', 'c'])



    def test_navigation_and_russian_phrase_inflection_do_not_bury_contents(self):
        self.write('00_INDEX.md', '# Index\n## Studied question packets\nTable of contents of studied question packets.\n')
        self.write('46_DETAIL.md', '# Detail\nStudied question packets in a long unrelated detail.\n')
        self.save('knowledge/search-aliases.json', {'groups': [
            ['studied question', '\u0438\u0437\u0443\u0447\u0435\u043d\u043d\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b'],
            ['table of contents', '\u043e\u0433\u043b\u0430\u0432\u043b\u0435\u043d\u0438\u0435']]})
        query = '\u0413\u0434\u0435 \u043e\u0433\u043b\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0438\u0437\u0443\u0447\u0435\u043d\u043d\u044b\u0445 \u0432\u043e\u043f\u0440\u043e\u0441\u043e\u0432'
        result = searcher.search(self.root, query)
        self.assertEqual(result['results'][0]['canonical_path'], 'knowledge/00_INDEX.md')
        self.assertTrue(any(c['expanded'] and 'studied question' in c['variants'] for c in result['query_concepts']))
        self.assertEqual(searcher.search(self.root, 'child asthma')['results'][0]['heading'], 'Asthma')

    def test_catalog_active_use_limit_survives_bounded_source_summary(self):
        self.save('knowledge/source-catalog.json', {'records': [{'qualified_id':'medical:S01',
            'url':'https://restricted.example/page','active_use':'bibliographic_only',
            'reading_status':'historical selected reading'}]})
        result=searcher.search(self.root,'asthma')['results'][0]
        self.assertEqual(result['sources'][0]['active_use'],'bibliographic_only')
        self.assertFalse(result['sources'][0]['permission_inferred'])

if __name__ == '__main__':
    unittest.main()
