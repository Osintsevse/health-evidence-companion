# Laboratory graphs and aggregate health review

This module governs private derived views. It adds no diagnosis, prescription, monitoring service, validated predictor or patient data to public knowledge. Use modules 20–24 for accepted facts, feedback, source reconciliation and incremental saving. Medical explanations follow module 19 and the relevant clinical skill. [S28]

## Two different outputs

An offline numeric projection can compare a verified result with its own report's reference and show source-linked numerical changes. It must not advertise that comparison as an AI assessment, a diagnosis or a critical alert. A reference interval, a laboratory desirable category and an individualized treatment target are different concepts. Preserve each result's report wording. Unparsed tiered categories remain unassessed unless a reviewed override matches the exact source text. Never choose one convenient interval from a multi-population report. [S28]

A substantive AI review is a separately saved, dated assessment of the aggregate accepted record. Retrieve latest and earlier relevant results, current dated medicine reconciliation, allergies, clinician-recorded conditions, owner-reported symptoms and important gaps. Distinguish facts, interpretation and proposed clinician questions. State coverage, the date of each supporting result, applicable primary sources and actual reading/access status. A contemporary review date does not make old tests contemporary. Give the owner the useful overall conclusions, not just a document catalogue. Do not declare global good health from a normal panel. [S28]

Keep that review separate from original facts and clinician diagnoses. Store a source fingerprint and version; mark it stale after relevant facts or reconciliation change. An `ai_reviewed` storage status identifies a saved AI draft, not approval by a clinician. The optional local generator reads a saved review; it does not call a model or create a review on its own.

## Numerical eligibility and interpretation

Use active rows resolved from committed/read-back imports. An exact point requires a reviewed finite numeric value, equality comparator and genuine complete event date. Do not treat a detection limit as its boundary value, invent a midyear collection date, turn blanks into zero or plot unreadable transcriptions. Retain excluded results and sources beside the graphs. Explicitly reported measurement dates and dates of reports remain distinguishable.

A translated display family is not proof of assay equivalence. Separate specimen, property and incompatible units. Use only reviewed exact conversion factors and transform numeric reference limits with the same factor. Keep the raw result/reference visible. The helper recognizes complete simple intervals and inequalities only; complex source categories need source-reviewed configuration. It is neither a UCUM parser nor a clinical terminology service. [S28]

Show separate aligned time plots with their own labelled units and scales, checkbox selection, original-name search, cross-category choice, date range and useful topic presets. Each point opens raw values, source locator and a separate original-document link. References belong to individual points; do not project the latest interval over all history. Support keyboard selection and horizontal chart scrolling on small screens.

Default to points. Optional exploratory joins require identical known recorded specimen, method and laboratory, and remain explicitly unvalidated. Numerical differences do not establish improvement, worsening, a significant biological change or treatment causality. Unknown or conflicting contexts do not acquire comparability through a name match. Do not fit future values or fabricate disease probabilities. A validated risk instrument requires all inputs and applicable population/setting; otherwise explain the missing inputs and useful next questions. [S28]

Distinguish report flags from actual critical-result notices. Display an explicit urgent laboratory instruction if documented, and route present severe symptoms under module 19. Do not manufacture universal urgent numeric thresholds, use historical flags to announce a present emergency or provide reassurance from absent flags.

## Optional, purposeful questionnaire

Offer a short optional questionnaire only for identifiable gaps relevant to the requested review: current symptoms, recent tests and collection context, relevant medicines/supplements, current blood pressure, nicotine exposure and family history, or measured height/weight/waist and activity context. Explain why each answer helps. Do not request an entire private history or repeat accepted unknowns. Approximate owner measurements remain approximate; a calculated index is a derived value, not a new measurement. BMI has limitations and is not an individual risk verdict; applicable adult guidance may combine it with waist-to-height information. [S141]

Reuse stable private review-question IDs, source links, browser-draft warnings, downloads at both ends and reviewed acceptance. A static HTML file does not automatically submit feedback or save accepted facts. A packet export downloads an aggregate file locally; it does not transmit to an AI. Preserve owner-selected privacy and ask no new sharing permission when none is needed.

Optional helpers under health-record-import: `scripts/lab_dashboard.py`, `assets/lab_dashboard_ui.mjs` and `assets/lab_dashboard.css`. They provide deterministic offline projections and rendering, not interpretation by an autonomous agent. Actual reports, configuration, private packets, assessment versions and QA screenshots stay in the chosen private archive.

## BP source-order exception

The exact-date requirement above applies to quantitative time plots. [Module 38](38_BLOOD_PRESSURE_AND_MEASUREMENT.md) permits a separate, explicitly ordinal blood-pressure display when dates are unknown, partial or unusable. Its x-axis is source order, never calendar time or elapsed duration. This does not relax the dated laboratory graph gate or establish temporal trends.
