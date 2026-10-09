"""Check that broken public evidence/routing graphs cannot be packaged."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from clinical_navigation import validate_clinical, UNDER_FIVE_MODULES
from sync_references import CLINICAL_TOPICS

class ClinicalNavigationTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.put('knowledge/sources.json', [{'id': 'S01'}])
        self.put('knowledge/clinical/source-use-policy.json', {'schema': 'external-clinical-source-use-v1', 'permission_assumed': False, 'preserve_bibliographic_history': True, 'rules': [{'id': 'restricted', 'host_suffix': 'nice.org.uk', 'path_prefix': '/', 'action': 'bibliographic_pointer_only', 'verified_permission_available': False, 'basis_urls': ['https://www.nice.org.uk/terms-and-conditions'], 'limits': 'AI permission not verified'}]})
        self.put('knowledge/clinical/intake-question-bank.json', {'schema': 'adaptive-history-question-bank-v1', 'contains_patient_answers': False, 'automatic_storage': False, 'questions': [{'id': 'goal', 'when': 'At start', 'question': 'What is your goal?', 'suggested_answers': [], 'unknown_and_decline_allowed': True}]})
        self.put('knowledge/clinical/terminology.json', {'schema': 'clinical-term-discovery-v1', 'entries': [{'id': 'lab.hb', 'domain': 'laboratory', 'english': ['hemoglobin'], 'serbian_latin': ['hemoglobin'], 'russian': ['hemoglobin alias'], 'limits': 'Discovery only; confirm specimen and original identity'}]})
        topics = []
        for name in CLINICAL_TOPICS:
            module = 'knowledge/clinical/' + name + '.md'
            path = self.root / module
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Original generic reference S01.', encoding='utf-8')
            topics.append({'id': name.lower(), 'module': module, 'skills': ['health-explain'], 'source_ids': ['S01'], 'route_ids': ['route'], 'evaluation_ids': ['case'], 'coverage_limits': ['Reference map only'], 'reading_depth': 'Relevant section only'})
            if name + '.md' in UNDER_FIVE_MODULES:
                topics[-1]['age_scope'] = {'minimum_months': 0, 'maximum_months': 59, 'routing_age': 'chronological'}
        self.put('knowledge/clinical/navigation.json', {'schema': 'clinical-navigation-v1', 'purpose': 'reference_navigation_not_diagnostic_engine', 'topics': topics})
        self.put('knowledge/clinical/routes.json', {'schema': 'clinical-routes-v1', 'routes': [{'id': 'route', 'actions': ['Seek appropriate assessment'], 'avoid': ['Unverified diagnosis'], 'minimum_context': ['Current concern'], 'escalation': ['Deterioration'], 'source_ids': ['S01']}]})
        self.put('evals/medical-expansion/cases.json', {'schema': 'synthetic-clinical-cases-v1', 'synthetic': True, 'model_or_clinical_validation': False, 'cases': [{'id': 'case', 'prompt': 'Fictional scenario', 'criteria': ['Preserve uncertainty'], 'source_ids': ['S01'], 'execution_status': 'not_executed_fixture'}]})
        self.put('knowledge/clinical/source-review.json', {'schema': 'clinical-source-reading-v1', 'records': [{'source_id': 'S01', 'retrieval_status': 'Relevant section read', 'limitations': 'Not the entire source', 'rights': 'Original paraphrase only'}]})

    def put(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value), encoding='utf-8')

    def alter(self, name, edit):
        value = json.loads((self.root / name).read_text(encoding='utf-8'))
        edit(value)
        self.put(name, value)

    def test_corrupted_alias_cannot_silently_ship(self):
        self.alter('knowledge/clinical/terminology.json', lambda d: d['entries'][0].update(russian=['�']))
        with self.assertRaisesRegex(ValueError, 'corrupted clinical alias'):
            validate_clinical(self.root)

    def test_duplicate_alias_id_is_rejected(self):
        self.alter('knowledge/clinical/terminology.json', lambda d: d['entries'].append(d['entries'][0].copy()))
        with self.assertRaisesRegex(ValueError, 'duplicate clinical alias'):
            validate_clinical(self.root)

    def test_stored_answer_cannot_enter_prompt_bank(self):
        self.alter('knowledge/clinical/intake-question-bank.json', lambda d: d['questions'][0].update(answer='Fictional response'))
        with self.assertRaisesRegex(ValueError, 'Populated'):
            validate_clinical(self.root)

    def test_question_bank_cannot_enable_auto_storage(self):
        self.alter('knowledge/clinical/intake-question-bank.json', lambda d: d.update(automatic_storage=True))
        with self.assertRaisesRegex(ValueError, 'no automatic storage'):
            validate_clinical(self.root)

    def test_connected_reference_graph_is_valid(self):
        result = validate_clinical(self.root)
        self.assertEqual(result['clinical_topics'], len(CLINICAL_TOPICS))
        self.assertFalse(result['clinical_validation'])

    def test_source_index_cannot_grant_ai_permission(self):
        self.alter('knowledge/clinical/source-use-policy.json', lambda d: d.update(permission_assumed=True))
        with self.assertRaisesRegex(ValueError, 'must not assume AI'):
            validate_clinical(self.root)

    def test_restricted_source_cannot_guide_new_pediatric_topic(self):
        self.put('knowledge/sources.json', [{'id': 'S01', 'url': 'https://www.nice.org.uk/guidance/example'}])
        with self.assertRaisesRegex(ValueError, 'AI-restricted source'):
            validate_clinical(self.root)

    def test_restricted_source_cannot_hide_only_in_a_route(self):
        self.put('knowledge/sources.json', [{'id': 'S01'}, {'id': 'S02', 'url': 'https://cks.nice.org.uk/example'}])
        self.alter('knowledge/clinical/routes.json', lambda d: d['routes'][0].update(source_ids=['S01', 'S02']))
        with self.assertRaisesRegex(ValueError, 'AI-restricted source'):
            validate_clinical(self.root)

    def test_restricted_source_cannot_hide_only_in_a_fixture(self):
        self.put('knowledge/sources.json', [{'id': 'S01'}, {'id': 'S02', 'url': 'https://www.nice.org.uk/example'}])
        self.alter('evals/medical-expansion/cases.json', lambda d: d['cases'][0].update(source_ids=['S01', 'S02']))
        with self.assertRaisesRegex(ValueError, 'AI-restricted source'):
            validate_clinical(self.root)

    def test_under_five_scope_cannot_omit_infants(self):
        def edit(d):
            next(t for t in d['topics'] if t['module'].endswith('/PEDIATRICS.md'))['age_scope']['minimum_months'] = 12
        self.alter('knowledge/clinical/navigation.json', edit)
        with self.assertRaisesRegex(ValueError, 'include birth'):
            validate_clinical(self.root)

    def test_under_five_scope_includes_last_preschool_months(self):
        def edit(d):
            next(t for t in d['topics'] if t['module'].endswith('/PEDIATRIC_CARE.md'))['age_scope']['maximum_months'] = 48
        self.alter('knowledge/clinical/navigation.json', edit)
        with self.assertRaisesRegex(ValueError, '59 chronological'):
            validate_clinical(self.root)

    def test_developmental_correction_cannot_replace_routing_age(self):
        def edit(d):
            next(t for t in d['topics'] if t['module'].endswith('/FONTANELS.md'))['age_scope']['routing_age'] = 'corrected'
        self.alter('knowledge/clinical/navigation.json', edit)
        with self.assertRaisesRegex(ValueError, 'chronological'):
            validate_clinical(self.root)

    def test_duplicate_module_with_distinct_id_is_rejected(self):
        def edit(d):
            duplicate = d['topics'][0].copy()
            duplicate['id'] = 'duplicate-module'
            d['topics'].append(duplicate)
        self.alter('knowledge/clinical/navigation.json', edit)
        with self.assertRaisesRegex(ValueError, 'Duplicate clinical module'):
            validate_clinical(self.root)

    def test_missing_topic_prevents_silent_loss_of_coverage(self):
        self.alter('knowledge/clinical/navigation.json', lambda d: d['topics'].pop())
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            validate_clinical(self.root)

    def test_dangling_route_is_rejected(self):
        self.alter('knowledge/clinical/navigation.json', lambda d: d['topics'][0].update(route_ids=['missing']))
        with self.assertRaisesRegex(ValueError, 'unknown route'):
            validate_clinical(self.root)

    def test_unknown_evidence_is_rejected(self):
        self.alter('knowledge/clinical/routes.json', lambda d: d['routes'][0].update(source_ids=['S99999']))
        with self.assertRaisesRegex(ValueError, 'route/evidence'):
            validate_clinical(self.root)

    def test_fixture_cannot_claim_executed_model_validation(self):
        self.alter('evals/medical-expansion/cases.json', lambda d: d['cases'][0].update(execution_status='passed'))
        with self.assertRaisesRegex(ValueError, 'impersonate'):
            validate_clinical(self.root)

    def test_rights_and_reading_limits_must_remain_explicit(self):
        self.alter('knowledge/clinical/source-review.json', lambda d: d['records'][0].update(rights=''))
        with self.assertRaisesRegex(ValueError, 'provenance or rights'):
            validate_clinical(self.root)

    def test_no_unresolved_agent_citations_can_ship(self):
        (self.root / 'knowledge/clinical/EMERGENCY.md').write_text('{{SRC:emergency:unresolved}}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unresolved'):
            validate_clinical(self.root)

    def test_clinical_certification_claim_is_rejected(self):
        self.alter('evals/medical-expansion/cases.json', lambda d: d.update(model_or_clinical_validation=True))
        with self.assertRaisesRegex(ValueError, 'must not claim'):
            validate_clinical(self.root)
if __name__ == '__main__':
    unittest.main()
