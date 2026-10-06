"""Build deterministic plugin and source ZIPs using an explicit source tree."""
import hashlib
import json
import zipfile
from pathlib import Path

from validate import ROOT, plugin_files, source_files, validate, validate_zip


def archive(root, files, target, prefix=''):
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(files):
            item = zipfile.ZipInfo(prefix + rel.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            z.writestr(item, (root / rel).read_bytes())


def build(root=ROOT, output=None):
    report = validate(root)
    dest = Path(output) if output else root / 'dist'
    dest.mkdir(parents=True, exist_ok=True)
    base = f"health-evidence-companion-{report['version']}"
    plugin = dest / (base + '.zip')
    source = dest / (base + '-source.zip')
    archive(root, plugin_files(root), plugin)
    validate_zip(plugin)
    archive(root, source_files(root), source, prefix='health-evidence-companion/')
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [plugin, source]}
    (dest / 'SHA256SUMS.txt').write_text(''.join(f'{h}  {name}\n' for name, h in hashes.items()))
    report['sha256'] = hashes
    report['plugin_members'] = len(plugin_files(root))
    report['contains_patient_data'] = 'prohibited; heuristic checks and blank-template checks passed, human review still required'
    (dest / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
