# Genetic evidence sources, repeat review and external-data consent

General knowledge checked 2026-10-09. Tools prepare an informational review of unconfirmed calls; they do not diagnose, validate an assay, prescribe or grant disclosure permission. Public examples are wholly fictional. Reference downloads and local analysis are separate operations.

## Professional practice and what to reuse

Genetic counselors need disease, inheritance and family-risk context; laboratory teams also evaluate analytical validity, variant evidence, quality systems and traceable classification. GeneReviews supplies expert-reviewed chapters covering diagnosis, management and counseling. [S253]

A 2023 survey of 178 counselors experienced in immunology, dermatology, endocrinology and pulmonology reported GeneReviews use by 99% and PubMed/literature use by 93% for learning about those specialties. This selected cohort does not establish use by all counselors. A survey of 17 UK germline cancer laboratories documented ClinVar, Alamut, CanVar-UK and in-house systems; many steps remained manual. These are observed workflows, not global product rankings. [S254] [S255]

| Question | Appropriate evidence | Limit |
| --- | --- | --- |
| What does this inherited condition mean? | GeneReviews and OMIM | A disease overview does not classify every allele or establish a patient's condition |
| How has this exact variant been assessed? | ClinVar assertions and ClinGen expert variant curations | Record condition, accession/version, review status, conflicting submissions and dates |
| Is this gene-disease relationship established? | ClinGen Gene-Disease Validity | Gene-level evidence cannot be substituted for a variant classification |
| How frequent is the allele? | gnomAD | Rare is not automatically pathogenic; coverage and ancestry matter |
| Which transcript/consequence is affected? | Ensembl VEP and verified HGVS descriptions | Annotation is distinct from measured-call validity and actionability |
| Is the call supported by reads? | IGV with actual BAM/CRAM and local reference data | An array text file has no aligned sequencing reads |
| What clinical action follows? | Disease-specific guidance and a clinician; CPIC for relevant gene-drug pairs | Do not derive treatment or individual risk from a raw consumer call |

Use the ACMG/AMP framework with applicable current ClinGen general, criterion-specific and gene-specific specifications. Distinguish germline interpretation from somatic oncology, pharmacogenomics, CNV classification and polygenic scores. A specification index is not a completed clinical evaluation. [S256]

ELLA documents standardized assessments, peer review, complete change histories and optional air-gapped deployment. Alamut supports genomic visualization and source aggregation. Franklin and VarSome provide optional annotation/classification workbenches; feature descriptions are vendor claims and no proprietary engine was tested here. A shared ClinVar record used by two platforms is one evidence source, not two independent confirmations. [S260] [S261] [S263] [S264]

## Public downloads and local reuse

The existing ClinVar pipeline retains its explicit GRCh37/forward, biallelic SNP scope. VCF summaries have partial coverage: no match is not a negative clinical test. Check the official latest dated release and MD5 before reusing a cache. If no newer snapshot is available, state that the same release was verified again; retain the old run. Never relabel a download or refresh reading dates to manufacture new evidence.

The optional genetic_evidence.py helper adds a fixed-endpoint public ClinGen gene-validity CSV download. It accepts no private search input. Each new external cache records retrieval time, the source's FILE CREATED date, byte count, local SHA-256 and curation count. HTTPS plus a local digest is not a publisher signature. Cached files are not distributed in this package. The complete gene table is fetched before private matching. [S257]

Offline enrichment preserves all exact-symbol gene/disease/inheritance assertions. It does not infer aliases, match a person's phenotype, classify variants or alter the ClinVar priority flag. Missing curations remain unknown. Stored source lines and report links support later review.

Offline comparison requires the same raw source fingerprint, staged input bytes and assembly/strand declarations. It compares exact variant observations and multisets of annotation records, preserving duplicate assertions. Changed or removed matches require review; removed annotations do not establish benignity or a negative test. Separate changed evidence, changed matching policy and clinically confirmed biological changes.

## Recipient-specific informed consent

Reuse an existing owner's authorization within its original scope. Archive processing permission does not authorize a new recipient, public sharing, training, family-data disclosure or raw-file upload. Before a new transmission show:
- The recipient and specific purpose.
- The exact minimal payload, with identity, genotype, phenotype and full-file fields omitted unless needed and explicitly authorized.
- Current contractual retention, deletion, subprocessors, training, jurisdiction and community-sharing terms.
- The implications of derived genetic information and the option of local-only review.
- The authorization scope and any expiry; a changed recipient, purpose or payload needs renewed consent.

The plan-transfer command prepares a private plan for selected variants, a payload digest and a scope digest binding recipient, purpose and terms. It always reports consent_granted=false and transmitted=false. It has no sending command, OAuth access or provider account. A generated plan/configuration is not evidence that a human approved it. The executing host must verify actual scoped human authorization before an independently available adapter transmits anything.

Franklin's public policy separates uploaded genetic Submitted Data, governed by a customer processing addendum, from ordinary account/site data. Review the applicable contract and sharing settings; do not infer that a general privacy page settles patient-data processing. VarSome API integration likewise requires current access/license and privacy terms; Stable and Live environments can differ in freshness. [S262] [S263]

GeneCards is useful for gene navigation and links to primary sources. Its terms prohibit automated scraping; user consent does not grant a data license. Use permitted browsing or a separately authorized licensed integration. No scraping adapter is included. [S266]

## Reporting and professional review

Keep the original provider report, raw genotype, database annotation and human-reviewed interpretation separate. An updated database cannot confirm that an array measurement is real. Show technical limitations, condition/inheritance uncertainty and confirmation status beside consequential candidates. Save a dated private comparison and refreshed explanation; preserve prior versions and unrelated medical history. Publishing code or passing tests does not constitute clinical validation or approval.
