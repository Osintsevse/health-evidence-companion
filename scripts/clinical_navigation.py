"""Validate the public clinical navigation graph; no patient input or medical decisions."""
import json
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from sync_references import CLINICAL_TOPICS, MAP

ROOT = Path(__file__).resolve().parents[1]
UNDER_FIVE_MODULES = {'PEDIATRICS.md', 'PEDIATRIC_CARE.md', 'FONTANELS.md'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))


def validate_clinical(root=ROOT):
    source_rows = read(root, 'knowledge/sources.json')
    sources = {s['id'] for s in source_rows}
    use_policy = read(root, 'knowledge/clinical/source-use-policy.json')
    require(use_policy.get('schema') == 'external-clinical-source-use-v1' and
            use_policy.get('permission_assumed') is False and
            use_policy.get('preserve_bibliographic_history') is True,
            'Source catalog must not assume AI reuse permission')
    rules = use_policy.get('rules', [])
    require(rules and len({r['id'] for r in rules}) == len(rules) and
            all(r.get('host_suffix') and r.get('path_prefix') and r.get('action') and
                r.get('verified_permission_available') is False and r.get('basis_urls')
                and r.get('limits') for r in rules), 'Missing source-use restriction provenance')
    def restricted(url):
        parsed = urlsplit(url)
        host = (parsed.hostname or '').lower()
        return any((host == r['host_suffix'] or host.endswith('.' + r['host_suffix']))
                   and parsed.path.startswith(r['path_prefix']) for r in rules)
    restricted_ids = {r['id'] for r in source_rows if restricted(r.get('url', ''))}
    navigation = read(root, 'knowledge/clinical/navigation.json')
    routes = read(root, 'knowledge/clinical/routes.json')
    evaluations = read(root, 'evals/medical-expansion/cases.json')
    reviews = read(root, 'knowledge/clinical/source-review.json')
    bank = read(root, 'knowledge/clinical/intake-question-bank.json')
    require(bank.get('schema') == 'adaptive-history-question-bank-v1' and
            bank.get('contains_patient_answers') is False and bank.get('automatic_storage') is False,
            'Question bank must contain prompts only with no automatic storage')
    questions = bank.get('questions', [])
    require(questions and len({q['id'] for q in questions}) == len(questions),
            'Empty or duplicate history question prompts')
    for question in questions:
        require(set(question) == {'id','when','question','suggested_answers','unknown_and_decline_allowed'}
                and question['unknown_and_decline_allowed'] is True,
                'Populated or constrained history question bank')
    terminology = read(root, 'knowledge/clinical/terminology.json')
    require(terminology.get('schema') == 'clinical-term-discovery-v1', 'Unknown clinical alias schema')
    entries = terminology.get('entries', [])
    require(entries and len({entry['id'] for entry in entries}) == len(entries),
            'Empty or duplicate clinical alias')
    for entry in entries:
        require(entry.get('domain') and entry.get('limits') and
                all(isinstance(entry.get(language), list) and entry[language] and
                    all(isinstance(term, str) and term.strip() and '\ufffd' not in term
                        for term in entry[language])
                    for language in ('english', 'serbian_latin', 'russian')),
                'Missing or corrupted clinical alias; aliases do not establish result identity')
    require(navigation.get('schema') == 'clinical-navigation-v1', 'Unknown clinical navigation schema')
    require(navigation.get('purpose') == 'reference_navigation_not_diagnostic_engine',
            'Clinical catalog must preserve informational scope')
    topics = navigation.get('topics', [])
    require({t['module'] for t in topics} == {
        'knowledge/clinical/' + name + '.md' for name in CLINICAL_TOPICS},
        'Clinical coverage map is incomplete')
    require(len(topics) == len(CLINICAL_TOPICS), 'Duplicate clinical module coverage')
    require(len({t['id'] for t in topics}) == len(topics), 'Duplicate clinical topic')
    require(routes.get('schema') == 'clinical-routes-v1', 'Unknown clinical route schema')
    require(evaluations.get('schema') == 'synthetic-clinical-cases-v1' and
            evaluations.get('synthetic') is True and
            evaluations.get('model_or_clinical_validation') is False,
            'Synthetic cases must not claim clinical validation')
    route_rows = routes.get('routes', [])
    case_rows = evaluations.get('cases', [])
    route_ids = {r['id'] for r in route_rows}
    case_ids = {c['id'] for c in case_rows}
    require(len(route_ids) == len(route_rows) and len(case_ids) == len(case_rows),
            'Duplicate clinical route or evaluation')
    require(reviews.get('schema') == 'clinical-source-reading-v1', 'Unknown source reading schema')
    for review in reviews['records']:
        require(review['source_id'] in sources and review.get('retrieval_status') and
                review.get('limitations') and review.get('rights'),
                'Missing clinical source provenance or rights')
    for topic in topics:
        module = topic['module']
        path = PurePosixPath(module)
        require(not path.is_absolute() and '..' not in path.parts and '\\' not in module and ':' not in module,
                'Unsafe clinical module path')
        require((root / module).is_file(), 'Missing clinical module')
        if path.name in UNDER_FIVE_MODULES:
            scope = topic.get('age_scope', {})
            require(scope.get('minimum_months') == 0 and scope.get('maximum_months') == 59
                    and scope.get('routing_age') == 'chronological',
                    'Under-five scope must include birth through 59 chronological months')
        require(topic.get('skills') and set(topic['skills']) <= set(MAP),
                'Clinical topic has no valid skill')
        require(topic.get('source_ids') and set(topic['source_ids']) <= sources,
                'Clinical topic has missing or unknown evidence')
        require(topic.get('route_ids') and set(topic['route_ids']) <= route_ids,
                'Clinical topic has missing or unknown route')
        require(topic.get('evaluation_ids') and set(topic['evaluation_ids']) <= case_ids,
                'Clinical topic has missing or unknown synthetic case')
        if path.name in UNDER_FIVE_MODULES:
            active_ids = set(topic['source_ids'])
            for row in route_rows:
                if row['id'] in topic['route_ids']:
                    active_ids.update(row.get('source_ids', []))
            for row in case_rows:
                if row['id'] in topic['evaluation_ids']:
                    active_ids.update(row.get('source_ids', []))
            require(active_ids.isdisjoint(restricted_ids),
                    'Under-five active evidence includes an AI-restricted source')

        require(topic.get('coverage_limits') and topic.get('reading_depth'),
                'Clinical topic must disclose coverage limits')
        text = (root / module).read_text(encoding='utf-8')
        require('{{SRC:' not in text, 'Unresolved clinical source token')
        for skill in topic['skills']:
            require(module in MAP[skill], 'Clinical topic is not shipped with its skill')
    for route in route_rows:
        require(route.get('actions') and route.get('avoid') and route.get('minimum_context') and
                route.get('escalation') and route.get('source_ids') and
                set(route['source_ids']) <= sources, 'Incomplete clinical route/evidence')
    for case in case_rows:
        require(case.get('prompt') and case.get('criteria') and case.get('source_ids') and
                set(case['source_ids']) <= sources, 'Incomplete clinical evaluation/evidence')
        require(case.get('execution_status') == 'not_executed_fixture',
                'Reusable fixtures must not impersonate executed model tests')
    return {'clinical_topics': len(topics), 'clinical_routes': len(route_rows),
            'synthetic_cases': len(case_rows), 'clinical_validation': False}


if __name__ == '__main__':
    print(json.dumps(validate_clinical(), indent=2))
