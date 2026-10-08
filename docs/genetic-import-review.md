# Genetic provider import review

Checked 2026-10-08. Version 0.5.1 adds provider-aware intake for MyHeritage and Genotek, and an optional offline raw-genotype staging helper.

## Supported mechanics

The helper accepts explicitly declared four-column CSV, five-column tab-separated text and standard single-sample textual VCFv4. It retains source bytes, hashes, line locators, raw fields, missing calls, symbolic alleles, duplicate/conflicting loci and uncertain quality/filter information. Output is a new private directory outside the public checkout. It makes no network requests and does not write to the medical ledger.

ZIP input is bounded to one supported text member with path, compression and size checks. Maximum input/payload size is 100 MiB; large sequencing outputs require another suitable tool. No FASTQ/CRAM alignment, variant calling, clinical annotation, polygenic score calculation, automatic provider access or genetic diagnosis is implemented.

Provider documentation describes different generations and products. MyHeritage current TSV documentation and CSV/TXT descriptions are preserved with their limits. Genotek VCF availability does not by itself establish WGS. Converted 23andMe text keeps its original provider provenance; its four-column TSV schema is not handled by this helper. Actual header inspection is required.

## Archive and report rules

Consumer health reports are provider interpretation snapshots. Saved web/MHTML content must be decoded and inspected without executing scripts or requesting external resources. Dates, hidden tabs and variant coverage remain unresolved when not present. Raw variants are separate datasets, not laboratory time-series points or clinician diagnoses. Current graphs and original medical records must be preserved during an incremental import.

No actual patient records, real variants, kit/account identifiers, medical histories, private paths or source-derived test fixtures are included here.

## Validation

Ten parser tests use wholly fictional inputs and check preservation, schema rejection, no-calls, conflicting duplicates, VCF filter/quality limits, archive defenses and private atomic staging without overwrites. The full repository suite ran 157 tests successfully with three host-dependent skips (two symlink checks and optional Pillow). Structural/reference checks, package build and whitespace checks passed.

A fresh-context synthetic review inspected four requests concerning absent variants, symbolic I/D, genealogy versus genotype CSV and external upload authorization. It found two VCF uncertainty gaps, which were corrected and tested. These checks validate selected mechanics and workflow boundaries, not clinical accuracy or every provider export version.

## 0.5.2 annotation and reader checks

Checked 2026-10-08. The reusable pipeline adds dated public ClinVar download and index, exact forward GRCh37 SNP cross-references, policy rechecks, identifier/reference-locus lookup, MHTML extraction and a bounded private review queue. The optional archive Genetics tab preserves the existing default navigation and chart data. Russian display dictionaries retain original database codes.

The full repository suite ran 187 tests successfully with three host-dependent skips. Synthetic tests cover conflict/review separation, incompatible build and strand declarations, allele mismatches, missing calls, absent reference loci, duplicate flags, exact provenance, private and installed-skill output boundaries, partial-download preservation, bounded summaries and localization. Build, reference synchronization and source allowlist checks pass. Offline browser checks cover tab placement, search, filters, pagination, existing chart/timeline rendering, mobile overflow and blocked external requests.

These checks verify software behavior and selected workflow boundaries. They do not validate array probe accuracy, all provider exports, rare variant calls, ploidy, haplotypes, clinical diagnoses or personal risk calibration. A reference match is not clinical confirmation.
