# Maintain the evidence library

The canonical inventory is sources.json. The generated source map and CSV are views, not additional independent references. Every retained entry has a stable ID, URL, region, actual reading status, purpose and check date. Modules 27-30 distinguish inspected sections, abstract-only sources, curriculum catalogues and inaccessible candidates.

## Review procedure

1. Start from the clinical question and existing module/source IDs. Do not repeat a whole curriculum audit for a simple question.
2. Check the publisher's current version, replacements, corrections, retractions and search end date of reviews. Confirm population, jurisdiction, intervention and meaningful outcomes. A new website date is not proof that recommendations changed.
3. Read the relevant updated sections. Record actual access: full relevant section, abstract, official indexed excerpt, catalogue only or blocked. A successful HTTP response may be a login/CAPTCHA and does not count as reading.
4. Compare the old and new conclusions, benefits, harms and uncertainty. Update all affected canonical modules and synthetic behavior cases. Preserve disagreement rather than choosing the newest document automatically.
5. Update checked_on only for the source actually inspected; a broken-link attempt must retain the limitation in retrieval_status. Never label an entire book read because its landing page opened.
6. Regenerate the register views and references, run checks, and prepare a general-knowledge PR for substantive review. Do not auto-merge clinical updates. Installed snapshots change only after a reviewed release and explicit update.

## Planning future checks

scripts/source_review.py provides an offline queue for every registered source. Run `python scripts/source_review.py --as-of YYYY-MM-DD --interval-days 90` with the actual review date. It reads public metadata only, performs no network request and never changes checked_on. Its interval is a maintainer planning choice, not a medical freshness guarantee. A source can become outdated before its due date.

Use a shorter review interval for vaccines, recalls, changing local product labels, screening or insurance rules; verify these again at point of use. Review foundational textbooks/lectures by edition and correction triggers rather than claiming daily refresh. Revisit blocked/indexed-only candidates before using them for a new clinical claim.

A practical maintenance cycle is quarterly review of high-impact guidance and unresolved access, annual review of foundations, plus immediate review of known safety alerts or major guideline changes. This is a proposed procedure, not an active scheduled monitor. Only schedule one when the owner explicitly requests it. A monitor should inspect public sources, never the patient's archive, and notify on meaningful change rather than unchanged status.

## What a source supports

Curricula establish teaching scope. Lecture notes and textbooks explain foundations; they do not establish current clinical efficacy. Guidelines provide bounded recommendations, with jurisdiction and evidence quality. A systematic review is not timeless: record its search date, study selection and applicability. Vendor manuals describe formats/features, not clinical validation. Insurance terms describe contractual processes, not clinical necessity.

Maintain chapter-level reading locators and rights notes in original concept cards. Link protected books and recordings; do not copy full text, illustrations, question banks or videos into a retrieval corpus without suitable rights. Public availability does not imply redistribution permission. The repository's MIT license applies only to its original material.

Source refresh must not collect real-user queries, transcripts, genetics or medical records for author feedback. Newly found sources stay general and independent of an actual case.

## Combined-package source domains

The medical and psychology registers retain their original schemas, source IDs, dates and access histories. source-catalog.json provides domain-qualified identifiers and duplicate-URL aliases. The bundled health-contribute source planner can prepare an all-domain or one-domain queue without network access. Its counts are records, not independent studies; transfer does not count as a new source review.
