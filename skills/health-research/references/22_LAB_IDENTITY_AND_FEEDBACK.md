# Laboratory identity, multilingual grouping and owner feedback

Checked 2026-10-07. Scope: adult private report archives and cautious result explanation. Read module 16 for clinical literacy and modules 20-21 for storage. This module supplies a workflow, not a terminology dataset, clinical qualification, validated diagnostic algorithm or automatic account integration. General examples below are vocabulary examples, never patient results.

## Identify the test before interpreting the number

LOINC identifies an observation through component, property, timing, system/sample, scale and, when relevant, method. Analyte spelling alone cannot establish identity. Preserve fasting/challenge conditions, fractions and molecular targets when stated. A panel title is not an individual result. A formal LOINC code requires checking the actual term against available source context; missing axes stay unknown. [S137]

The method axis distinguishes clinically significant method classes. It need not split every routine test by instrument. Retain the source method even when a broader display family is useful, and do not declare analytic interchangeability from that family. [S139]

## Three different operations

1. **Translation:** attach a readable label while retaining the literal original. Case folding and spacing cleanup may propose name candidates; fuzzy similarity cannot approve a match.
2. **Display grouping:** place concept-compatible results in one browsing row with source details. Unknown specimen or method must remain explicit in each cell. Label this `display_group_only`; it is not an assertion of formal identity or safe quantitative trending. Source evidence must at least establish the specimen family and exclude incompatible targets/properties.
3. **Quantitative harmonization:** require a checked component, property, specimen, timing/conditions, scale, relevant method and unit transformation. Use a separate reviewed mapping record. Unknown or incompatible fields block quantitative pooling and derived trend conclusions.

If the report does not establish a specimen family, keep the result separate. Do not infer serum from a plausible reference interval. A known blood-biochemistry report with an unspecified exact sample may sit in a clearly labelled blood display family, with the exact specimen still unknown. This is an archive design policy, not a LOINC equivalence claim.

## Bilingual candidates, checked in context

Store owner-specific native spelling aliases in the private configuration; public prose below uses English/Serbian names and transliterations of Russian names. These are original translation candidates, not an exhaustive official dictionary.

| Candidate labels | Common display concept | Required distinction |
|---|---|---|
| Glukoza, glucose, glyukoza | Glucose | Blood versus urine; concentration versus strip result; fasting/challenge context |
| ALT, SGPT, AlAT | Alanine aminotransferase | Activity units and relevant method |
| AST, SGOT, AsAT | Aspartate aminotransferase | Separate from ALT |
| Kreatinin, creatinine, kreatinin | Creatinine | Sample, concentration versus excretion/clearance |
| Urea, mochevina | Urea | Urea is not the same reported quantity as urea nitrogen |
| WBC, Leukociti, leukotsity | Leukocytes | Blood concentration versus urine microscopy |
| RBC, Eritrociti, eritrotsity | Erythrocytes | Sample, concentration versus microscopic field |
| PLT, Trombociti, trombotsity | Platelets | Absolute concentration |
| Neutrofili, neytrofily | Neutrophils | Percentage and absolute concentration remain separate |
| Hemoglobin, gemoglobin | Hemoglobin | Blood concentration and urine strip heme remain separate |
| Hematokrit, gematokrit | Hematocrit | Fraction versus percent; checked conversion |
| TSH, TTG; FT4, free T4 | TSH; free T4 | Keep separate concepts and free versus total hormone |
| HDL holesterol, HDL cholesterol | HDL cholesterol | Keep HDL, LDL, non-HDL and total cholesterol separate |
| Relativna gustina, specific gravity | Urine specific gravity | Preserve method and do not reinterpret as a mass density |

CBC panel prefixes may be removed only as a reviewed, finite naming rule. Sample abbreviations such as `S`, `U`, `eK` or `cK` require the report's legend or a checked laboratory catalogue; no global abbreviation guess is authoritative. Keep special fractions, direct/calculated LDL, high-sensitivity versus routine CRP, assay equations and specimen-specific tests visible. These are implementation safeguards derived from the identity axes. [S137, S139]

## Units and result scales

UCUM is case-sensitive in its usual representation. A readable Cyrillic or local laboratory unit can have a reviewed explicit alias; lowercasing every unit is unsafe. Arbitrary/procedure-defined units cannot be treated as mutually convertible physical quantities. [S133]

Examples of exact dimensional transformations, when the concept is checked: `g/dL -> g/L` multiplies by 10; `L/L -> %` multiplies by 100; `10^3/uL` and `10^9/L` have equal numerical values; `10^6/uL` and `10^12/L` likewise. These follow the prefix and percent definitions. Use decimal arithmetic, store the factor and retain the original. Mass-to-molar conversions additionally require the particular substance; do not apply a universal factor. [S133]

A quantitative inequality remains a bound. Ordinal `1+`, categories and strip bins are not exact continuous measurements. Preserve qualitative tokens and unconfirmed slash/dash notation literally rather than replacing them with zero or a negative result. Do not average several results from one event or turn an interval into its midpoint without a justified, separate derivation. [S138]

## Reading and explaining a result

Verify row alignment and decimal signs, then read the result together with its original unit, reference interval, flags, collection date, laboratory and available context. Reference intervals can differ by laboratory; an out-of-range result is a clue, not a diagnosis by itself. Clinical interpretation also requires history and examination. [S28]

Use module 16's analyte-specific guidance and current primary guidance for consequential clinical questions. Avoid transferring one laboratory's interval to another source. A converted display value must either have a separately identified converted reference or show the original reference with its original units. Do not compare a converted value to an unlabeled raw interval. A printed flag remains a source flag.

## Persistent clarification page

Keep an owner-readable questions page apart from raw system files. Each question needs a stable ID, the ambiguous field, source/page link, exact uncertainty, what the owner can clarify, status and an editable answer. Group repeated uncertainties from one source where possible. Existing answers such as 'I do not remember' are useful evidence; retain them and avoid repeatedly requesting the same answer. Place reconciled accepted or explicitly closed questions in a separate answered section, collapsed by default. Accepted unknowns also belong there. Keep unanswered, pending-review and partial questions visible in the open section. Preserve stable IDs, source links, prior answers, drafts and review outcomes; downloads must include both sections.

For Drive, a private native feedback Sheet can hold durable answers. Preserve existing permissions. Before any regeneration, read answers and bind by question ID, not row number. Update only managed question/context/status columns; retain answer columns, completed questions and their history. New questions append. Do not sort/recreate the file and silently detach answers from questions.

An offline HTML form can keep a browser-local draft and export an answer file. Show a prominent, high-contrast red notice at both the beginning and end: answers are not sent or accepted automatically. Provide working download buttons in both positions. Explain the next step in the user language: transfer the exported file or use the private native feedback Sheet. Never label browser-local persistence as submitted or ingested. After authorized reconciliation, display the saved response and its review outcome, including accepted uncertainty or unresolved fields. Clearly state that a draft is not saved to Drive or the ledger. Provide an actual download/import path; do not promise that a static page writes SQLite. On subsequent authorized work, inspect the feedback file or native Sheet. Append the answer as an owner report with date, source locator and pending review; accept factual corrections through the normal correction chain. A response never silently proves assay equivalence or updates treatment.

## Mapping audit and checks

A private mapping extension can retain mapping run/version, source observation ID, original input digest, component/property/sample/scale/method decisions, canonical display unit, decimal factor, derived value, status, reviewer/date and rationale. Keep canonical source rows and unknown formal codes unchanged. Only finalized, read-back-verified mapping runs may drive views.

Check source-row invariance, one-to-one coverage of eligible observation IDs, duplicate cells, unit factors, detection limits, absent versus zero values, specimen/property collisions and date grouping. Verify native spreadsheet typed values, notes and raw source tabs after writes. Exercise the feedback export, persistence boundaries, answer preservation and unknown question rejection using wholly synthetic records. These checks establish implementation behavior, not clinical validation.

## Reading scope and limits

Sources: LOINC's inspected naming [S137], scale [S138] and method [S139] pages; selected UCUM 2.2 sections [S133]; MedlinePlus result/context guidance [S28]. No full terminology dataset, all laboratory catalogues or complete clinical guidelines were appraised. Do not claim complete laboratory interpretation coverage, trained model weights or clinician approval. Maintainer review is required before releasing the changed general guidance.
