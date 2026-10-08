# Offline graph and health-review adapter

The generator embeds laboratory/measurement plots with source links, checkbox selection across categories, original-name search, private presets, independent axes and date filters. It also renders a separately saved AI assessment and optional follow-up questions. No model API, internet request, automatic feedback submission, clinical score or forecast is implemented.

## Configuration and storage

Use the existing private configuration; all filled values stay outside this repository. Optional keys:

- `lab_presets`: reviewed browsing topics with `label`, `components` and optional `category`.
- `lab_dashboard_default_components` and `lab_default_from`: initial selection/window.
- `lab_dashboard_labels`: localized UI text.
- `lab_reference_overrides`: per accepted observation ID, exact `raw` reference text, nullable `low`/`high`, inclusivity and source/category notes. Review multi-tier wording manually. These limits are not individual treatment targets.
- `health_questionnaire`: existing stable question IDs; questions retain the private feedback workflow.
- `health_review`: an optional privately authored review object with `reviewed_on`, `status`, `summary`, `scope`, `items`, `clinician_questions`, `limitations` and `source_fingerprint`. Each item includes `title`, `finding`, `interpretation`, `action`, accepted `entry_ids` and primary `evidence_urls`.

Alternatively, an existing private SQLite adapter can provide an optional `health_assessments` extension with `review_id`, `record_id`, `recorded_at`, `reviewed_on`, `source_fingerprint`, `status`, and `assessment_json` columns. Only the matching owner and `ai_reviewed` status are read. Preserve versions, and do not treat this status as clinician confirmation. This optional extension does not change the seven accepted-fact table contracts or migrate a database automatically.

The helper fingerprint covers accepted fact tables, current medicine reconciliation/use and archived context. Changes invalidate the saved review. The fingerprint is a staleness check, not authentication or clinical validation. Raw facts and old assessment versions remain separate. Unreviewed or outdated AI text cannot create accepted diagnoses.

## Verification

Use wholly synthetic fixtures for public tests. Verify inequalities stay excluded, partial/invalid dates are not invented, conversions transform reference bounds consistently, ambiguous ranges stay unparsed, source mutations invalidate overrides, duplicate-date observations do not produce a unique delta, and context differences block descriptive joins. Check plots and keyboard point activation, source/original links, date and category filters, mobile scroll, assessment staleness, questionnaire drafts and answer downloads. Hash the ledger before/after view generation.

The source-linked numerical review does not replace a fresh substantive AI review using the relevant health skill. A successful browser/test run verifies implementation behavior, not medical truth. Real patient outputs and screenshots are never public test fixtures.
