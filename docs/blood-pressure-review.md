# Blood pressure view contribution review

Implementation decision, 2026-10-09: fix source-local repeated-measurement grouping and add a reusable offline BP view. This contribution implements a general display contract using wholly invented fixtures; it contains no anonymized real records, private locators, transcripts or configuration.

Baseline: public main bef1bdb5e06aa1e4ec4c15104fe8a4d3d5a2673f (0.8.1). Candidate version: 0.8.2. No issue submission, merge, release, clinical approval or installed-copy update is implied.

Changes: deterministic read-only projection, exact bilingual aliases, ambiguous pairing and partial triple preservation; date/time/source table; separate pressure and pulse axes; up/down/lightning markers and full-reading pointer/keyboard details; default All filter; framed collapsed adult guide above the graph. Educational AHA 2025 categories require explicit adult-scope opt-in and exclude ABPM. Source-order spacing is labelled and does not establish chronological intervals or trends.

Evidence: S637 selected sections of AHA 2019 measurement statement, S389 official 2025 guideline summary, S638 NHS test, S391 NHS low pressure, S639 AHA pulse, S388 home instructions and S640 home monitoring. Rechecked selected public guidance 2026-10-09; no full guideline review or device-specific validation. Sources retain their rights; NHS adaptation attribution travels with medical skill references. No NICE clinical content was used for new guidance.

## Reproducible checks

- Core BP tests: `python -m unittest discover -s tests -p test_blood_pressure.py -v`.
- Optional browser: set `BP_BROWSER_NODE` to a Node executable, `BP_PLAYWRIGHT_MODULE` to an installed Playwright module if needed, and optional `BP_BROWSER_CHANNEL` (for example `msedge`); run `python -m unittest discover -s tests -p test_blood_pressure_browser.py -v`. Nothing is downloaded by the test.
- The fixture generator builds five entirely fictional readings plus an unreviewed value and MAP, through the real SQLite-to-view generator, outside the public source tree. It checks the ledger hash before/after. The browser exercises two locales, repeated rows, absent pulse/time/date, pair details from all three markers, shared BP colour versus pulse colour, keyboard activation, filter reset/ABPM time, collapsed guide placement, narrow-screen overflow and preservation of excluded/MAP raw values. HTTP(S) requests are blocked and counted.
- README canonical/reference/manifest checks, complete unit suite, offline adapters and build remain required. Core tests run without Node; an unconfigured optional browser check is explicitly skipped.

## Limits

Synthetic software checks do not establish clinical validity, independent device accuracy or host installation. Suitable clinical and maintainer review are required for the general guide and optional category scheme. All personal archives and any real example code remain outside this contribution. The module transmits no medical records or telemetry. Merge, release and installed updates are separate operations.

## Fresh-context forward check

One fresh-context executing agent read the changed import/explain skills and minimum relevant references, then answered a wholly fictional BP-view/cuff question without an expected-answer rubric or network access. The inspected output kept repeat measurements separate, preserved missing pulse/time/date, avoided classifying ABPM points and universal health scores, explained cuff mechanisms and distinguished a low diastolic component from a historical high systolic component. It did not infer present urgency from the old point. The check identified an exact-date/ordinal-display documentation tension; module 25 now explicitly cross-references the BP source-order exception. This single response is not a benchmark or clinical approval.

## Executed validation, 2026-10-09

On Windows/Python 3.11: 269 main tests, 266 passed and three skipped (two Windows symlink-privilege checks and optional Pillow). The optional Node/Playwright/Edge BP browser test was configured and passed inside that run for English and Russian. Eight offline adapter tests passed separately. All README registry/index/blank-form/reference/platform checks and validation passed. Build 0.8.2 passed ZIP validation; the complete runtime ZIP (875 members) and source ZIP (1,118 members) matched their reviewed allowlists and passed ZIP CRC checks. `git diff --check` passed. Clinical navigation remains 15 topics/189 routes/214 prior synthetic fixtures; these counts do not certify the new medical guide. Main was rechecked at the unchanged baseline before finishing.
