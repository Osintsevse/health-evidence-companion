# Longevity packet: review state and verification

Evidence cut-off 2026-10-18. Version 0.9.2 is a local contribution candidate. It is not a release announcement, installed update, formal clinical guideline or clinical approval.

## Scope and source reading

The packet covers adult prevention/lifestyle, selected human geroscience interventions, early radical-extension approaches and demographic inference. There are 26 bounded topical cards and 28 source records, including guidance, registry navigation and sponsor announcements; these are not 28 independent trials. Twenty-five source records are new and three existing identifiers are reused with additional reading history preserved. Actual methods/results/limitations reading, indexed-text access, abstract/overview limits and unread supplements are recorded separately in the evidence ledger.

The review corrected several consequential interpretations: remaining versus total mouse lifespan; percentage points versus kilograms in PEARL; primary ITT versus sensitivity findings and uncertain adverse-event incidence in RAPA-EX; biomarker versus observed mortality in CALERIE; and October 2026 ER-100 sponsor observations versus a June-only trial-start account. TAME's undated official page is not a confirmed live registry status or positive result.

The primary-data selection and numerical extraction are purposive rather than systematic. No PRISMA claim, exhaustive search, independent individual-participant reanalysis, supplement-complete review or completed specialty training is made. Sources with current processing restrictions were not bypassed using mirrors. Original factual summaries do not relicense external works.

## Knowledge architecture

The implementation uses the existing canonical source registry and derived skill references, a bounded reading ledger and numerical dataset, explicit state, lazy loading and offline search. It adds no private medical archive, external model, vector service, telemetry or scheduler. Clinical knowledge, source metadata, numerical observations, retrieval results, authored checks and observed check outcomes remain distinct.

The study plan gives completion and maintenance criteria. The bibliography is an annotated reading record, with future research leads clearly separate from active evidence. The query aliases are navigation terms, not assertions that longevity, ageing, reprogramming and disease treatment are clinically interchangeable.

An installed-pack retrieval check initially failed to find the new cessation card for the Russian cessation query: its heading did not contain the curated phrase. The card headings were made explicit, then references were regenerated and the same query was rerun. This was a navigation failure, not absent evidence or a reason to change clinical conclusions.

## Synthetic forward checks actually executed

A fresh-context assistant read the candidate health-research instructions and selected canonical cards, without access to evaluation rubrics, tests or integration scripts. It answered three wholly fictional prompts in Russian. Its primary sources were the saved candidate notes, not an independent external literature recheck.

| Prompt theme | Observed behavior | Bounded review |
|---|---|---|
| OSK 8.86 versus 18.5 weeks after treatment at week 124 | Distinguished remaining/total medians; calculated approximately 7.3% total-age difference; retained animal and control limitations | No consequential unsupported lifespan transfer observed |
| ER-100 status on 2026-10-18 | Included October 8 sponsor report, three glaucoma participants and short uncontrolled observation; did not claim proven rejuvenation or survival | Preserved current evidence category and access limits |
| CALERIE mortality claim and a 2045 breakthrough probability | Rejected observed 15% mortality inference; separated biomarkers; supplied no invented personal probability and explained missing inputs | Preserved surrogate/prognosis boundary |

Eight synthetic prompts are authored in `evals/longevity-cases.json`; only the three themes above were executed as fresh-context response checks in this review. This small purposive exercise is not a blinded benchmark, clinical safety study or estimate of overall answer accuracy. Technical tests and retrieval checks are documented separately by actual command reports.

## Remaining review and access gaps

- Substantive maintainer and suitable clinical review of conclusions, eligibility language, numerical transcription and source-specific reuse.
- Full ER-100 registry/protocol/history and independent longer-term clinical results.
- Unread trial supplements, raw-data checks and independent figure inspection for the noted mouse sample count.
- Better permitted causal diet/function evidence, current local risk-treatment pathways, and later trial/safety updates.
- No validated model for breakthrough timing, future treatment access or individual survival benefit.

Packaging does not resolve these scientific gaps. No external publication, merge, release or installed update should be claimed without that separate verified event.

## Technical checks executed

Initial broader unit-test attempts were blocked by Windows sandbox access to their own temporary directories. The same suites were rerun outside that sandbox; no clinical result or test assertion was changed to hide an environment error.

| Suite | Tests | Result |
|---|---:|---|
| test_longevity_packet | 8 | Passed |
| test_knowledge_search | 9 | Passed |
| test_package | 34 | Passed |
| test_unified_catalog | 12 | Passed |

The package validator and deterministic builder ran after these checks. Exact build hashes and archive member counts are recorded in the build report. Structural checks cover source identifiers, reference synchronization, nested installed-pack retrieval, numerical denominators/units and packaging rejection paths. They do not establish clinical truth.

Across these suites, 63 tests ran: 62 passed and one was skipped. The skipped test requires Windows symlink-creation privilege, which this host lacked; the Linux CI check remains necessary. Separate archive-member symlink rejection coverage passed.

## Independent bounded source check

A separate fresh-context assistant checked the smoking/cessation, RAPA-EX and CALERIE numerical interpretations against permitted primary-source text. It found no material transcription or inference error within those three checks. CALERIE's exact biomarker estimates were accessible through indexed original-publisher text and the PubMed abstract after direct publisher/PMC access failed; supplements and participant data were not audited. This is an additional bounded source check, not clinician review, approval or whole-packet validation.
