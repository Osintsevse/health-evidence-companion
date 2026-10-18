# PR 26 review repairs, 2026-10-18

This repair starts from PR head `23b372a5efcc1861aeecbc42302611143e72fced`.
It addresses stale retrieval evidence, inconsistent source-policy use and the
unstable README source count. Original source identifiers and reading history,
psychology import pins and unadjudicated retrieval labels remain traceable.

## Source reconciliation

`pr26-source-reconciliation.json` records selected independent reading, version,
scope, rights limits and old paragraph/route fingerprints. Restricted originals
were not retrieved through mirrors or excerpt substitution. Dependent claims
were narrowed or suspended; independent patient education does not replace a
complete condition-specific guideline. In particular, the repair removes a
universal heart-failure fluid rule, a fixed-day refeeding rule and unsupported
therapy hierarchies. Sudden confusion calls for immediate assessment.

The canonical register retains historical entries. The generated source catalog
and bounded lookup expose `active_use`: `bibliographic_only`,
`rights_metadata_only` or `not_determined`. The last value is deliberately not
permission or clinical approval. The explicit rights-notice exceptions are
medical S84, S360 and S521. Citation checks cover canonical Markdown and active
route/case source IDs. They catch consistency regressions, not semantic clinical
errors; a passive marker alone does not establish that surrounding prose is safe.

Source replacement is claim-specific. Selected NHS/NIH patient information
supports only the recorded explanation or urgency boundary. Old review dates,
unread linked guidelines and local applicability remain limitations. Current
professional appraisal is still needed before care recommendations.

## Retrieval and evaluation

Reviewed passage hashes and line boundaries are checked independently in CI
before evaluation. Revisions retain prior values and reasons in
`../evals/knowledge-search-label-revisions.json`; no case becomes eligible merely
because its source changed. Bounded Russian aliases support common navigation
and biomedical inflections. Navigation intent prefers index candidates; ordinary
clinical queries continue to prefer substantive passages. No automatic external
translation or private query export was added.

Saved native and host-alternate evaluations record corpus fingerprint, algorithm
and case hash. These are authored retrieval measurements, not clinical validity,
absence accuracy or blinded generalization. The existing 132 unadjudicated cases
remain outside primary metrics, including applicability and conflict gaps.

## Validation record

Final commands and observed results are recorded after execution. Synthetic
response checks retain actual output separately from author review. No merge,
release, installed-plugin update or clinical approval is implied by this repair.

## Observed retrieval results

| Query mode | Scored cases | Module recall at 5 | Module recall at 20 | Passage hit at 20 |
|---|---:|---:|---:|---:|
| Original only | 68 | 54.4% | 63.2% | 55.9% |
| Original with authored alternate | 68 | 72.1% | 85.3% | 79.4% |
| Russian original only | 42 | 38.1% | 45.2% | 38.1% |
| Russian with English alternate | 42 | 66.7% | 81.0% | 76.2% |
| English original, either mode | 26 | 80.8% | 92.3% | 84.6% |

Both 200-query runs completed without errors. Native mode still has 48 empty
lists; alternate mode has none, which does not establish answerability. Relative
to the historical report, the corpus and ranking both changed: these figures are
not an isolated algorithm ablation. Applicability/conflict candidates remain
unadjudicated. Twelve evidence records changed with old hashes and reasons kept.

## Observed longevity responses

All eight authored prompts were executed in one isolated fresh session without
rubrics; actual answers, access failures and author review are saved in
`evals/longevity-forward-checks.json`. Seven meet the authored criteria. One is
partial: the breakthrough-probability answer properly refuses an invented
estimate but omits a useful practical prevention step. This is not eight
independent contexts or a perfect pass claim. Direct-source access and sponsor
report limits remain explicit. Hashes of prompts and stable skill instructions
are retained; final reference hashes were captured after execution, with that
timing limitation disclosed.

## Final executed technical checks

- `python -X utf8 scripts/validate.py`: passed, including canonical/generated consistency, source policy, import provenance and the explicit archive allowlist.
- `python -X utf8 scripts/evaluate_knowledge_search.py --root . --cases evals/knowledge-search-cases.json --validate-only`: all 200 records checked, 68 reviewed evidence sets verified.
- `python -X utf8 -m unittest discover -s tests -v`: 319 tests, 316 passed and three environment skips (Windows symlink privileges and optional browser runtime).
- `python -X utf8 -m unittest discover -s examples/drugbank -v`: eight offline tests passed, no provider requests.
- `python -X utf8 scripts/build.py`: passed. Deterministic build and archive-member rejection checks also passed in the full suite.
- Native and alternate retrieval runs: 200 queries each, zero execution errors; the same final corpus fingerprint and evidence-case hash are retained in both result files.

The initial full run had two repair-introduced failures: the dated release heading
was split, and a minimal catalog test fixture lacked its new required policy.
The heading and explicit fixture policy were corrected without weakening the
production requirement or release parser. The complete suite was then rerun.
Passing structure, synthetic behavior and CI do not establish clinical validity.
