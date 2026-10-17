"""Evaluate authored retrieval relevance; never infer clinical validation."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import time

import knowledge_search


def validate_cases(data, root):
    cases = data['cases']
    if len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Duplicate case IDs')
    groups = defaultdict(set)
    for case in cases:
        groups[case['topic_group']].add(case['split'])
        if not case.get('primary_metric_eligible', False):
            continue
        if case.get('adjudication_status') != 'author_adjudicated_from_canonical_text' or not case.get('evidence'):
            raise ValueError('Eligible case requires reviewed evidence: ' + case['id'])
        for evidence in case['evidence']:
            path = (root / evidence['path']).resolve()
            if not path.is_relative_to(root.resolve()):
                raise ValueError('Evidence path escapes corpus')
            text = path.read_text(encoding='utf-8')
            matches = list(re.finditer(r'^(#{1,6}) (.+)$', text, re.M))
            start = next((m for m in matches if m.group(2) == evidence['heading'] and text[:m.start()].count('\n') + 1 == evidence['line']), None)
            if start is None:
                raise ValueError('Evidence heading/line changed: ' + case['id'])
            level = len(start.group(1))
            end = next((m.start() for m in matches if m.start() > start.start() and (level == 1 or len(m.group(1)) <= level)), len(text))
            passage = text[start.start():end]
            if hashlib.sha256(passage.encode('utf-8')).hexdigest() != evidence['text_sha256']:
                raise ValueError('Evidence passage hash changed: ' + case['id'])
            if evidence['line_end'] != evidence['line'] + passage.count('\n'):
                raise ValueError('Evidence end locator changed: ' + case['id'])
    if any(len(splits) != 1 for splits in groups.values()):
        raise ValueError('Topic group leaks across splits')
    return cases


def score(case, results):
    expected = {e['path'] for e in case['evidence']}
    metrics = {}
    for limit in (5, 20):
        found = {r['canonical_path'] for r in results[:limit]}
        metrics['module_recall_at_' + str(limit)] = len(expected & found) / len(expected)
    hits = []
    for rank, result in enumerate(results[:20], 1):
        for evidence in case['evidence']:
            headings = set(result.get('heading_path', [])) | {result.get('heading')}
            # Expected ranges use the exclusive next-line boundary when newline terminated.
            overlap = result['line_start'] < evidence['line_end'] and result['line_end'] >= evidence['line']
            if result['canonical_path'] == evidence['path'] and evidence['heading'] in headings and overlap:
                hits.append(rank)
    metrics['passage_hit_at_20'] = int(bool(hits))
    metrics['first_supporting_passage_rank'] = min(hits) if hits else None
    return metrics


def summarize(rows):
    scored = [r for r in rows if r['primary_metric_eligible']]
    return {
        'cases': len(rows), 'scored_cases': len(scored),
        'excluded_cases': len(rows) - len(scored),
        'errors': sum(r['error'] is not None for r in rows),
        'no_hits': sum(r['result_count'] == 0 and r['error'] is None for r in rows),
        'metrics': {key: sum(r['metrics'][key] for r in scored) / len(scored) if scored else None
                    for key in ('module_recall_at_5', 'module_recall_at_20', 'passage_hit_at_20')},
    }


def evaluate(data, root, index_path, search_function=None, use_alternates=True):
    cases = validate_cases(data, root)
    search_function = search_function or knowledge_search.search
    rows = []
    started = time.perf_counter()
    for case in cases:
        before = time.perf_counter()
        error = None
        try:
            options = {'limit': 20, 'index_path': index_path}
            if use_alternates and case.get('alternate_queries'):
                options['alternate_queries'] = case['alternate_queries']
            results = search_function(root, case['query'], **options)['results']
        except Exception as exc:
            # Do not export exception strings that could expose local filesystem paths.
            error = type(exc).__name__
            results = []
        eligible = case.get('primary_metric_eligible', False)
        rows.append({'id': case['id'], 'split': case['split'], 'category': case['category'],
                     'language': case['language'], 'primary_metric_eligible': eligible,
                     'error': error, 'result_count': len(results),
                     'elapsed_seconds': time.perf_counter() - before,
                     'metrics': score(case, results) if eligible else None,
                     'retrieved': [{'canonical_path': r['canonical_path'], 'heading': r['heading'],
                                    'line_start': r['line_start'], 'line_end': r['line_end']}
                                   for r in results]})
    groups = {}
    for dimension in ('split', 'category', 'language'):
        groups[dimension] = {value: summarize([r for r in rows if r[dimension] == value])
                             for value in sorted({r[dimension] for r in rows})}
    return {'schema': 'knowledge-search-relevance-results-v1',
            'execution_status': 'executed_authored_retrieval_cases',
            'split_visibility': data.get('split_visibility', 'unknown'),
            'clinical_validation': False, 'evidence_hashes_verified_before_queries': True,
            'query_mode': 'host_authored_alternates' if use_alternates and any(c.get('alternate_queries') for c in cases) else 'native_query_only',
            'ndcg': {'reported': False, 'reason': 'Supporting labels are incomplete; no whole-corpus graded relevance gold exists.'},
            'limitations': ['Authored relevance judgments are not independent clinical review.',
                           'Only eligible reviewed cases enter primary metrics; unreviewed cases are diagnostic only.',
                           'Partitioned control questions were visible to authoring agents; no blinded generalization claim.',
                           'No absence accuracy is reported because substantive absence candidates are unadjudicated.',
                           'Errors count as retrieval failures in scored denominators; runtime is descriptive on this machine.',
                           'Source-map exclusions remain scored misses; direct source lookup is a separate interface.'],
            'overall': summarize(rows), 'by': groups,
            'total_elapsed_seconds': time.perf_counter() - started,
            'rows': rows}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--native-only', action='store_true', help='Ignore host-authored alternate queries without changing labels')
    args = parser.parse_args(argv)
    data = json.loads(args.cases.read_text(encoding='utf-8'))
    # Verify labels before building or querying the index.
    validate_cases(data, args.root)
    knowledge_search.build_index(args.root, args.index)
    result = evaluate(data, args.root, args.index, use_alternates=not args.native_only)
    args.output.write_text(json.dumps(result, ensure_ascii=True, indent=2) + '\n', encoding='ascii')
    print(json.dumps(result['overall'], ensure_ascii=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
