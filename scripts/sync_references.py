"""Copy canonical general material into each installable skill; never ingest user files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = ['knowledge/00_KNOWLEDGE_POLICY.md', 'knowledge/01_SOURCE_MAP.md', 'knowledge/sources.json']
MAP = {
    'health-explain': COMMON + [f'knowledge/{name}' for name in [
        '02_PRIMARY_CARE.md', '03_RESPIRATORY.md', '04_MEDICATIONS.md', '05_ALLERGY_SKIN_EYES.md',
        '06_PSYCHIATRY.md', '07_LABS_PREVENTION_METABOLISM.md', '08_MEDICAL_AI.md',
        '09_STUDY_LOG_AND_ROADMAP.md', '10_WORKFLOW_AND_TEMPLATES.md', '11_PHARMACOLOGY_FOUNDATIONS.md',
        '12_DRUG_INTERACTIONS.md', '13_MEDICAL_CURRICULUM.md', '14_PATIENT_RECORD_RULES.md']],
    'health-medicine-info': COMMON + [f'knowledge/{name}' for name in [
        '04_MEDICATIONS.md', '06_PSYCHIATRY.md', '08_MEDICAL_AI.md',
        '11_PHARMACOLOGY_FOUNDATIONS.md', '12_DRUG_INTERACTIONS.md']] + ['docs/research/free-medical-tools.md'],
    'health-research': COMMON + ['knowledge/EVIDENCE_METHODS.md', 'knowledge/08_MEDICAL_AI.md', 'docs/research/free-medical-tools.md'],
    'health-mental-health': COMMON + ['knowledge/06_PSYCHIATRY.md', 'knowledge/11_PHARMACOLOGY_FOUNDATIONS.md', 'knowledge/12_DRUG_INTERACTIONS.md'],
    'health-record-design': COMMON + ['knowledge/14_PATIENT_RECORD_RULES.md'] + [
        'knowledge/templates/' + name for name in ['README.md', 'patient_card.template.md',
        'patient_record.template.json', 'medication_entry.template.json', 'episode_entry.template.json']],
    'health-contribute': COMMON + ['CONTRIBUTING.md', 'knowledge/EVIDENCE_METHODS.md'],
}


def destination(source):
    if source.startswith('knowledge/templates/'):
        return 'templates/' + Path(source).name
    return {'CONTRIBUTING.md': 'contributing.md', 'EVIDENCE_METHODS.md': 'evidence-methods.md'}.get(Path(source).name, Path(source).name)


def expected(root=ROOT):
    return {Path('skills') / skill / 'references' / destination(src): (root / src).read_bytes()
            for skill, sources in MAP.items() for src in sources}


def sync(root=ROOT):
    wanted = expected(root)
    for skill in MAP:
        directory = root / 'skills' / skill / 'references'
        for old in directory.rglob('*'):
            if old.is_file() and old.relative_to(root) not in wanted:
                raise ValueError(f'Unexpected reference; inspect before deletion: {old.relative_to(root)}')
    for rel, data in wanted.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f'Synchronized {len(wanted)} reference files for {len(MAP)} skills.')


if __name__ == '__main__':
    sync()
