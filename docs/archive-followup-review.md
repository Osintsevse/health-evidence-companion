# Archive timeline and history follow-up

General functionality review against version 0.4.3, preserving its incremental-save workflow. The table describes reusable requirements, not an actual record or patient history. Existing source, privacy and medical-response boundaries remain in force.

| Requirement | Status in this contribution |
| --- | --- |
| One reader area, system area and reproducible source-linked exports | Existing modules 20-23 retained |
| Transposed labs, conservative multilingual display families and raw references | Existing modules 16/21/22 retained |
| Date-ordered condition summaries and separate allergies | Existing reader views retained |
| Parsed/original links, previews, explicit answer transfer and collapsed accepted questions | Existing feedback workflow retained |
| Horizontal medication scale, supported bands and care-context topics | Added generic model, local assets and controls |
| Cross-category laboratory graphs, source reference comparisons and separate dated aggregate review | Added module 25 and optional offline components |
| Purposeful optional questions, staleness and local-only AI packet export | Added source-bound assessment rendering and retained feedback acceptance |
| Last-reconciled actual use without prescription/current-state inference | Added optional accepted local reconciliation reader/panel |
| Handwritten historical batches and page/date/duplicate coverage | Added module 20 checklist |
| Confirmed use versus unknown boundaries; archive access versus unknown facts | Added explicit retrieval routing and scope guidance |
| Unclear spoken product names and model-specific care instructions | Added source-verification rules in module 19 |
| Codex, Claude Code and Claude skill upload packages | Existing manifests and packaging retained with updated version |
| Contributions reviewed by the maintainer with no actual records in public | Existing policy and submission workflow retained |

FHIR R4 MedicationStatement's effective time, assertion date, status and information source and the Period boundary notes were rechecked in their selected sections (S85/S140). This is conceptual source grounding for display/reconciliation rules; no FHIR implementation, clinical validation or new treatment claim is introduced.

All reusable fixtures are wholly fictional. New skill-case prompts are a review checklist, not a claim that every case was independently executed by an AI. Deterministic checks and synthetic browser results are recorded below after execution. Native account installation remains untested by this change.

Validation: 143 repository tests passed with two environment-specific Windows symlink checks skipped; eight optional-adapter tests passed. Source, reference, English/privacy, manifest, exact ZIP membership and deterministic package checks passed. Two wholly synthetic browser scenarios verified medication bands/current-use reconciliation and result plots/saved-review rendering/keyboard point selection/date filters/feedback export/mobile chart scrolling, with no JavaScript errors and unchanged synthetic ledgers. The package contains 141 source entries, 120 synchronized references and 158 runtime members. Native cloud account installation and clinical validity were not tested. Maintainer review remains required.
