"""Copy canonical general material into each installable skill; never ingest user files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = ['knowledge/00_KNOWLEDGE_POLICY.md', 'knowledge/01_SOURCE_MAP.md', 'knowledge/sources.json',
          'knowledge/19_SYMPTOM_REASONING_AND_SELF_CARE.md']
ARCHIVE = ['knowledge/36_PRIVATE_INTAKE_QUEUE.md', 'knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md', 'knowledge/23_MEDICATION_TIMELINES_AND_ARCHIVE_DEFAULTS.md', 'knowledge/22_LAB_IDENTITY_AND_FEEDBACK.md', 'knowledge/20_PRIVATE_DOCUMENT_IMPORT_AND_HISTORY.md', 'knowledge/archive_tables.json', 'knowledge/21_READABLE_ARCHIVE_VIEWS.md']
TEMPLATES = ['knowledge/templates/' + name for name in [
    'README.md', 'patient_card.template.md', 'patient_record.template.json',
    'medication_entry.template.json', 'episode_entry.template.json',
    'archive_config.template.json', 'archive_import.template.json', 'source_document.template.json',
    'lab_result.template.json', 'clinical_entry.template.json', 'medication_order.template.json',
    'medication_use_event.template.json', 'correction_entry.template.json']]
DASHBOARD = ['knowledge/25_LAB_GRAPHS_AND_HEALTH_REVIEW.md']
MAP = {
    'health-explain': COMMON + DASHBOARD + ARCHIVE + [f'knowledge/{name}' for name in [
        '02_PRIMARY_CARE.md', '03_RESPIRATORY.md', '04_MEDICATIONS.md', '05_ALLERGY_SKIN_EYES.md',
        '06_PSYCHIATRY.md', '07_LABS_PREVENTION_METABOLISM.md', '08_MEDICAL_AI.md',
        '09_STUDY_LOG_AND_ROADMAP.md', '10_WORKFLOW_AND_TEMPLATES.md', '11_PHARMACOLOGY_FOUNDATIONS.md',
        '12_DRUG_INTERACTIONS.md', '13_MEDICAL_CURRICULUM.md', '14_PATIENT_RECORD_RULES.md',
        '15_ALLERGOLOGY.md', '16_LABORATORY_LITERACY.md', '17_VACCINATION.md',
        '18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md']],
    'health-medicine-info': COMMON + ['knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md'] + [f'knowledge/{name}' for name in [
        '04_MEDICATIONS.md', '06_PSYCHIATRY.md', '08_MEDICAL_AI.md',
        '11_PHARMACOLOGY_FOUNDATIONS.md', '12_DRUG_INTERACTIONS.md', '15_ALLERGOLOGY.md',
        '18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md']] + ['docs/research/free-medical-tools.md'],
    'health-research': COMMON + ['knowledge/EVIDENCE_METHODS.md', 'knowledge/08_MEDICAL_AI.md',
        'knowledge/15_ALLERGOLOGY.md', 'knowledge/16_LABORATORY_LITERACY.md', 'knowledge/22_LAB_IDENTITY_AND_FEEDBACK.md',
        'knowledge/17_VACCINATION.md', 'knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md',
        'docs/research/free-medical-tools.md'],
    'health-mental-health': COMMON + ['knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md'] + ['knowledge/06_PSYCHIATRY.md', 'knowledge/11_PHARMACOLOGY_FOUNDATIONS.md',
        'knowledge/12_DRUG_INTERACTIONS.md', 'knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md'],
    'health-record-design': COMMON + DASHBOARD + ARCHIVE + ['knowledge/14_PATIENT_RECORD_RULES.md'] + TEMPLATES,
    'health-record-import': COMMON + DASHBOARD + ARCHIVE + ['knowledge/14_PATIENT_RECORD_RULES.md'] + TEMPLATES,
    'health-contribute': COMMON + ['CONTRIBUTING.md', 'docs/contribution-workflow.md', 'knowledge/EVIDENCE_METHODS.md',
        'knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md'],
}


for _name in ['health-explain','health-record-design','health-record-import']:
    MAP[_name]=list(dict.fromkeys(MAP[_name]+DASHBOARD))


EXPANSION = ['knowledge/26_CLINICAL_ROUTING_AND_SCOPE.md', 'knowledge/27_FOUNDATIONS_AND_LEARNING_INDEX.md', 'knowledge/28_SPECIALTY_AND_LIFE_STAGE_ROUTING.md', 'knowledge/29_PREVENTION_NUTRITION_AND_SHARED_DECISIONS.md', 'knowledge/30_PRIVATE_IMAGES_GENETICS_AND_ACTIVITY.md', 'knowledge/31_SOURCE_MAINTENANCE.md', 'knowledge/32_RISK_COMMUNICATION.md']
MAP['health-family-care'] = COMMON + EXPANSION + ['knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md']
MAP['health-prevention'] = COMMON + EXPANSION + ['knowledge/17_VACCINATION.md', 'knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md', 'knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md']
for _skill in ['health-explain', 'health-research', 'health-contribute']:
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + EXPANSION))
for _skill in ['health-medicine-info', 'health-mental-health']:
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + [EXPANSION[0], EXPANSION[2], EXPANSION[6]]))
for _skill in ['health-record-design', 'health-record-import']:
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + [EXPANSION[4]]))


for _skill in ['health-explain', 'health-record-design', 'health-record-import', 'health-research', 'health-contribute', 'health-medicine-info']:
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + ['knowledge/33_GENETIC_PROVIDER_IMPORT.md', 'knowledge/30_PRIVATE_IMAGES_GENETICS_AND_ACTIVITY.md']))

for _skill in ['health-explain','health-record-design','health-record-import','health-research','health-contribute','health-medicine-info']:
    MAP[_skill]=list(dict.fromkeys(MAP[_skill]+['knowledge/34_GENETIC_ANNOTATION_AND_INTERPRETATION.md','docs/genetic-analysis-workflow.md']))


PSYCHOLOGY_FILES = ["00_COMMON_INDEX.md","01_EVIDENCE_MAP.md","02_ETHICS_AND_DIALOGUE.md","03_CBT_ACT_WORKFLOW.md","04_RELATIONSHIPS.md","05_SEXUALITY.md","06_MEANING_MORTALITY_TIME.md","07_TOOLBOX.md","08_RISK_AND_REFERRAL.md","09_AI_EVIDENCE_AND_TOOLKITS.md","10_RESEARCH_AND_MAINTENANCE.md","12_SESSION_TEMPLATES.md","13_START_INSTRUCTIONS.md","14_FOUNDATIONS.md","15_MODERN_APPROACHES.md","16_AUTO_ROUTING.md","17_COUPLE_FAMILY_APPROACHES.md","18_JOINT_CONVERSATION_PROTOCOL.md","19_PREVENTIVE_CHECKIN.md","20_DATA_BOUNDARIES.md","21_SHARING_GUIDE.md","22_GLOBAL_AND_CULTURAL_CONTEXT.md","23_SPORT_PSYCHOLOGY.md","24_MOTORSPORT_PRACTICES.md","25_SPORT_PRACTITIONER_PROTOCOL.md","26_HELPING_COMPETENCIES.md","27_CBT_SYSTEM.md","28_ACT_SYSTEM.md","29_MCT_AND_MODERN_EVIDENCE.md","30_EVIDENCE_TRIAGE.md","31_MOTORSPORT_CONSULTING.md","32_OUTCOMES_AND_REVIEW.md","33_ASSESSMENT_AND_REFERRAL.md","34_PSYCHOLOGY_CURRICULUM.md","CHANGELOG.md","QUALITY_REVIEW.md","SOURCES.md","sources.json"]
PSYCHOLOGY_SKILLS = ["psyops-dialogue","psyops-cbt-act-mct","psyops-sport","psyops-relationships","psyops-research","psyops-private-records"]
UNIFIED = ['knowledge/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md']
for _skill in list(MAP):
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + UNIFIED))
for _skill in PSYCHOLOGY_SKILLS:
    MAP[_skill] = UNIFIED + ['knowledge/psychology/' + name for name in PSYCHOLOGY_FILES]
for _skill in ['psyops-private-records', 'psyops-sport']:
    MAP[_skill] += ['knowledge/psychology/templates/session-review.blank.json', 'knowledge/psychology/templates/sport-review.blank.json']
for _skill in ['health-research','health-contribute']:
    MAP[_skill] += ['knowledge/psychology/SOURCES.md','knowledge/psychology/sources.json','knowledge/source-catalog.json']

for _skill in ['health-record-import','psyops-private-records']:
    MAP[_skill] += ['docs/private-record-sharing.md']

for _skill, _sources in MAP.items():
    if 'knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md' in _sources:
        MAP[_skill] = list(dict.fromkeys(_sources + ['knowledge/36_PRIVATE_INTAKE_QUEUE.md']))

def destination(source):
    if source.startswith('knowledge/psychology/'):
        return 'psychology/' + source[len('knowledge/psychology/'):]
    if source.startswith('knowledge/templates/'):
        return 'templates/' + Path(source).name
    return {'CONTRIBUTING.md': 'contributing.md', 'EVIDENCE_METHODS.md': 'evidence-methods.md'}.get(Path(source).name, Path(source).name)


for _skill in ['health-record-import','health-record-design','health-research','health-contribute','health-explain','health-medicine-info']:
    MAP[_skill] += ['knowledge/37_GENETIC_EVIDENCE_SOURCES_AND_CONSENT.md']



CLINICAL_TOPICS = ['EMERGENCY','MEDICINES','NUTRITION','ANATOMY','CHRONIC','NEURO',
                   'SYMPTOMS','DIAGNOSTICS','NAVIGATION','AGEING_REHAB','ENDOMETRIOSIS','ARCHITECTURE',
                   'PEDIATRICS','PEDIATRIC_CARE','FONTANELS']
CLINICAL_PACK = ['knowledge/clinical/'+name+'.md' for name in CLINICAL_TOPICS] + [
    'knowledge/clinical/CLINICAL_INDEX.md','knowledge/clinical/navigation.json',
    'knowledge/clinical/routes.json','knowledge/clinical/source-review.json',
    'knowledge/clinical/intake-question-bank.json','knowledge/clinical/terminology.json',
    'knowledge/clinical/source-use-policy.json','docs/medical-source-attribution.md',
    'knowledge/53_TREATMENT_OUTCOMES_AND_DIAGNOSTIC_REASONING.md']
for _skill in ['health-first-aid','health-nutrition','health-care-navigation','health-history-intake']:
    MAP[_skill] = COMMON + ['knowledge/26_CLINICAL_ROUTING_AND_SCOPE.md',
        'knowledge/32_RISK_COMMUNICATION.md','knowledge/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md']
for _skill in MAP:
    if _skill.startswith('health-'):
        MAP[_skill] = list(dict.fromkeys(MAP[_skill] + CLINICAL_PACK))

MAP['health-feedback'] = ['docs/feedback.md']
MAP['health-contribute'] += ['docs/feedback.md']

for _skill in ['health-explain','health-record-design','health-record-import','health-research','health-contribute']:
    MAP[_skill] += ['knowledge/38_BLOOD_PRESSURE_AND_MEASUREMENT.md']


GROUNDED_SKILLS = ['health-explain', 'health-research', 'health-contribute',
                   'health-family-care', 'health-medicine-info',
                   'health-prevention', 'health-mental-health',
                   'health-nutrition', 'health-care-navigation',
                   'psyops-dialogue', 'psyops-research', 'psyops-cbt-act-mct', 'psyops-sport']
GROUNDED_REFERENCES = ['knowledge/54_MODELS_STRATEGIES_AND_IRON_MARKERS.md', 'knowledge/53_TREATMENT_OUTCOMES_AND_DIAGNOSTIC_REASONING.md', 'knowledge/52_DETECTION_OUTCOMES_AND_ATTENTION.md', 'knowledge/51_METHODS_POPULATIONS_AND_FOLLOWUP.md', 'knowledge/50_MEASUREMENTS_MODELS_AND_TRANSFER.md', 'knowledge/49_INFLAMMATION_ENERGY_AND_HEADACHE.md', 'knowledge/48_CELLULAR_AND_RENAL_FOUNDATIONS.md', 'knowledge/46_EXERCISE_VISION_AND_SCALP.md', 'knowledge/47_TICKS_AND_SNAKEBITES.md', 'knowledge/44_LABS_BP_ALLERGY_CHILDREN.md', 'knowledge/45_PSYCHOLOGICAL_METHODS_AND_OUTCOMES.md', 'knowledge/43_EVIDENCE_SLEEP_AGEING_REPRODUCTIVE.md', 'knowledge/42_STUDIED_QUESTIONS.md', 'knowledge/40_BROAD_HEALTH_LEARNING_MAP.md', 'knowledge/41_EVERYDAY_HEALTH_NOTES.md',
    'knowledge/39_GROUNDED_REASONING.md', 'knowledge/EVIDENCE_METHODS.md',
    'knowledge/27_FOUNDATIONS_AND_LEARNING_INDEX.md', 'knowledge/31_SOURCE_MAINTENANCE.md',
    'knowledge/15_ALLERGOLOGY.md', 'knowledge/clinical/ENDOMETRIOSIS.md',
    'knowledge/clinical/source-use-policy.json', 'knowledge/sources.json',
    'knowledge/psychology/14_FOUNDATIONS.md', 'knowledge/psychology/30_EVIDENCE_TRIAGE.md',
    'knowledge/psychology/sources.json']
for _skill in GROUNDED_SKILLS:
    MAP[_skill] = list(dict.fromkeys(MAP[_skill] + GROUNDED_REFERENCES))

# Bounded bite notes are available to first aid without the full research pack.
MAP['health-first-aid'] += ['knowledge/41_EVERYDAY_HEALTH_NOTES.md', 'knowledge/47_TICKS_AND_SNAKEBITES.md']

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
    helper=root/'skills/health-contribute/scripts/source_review.py'
    helper.parent.mkdir(parents=True,exist_ok=True)
    helper.write_bytes((root/'scripts/source_review.py').read_bytes())
    psychology_helper=root/'skills/psyops-private-records/scripts/psychology_records.py'
    psychology_helper.parent.mkdir(parents=True,exist_ok=True)
    psychology_helper.write_bytes((root/'skills/health-record-import/scripts/psychology_records.py').read_bytes())
    print(f'Synchronized {len(wanted)} reference files for {len(MAP)} skills.')


if __name__ == '__main__':
    sync()
