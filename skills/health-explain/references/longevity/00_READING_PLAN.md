# Longevity: study plan, reading record and knowledge maintenance

Prepared 2026-10-18. This is a bounded evidence review and a package contribution, not a systematic review of every longevity publication, a new clinical guideline, or completed medical training. The canonical knowledge packet is [module 57](../57_LONGEVITY_AND_PREVENTION.md). Its source ledger records actual reading depth and unresolved questions. Package review remains pending.

## Questions and completion criteria

| Workstream | Required questions | Reviewable output |
|---|---|---|
| Prevention | Which modifiable exposures and indicated treatments reduce mortality, major disease or loss of function? How does quitting smoking help? | Current guidance and outcome-specific cards, including uncertainty and eligibility |
| Experimental geroscience | What do rapamycin, metformin, senolytics, NAD precursors, spermidine and calorie restriction show in humans? | PICO, design, population, sample, follow-up, primary endpoint, effect/CI, harms and funding |
| Radical extension | What has been demonstrated in animals, early human reprogramming and organ replacement? | Separate animal, sponsor-only, registry and controlled human evidence |
| Probability | What do life tables and demographic projections estimate? What is unknown about future therapies? | Conditional survival framework without invented breakthrough probabilities |
| Statistics | Which reported numbers can be shown without changing their meaning? | Machine-readable estimates retaining measure, denominator, comparator, time and population |
| Integration | Can an installed relevant skill find and correctly use the packet? | Canonical sources, synchronized references, search checks, synthetic response checks and build |

The first review closes when these streams have bounded source-backed conclusions, important contrary findings are retained, every numerical claim has a source and locator, access limits are visible, and structural/build checks have been run. Inaccessible full texts and future trials remain explicit gaps; they are not silently counted as read.

## Sequence

1. Inventory existing modules, source records and knowledge search; reuse stable identifiers and useful prior reading.
2. Read applicable source-use policy. Locate primary studies and current official guidance; check article-specific licence before processing restricted publisher work.
3. Read relevant methods/results/limitations and corrections. Distinguish the randomized cohort from an analysis subset, clinical outcomes from biomarkers, absolute from relative effects, and association from causation.
4. Write a short original English card per bounded question. Record exact reading scope, source URL/version, checked date, population, comparator, uncertainty and harms. Keep preregistration and sponsor reports distinct from peer-reviewed results.
5. Reconcile findings. A statistically non-significant result does not prove equivalence; a favorable subgroup or secondary endpoint does not rescue an unsuccessful primary endpoint without qualification.
6. Integrate sources, recommendations and numerical records, regenerate derived copies, then check retrieval and fresh-context response behavior.
7. Package a versioned candidate for substantive maintainer review. A successful build does not establish clinical validity or update an installed copy.

## Reading list and study record

The three packet documents provide the annotated bibliography and study cards:

- [Prevention, lifestyle and indicated treatment](10_PREVENTION_EVIDENCE.md).
- [Human geroscience interventions](20_GEROSCIENCE_EVIDENCE.md).
- [Radical extension and demographic uncertainty](30_RADICAL_EXTENSION_EVIDENCE.md).

The machine-readable evidence ledger separates newly inspected material from retained source history. The statistics file is a set of within-study records, not an effectiveness league table. Titles and URLs in a bibliography do not establish full-text reading. Further reading queues in the cards are research leads, not active support for additional claims.

## How this knowledge is stored and used

Maintain one canonical version of general knowledge in Git. Keep original articles at their publishers/official repositories; this contribution contains original factual notes, not article copies, proprietary scales or reconstructed chapters. Personal histories and private reading/acquisition files remain outside the public package.

Use the project's existing layers rather than introducing another database:

| Layer | Canonical location | Purpose |
|---|---|---|
| Clinical question and recommendation boundary | `knowledge/57_LONGEVITY_AND_PREVENTION.md` | Runtime entry and routing |
| Bounded synthesis | `knowledge/longevity/*.md` | Context, comparisons and source-linked limitations |
| Source identity | `knowledge/sources.json` | Stable medical identifiers and historical reading scope |
| Review ledger | `knowledge/longevity/evidence-ledger.json` | Reading locators, rights, provenance, review state and recheck triggers |
| Numerical observations | `knowledge/longevity/statistics.json` | Measure, CI, comparator, population and horizon travel together |
| Retrieval | Existing offline knowledge-search helper/maps | Derived navigation with source locators; never a substitute for reading |
| Verification | Synthetic cases, source/statistics checks, build report | Separate technical integrity from scientific and clinical review |

Load the entry module first, then only the relevant card and source metadata. A search hit is a candidate passage. Inspect the complete card, its qualifiers and actual source reading depth before answering. Recheck fast-changing claims against permitted current primary sources. Do not treat several assistant summaries of one paper as independent corroboration.

Relations such as `supported_by`, `contrasts_with`, `measured_by` and `updates` can connect cards to evidence. They are navigation, not assertions of causality. Preserve source identifiers and dated corrections; an updated conclusion must explain what new evidence changed it.

This arrangement implements general engineering principles of explicit state, source provenance, progressive context loading and evaluated retrieval. It does not require a vector service, external embeddings, a new model or changes to model weights. Add another retrieval technology only after a measured failure of existing search on representative questions.

## Maintenance and state

This packet's evidence cut-off is 2026-10-18. New clinical results, corrections/retractions, guideline changes, safety notices and authorization changes trigger immediate review before consequential use. Suggested manual review: experimental human trials after 90 days, stable prevention summaries after 180 days, and any individual recommendation when clinical context or jurisdiction changes. No scheduled monitoring is created.

Track work as `located`, `metadata_checked`, `abstract_read`, `sections_read`, `source_checked`, `maintainer_reviewed`, `released`. Only an actual review or release promotes the corresponding status. Keep the package/source/build/installed states distinct. Do not use the number of sources, words, tests or agent messages as a measure of clinical competence.

Remaining work after a technically complete candidate: substantive maintainer and suitable clinical review, release decision, and any expressly requested installed update. Unknown future survival effects and inaccessible trial details remain unknown after packaging.
