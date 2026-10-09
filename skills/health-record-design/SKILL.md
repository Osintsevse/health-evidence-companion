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

## Readable archive views

For dashboards, vaccination tables, laboratory matrices, reader/system organization and repeatable exports, read [readable-view rules](references/21_READABLE_ARCHIVE_VIEWS.md). Preserve the accepted ledger, older context, raw values, uncertainty and source permissions; keep all actual outputs/configuration private. Save the chosen generation rules and scripts with the owner archive, verify every view, and distinguish a generated snapshot from a correction or current clinical state.

## Laboratory identity and clarification

For multilingual analyte labels, specimen/property distinctions, unit transforms and persistent owner feedback, read [laboratory identity and feedback](references/22_LAB_IDENTITY_AND_FEEDBACK.md). Preserve raw source rows. A browsing family does not establish quantitative comparability. Keep a separate source-linked questions page, retain prior owner answers and accept corrections through reviewed provenance.


For a complete archive or medication timeline, use [default views and timeline rules](references/23_MEDICATION_TIMELINES_AND_ARCHIVE_DEFAULTS.md). Provide the standard reader/system layout and source-linked views without requiring layout coaching. Reconcile whole supplied medicine histories, distinguish orders from actual use, retain explicit non-initiation and unknown dates/doses, and move accepted questions into the collapsed answered section. Use the owner chosen store and available host tools.

For an existing archive, design a small-update path with separate source, ledger and view statuses, stable operation IDs and private verified file hashes. Use [incremental saves and recovery](references/24_INCREMENTAL_ARCHIVE_SAVES.md); complete defaults must not force a full rebuild after every clarification.

For interactive result plots, a substantive aggregate AI review or a purposeful follow-up questionnaire, follow [graphs and health-review rules](references/25_LAB_GRAPHS_AND_HEALTH_REVIEW.md). A reference comparison is not an AI assessment. Save a separately dated source-linked review, retain uncertainty and mark it stale after relevant changes. The offline renderer does not call an AI or make clinical predictions.

For genetic exports, fitness data, symptom photos or radiological images, read [private data and image limits](references/30_PRIVATE_IMAGES_GENETICS_AND_ACTIVITY.md). These are preparation/review workflows, not implemented live connectors or validated diagnostic engines. Never send patient data to the author or public issue tracker.

For consumer genetics preserve provider reports and raw calls as separate source-linked datasets under [provider intake](references/33_GENETIC_PROVIDER_IMPORT.md). The laboratory table is not a universal genotype schema; do not force raw variants into clinical diagnoses or numerical charts.

For psychological dialogue, relationships, sport or cross-domain private sharing, consult [unified routing](references/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md). Select the relevant psyops-* skill when available; keep full psychological notes separate and load only explicitly authorized, selected summaries. Medical archive authorization alone does not grant psychological-journal access.


For a save from a chat without safe accepted-ledger access, read [private intake queues](references/36_PRIVATE_INTAKE_QUEUE.md). Use an authorized private inbox with source/content readback; report queued, ledger-verified and view-verified stages separately. If upload is unavailable, provide a downloadable file and name the remaining manual placement step. Reuse the import skill's bundled `intake_queue.py` and `accept_owner_report.py` in an authorized local host; no wearable, smart home, home server or new ledger is required. Preserve relatives as family reports rather than the owner's diagnoses/allergies.

## History and assessment structure

For the design of a voluntary adaptive intake or dated aggregate review, read [history/test guidance](references/DIAGNOSTICS.md) and [clinical navigation](references/CLINICAL_INDEX.md). Structure symptoms, functioning, actual medicine use, family reports, objective evidence, hypotheses, goals and unresolved questions separately. A form must allow unknown and declined responses; do not encode an empty answer as absence of disease.

Clinical decision-tool names and versions are references, not a license to recreate a score or diagnosis. Source-linked facts and interpretation have different provenance. Keep actual interviews, food diaries, genetic data and reports solely in the owner's authorized private destination.

## Blood pressure and measurement

For BP parameters, manual versus electronic cuffs or requested BP views, read [blood pressure and measurement](references/38_BLOOD_PRESSURE_AND_MEASUREMENT.md). Preserve complete source-local readings and unknown date/time; never guess pairs from repeated same-day components. Colours are optional named adult educational categories, not a universal good/bad health score. Keep pulse separate, show the full pair and source in a tooltip, and distinguish historical observations from present urgency.
