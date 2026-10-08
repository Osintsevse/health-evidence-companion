# Reusable private genetics workflow

The package distributes reviewed source code and blank display contracts. Never generate a replacement parser when a supplied helper supports the observed format. Run tools locally with explicit private input/output paths. Keep public reference caches outside the plugin checkout; record their snapshot/version and hashes. No actual genetic data, report text, account identifiers or private paths belong in contributions, examples, logs or issues.

## Pipeline

1. Preserve exact originals and source provenance using the archive commit/readback workflow. genetic_staging.py stages supported raw formats into a separate SQLite dataset; genetic_reports.py extracts saved MHTML text strictly without running HTML or fetching assets.
2. Review source assembly, strand, product and flags. genetic_marker_query.py retrieves supplied identifiers and all competing observations at their loci; missing identifiers remain absent, never reference or negative disease results.
3. In a separate public-only operation, genetic_annotation.py download accepts a dated NCBI GRCh37 snapshot, verifies the published MD5 and records SHA-256. index creates a reusable public SQLite cache of biallelic SNP records, preserving INFO, raw VCF, header and line provenance. The reference cache is intentionally not included in the small plugin ZIP.
4. annotate reads local staged calls and the local cache without network calls. Explicit GRCh37/forward declarations are required; conflicting source declarations are rejected. Results retain flagged, weak-review, conflicting and haplotype-dependent candidates. priority_for_manual_review means an unconfirmed, technically compatible germline candidate with a qualifying aggregate review status; it is not a clinical classification of the person or a diagnosis.
5. Clinician-facing interpretation requires variant-condition and inheritance review, evidence of assay validity, clinical context and confirmation before consequential decisions. VUS, risk factors, response associations and benign classifications are distinct. See module34; the VCF is partial and aggregate condition names may combine several assertions.
6. Save a separately dated private interpretation with method, source hashes, population/time-horizon limits, unresolved disagreements, next clinician questions and full technical appendix. Keep the provider's source claim intact. Generated views require reviewed owner data; the renderer never invents an assessment.

## Commands (placeholders only)

`python genetic_staging.py INPUT NEW_PRIVATE_DIRECTORY`

`python genetic_reports.py SAVED_MHTML --output NEW_PRIVATE_JSON`

`python genetic_marker_query.py --staging PRIVATE_STAGING --rsid MARKER_ID --output NEW_PRIVATE_JSON`

`python genetic_annotation.py download --url DATED_PUBLIC_GRCH37_URL --output EXTERNAL_VCF`

`python genetic_annotation.py index --vcf EXTERNAL_VCF --output NEW_EXTERNAL_SQLITE`

`python genetic_annotation.py annotate --staging PRIVATE_STAGING --index EXTERNAL_INDEX --output NEW_PRIVATE_SQLITE --assembly GRCh37 --strand forward`

Download and indexing are once per snapshot; many private imports reuse the same public cache. Annotation and lookup use already parsed SQLite, reducing repeated extraction/token use. Tools refuse existing output targets and public-repository patient output. Archive acceptance, locks, backups, sync and clinical review remain separate responsibilities.

## Genetics sidebar contract

The existing archive config may add `genetics: {assessment_path: EXPLICIT_PRIVATE_JSON_PATH}`, or the same object inline. The JSON has optional title, summary, sections [{title,text,collapsed}], reports [{title,text,source,source_href}], sources [{title,url,accessed,text}]. Text remains literal, including newlines. The optional Genetics tab appears beside allergies. Relative source links are validated against encoded traversal; HTTPS source links require a deliberate click. The view does not load external resources. Older configs without genetics retain existing navigation. Keep per-person assessments and config paths private.

## Validation and limits

Synthetic tests cover explicit schemas, no-calls, duplicated/conflicting loci, assembly contradictions, exact allele compatibility, no complement/liftover inference, bounded download origins/checksums, offline annotation, MHTML decoding and protected output publication. They do not demonstrate clinical validity, universal provider account compatibility, sequencing analysis or genome-wide negative screening. FASTQ/CRAM processing needs a different reviewed read-based workflow, not a renamed array file. See sources S221-S250 and module33 for provider differences.

Source refresh: fetch a new dated public snapshot into a new cache; retain the old hashes and analysis. Re-run privately, compare changed annotations, flag stale interpretations and review consequential changes against current primary clinical sources. Do not schedule or notify without owner instructions.

The optional marker-query reference-index argument inventories aliases at explicitly confirmed GRCh37/forward loci; it does not establish allele equivalence. Recheck stored candidates after a matching-policy change with `genetic_annotation.py recheck --source PRIVATE_CANDIDATES --output NEW_PRIVATE_SQLITE`, preserving earlier results. A new reference snapshot still requires a new annotation. Literal source tokens remain separate from biological copy number. Optional private classification_labels/review_status_labels/flag_labels and config.labels.geneticsLabel0..31 localize the technical appendix without altering raw source codes.

Russian UI labels and explanatory classification/review/flag translations are bundled in genetic_labels.json. The generator applies them for locale ru without rewriting source codes. Preserve this asset with private scripts for future generations; unfamiliar codes remain literal rather than receiving guessed translations. Section source_ids can reference the assessment sources list for immediately adjacent clickable citations.

### Reuse a bounded review queue

Use the bundled helper instead of generating another ad hoc database reader:

```sh
python genetic_reports.py --candidates /private/candidates.sqlite --limit 50 --output /private/review-queue.json
```

This retains all aggregate counts, returns a bounded queue of pathogenic-source classifications including unresolved flags, and reports omitted rows. It does not infer diagnoses or remove other records from the full database. The helper refuses replacement of an existing output. Use new filenames for each review.
