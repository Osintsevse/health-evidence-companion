"""Local packaging/content checks. This is not medical or platform certification."""
import csv
import datetime
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from sync_references import MAP, destination, expected

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {'.codex-plugin/plugin.json', '.claude-plugin/plugin.json', 'plugin.json', 'LICENSE', 'NOTICE.md', 'PRIVACY.md', 'TERMS.md'}
TEXT_SUFFIXES = {'.md', '.json', '.csv', '.py', '.yaml', '.yml', '.svg', '.txt', '.html', '.mjs', '.css'}
SKIP_DIRS = {'.git', 'dist', '__pycache__', '.venv'}
SOURCE_MANIFEST = Path('scripts/source-files.txt')
# Only reviewed, entirely blank Markdown forms may be distributed. A layout
# change requires reviewing the new blank form and updating its digest here.
BLANK_MARKDOWN_SHA256 = {
    'patient_card.template.md': '86b3ebbb738771728466ee92c4c9d424d335464d0b6b4865dcfd2dc918c1ee41',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def privacy_check(text, path):
    # Deliberately heuristic. Never print matched secrets/content in errors.
    patterns = [r'https?://(?:drive\.google\.com|docs\.google\.com)/',
                r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})',
                r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'\bsk-[A-Za-z0-9]{32,}\b', r'sediment://file_[A-Za-z0-9]+']
    require(not any(re.search(p, text) for p in patterns), f'Potential private link or secret in {path}')
    require(not re.search('[\u0400-\u04ff]', text), f'Non-English source content in {path}')


def check_blank(template, path):
    require(template.get('is_blank_template') is True, f'Filled/unmarked template: {path}')
    allowed = {
        'format': 'personal_health_archive', 'schema_version': '1.0',
        'privacy': 'filled_copy_must_be_outside_general_knowledge',
        'reconciliation_status': 'unknown', 'information_status': 'unknown',
        'event_date_precision': 'unknown', 'prescription_status': 'unknown',
        'actual_use_status': 'unknown', 'verification_status': 'unknown',
    }

    def visit(value, key=None):
        if isinstance(value, dict):
            for k, v in value.items():
                visit(v, k)
        elif isinstance(value, list):
            require(value == [], f'Nonempty template list: {path}')
        elif key == 'is_blank_template':
            require(value is True, f'Unmarked template: {path}')
        elif value is not None:
            require(key in allowed and allowed[key] == value, f'Populated template field: {path}')
    visit(template)


def check_blank_markdown(text, path):
    digest = BLANK_MARKDOWN_SHA256.get(PurePosixPath(path).name)
    require(digest is not None, f'Unreviewed Markdown template: {path}')
    # Normalize line endings only, preserving every other character. Never echo
    # the content of a potentially populated form in validation errors.
    normalized = text.replace('\r\n', '\n')
    require(hashlib.sha256(normalized.encode('utf-8')).hexdigest() == digest,
            f'Populated or changed Markdown template: {path}')


def plugin_paths():
    paths = ROOT_FILES | {'skills/health-record-import/scripts/lab_dashboard.py','skills/health-record-import/assets/lab_dashboard_ui.mjs','skills/health-record-import/assets/lab_dashboard.css','skills/health-record-import/scripts/medication_chart.py','skills/health-record-import/scripts/medication_reconciliation.py','skills/health-record-import/assets/medication_chart_ui.mjs','skills/health-record-import/assets/medication_chart.css','skills/health-record-import/scripts/plan_archive_sync.py','assets/icon.svg', 'skills/health-record-import/scripts/generate_views.py', 'skills/health-record-import/scripts/build_labs.mjs', 'skills/health-record-import/scripts/lab_identity.py', 'skills/health-record-import/scripts/document_previews.py', 'skills/health-record-import/scripts/medication_timeline.py', 'skills/health-record-import/scripts/record_feedback.py', 'skills/health-record-import/scripts/collect_feedback.py', 'skills/health-record-import/assets/archive-view.html'}
    for skill, sources in MAP.items():
        paths.update({f'skills/{skill}/SKILL.md', f'skills/{skill}/agents/openai.yaml'})
        paths.update(f'skills/{skill}/references/{destination(src)}' for src in sources)
    return paths


def check_manifest(manifest, paths):
    allowed = {'$schema', 'name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'}
    require(set(manifest) <= allowed, 'Unknown portable manifest field')
    require(set(manifest.get('author', {})) <= {'name', 'email', 'url'}, 'Unknown author field')
    require(all(isinstance(v, str) for v in manifest.get('author', {}).values()), 'Invalid author field type')
    require(all(isinstance(v, dict) for v in manifest.get('extensions', {}).values()), 'Invalid extension type')
    require(all(isinstance(v, str) for v in manifest.get('keywords', [])), 'Invalid keywords')
    require(manifest.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Unsupported schema')
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest.get('name', '')) is not None, 'Invalid plugin name')
    require(len(manifest['name']) <= 64, 'Plugin name too long')
    require(re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')) is not None, 'Invalid release version')
    require(manifest.get('author', {}).get('name'), 'Missing author')
    ext = manifest.get('extensions', {}).get('com.openai', {})
    ui = ext.get('interface', {})
    for key, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)]:
        value = ui.get(key, '')
        require(isinstance(value, str) and value.strip() and len(value) <= limit, f'Invalid listing {key}')
    require(ui.get('category'), 'Missing category')
    prompts = ui.get('defaultPrompt', [])
    require(isinstance(prompts, list) and len(prompts) <= 3 and all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts), 'Invalid prompts')
    for key in ['websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL']:
        u = urlparse(ui.get(key, ''))
        require(u.scheme == 'https' and u.hostname and not u.username and not u.password, f'Invalid public {key}')
    for key in ['composerIcon', 'logo']:
        path = ui.get(key, '')
        require(path.startswith('./') and '..' not in PurePosixPath(path).parts and path[2:] in paths, f'Missing/unsafe {key}')
    onboard = ext.get('onboardingSkill', '')
    require(onboard.startswith('./') and onboard[2:] in paths, 'Missing onboarding skill')
    require('mcpServers' not in manifest and 'apps' not in manifest and 'hooks' not in manifest, 'Unexpected runtime integration')
    require(not any(key in ext for key in ['hooks', 'apps', 'mcpServers']), 'Unexpected extension integration')


def parse_skill(text):
    # Accepted project frontmatter is deliberately small; platform scan is separate.
    require(text.startswith('---\n'), 'Missing skill frontmatter')
    chunks = text.split('---\n', 2)
    require(len(chunks) == 3, 'Unclosed frontmatter')
    fields = {}
    for line in chunks[1].strip().splitlines():
        key, value = line.split(':', 1)
        fields[key.strip()] = value.strip()
    require(set(fields) == {'name', 'description'}, 'Unexpected frontmatter fields')
    require(fields['description'], 'Empty description')
    return fields


def relative_links(text, relative_path, paths):
    for link in re.findall(r'\]\(([^\s)]+)\)', text):
        link = link.split('#')[0]
        if not link or urlparse(link).scheme:
            continue
        require(not link.startswith('/'), f'Absolute file link: {relative_path}')
        resolved = PurePosixPath(relative_path).parent / link
        parts = []
        for part in resolved.parts:
            if part == '..':
                require(parts, f'Escaping link: {relative_path}')
                parts.pop()
            elif part != '.':
                parts.append(part)
        require('/'.join(parts) in paths, f'Missing relative link from {relative_path}: {link}')


def source_files(root=ROOT):
    manifest = root / SOURCE_MANIFEST
    require(not manifest.is_symlink(), f'Symlink forbidden: {SOURCE_MANIFEST}')
    require(manifest.is_file(), 'Missing source-file manifest')
    entries = manifest.read_text(encoding='utf-8').splitlines()
    require(entries and all(entries) and len(entries) == len(set(entries)),
            'Empty/duplicate source-file manifest entry')
    allowed = set()
    for entry in entries:
        rel = PurePosixPath(entry)
        require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in entry
                and ':' not in entry and rel.as_posix() == entry
                and not any(part in SKIP_DIRS for part in rel.parts),
                'Unsafe source-file manifest entry')
        allowed.add(entry)
    require(SOURCE_MANIFEST.as_posix() in allowed, 'Source manifest must list itself')
    files = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        require(not path.is_symlink(), f'Symlink forbidden: {rel}')
        if path.is_file():
            require(rel.as_posix() in allowed, f'Unexpected source file: {rel}')
            files.append(rel)
    require({p.as_posix() for p in files} == allowed, 'Missing allowlisted source file')
    return sorted(files)


def plugin_files(root=ROOT):
    result = []
    allowed = plugin_paths()
    for rel in source_files(root):
        p = rel.as_posix()
        if p in ROOT_FILES or p.startswith('skills/') or p.startswith('assets/'):
            require(p in allowed, f'Unexpected plugin file: {p}')
            require(rel.suffix in TEXT_SUFFIXES or p == 'LICENSE', f'Unexpected plugin file: {p}')
            require(p in {'.codex-plugin/plugin.json','.claude-plugin/plugin.json'} or not any(part.startswith('.') for part in rel.parts), f'Hidden plugin file: {p}')
            result.append(rel)
    require({p.as_posix() for p in result} == allowed, 'Missing plugin file')
    return result


def validate(root=ROOT):
    files = source_files(root)
    paths = {p.as_posix() for p in files}
    manifest = json.loads((root / 'plugin.json').read_text())
    check_manifest(manifest, paths)
    from sync_platforms import expected as platform_expected
    for name,value in platform_expected(root).items():
        require(json.loads((root/name).read_text(encoding='utf8'))==value,'Platform manifest drift: '+name)
    require({p.name for p in (root / 'skills').iterdir() if p.is_dir()} == set(MAP), 'Skill directory/reference map mismatch')
    sources = json.loads((root / 'knowledge/sources.json').read_text())
    require(len(sources) >= 88, 'Original sources were lost')
    ids = [s['id'] for s in sources]
    require(len(ids) == len(set(ids)), 'Duplicate source ID')
    require(len({s['url'] for s in sources}) == len(sources), 'Duplicate source URL')
    require({f'S{i:02d}' for i in range(1, 89)} <= set(ids), 'Missing original source IDs')
    for s in sources:
        require(set(s) == {'id', 'title', 'url', 'region', 'retrieval_status', 'use', 'checked_on'}, 'Invalid source fields')
        require(all(isinstance(v, str) and v.strip() for v in s.values()), 'Empty source field')
        require(re.fullmatch(r'S\d{2,}', s['id']) is not None, 'Invalid source ID')
        require(urlparse(s['url']).scheme == 'https', 'Non-HTTPS source URL')
        datetime.date.fromisoformat(s['checked_on'])
    with (root / 'knowledge/sources.csv').open(newline='') as f:
        require(list(csv.DictReader(f)) == sources, 'CSV differs from canonical JSON')
    for rel, wanted in expected(root).items():
        require((root / rel).is_file() and (root / rel).read_bytes() == wanted, f'Stale/missing generated reference: {rel}')
    actual_refs = {p for p in files if p.parts[0] == 'skills' and len(p.parts) > 2 and p.parts[2] == 'references'}
    require(actual_refs == set(expected(root)), 'Unexpected reference file')
    for name in MAP:
        text = (root / 'skills' / name / 'SKILL.md').read_text()
        require(parse_skill(text)['name'] == name, f'Skill name mismatch: {name}')
        require('TODO' not in text, f'Unfinished skill: {name}')
        require(len(text.splitlines()) <= 500, f'Skill too long: {name}')
    for rel in files:
        if rel.suffix not in TEXT_SUFFIXES and rel.name not in {'LICENSE', 'CODEOWNERS', '.gitignore'}:
            raise ValueError(f'Unexpected binary/source file: {rel}')
        text = (root / rel).read_text(encoding='utf-8')
        privacy_check(text, rel)
        if rel.suffix == '.json':
            data = json.loads(text)
            if '.template.' in rel.name:
                check_blank(data, rel)
        if rel.suffix == '.md':
            if '.template.' in rel.name:
                check_blank_markdown(text, rel.as_posix())
            relative_links(text, rel.as_posix(), paths)
            for source_id in re.findall(r'\bS\d{2,}\b', text):
                require(source_id in ids, f'Unknown source ID {source_id} in {rel}')
    icon = (root / 'assets/icon.svg').read_text()
    require('viewBox="0 0 256 256"' in icon and '<script' not in icon and 'href=' not in icon, 'Invalid/external icon')
    require('pull_request_target:' not in (root / '.github/workflows/ci.yml').read_text(), 'Unsafe PR trigger')
    for name in ['ci.yml', 'release.yml']:
        workflow = (root / '.github/workflows' / name).read_text()
        require(all(re.fullmatch(r'[^@]+@[a-f0-9]{40}', action) for action in re.findall(r'uses: (\S+)', workflow)), f'Unpinned action in {name}')
    installed = {p.as_posix() for p in plugin_files(root)}
    for rel in plugin_files(root):
        if rel.suffix == '.md':
            relative_links((root / rel).read_text(), rel.as_posix(), installed)
    return {'version': manifest['version'], 'skills': len(MAP), 'sources': len(sources), 'source_files': len(files),
            'validation': 'local structure/content checks only; not clinical or platform certification'}


def validate_zip(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'Duplicate archive members')
        require('plugin.json' in names, 'Manifest must be at archive root')
        require(sum(i.file_size for i in z.infolist()) <= 16 * 1024 * 1024, 'Archive exceeds project size limit')
        for i in z.infolist():
            p = PurePosixPath(i.filename)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename, 'Unsafe archive path')
            require(not stat.S_ISLNK(i.external_attr >> 16), 'Archive symlink')
            allowed = i.filename in plugin_paths()
            require(allowed, 'Unexpected archive member')
            require(i.filename in {'.codex-plugin/plugin.json','.claude-plugin/plugin.json'} or not any(part.startswith('.') for part in p.parts), 'Hidden archive member')
            text = z.read(i).decode('utf-8')
            privacy_check(text, p)
            if p.suffix == '.md':
                if '.template.' in p.name:
                    check_blank_markdown(text, i.filename)
                relative_links(text, i.filename, set(names))
            if '.template.' in p.name and p.suffix == '.json':
                check_blank(json.loads(text), p)
        manifest = json.loads(z.read('plugin.json'))
        check_manifest(manifest, set(names))
        skills = {p.split('/')[1] for p in names if p.startswith('skills/') and p.endswith('/SKILL.md')}
        require(skills == set(MAP), 'Wrong archive skills')
        require(set(names) == plugin_paths(), 'Missing plugin archive member')
        require(z.testzip() is None, 'Corrupt archive')


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
