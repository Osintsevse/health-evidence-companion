---
name: health-contribute
description: Prepare general medical knowledge contributions with English content, primary sources, reading status, dates, limitations and maintainer review. Use to add topics, correct sources, extend a skill or prepare a GitHub pull request. Exclude real cases and private health data.
---

# Contribute general knowledge

For feedback-only requests, use `health-feedback` when available, or [the feedback guide](references/feedback.md). Feature/knowledge-gap/prompt issues can precede implementation; do not turn a feedback draft into an unrequested PR.

Reply in the user's language; write package content in English. Read [policy](references/00_KNOWLEDGE_POLICY.md), [contribution guide](references/contributing.md) and [evidence methods](references/evidence-methods.md) and [study-to-PR workflow](references/contribution-workflow.md). Draft with installed references; edit canonical repository knowledge files when in a checkout.

Formulate an independent general question. Never copy a real symptom history, regimen, document or chronology, even with names removed. Collect no patient data/keys. Write original prose with scope, evidence, exceptions, actual reading status, URL/version, check date and uncertainty. Recheck current primary sources.

Use the [treatment-evidence workflow](references/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md) for drug claims. Secondary lists can identify candidates but cannot support a final efficacy classification. Specify indication, outcome, certainty and current guidance. Avoid universal brand/class bans, claims that every weak-evidence product is harmless, or manufacturer funding as the sole exclusion reason.

Add unique entries to canonical `knowledge/sources.json`; regenerate CSV/source map/references with documented scripts. Preserve stable IDs. Update relevant modules and the build map as needed. Do not add incompatible datasets or copyrighted full texts; check code/data/model licenses separately.

Prepare a diff, checks and concise PR draft. Requests such as "add this study and open a PR/merge request" explicitly authorize preparing a branch/fork and submitting its PR using the connected account. Use upstream branch permission or an authorized fork, target the maintainer repository, and never merge or approve it. A summary-only request does not authorize publication. If submission was not requested or the required GitHub tools/permissions are unavailable, provide a reviewable draft and state the missing operation. Follow the study-to-PR workflow; do not collect credentials. Do not claim submission, approval, merge or publication without verification. Clinical changes need substantive maintainer source review; the skill cannot approve itself.

Describe change, evidence and limits without invented clinician review. CI validates files, not medical truth. A source merge does not update installed snapshots: manual users need the next reviewed ZIP and an explicit personal/workspace update. Public directory publication is not the distribution target. Include module 19's disclaimer when the contribution response contains health advice.

Use [source maintenance](references/31_SOURCE_MAINTENANCE.md) and [the learning index](references/27_FOUNDATIONS_AND_LEARNING_INDEX.md) for curriculum expansion and periodic evidence audits. Preserve actual reading depth, rights and remaining gaps.

For psychological dialogue, relationships, sport or cross-domain private sharing, consult [unified routing](references/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md). Select the relevant psyops-* skill when available; keep full psychological notes separate and load only explicitly authorized, selected summaries. Medical archive authorization alone does not grant psychological-journal access.

The [bundled offline source planner](scripts/source_review.py) reads the domain-qualified catalog; use --domain all, medical or psychology. It makes no network requests and does not refresh reading dates. Psychology entries remain in their original richer register and namespace.

For genetic source selection, repeat annotation review or external disclosure, read [genetic evidence and consent](references/37_GENETIC_EVIDENCE_SOURCES_AND_CONSENT.md). Use the bundled offline evidence helper for a public ClinGen cache, gene-level context, same-input annotation comparison and a private minimal transfer plan. No transmission or consent approval is implemented; preserve the owner's exact authorization scope and verify any new recipient before using a separate host adapter.

## Clinical packet review

For substantial clinical additions, use [clinical navigation](references/CLINICAL_INDEX.md) and [resource architecture](references/ARCHITECTURE.md). Maintain task-to-module-to-source-to-evaluation links. Store original bounded guidance with actual reading depth, jurisdiction and remaining uncertainty; do not enlarge source counts by presenting technical URLs as independent clinical evidence.

Review first-aid actions, treatment choices, risk instruments and unit transforms at their applicable population/product/setting. New clinical content needs substantive maintainer and suitable clinical review; software tests and synthetic forward checks do not approve it. Communities and other AI skills can identify research leads but never replace primary evidence.

Before consequential external medical reading or knowledge contribution, consult [source-use policy](references/source-use-policy.json). NICE clinical text requires separately verified AI-use permission; without it keep the link bibliographic and use independent usable primary evidence. Do not bypass restrictions through an indexed excerpt or mirror. Historical source records do not override this current policy. Read [source attribution](references/medical-source-attribution.md) before public export.
