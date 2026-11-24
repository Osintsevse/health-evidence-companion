"""Bounded offline lexical search of packaged project notes (Python stdlib only)."""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
import unicodedata
from pathlib import Path

SCHEMA = 'knowledge-search-v1'
INDEX_ALGORITHM = '2026-10-18.1'
APPLICATION_ID = 1212500785
TOKEN = re.compile(r'[^\W_]+', re.UNICODE)
STOP_WORDS = set('a an the and or not no is are was were be been being do does did can could would should will may might how what which when where why who whom whose with without for from into onto about between of on in at to by as it its this that these those i we you my our your me us find locate explain interpret describe tell show give please start begin bundled packaged note notes module modules medical health information difference differs distinguish mean means'.split())
STOP_WORDS.update('\u043a\u0430\u043a \u0447\u0442\u043e \u0433\u0434\u0435 \u043f\u043e\u0447\u0435\u043c\u0443 \u0437\u0430\u0447\u0435\u043c \u043a\u043e\u0433\u0434\u0430 \u043a\u0430\u043a\u043e\u0439 \u043a\u0430\u043a\u0430\u044f \u043a\u0430\u043a\u0438\u0435 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043b\u0438 \u0436\u0435 \u0431\u044b \u043d\u0435 \u043d\u0438 \u0438 \u0438\u043b\u0438 \u0430 \u043d\u043e \u0432 \u0432\u043e \u043d\u0430 \u043e \u043e\u0431 \u043e\u0442 \u0434\u043e \u0438\u0437 \u0441 \u0441\u043e \u043f\u043e \u0437\u0430 \u0434\u043b\u044f \u043f\u0440\u0438 \u0431\u0435\u0437 \u0443 \u044d\u0442\u043e \u044d\u0442\u043e\u0442 \u044d\u0442\u0430 \u044d\u0442\u0438 \u043c\u043d\u0435 \u043c\u044b \u044f \u0432\u044b \u043e\u043d \u043e\u043d\u0430 \u043c\u043e\u0436\u043d\u043e \u043c\u043e\u0436\u0435\u0442 \u043d\u0443\u0436\u043d\u043e \u043d\u0443\u0436\u0435\u043d \u0435\u0441\u0442\u044c \u0431\u044b\u0442\u044c \u0431\u044b\u043b \u0431\u044b\u043b\u043e \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430 \u043d\u0430\u0439\u0434\u0438 \u043d\u0430\u0439\u0442\u0438 \u043e\u0431\u044a\u044f\u0441\u043d\u0438 \u0440\u0430\u0441\u0441\u043a\u0430\u0436\u0438 \u043f\u043e\u043a\u0430\u0436\u0438 \u043e\u0442\u043b\u0438\u0447\u0438\u0442\u044c \u043e\u0442\u043b\u0438\u0447\u0430\u0435\u0442\u0441\u044f \u043e\u0442\u043b\u0438\u0447\u0430\u044e\u0442\u0441\u044f \u0437\u043d\u0430\u0447\u0438\u0442'.split())
STOP_WORDS.update('check checking verify understand \u043f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043e\u0437\u043d\u0430\u0447\u0430\u0435\u0442'.split())


def _hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _json(path, fallback):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else fallback


def discover_root():
    base = Path(__file__).resolve().parents[1]
    return base / 'references' if (base / 'references/knowledge-search-map.json').exists() else base


def _inputs(root):
    root = Path(root).resolve()
    mapping = root / 'knowledge-search-map.json'
    if mapping.exists():
        data = _json(mapping, {})
        if not isinstance(data, dict) or not isinstance(data.get('entries'), list):
            raise ValueError('Map requires an entries array')
        entries = data['entries']
    else:
        if not (root / 'knowledge/00_KNOWLEDGE_POLICY.md').is_file():
            raise ValueError('Expected canonical plugin root or installed references map')
        entries = [{'canonical_path': p.relative_to(root).as_posix(),
                    'local_path': p.relative_to(root).as_posix()}
                   for p in sorted((root / 'knowledge').rglob('*.md'))
                   if 'templates' not in p.relative_to(root).parts
                   and p.name not in {'01_SOURCE_MAP.md', 'SOURCES.md', 'CHANGELOG.md', 'QUALITY_REVIEW.md'}]
    result = []
    seen = set()
    for item in entries:
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) for k in ['canonical_path', 'local_path']):
            raise ValueError('Map entries require canonical_path and local_path strings')
        canonical = item['canonical_path']
        parts = Path(canonical).parts
        if ('\\' in canonical or ':' in canonical or canonical.startswith('/')
                or not canonical.startswith('knowledge/') or '..' in canonical.split('/')
                or not canonical.endswith('.md') or 'templates' in parts):
            raise ValueError('Map accepts canonical project Markdown notes only')
        path = (root / item['local_path']).resolve()
        if not path.is_relative_to(root) or not path.is_file() or canonical in seen:
            raise ValueError('Invalid, missing or duplicate mapped note')
        seen.add(canonical)
        result.append((canonical, path.read_text(encoding='utf-8')))
    return root, sorted(result)


def _metadata(root, name, default):
    for path in [root / 'knowledge' / name, root / name]:
        if path.exists():
            return _json(path, default)
    return default


def _snapshot(root):
    root, notes = _inputs(root)
    catalog = _metadata(root, 'source-catalog.json', {'records': []})
    policy = _metadata(root, 'clinical/source-use-policy.json', None)
    if policy is None:
        policy = _metadata(root, 'source-use-policy.json', {'rules': []})
    aliases = _metadata(root, 'search-aliases.json', {'groups': []})
    payload = [SCHEMA, INDEX_ALGORITHM, notes, catalog, policy, aliases]
    return root, notes, catalog, policy, aliases, _hash(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def _sections(canonical, body):
    lines = body.splitlines(keepends=True)
    boundaries = [(0, 0, '(preamble)')]
    fence = None
    hierarchy = []
    counts = {}
    for i, line in enumerate(lines):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not line[marker.end():].strip():
                fence = None
            continue
        heading = re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if not fence and heading:
            boundaries.append((i, len(heading.group(1)), heading.group(2)))
    for j, (start, level, title) in enumerate(boundaries):
        end = boundaries[j + 1][0] if j + 1 < len(boundaries) else len(lines)
        text = ''.join(lines[start:end])
        if not text.strip():
            continue
        if level:
            hierarchy = [(n, t) for n, t in hierarchy if n < level] + [(level, title)]
        key = '/'.join(t for _, t in hierarchy) if level else title
        counts[key] = counts.get(key, 0) + 1
        sid = _hash(canonical + '\n' + key + '\n' + str(counts[key]))[:24]
        # Keep exact source line ranges; chunks break at line boundaries.
        chunk_start = start
        length = 0
        chunks = []
        for pos in range(start, end):
            if length and length + len(lines[pos]) > 6000:
                chunks.append((chunk_start, pos))
                chunk_start, length = pos, 0
            length += len(lines[pos])
        chunks.append((chunk_start, end))
        yield {'section_id': sid, 'parent_section_id': None, 'canonical_path': canonical,
               'heading': title, 'heading_path': [t for _, t in hierarchy], 'line_start': start + 1,
               'line_end': end, 'text': text, 'content_sha256': _hash(text), 'kind': 'section'}
        if len(chunks) > 1:
            for number, (a, b) in enumerate(chunks):
                chunk = ''.join(lines[a:b])
                yield {'section_id': sid + ':' + str(number), 'parent_section_id': sid,
                       'canonical_path': canonical, 'heading': title, 'heading_path': [t for _, t in hierarchy],
                       'line_start': a + 1, 'line_end': b, 'text': chunk,
                       'content_sha256': _hash(chunk), 'kind': 'chunk'}


def _connect(snapshot, index_path=None, rebuild=False):
    root, notes, catalog, policy, aliases, fingerprint = snapshot
    if index_path:
        path = Path(index_path).resolve()
        if (root / 'knowledge').exists():
            protected = path.is_relative_to(root) and not path.is_relative_to(root / 'dist')
        else:
            installation = root.parent if (root.parent / 'SKILL.md').exists() else root
            protected = path.is_relative_to(installation)
        if protected:
            raise ValueError('Index must be outside installed skills and source files; use a disposable cache or repository dist')
        existing = path.exists()
    else:
        existing = False
    previous = None
    if existing:
        previous = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
        try:
            if previous.execute('PRAGMA application_id').fetchone()[0] != APPLICATION_ID:
                raise ValueError('Refusing unrelated SQLite database')
            saved = previous.execute('SELECT schema_magic, fingerprint FROM metadata').fetchone()
            if saved is None or saved[0] != SCHEMA:
                raise ValueError('Unrecognized search cache schema')
            if not rebuild:
                if saved[1] != fingerprint:
                    raise ValueError('Stale index; run build explicitly')
                return previous
        except Exception:
            previous.close()
            raise
        previous.close()
    conn = sqlite3.connect(':memory:')
    try:
        conn.executescript('CREATE TABLE metadata(schema_magic TEXT, fingerprint TEXT); CREATE TABLE sections(id TEXT PRIMARY KEY, data TEXT); CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED, heading, body, tokenize="unicode61 remove_diacritics 2");')
        conn.execute(f'PRAGMA application_id={APPLICATION_ID}')
        conn.execute('INSERT INTO metadata VALUES (?,?)', (SCHEMA, fingerprint))
        for canonical, text in notes:
            for section in _sections(canonical, text):
                conn.execute('INSERT INTO sections VALUES (?,?)', (section['section_id'], json.dumps(section, ensure_ascii=False)))
                if section['kind'] == 'chunk' or len(section['text']) <= 6000:
                    conn.execute('INSERT INTO search VALUES (?,?,?)',
                                 (section['section_id'], section['heading'].replace('\u0451', '\u0435').replace('\u0401', '\u0415'),
                                  _lexical_body(section['text']).replace('\u0451', '\u0435').replace('\u0401', '\u0415')))
        conn.commit()
        if index_path:
            handle, temporary = tempfile.mkstemp(prefix='.knowledge-search-', suffix='.sqlite', dir=path.parent)
            os.close(handle)
            try:
                destination = sqlite3.connect(temporary)
                try:
                    conn.backup(destination)
                finally:
                    destination.close()
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return conn
    except Exception:
        conn.close()
        raise


def build_index(root, index_path=None):
    snapshot = _snapshot(root)
    conn = _connect(snapshot, index_path, rebuild=True)
    count = conn.execute('SELECT count(*) FROM sections').fetchone()[0]
    conn.close()
    return {'schema': SCHEMA, 'fingerprint': snapshot[-1], 'sections': count, 'persistent': index_path is not None}


def _tokens(value):
    return TOKEN.findall(unicodedata.normalize('NFKC', value).casefold().replace('\u0451', '\u0435'))


def _lexical_body(text):
    # URL slugs identify a link, not an explanation of its clinical contents.
    return re.sub(r'https?://[^\s<>)]*', '', text)


def _ru_key(word):
    """A bounded suffix heuristic only for matching curated navigation aliases."""
    if not re.fullmatch(r'[\u0430-\u044f]{4,}', word):
        return None
    endings = ('\u044b\u0445','\u0438\u0445','\u044b\u043c','\u0438\u043c','\u0438\u044f\u043c\u0438','\u044f\u043c\u0438','\u0430\u043c\u0438','\u043e\u0433\u043e','\u0435\u043c\u0443','\u043e\u043c\u0443','\u044b\u043c\u0438','\u0438\u043c\u0438','\u0430\u044f','\u044f\u044f','\u044b\u0435','\u0438\u0435','\u044b\u0439','\u0438\u0439','\u043e\u0439','\u043e\u0435','\u0435\u0435','\u0443\u044e','\u044e\u044e','\u0430\u0445','\u044f\u0445','\u043e\u0432','\u0435\u0432','\u043e\u043c','\u0435\u043c','\u0430\u043c','\u044f\u043c','\u0435\u0439','\u0438\u044f','\u0438\u0438','\u0438\u044e','\u044b','\u0438','\u0430','\u044f','\u0443','\u044e','\u0435')
    return next((word[:-len(e)] for e in endings if word.endswith(e) and len(word)-len(e)>=4), word)


def _ru_phrase_key(value):
    words = value.split()
    if not words or not all(re.fullmatch(r'[\u0430-\u044f]+', word) for word in words):
        return None
    return tuple(_ru_key(word) or word for word in words)


def _navigation_requested(query, concepts):
    words = set(_tokens(query))
    variants = {value for concept in concepts for value in concept['variants']}
    if words & {'index','map','routing','catalog','catalogue','contents'} or 'table of contents' in variants:
        return True
    russian = {'\u043e\u0433\u043b\u0430\u0432\u043b\u0435\u043d\u0438\u0435','\u043a\u0430\u0442\u0430\u043b\u043e\u0433','\u043a\u0430\u0440\u0442\u0430','\u043c\u0430\u0440\u0448\u0440\u0443\u0442','\u0443\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c'}
    if any(_ru_key(w) == _ru_key(n) for w in words for n in russian):
        return True
    return bool(words & {'where','\u0433\u0434\u0435'} and variants & {'search','searching','psychology','health'})


def _query_plan(query, aliases):
    if not isinstance(query, str) or len(query) > 500:
        raise ValueError('Query must be at most 500 characters')
    terms = _tokens(query)
    if not terms or len(terms) > 24:
        raise ValueError('Query must contain 1-24 tokens')
    groups = []
    for group in aliases.get('groups', []):
        if not isinstance(group, list) or not 1 <= len(group) <= 32:
            raise ValueError('Alias groups require 1-32 entries')
        if any(not isinstance(v, str) or len(v) > 100 for v in group):
            raise ValueError('Invalid navigation alias')
        groups.append(sorted(set(' '.join(_tokens(v)) for v in group if _tokens(v))))
    ru_groups = [{key for value in values if (key := _ru_phrase_key(value)) is not None} for values in groups]
    concepts, seen = [], set()
    position = 0
    while position < len(terms):
        found, consumed = [], 1
        for size in range(min(5, len(terms) - position), 0, -1):
            phrase = ' '.join(terms[position:position + size])
            phrase_key = _ru_phrase_key(phrase) if size > 1 else None
            found = [i for i, values in enumerate(groups) if phrase in values
                     or (phrase_key is not None and phrase_key in ru_groups[i])]
            if found:
                consumed = size
                break
        term = ' '.join(terms[position:position + consumed])
        position += consumed
        if not found and consumed == 1 and _ru_key(term):
            found = [i for i, values in enumerate(groups)
                     if any(' ' not in v and _ru_key(v) == _ru_key(term) for v in values)]
        if not found and (term in STOP_WORDS or len(term) < 2):
            continue
        key = ('alias', *found) if found else ('literal', term)
        if key in seen:
            continue
        seen.add(key)
        variants = sorted({term, *(v for i in found for v in groups[i])})
        concepts.append({'term': term, 'variants': variants, 'expanded': bool(found)})
    return concepts


def _expression(query, aliases):
    concepts = _query_plan(query, aliases)
    return ' OR '.join('(' + ' OR '.join('"' + v + '"' for v in c['variants']) + ')'
                       for c in concepts) or '"__no_search_terms__"'


def _coverage(section, concepts):
    words = ' ' + ' '.join(_tokens(section['heading'] + '\n' + _lexical_body(section['text']))) + ' '
    matched = [c['term'] for c in concepts if any(' ' + v + ' ' in words for v in c['variants'])]
    return matched, len(matched) / len(concepts) if concepts else 0.0


def _snippet(body, concepts):
    positions = [m.start() for c in concepts for v in c['variants']
                 for m in [re.search(r'(?<!\w)' + re.escape(v) + r'(?!\w)', body, re.I)] if m]
    start = max(0, min(positions) - 100) if positions else 0
    return start, min(len(body), start + 500)


def _provenance(section, snapshot):
    catalog, policy = snapshot[2], snapshot[3]
    records = {r['qualified_id']: r for r in catalog.get('records', [])}
    citation_text = re.sub(r'https?://\S+', '', section['text'])
    ids = set(re.findall(r'\b(?:medical|psychology):S\d+\b', citation_text))
    domain = 'psychology' if section['canonical_path'].startswith('knowledge/psychology/') else 'medical'
    ids.update(domain + ':' + sid for sid in re.findall(r'(?<![:\w])S\d+\b', citation_text))
    sources = []
    from urllib.parse import urlparse
    for sid in sorted(ids):
        record = records.get(sid, {'qualified_id': sid, 'reading_status': 'unknown'})
        parsed = urlparse(record.get('url', ''))
        matches = [rule for rule in policy.get('rules', [])
                   if (parsed.hostname == rule.get('host_suffix') or (parsed.hostname or '').endswith('.' + rule.get('host_suffix', '!')))
                   and parsed.path.startswith(rule.get('path_prefix', '/'))]
        sources.append({**record, 'rights_rules': matches, 'permission_inferred': False,
                        'rights_status': 'restricted' if matches else 'unknown',
                        'citation_scope': 'parent_section; citation presence is not claim support'})
    return sources


def _source_context(conn, section):
    if section['parent_section_id']:
        row = conn.execute('SELECT data FROM sections WHERE id=?', (section['parent_section_id'],)).fetchone()
        return json.loads(row[0])
    return section


def _source_summary(sources):
    summaries = []
    for source in sources[:3]:
        clipped = {}
        shortened = False
        for key, maximum in [('qualified_id', 40), ('title', 200), ('url', 700),
                             ('reading_status', 350), ('active_use', 40), ('limitations', 450), ('checked_on', 30)]:
            if key in source:
                value = str(source[key])
                clipped[key] = value[:maximum]
                shortened |= len(value) > maximum
        clipped.update(rights_status=source['rights_status'],
                       rights_rules=[{'id': rule['id'], 'action': rule.get('action'),
                                      'verified_permission_available': rule.get('verified_permission_available', False)}
                                     for rule in source['rights_rules']],
                       citation_scope=source['citation_scope'], permission_inferred=False,
                       metadata_truncated=shortened, full_metadata_source_id=source['qualified_id'])
        summaries.append(clipped)
    return {'sources': summaries, 'source_count': len(sources),
            'source_ids': [s['qualified_id'] for s in sources[:64]],
            'source_ids_truncated': len(sources) > 64, 'sources_truncated': len(sources) > 3,
            'source_metadata_level': 'bounded summary; use source command for a selected full record'}


def _range(section, text, start, end):
    first = section['line_start'] + text[:start].count('\n')
    last = section['line_start'] + text[:end].count('\n')
    if end > start and text[:end].endswith('\n'):
        last -= 1
    return {'char_start': start, 'char_end': end, 'line_start': first, 'line_end': max(first, last)}


def _search_one(root, query, limit=5, index_path=None):
    if not 1 <= limit <= 20:
        raise ValueError('limit must be 1-20')
    snapshot = _snapshot(root)
    expression = _expression(query, snapshot[4])
    concepts = _query_plan(query, snapshot[4])
    conn = _connect(snapshot, index_path)
    try:
        rows = conn.execute('SELECT id, bm25(search,0,5,1) AS rank FROM search WHERE search MATCH ? ORDER BY rank,id LIMIT 400', (expression,)).fetchall()
        candidates = []
        navigation_intent = _navigation_requested(query, concepts)
        for sid, rank in rows:
            section = json.loads(conn.execute('SELECT data FROM sections WHERE id=?', (sid,)).fetchone()[0])
            matched, coverage = _coverage(section, concepts)
            bibliography = bool(re.search(r'^(?:source register|sources?|references?|bibliograph)', section['heading'], re.I))
            is_navigation = bool(re.search(r'INDEX|CURRICULUM|_MAP', Path(section['canonical_path']).name))
            navigation = not is_navigation if navigation_intent else is_navigation
            heading_coverage = _coverage({**section, 'text': ''}, concepts)[1]
            candidates.append((bibliography, navigation, coverage, heading_coverage, rank, sid, matched, section))
        candidates.sort(key=lambda row: (row[0], row[1], -row[2], -row[3], row[4], row[5]))
        results = []
        seen_parents = set()
        for bibliography, navigation, coverage, heading_coverage, rank, sid, matched, section in candidates:
            parent = section['parent_section_id'] or sid
            if parent in seen_parents:
                continue
            seen_parents.add(parent)
            provenance = _provenance(_source_context(conn, section), snapshot)
            body = section.pop('text')
            start, end = _snippet(body, concepts)
            results.append({**section, 'result_type': 'bibliographic_navigation' if bibliography else 'project_note', 'rank': rank,
                            'matched_terms': matched, 'lexical_coverage': coverage,
                            'unmatched_terms': [c['term'] for c in concepts if c['term'] not in matched],
                            'snippet': body[start:end], 'snippet_truncated': start > 0 or end < len(body),
                            'snippet_range': _range(section, body, start, end),
                            'evidence_status': 'not_appraised_by_search',
                            **_source_summary(provenance), 'reading_status': 'project_note; original-source access is separate'})
            if len(results) == limit:
                break
        return {'schema': SCHEMA, 'query': query, 'query_mode': 'lexical_concept_coverage_with_curated_aliases',
                'query_concepts': concepts, 'candidate_limit': 400,
                'ranking': 'navigation requests prefer indexes; other queries prefer content; then concept/heading coverage and BM25; no evidence confidence score',
                'fingerprint': snapshot[-1], 'results': results, 'permission_inferred': False}
    finally:
        conn.close()


def search(root, query, limit=5, index_path=None, alternate_queries=None):
    if not 1 <= limit <= 20:
        raise ValueError('limit must be 1-20')
    if not alternate_queries:
        return _search_one(root, query, limit, index_path)
    if not isinstance(alternate_queries, list) or len(alternate_queries) > 2:
        raise ValueError('Use at most two host-authored alternate queries')
    if any(not isinstance(value, str) for value in alternate_queries):
        raise ValueError('Alternate queries must be text')
    queries = list(dict.fromkeys([query, *alternate_queries]))
    batches = [_search_one(root, value, 20, index_path) for value in queries]
    if len({batch['fingerprint'] for batch in batches}) != 1:
        raise ValueError('Corpus changed between alternate queries; retry the search')
    fused = {}
    for query_index, batch in enumerate(batches):
        for rank, hit in enumerate(batch['results'], 1):
            identity = hit['parent_section_id'] or hit['section_id']
            entry = fused.setdefault(identity, {'hit': hit, 'score': 0.0, 'indices': [], 'best_rank': rank})
            entry['score'] += 1.0 / (60 + rank)
            entry['indices'].append(query_index)
            if rank < entry['best_rank']:
                entry['hit'], entry['best_rank'] = hit, rank
    ordered = sorted(fused.items(), key=lambda pair: (-pair[1]['score'], pair[0]))[:limit]
    return {'schema': SCHEMA, 'query': query, 'queries': queries,
            'query_mode': 'reciprocal_rank_fusion_of_host_authored_queries',
            'translation_generated_by_helper': False,
            'fingerprint': batches[0]['fingerprint'], 'permission_inferred': False,
            'results': [{**entry['hit'], 'fusion_score': entry['score'],
                         'matched_query_indices': entry['indices']} for _, entry in ordered],
            'ranking': 'RRF with constant 60 over bounded lexical lists; no evidence confidence score'}


def fetch(root, section_id, offset=0, max_chars=12000, index_path=None, expected_sha256=None):
    if not re.fullmatch(r'[a-f0-9]{24}(?::\d+)?', section_id):
        raise ValueError('Invalid section ID')
    if offset < 0 or not 1 <= max_chars <= 20000:
        raise ValueError('Invalid fetch bounds')
    snapshot = _snapshot(root)
    conn = _connect(snapshot, index_path)
    try:
        row = conn.execute('SELECT data FROM sections WHERE id=?', (section_id,)).fetchone()
        if row is None:
            raise ValueError('Unknown section ID')
        section = json.loads(row[0])
        if expected_sha256 is not None and section['content_sha256'] != expected_sha256:
            raise ValueError('Section changed since the search result; search again')
        provenance = _provenance(_source_context(conn, section), snapshot)
        text = section.pop('text')
        if offset > len(text):
            raise ValueError('Offset exceeds section length')
        end = min(len(text), offset + max_chars)
        return {**section, 'schema': SCHEMA, 'text': text[offset:end], 'offset': offset,
                'total_chars': len(text), 'truncated': end < len(text),
                'next_offset': end if end < len(text) else None,
                'text_range': _range(section, text, offset, end),
                'evidence_status': 'not_appraised_by_search',
                **_source_summary(provenance), 'permission_inferred': False}
    finally:
        conn.close()


def lookup_source(root, qualified_id):
    if not re.fullmatch(r'(?:medical|psychology):S\d{2,}', qualified_id):
        raise ValueError('Use an explicit medical:Sxx or psychology:Sxx source ID')
    snapshot = _snapshot(root)
    if not any(r['qualified_id'] == qualified_id for r in snapshot[2].get('records', [])):
        raise ValueError('Unknown source ID')
    source = _provenance({'text': qualified_id, 'canonical_path': 'knowledge/00_KNOWLEDGE_POLICY.md'}, snapshot)[0]
    return {'schema': SCHEMA, 'result_type': 'bibliographic_metadata', 'source': source,
            'external_content_fetched': False, 'evidence_status': 'not_appraised_by_search',
            'permission_inferred': False, 'fingerprint': snapshot[-1]}


def status(root, index_path=None):
    snapshot = _snapshot(root)
    conn = _connect(snapshot, index_path)
    try:
        return {'schema': SCHEMA, 'fingerprint': snapshot[-1], 'notes': len(snapshot[1]),
                'sections': conn.execute('SELECT count(*) FROM sections').fetchone()[0],
                'searchable_units': conn.execute('SELECT count(*) FROM search').fetchone()[0],
                'source_records': len(snapshot[2].get('records', [])), 'permission_inferred': False}
    finally:
        conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=None)
    parser.add_argument('--index', type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build')
    sub.add_parser('status')
    find = sub.add_parser('search')
    find.add_argument('query')
    find.add_argument('--limit', type=int, default=5)
    find.add_argument('--alternate-query', action='append', default=[])
    get = sub.add_parser('fetch')
    get.add_argument('section_id')
    get.add_argument('--offset', type=int, default=0)
    get.add_argument('--max-chars', type=int, default=12000)
    get.add_argument('--expected-sha256')
    source = sub.add_parser('source')
    source.add_argument('qualified_id')
    args = parser.parse_args(argv)
    root = args.root or discover_root()
    try:
        if args.command == 'search':
            result = search(root, args.query, args.limit, args.index, args.alternate_query)
        elif args.command == 'fetch':
            result = fetch(root, args.section_id, args.offset, args.max_chars, args.index, args.expected_sha256)
        elif args.command == 'source':
            result = lookup_source(root, args.qualified_id)
        else:
            result = (build_index if args.command == 'build' else status)(root, args.index)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error, KeyError, TypeError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
