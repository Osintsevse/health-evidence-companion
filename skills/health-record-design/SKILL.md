---
name: health-record-design
description: Design private medical archives and blank forms for source-linked laboratory, visit, prescription and actual medicine-use histories. Use for choosing storage/structure, provenance, reconciliation, corrections and graph-ready data. For actual owner-authorized report import or history retrieval, route to health-record-import; public knowledge contains no patient records.
---

# Private record design

Reply in the user's language. Apply [response limits and the short disclaimer](references/19_SYMPTOM_REASONING_AND_SELF_CARE.md) in every health-facing answer, including follow-ups; do not delay emergency action. Read [policy](references/00_KNOWLEDGE_POLICY.md), [universal rules](references/14_PATIENT_RECORD_RULES.md) and [template guide](references/templates/README.md). Explain or provide a blank form; do not ask for identity, dates of birth, results, personal medicine lists or private document links.

Describe separate owner-controlled storage: summary, physical episodes, psychiatric monitoring, unified medicine history, allergies/reactions, vaccinations, investigations, originals, uncertainties and corrections. Psychotherapy can have independent permissions. This package does not implement storage, consent/access control, encryption or automatic updates.

Explain event/recording dates; reported/documented/inferred information; unknown/explicitly absent findings; prescription/actual use; adverse reaction/allergy. Preserve date precision and units. Empty lists do not establish absence. Old prescriptions do not establish present use.

Use [blank summary](references/templates/patient_card.template.md), [blank archive](references/templates/patient_record.template.json), [blank medicine entry](references/templates/medication_entry.template.json) and [blank episode](references/templates/episode_entry.template.json). Keep public forms blank. These are project JSON structures informed by FHIR concepts, not validated FHIR resources or official charts.

For a Drive-first longitudinal archive, read [document/history workflow](references/20_PRIVATE_DOCUMENT_IMPORT_AND_HISTORY.md) and the [row contract](references/archive_tables.json). Design separate originals, import snapshots/receipts, one accepted-history ledger and derived views; reuse the owner's existing folders. Keep prescribed plans and explicit actual-use events separate. Describe exactly which host tools are required, without claiming the package automatically connects them.

If asked to import, maintain or retrieve an actual record, route to health-record-import with the owner's explicit destination/source authorization and available private storage tools. Do not reject an authorized private task merely because the public repository excludes patient data. Requests to share need explicit recipients. A folder alone does not implement secure record management. Do not claim unseen-chat access or background updates.

Never add records, anonymized real cases or filled templates to source, PRs or releases. Use only explicitly synthetic exercises if examples are necessary.
