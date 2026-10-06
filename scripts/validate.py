"""Local packaging/content checks. This is not medical or platform certification."""
import csv
import datetime
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from sync_references import MAP, expected

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {'plugin.json', 'LICENSE', 'NOTICE.md', 'PRIVACY.md', 'TERMS.md'}
TEXT_SUFFIXES = {'.md', '.json', '.csv', '.py', '.yaml', '.yml', '.svg', '.txt'}
SKIP_DIRS = {'.git', 'dist', '__pycache__', '.venv'}


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
    files = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        require(not path.is_symlink(), f'Symlink forbidden: {rel}')
        if path.is_file():
            files.append(rel)
    return sorted(files)


def plugin_files(root=ROOT):
    result = []
    for rel in source_files(root):
        p = rel.as_posix()
        if p in ROOT_FILES or p.startswith('skills/') or p.startswith('assets/'):
            require(rel.suffix in TEXT_SUFFIXES or p == 'LICENSE', f'Unexpected plugin file: {p}')
            require(not any(part.startswith('.') for part in rel.parts), f'Hidden plugin file: {p}')
            result.append(rel)
    return result


def validate(root=ROOT):
    files = source_files(root)
    paths = {p.as_posix() for p in files}
    manifest = json.loads((root / 'plugin.json').read_text())
    check_manifest(manifest, paths)
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
            allowed = i.filename in ROOT_FILES or (p.parts and p.parts[0] in {'skills', 'assets'})
            require(allowed, 'Unexpected archive member')
            require(not any(part.startswith('.') for part in p.parts), 'Hidden archive member')
            text = z.read(i).decode('utf-8')
            privacy_check(text, p)
            if p.suffix == '.md':
                relative_links(text, i.filename, set(names))
            if '.template.' in p.name and p.suffix == '.json':
                check_blank(json.loads(text), p)
        manifest = json.loads(z.read('plugin.json'))
        check_manifest(manifest, set(names))
        skills = {p.split('/')[1] for p in names if p.startswith('skills/') and p.endswith('/SKILL.md')}
        require(skills == set(MAP), 'Wrong archive skills')
        require(z.testzip() is None, 'Corrupt archive')


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
