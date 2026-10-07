# General workflows and blank structures

Project procedures, not clinical guidelines. Only blank forms belong here; filled individual outputs and private links belong in a separate authorized archive. See modules 00, 14 and 20.

## Symptom explanation

Explain plausible causes and uncertainty; identify urgent warning signs; state relevant next steps; ask only questions that change the interpretation; provide sources for material clinical claims. Do not assign a final diagnosis. Apply module 19 for safe self-checks, basic recommendations, observation limits and the required short disclaimer. Actual conversations remain outside the corpus.

## Label or prescription explanation

| Product/form | Purpose | Label dose/interval/duration | Exact label URL/date | Interactions or uncertainties | Question for clinician |
|---|---|---|---|---|---|

Do not conclude "safe" with incomplete ingredient/form information. Use module 12 to separate mechanism, consequence, evidence and conditions. "No significant interaction found in consulted sources" differs from "insufficient data".

## Knowledge card

Question -> scope/age/region -> explanation -> benefit/harm -> exceptions -> primary sources/version -> check date -> remaining uncertainty.

## Private episode design

ID, event date, recording date, source, reported symptoms, measurements, explicitly absent findings, established diagnoses separate from hypotheses, prescribed treatment separate from actual use, changes and next contact. A schema alone grants no access; owner-authorized import uses health-record-import and module 20 with available private storage tools.

## Clinician summary design

Main question -> onset/trajectory -> relevant conditions/allergies -> actual medicines -> investigations -> two to four questions. A private system may prepare a minimal Serbian or English version under the owner's authorization.

## Updating a private record

Read current files; add a dated sourced fact; preserve prior entries; update the summary; read back and check for lost text. Explicitly correct rather than silently erase contradictions. This workflow requires a separately authorized private environment.

## New record design

Copy a blank form from `templates/` into private storage, establish owner/access, preserve originals and unknown fields. The general repository never stores a filled copy. Project JSON templates do not claim FHIR compliance.

## Document-to-history workflow

Use module 20: resolve the private archive, preserve received originals, inspect actual image/PDF pages, stage a source-linked extraction, separate results/clinical entries/orders/actual-use events, commit with a private journal and storage readback, then query committed history for charts or questions. Keep ambiguous transcription pending and corrections explicit. The public project does not receive or automatically upload those documents.
