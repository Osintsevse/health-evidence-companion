---
name: health-contribute
description: Prepare general medical knowledge contributions with English content, primary sources, reading status, dates, limitations and maintainer review. Use to add topics, correct sources, extend a skill or prepare a GitHub pull request. Exclude real cases and private health data.
---

# Contribute general knowledge

Reply in the user's language; write package content in English. Read [policy](references/00_KNOWLEDGE_POLICY.md), [contribution guide](references/contributing.md) and [evidence methods](references/evidence-methods.md) and [study-to-PR workflow](references/contribution-workflow.md). Draft with installed references; edit canonical repository knowledge files when in a checkout.

Formulate an independent general question. Never copy a real symptom history, regimen, document or chronology, even with names removed. Collect no patient data/keys. Write original prose with scope, evidence, exceptions, actual reading status, URL/version, check date and uncertainty. Recheck current primary sources.

Use the [treatment-evidence workflow](references/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md) for drug claims. Secondary lists can identify candidates but cannot support a final efficacy classification. Specify indication, outcome, certainty and current guidance. Avoid universal brand/class bans, claims that every weak-evidence product is harmless, or manufacturer funding as the sole exclusion reason.

Add unique entries to canonical `knowledge/sources.json`; regenerate CSV/source map/references with documented scripts. Preserve stable IDs. Update relevant modules and the build map as needed. Do not add incompatible datasets or copyrighted full texts; check code/data/model licenses separately.

Prepare a diff, checks and concise PR draft. Requests such as "add this study and open a PR/merge request" explicitly authorize preparing a branch/fork and submitting its PR using the connected account. Use upstream branch permission or an authorized fork, target the maintainer repository, and never merge or approve it. A summary-only request does not authorize publication. If submission was not requested or the required GitHub tools/permissions are unavailable, provide a reviewable draft and state the missing operation. Follow the study-to-PR workflow; do not collect credentials. Do not claim submission, approval, merge or publication without verification. Clinical changes need substantive maintainer source review; the skill cannot approve itself.

Describe change, evidence and limits without invented clinician review. CI validates files, not medical truth. A source merge does not update installed snapshots: manual users need the next reviewed ZIP and an explicit personal/workspace update. Public directory publication is not the distribution target. Include module 19's disclaimer when the contribution response contains health advice.
