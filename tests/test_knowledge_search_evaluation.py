import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import evaluate_knowledge_search as evaluation


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'knowledge').mkdir()
        text = '# Note\n\n## Support\n\nBounded explanation.\n'
        (self.root / 'knowledge/note.md').write_text(text, encoding='utf-8')
        passage = '## Support\n\nBounded explanation.\n'
        self.case = {'id': 'one', 'query': 'question', 'topic_group': 'topic', 'split': 'dev',
                     'category': 'discovery', 'language': 'en', 'primary_metric_eligible': True,
                     'adjudication_status': 'author_adjudicated_from_canonical_text',
                     'evidence': [{'path': 'knowledge/note.md', 'heading': 'Support', 'line': 3,
                                   'line_end': 6, 'text_sha256': hashlib.sha256(passage.encode()).hexdigest()}]}

    def test_changed_passage_fails_before_query(self):
        (self.root / 'knowledge/note.md').write_text('# Note\n\n## Support\n\nChanged.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'hash changed'):
            evaluation.evaluate({'cases': [self.case]}, self.root, None,
                                lambda *a, **k: self.fail('queried before hash verification'))

    def test_unreviewed_cases_are_diagnostic_only(self):
        excluded = dict(self.case, id='two', primary_metric_eligible=False, evidence=[], topic_group='other')
        result = evaluation.evaluate({'cases': [self.case, excluded]}, self.root, None,
                                     lambda *a, **k: {'results': []})
        self.assertEqual(result['overall']['scored_cases'], 1)
        self.assertEqual(result['overall']['excluded_cases'], 1)
        self.assertIsNone(result['rows'][1]['metrics'])
        self.assertEqual(result['overall']['metrics']['module_recall_at_20'], 0)

    def test_module_hit_is_not_passage_hit(self):
        result = {'canonical_path': 'knowledge/note.md', 'heading': 'Other',
                  'heading_path': ['Note', 'Other'], 'line_start': 7, 'line_end': 9}
        scores = evaluation.score(self.case, [result])
        self.assertEqual(scores['module_recall_at_5'], 1)
        self.assertEqual(scores['passage_hit_at_20'], 0)
        result.update(heading='Support', heading_path=['Note', 'Support'], line_start=4, line_end=5)
        self.assertEqual(evaluation.score(self.case, [result])['passage_hit_at_20'], 1)

    def test_topic_split_leakage_rejected(self):
        other = dict(self.case, id='two', split='heldout')
        with self.assertRaisesRegex(ValueError, 'leaks'):
            evaluation.validate_cases({'cases': [self.case, other]}, self.root)

    def test_native_only_ignores_alternates_without_mutating_labels(self):
        case = dict(self.case, alternate_queries=['faithful English query'])
        observed = []
        def search(*args, **kwargs):
            observed.append(kwargs)
            return {'results': []}
        result = evaluation.evaluate({'cases': [case]}, self.root, None, search, use_alternates=False)
        self.assertNotIn('alternate_queries', observed[0])
        self.assertEqual(case['alternate_queries'], ['faithful English query'])
        self.assertEqual(result['query_mode'], 'native_query_only')

    def test_authored_fixture_counts_and_filter(self):
        path = Path(__file__).resolve().parents[1] / 'evals/knowledge-search-cases.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(len(data['cases']), 200)
        self.assertEqual(sum(c['split'] == 'dev' for c in data['cases']), 120)
        self.assertEqual(sum(c['split'] == 'heldout' for c in data['cases']), 80)
        self.assertEqual(sum(c.get('primary_metric_eligible', False) for c in data['cases']), 68)
        self.assertEqual(data['split_visibility'], 'partitioned_not_blinded')


if __name__ == '__main__':
    unittest.main()
