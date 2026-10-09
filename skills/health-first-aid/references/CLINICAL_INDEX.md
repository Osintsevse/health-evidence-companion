# Clinical reading and decision navigation

Select the smallest relevant section. This is a reference graph for explanation, urgency and source retrieval, not an executable diagnostic or prescribing engine. A current emergency starts with verified lay actions and dispatch before research, photos, questionnaires or archive work.

## Choose the entry skill

| Task | Entry skill and reading |
|---|---|
| Current suspected emergency | health-first-aid; [EMERGENCY](EMERGENCY.md) |
| Symptoms and diagnostic questions | health-explain / health-family-care; [SYMPTOMS](SYMPTOMS.md), [DIAGNOSTICS](DIAGNOSTICS.md) |
| Ingredients, prescriptions and therapy choices | health-medicine-info; [MEDICINES](MEDICINES.md); current exact local label and indication guideline |
| Food diary, calories/macros or diet quality | health-nutrition; [NUTRITION](NUTRITION.md); condition-specific exceptions |
| Find appropriate local care | health-care-navigation; [NAVIGATION](NAVIGATION.md); emergency destination follows dispatch |
| Voluntary focused history and dated review | health-history-intake; [DIAGNOSTICS](DIAGNOSTICS.md), [question prompts](intake-question-bank.json) |
| Established disease, pressure/glucose or several conditions | health-explain; [CHRONIC](CHRONIC.md) and the existing care plan |
| Psychiatric medicines, cognition and dementia | health-mental-health; [NEURO](NEURO.md); adult psychological skills retain their separate scope |
| Child from birth to the fifth birthday | health-family-care; [PEDIATRICS](PEDIATRICS.md), [preventive care and plans](PEDIATRIC_CARE.md), [fontanels/head shape](FONTANELS.md) |
| Pelvic pain, endometriosis and fertility | health-family-care; [ENDOMETRIOSIS](ENDOMETRIOSIS.md); new acute symptoms still use emergency triage |
| Function, older age, rehabilitation or massage | health-prevention / health-family-care; [AGEING_REHAB](AGEING_REHAB.md) |

## Topic, evidence and coverage map

| Module | Question families | Evidence records / routes / synthetic cases |
|---|---|
| [Lay emergencies and first aid](EMERGENCY.md) | stroke/TIA, chest symptoms, CPR/AED, choking, bleeding, anaphylaxis, poisoning, heat/cold | 32 / 15 / 19 |
| [Medicine and therapy class navigation](MEDICINES.md) | classes/mechanisms, exact products, prescription review, errors, monitoring, new therapies | 39 / 10 / 12 |
| [Nutrition and food-diary review](NUTRITION.md) | calories/macros, food labels, LDL/triglycerides, diabetes/renal diets, restricted intake | 19 / 11 / 12 |
| [Anatomy, physiology and disease families](ANATOMY.md) | organ networks, disease mechanisms, sex/life stages, ancestry, measurement bias | 20 / 7 / 12 |
| [Chronic conditions and multimorbidity](CHRONIC.md) | blood pressure, diabetes/insulin plans, asthma/COPD, CKD, vascular disease, care plans | 25 / 11 / 14 |
| [Neuropsychiatry and dementia](NEURO.md) | brain physiology, psychiatry, withdrawal, delirium, Alzheimer, antiamyloid/biomarkers | 27 / 8 / 14 |
| [Symptom and specialty entry cards](SYMPTOMS.md) | head/chest/abdominal pain, dizziness, GI/urinary, eyes/ENT, skin, trauma/surgery | 34 / 28 / 17 |
| [Tests, reports, history and risk tools](DIAGNOSTICS.md) | blood/urine/stool/semen, pathology, units/assays, critical results, risk scores, anamnesis | 27 / 14 / 16 |
| [Local care and travel assistance](NAVIGATION.md) | current location, service capability, official directories, local language, insurance | 17 / 8 / 12 |
| [Ageing, function and rehabilitation](AGEING_REHAB.md) | frailty/falls, polypharmacy, urology, hair/nails, massage/devices, rehabilitation | 23 / 10 / 13 |
| [Endometriosis, fertility and emerging evidence](ENDOMETRIOSIS.md) | pelvic pain, clinical diagnosis, imaging limits, hormonal/surgical choices, fertility, biomarkers | 27 / 9 / 12 |
| [Learning resources and evidence architecture](ARCHITECTURE.md) | legal textbooks, curricula/CPD, repositories, AI research, decision cards, evaluation design | 26 / 10 / 12 |
| [Under-five illness, urgent care and procedures](PEDIATRICS.md) | birth/newborn, young-infant fever, jaundice, reflux, croup/wheeze, seizures, dehydration/ORS, ear/urine/limb pain, medicine errors, batteries/magnets, pediatric tests and intervals | 37 / 18 / 18 |
| [Well-child care, development and prevention under five](PEDIATRIC_CARE.md) | newborn contacts/screens/results, 2/4/6/9/12/15/18/24/30/36/48 month development, feeding/formula/solids, growth charts, safe sleep/activity/screens, teeth/hearing/vision, toileting, vaccines/catch-up navigation, local plans | 38 / 19 / 19 |
| [Fontanelles, sutures, skull shape and head growth](FONTANELS.md) | anterior/posterior fontanel, closure variation, sutures/craniosynostosis, head circumference, bulging/sunken/pulsation, positional flattening/torticollis, vitamin D, brain/suture ultrasound, CT/MRI/referral/surgery | 25 / 11 / 12 |

Counts measure navigation/provenance records, not independent studies, medical completeness or a validated pass rate. Sources may overlap between topics. Reusable synthetic cases are fixtures; executed checks are reported separately.

## Reading limits and updating

Use navigation.json for topic-to-skill/source/route/case identifiers; its module field is the canonical repository path and reference_name is the installable reference filename. Use routes.json for minimum context, immediate/next actions, avoidances and escalation; these are informational cards, not autonomous clinical rules. Source IDs refer to the medical namespace.

Read source-review.json for the actual later reading scope, version/date and rights limits. Historical source IDs and dates remain preserved. Check current primary guidance and the exact product before consequential personal claims; a classification atlas or a portal link cannot establish product safety, dosing or efficacy. Terminology.json stores multilingual discovery aliases, not automatic equivalence or measurement merging.

### Lay emergencies and first aid

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Selected verified lay actions; no professional resuscitation, neonatal birth algorithm or invasive care.
- Regional paediatric sequences and rescue devices differ; live dispatch/current local training takes precedence.

### Medicine and therapy class navigation

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- 87-row foundational classification/navigation atlas; every exact product/indication still requires current label/guideline retrieval.
- Selected label examples and guideline excerpts do not establish an exhaustive formulary or a cleared personal regimen.

### Nutrition and food-diary review

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Diary estimates require actual portions/preparation/label definitions; missing intake is not zero.
- Therapeutic, paediatric, pregnancy, renal and eating-disorder plans require matching professional guidance.

### Anatomy, physiology and disease families

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Typical major structures and representative disease families; no complete surgical/cellular atlas or all-organ screening.
- Some standard foundational synthesis is broader than selected educational sections; targeted source supplementation is required for granular claims.

### Chronic conditions and multimorbidity

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Monitoring and care-plan navigation, not chat initiation/titration of prescription or insulin regimens.
- Pressure targets/urgency differ by population, measurement setting and jurisdiction.

### Neuropsychiatry and dementia

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- No psychiatric or dementia diagnosis from a questionnaire, medicine response or genotype.
- Novel therapy and biomarker status must be refreshed for exact market/product/lot; trial benefit is not a cure.

### Symptom and specialty entry cards

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Representative entry cards cannot rule out every disease or replace examination.
- Normal consumer readings/photos and earlier benign hypotheses do not clear changing danger signs.

### Tests, reports, history and risk tools

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Marker and name discovery does not authorize broad panels, automatic result merging or universal critical cutoffs.
- Risk tools require their verified version, eligible population, original implementation and rights; no recreated clinical calculators.

### Local care and travel assistance

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Directories/maps support discovery; current capability, hours, destination and payment still need verification.
- Time-critical help precedes insurance, language filtering, ratings or travel logistics.

### Ageing, function and rehabilitation

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Function and rehabilitation information does not confer procedure clearance or manual/device training.
- Massage/device claims remain indication-specific; serious new symptoms take priority.

### Endometriosis, fertility and emerging evidence

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Targeted deep review, not a systematic review, universal cure, local-stock claim or personal prescription.
- Selected trials/abstracts, regulatory differences and unresolved fertility/long-term/population evidence limits remain explicit.

### Learning resources and evidence architecture

Original targeted synthesis; actual section/abstract/indexed access, versions and rights are in source-review.json. Full courses and exhaustive evidence appraisal are not claimed.

- Indexed curricula/chapters are not completed medical training or a freely redistributable corpus.
- Repository/community/AI demonstrations are discovery leads, not validated clinical evidence or code to execute automatically.

### Under-five illness, urgent care and procedures

Original targeted synthesis excluding sources with explicit unverified AI-use restrictions. Source-review.json records actual page/section/abstract/indexed access, versions, jurisdiction, rights and remaining limits. No full pediatric course or systematic review is claimed.

- Selected illness and lay-action pathways, not a neonatal hospital protocol or pediatric prescribing engine.
- Young-infant urgency, medicine labels, test intervals and follow-up need matching age and current local guidance.

### Well-child care, development and prevention under five

Original targeted synthesis excluding sources with explicit unverified AI-use restrictions. Source-review.json records actual page/section/abstract/indexed access, versions, jurisdiction, rights and remaining limits. No full pediatric course or systematic review is claimed.

- Original surveillance and planning aids, not a licensed questionnaire, diagnostic milestone score or universal appointment calendar.
- Dated UK/US programme examples are localized; Serbia/Russia calendars, exact products and individual catch-up remain live verification tasks.

### Fontanelles, sutures, skull shape and head growth

Original targeted synthesis excluding sources with explicit unverified AI-use restrictions. Source-review.json records actual page/section/abstract/indexed access, versions, jurisdiction, rights and remaining limits. No full pediatric course or systematic review is claimed.

- Closure distributions describe selected imaging samples; no universal deadline, probability score or photo clearance.
- Head-growth referral thresholds and imaging choices depend on the chart, jurisdiction, indication and specialist expertise.

## Review output

For a nonurgent review, present the question and coverage, dated source facts, interpretation and uncertainty, priority findings, questions that change the decision, and the next step with timeframe and responsible service/person. A laboratory flag is not automatically a critical result; an explicit critical laboratory notification requires prompt contact even without symptoms. A report must preserve original units/specimen/method and distinguish unknown from absent.

Explain standard guideline options to prepare a clinician discussion, including the problem each option addresses, required facts, alternatives, meaningful benefits/harms and monitoring. Separate approved use, local access, off-label care and investigational evidence. No disclaimer converts an unverified or unsafe regimen into a supported recommendation.

Collect only relevant voluntary context. Offer a few adaptive questions in the host question UI if available, otherwise ordinary chat; do not promise universal UI capabilities. A conversation summary does not authorize storing it. Save selected facts only through an already authorized private-record workflow, preserving provenance and uncertainty.
