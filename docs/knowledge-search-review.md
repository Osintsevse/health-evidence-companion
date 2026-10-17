# Packaged knowledge retrieval and selected methods reading

Prepared 2026-10-17 against version 0.9.0. The change adds local retrieval to the existing knowledge and skills, with one bounded methods extension. It does not claim completion of the private-library study programme.

## Problem and behavior

The package has substantial general notes and independent medical/psychology source registers. Previously, a host had to select the right reference manually; the package had no executable common note search. The new standard-library helper searches canonical notes in a checkout or only the references available in one installed skill. The source distribution retains authored cases and a reproducible relevance runner.

Results expose canonical section/line locators, text hashes, query concept overlap and bounded source metadata. Fetching restores the section or its parent, with explicit partial-read offsets and optional expected-hash verification. Bibliographic sections remain distinct from original notes. Direct qualified-source lookup returns metadata without fetching external text. A policy match accompanies the source; absence of a match remains unknown permission.

Default indexing is ephemeral. Optional recognized caches are rebuilt in a temporary database and replaced only after completion; unrelated databases are refused. The package includes no model, vector database, paid API, external source fetcher, private-book corpus or patient archive. Hosts without Python use the generated canonical-to-local reference map and existing indexes.

## What changed in the skills

Nineteen existing health/psychology skills receive the same helper and guide, their own map, the shared source catalog, policy and navigation vocabulary. The feedback-only skill keeps its existing scope. A skill does not gain files absent from its reference pack; canonical paths and local paths remain separate. First aid explicitly prioritizes immediate actions over search. No new external tool or network integration is introduced.

The vocabulary is an inspectable bilingual navigation aid. Exact source concepts and conditions must still be read. Russian suffix matching is restricted to curated alias entries; related terms do not become clinically interchangeable. URL text is excluded from lexical matching so a link slug cannot stand in for a clinical explanation. Bibliography/general indexes are ranked behind substantive notes unless navigation is requested. Broader multilingual semantic search remains an experiment for a later measured change.

## STAT-F6 actual source reading

The researcher and integrating reviewer read *OpenIntro Statistics*, fourth edition (2019), screen-reader update 2022-10-21, section 7.5.6, printed/PDF pp. 329-331. Both visually inspected p. 330. The exact edition identity matched the previously registered source; three distinct new substantive pages were covered, not six and not an entire chapter or book. The current official [license](https://www.openintro.org/license/) and [terms](https://www.openintro.org/terms/) were inspected before the new bounded reading.

The original short STAT-F6 synthesis distinguishes multiple-comparison context, the global ANOVA question, particular-pair inference and nonrejection versus equality. Its fictional retrieval example supplies no measured performance or universal correction procedure. Source examples, arithmetic, figures, tables, exercises and data are not reproduced. This is not a clinical treatment claim or full statistical training. The source's CC BY-SA terms remain distinct from the repository's MIT license.

Existing psychology:S104 is extended without a new duplicate source ID. The original import pin and previous amendments remain preserved; the current canonical JSON hash is recorded in the amendment ledger. Earlier reading scopes remain historical and do not become whole-book reading. Independent maintainer review is not claimed.

## Evaluation scope

The authored collection contains 200 wholly fictional retrieval questions in 120 development and 80 control-partition cases, grouped by module. It is not blinded: authoring agents could see both partitions. Only 68 cases have reviewed supporting-passage labels; the other 132 are excluded from primary relevance metrics until adjudicated. Category coverage is uneven. No absence accuracy or clinical accuracy follows from these labels.

The runner verifies exact labeled passage hashes before querying, distinguishes module discovery from supporting-passage discovery, retains failures and reports language/category/partition denominators. Incomplete labels do not support a whole-corpus nDCG score. The generated source maps are deliberately outside default prose retrieval; their cases remain recorded misses rather than being relabeled to fit output. Direct source lookup is a separate operation.

The 68 scored cases produced the following observed results. Both runs use the same reviewed passages, corpus and result budget. Host-authored English alternates were prepared from original query text only by an agent without access to labels, module maps or retrieval outputs. They are stored explicitly in the case file; the helper did not generate them.

| Mode | Scored cases | Module recall at 5 | Module recall at 20 | Supporting-passage hit at 20 |
| --- | ---: | ---: | ---: | ---: |
| Original query only | 68 | 48.5% | 55.9% | 48.5% |
| Original plus host-authored alternate | 68 | 69.1% | 80.9% | 75.0% |
| Russian original only | 42 | 28.6% | 33.3% | 26.2% |
| Russian plus English alternate | 42 | 61.9% | 73.8% | 69.0% |
| English original (both modes) | 26 | 80.8% | 92.3% | 84.6% |

There were no execution errors. Zero empty result lists in the alternate-query run is not evidence that every question is answerable. General discovery remains weak: only 2/10 scored discovery questions find the labeled module at 20. Neither applicability nor conflicting-evidence candidates have reviewed supporting labels yet. The visible control partition contains only 18 scored cases; its higher result is not independent validation. Retained failures and denominators are in `evals/knowledge-search-results*.json`.

Reproduce both modes without modifying labels:

```text
python -X utf8 scripts/evaluate_knowledge_search.py --root . --cases evals/knowledge-search-cases.json --index dist/eval.sqlite --output dist/results.json
python -X utf8 scripts/evaluate_knowledge_search.py --root . --cases evals/knowledge-search-cases.json --index dist/eval.sqlite --output dist/results-native.json --native-only
```

Three actual fresh-context agents used installed skills without access to the case labels or repository code. They found and fully fetched selected methods notes, traced a restricted source without treating its catalog record as permission, and answered a Russian statistical-significance question with an explicitly supplied English alternate. Exact command replays and actual responses are in `evals/knowledge-search-forward-checks.json`. The Russian response check depended on the alternate query; the native query alone contributed no top-five result. A short ambiguous medicine query retrieved the wrong sense, which remains a documented failure and motivates query refinement. These authored observations are not independent clinical review.

Structural checks and synthetic responses cannot confer clinical approval. Full-library reading, additional source permissions, semantic/hybrid comparison, broad independent adjudication and clinical applicability review remain later stages.

## Executed technical checks

The isolated worktree passed `scripts/validate.py`, all 303 discovered repository tests (three environment-dependent skips), eight offline adapter tests and `scripts/build.py`. The skipped checks cover optional browser runtime and Windows symlink privileges; Linux CI remains required. The unit suite includes cache preservation, changed-source rejection, installed-pack independence, bounded partial reads, query fusion, evidence-hash verification, unreviewed-label exclusion and module-versus-passage scoring.

Before the passing isolated run, the working staging copy had failures caused by a residual temporary SQLite file, a missing new-file allowlist entry, a release-heading format error and a nested-checkout archive-boundary test. These were resolved; they are not counted as passing runs. No validator rule was relaxed to accept the residue. After preserving the temporary file outside the source tree, new test fixtures were moved to the normal temporary directory. The source registry's Unicode punctuation serialization was restored to avoid unrelated textual changes; parsed comparison confirmed that S104 alone changed, with its current hash retained in the amendment ledger. Final validation and release-candidate rebuilding cover that serialization and review-text update.

## Study and corpus boundaries

The implementation used the existing public notes, source registers and private bibliographic/processing metadata to choose a bounded study packet. No actual person's history was used in code, examples, tests or evaluation prompts. Private books, OCR, page images, acquisition records, paths, indexes and detailed reading journals are excluded from the public change. A selected pilot source is not presumed scientifically valid or permitted for every AI use. Pending permissions and technical defects remain explicit; no blanket label of pseudoscience is assigned to an unread book.
