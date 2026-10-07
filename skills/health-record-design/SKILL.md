---
name: health-record-design
description: Explain private health archive design using blank templates, provenance, medicine reconciliation, allergy status and corrections. Use for record structure, physical and psychiatric sections, unknown fields and clinician-summary templates. This public skill does not collect, read or write patient records.
---

# Private record design

Reply in the user's language. Apply [response limits and the short disclaimer](references/19_SYMPTOM_REASONING_AND_SELF_CARE.md) in every health-facing answer, including follow-ups; do not delay emergency action. Read [policy](references/00_KNOWLEDGE_POLICY.md), [universal rules](references/14_PATIENT_RECORD_RULES.md) and [template guide](references/templates/README.md). Explain or provide a blank form; do not ask for identity, dates of birth, results, personal medicine lists or private document links.

Describe separate owner-controlled storage: summary, physical episodes, psychiatric monitoring, unified medicine history, allergies/reactions, vaccinations, investigations, originals, uncertainties and corrections. Psychotherapy can have independent permissions. This package does not implement storage, consent/access control, encryption or automatic updates.

Explain event/recording dates; reported/documented/inferred information; unknown/explicitly absent findings; prescription/actual use; adverse reaction/allergy. Preserve date precision and units. Empty lists do not establish absence. Old prescriptions do not establish present use.

Use [blank summary](references/templates/patient_card.template.md), [blank archive](references/templates/patient_record.template.json), [blank medicine entry](references/templates/medication_entry.template.json) and [blank episode](references/templates/episode_entry.template.json). Keep public forms blank. These are project JSON structures informed by FHIR concepts, not validated FHIR resources or official charts.

If asked to import, maintain or share an actual record, explain that this public package supplies design guidance only; such processing needs a separately authorized suitable private environment and privacy review. A folder alone does not implement secure record management. Do not claim unseen-chat access or background updates.

Never add records, anonymized real cases or filled templates to source, PRs or releases. Use only explicitly synthetic exercises if examples are necessary.
