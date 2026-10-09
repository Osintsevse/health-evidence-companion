"""Generate a concise reading index from the reviewed public navigation graph."""
import json
from pathlib import Path
from clinical_navigation import ROOT, validate_clinical


def render(root=ROOT):
    validate_clinical(root)
    navigation=json.loads((root/'knowledge/clinical/navigation.json').read_text(encoding='utf-8'))
    routes=json.loads((root/'knowledge/clinical/routes.json').read_text(encoding='utf-8'))['routes']
    cases=json.loads((root/'evals/medical-expansion/cases.json').read_text(encoding='utf-8'))['cases']
    lines=['# Clinical reading and decision navigation','',
      'Select the smallest relevant section. This is a reference graph for explanation, urgency and source retrieval, not an executable diagnostic or prescribing engine. A current emergency starts with verified lay actions and dispatch before research, photos, questionnaires or archive work.','',
      '## Choose the entry skill','',
      '| Task | Entry skill and reading |','|---|---|',
      '| Current suspected emergency | health-first-aid; [EMERGENCY](EMERGENCY.md) |',
      '| Symptoms and diagnostic questions | health-explain / health-family-care; [SYMPTOMS](SYMPTOMS.md), [DIAGNOSTICS](DIAGNOSTICS.md) |',
      '| Ingredients, prescriptions and therapy choices | health-medicine-info; [MEDICINES](MEDICINES.md); current exact local label and indication guideline |',
      '| Food diary, calories/macros or diet quality | health-nutrition; [NUTRITION](NUTRITION.md); condition-specific exceptions |',
      '| Find appropriate local care | health-care-navigation; [NAVIGATION](NAVIGATION.md); emergency destination follows dispatch |',
      '| Voluntary focused history and dated review | health-history-intake; [DIAGNOSTICS](DIAGNOSTICS.md), [question prompts](intake-question-bank.json) |',
      '| Established disease, pressure/glucose or several conditions | health-explain; [CHRONIC](CHRONIC.md) and the existing care plan |',
      '| Psychiatric medicines, cognition and dementia | health-mental-health; [NEURO](NEURO.md); adult psychological skills retain their separate scope |',
      '| Pelvic pain, endometriosis and fertility | health-family-care; [ENDOMETRIOSIS](ENDOMETRIOSIS.md); new acute symptoms still use emergency triage |',
      '| Function, older age, rehabilitation or massage | health-prevention / health-family-care; [AGEING_REHAB](AGEING_REHAB.md) |','',
      '## Topic, evidence and coverage map','',
      '| Module | Question families | Evidence records / routes / synthetic cases |','|---|---|']
    for topic in navigation['topics']:
        name=Path(topic['module']).name
        lines.append(f'| [{topic["title"]}]({name}) | '+', '.join(topic['keywords'])+
          f' | {len(topic["source_ids"])} / {len(topic["route_ids"])} / {len(topic["evaluation_ids"])} |')
    lines+=['','Counts measure navigation/provenance records, not independent studies, medical completeness or a validated pass rate. Sources may overlap between topics. Reusable synthetic cases are fixtures; executed checks are reported separately.','',
      '## Reading limits and updating','',
      'Use navigation.json for topic-to-skill/source/route/case identifiers; its module field is the canonical repository path and reference_name is the installable reference filename. Use routes.json for minimum context, immediate/next actions, avoidances and escalation; these are informational cards, not autonomous clinical rules. Source IDs refer to the medical namespace.','',
      'Read source-review.json for the actual later reading scope, version/date and rights limits. Historical source IDs and dates remain preserved. Check current primary guidance and the exact product before consequential personal claims; a classification atlas or a portal link cannot establish product safety, dosing or efficacy. Terminology.json stores multilingual discovery aliases, not automatic equivalence or measurement merging.','']
    for topic in navigation['topics']:
        lines += ['### '+topic['title'],'',topic['reading_depth'],'']
        lines += ['- '+limit for limit in topic['coverage_limits']]
        lines += ['']
    lines+=['## Review output','',
      'For a nonurgent review, present the question and coverage, dated source facts, interpretation and uncertainty, priority findings, questions that change the decision, and the next step with timeframe and responsible service/person. A laboratory flag is not automatically a critical result; an explicit critical laboratory notification requires prompt contact even without symptoms. A report must preserve original units/specimen/method and distinguish unknown from absent.','',
      'Explain standard guideline options to prepare a clinician discussion, including the problem each option addresses, required facts, alternatives, meaningful benefits/harms and monitoring. Separate approved use, local access, off-label care and investigational evidence. No disclaimer converts an unverified or unsafe regimen into a supported recommendation.','',
      'Collect only relevant voluntary context. Offer a few adaptive questions in the host question UI if available, otherwise ordinary chat; do not promise universal UI capabilities. A conversation summary does not authorize storing it. Save selected facts only through an already authorized private-record workflow, preserving provenance and uncertainty.','']
    return '\n'.join(lines)


def update(root=ROOT):
    target=root/'knowledge/clinical/CLINICAL_INDEX.md'
    target.write_text(render(root),encoding='utf-8',newline='\n')
    return target

if __name__=='__main__':
    print(update().relative_to(ROOT).as_posix())
