# MyHeritage and Genotek export intake

## Scope and evidence boundary

This module supports owner-authorized private intake and explanation of consumer genetic exports. It provides a provider-aware workflow, with an optional staging parser tested on wholly synthetic fixtures; no diagnostic service or clinical variant interpretation. Actual exports, kit identifiers, account links, ancestry matches and family information remain outside this public package. Use modules 20 and 30 for private import and clinical interpretation boundaries; module 32 covers numerical risk communication.

Provider documentation was checked on 2026-10-08. No provider account was accessed and no export was downloaded during the public documentation review; synthetic tests do not establish vendor compatibility. Documentation can change or describe a different product generation from the supplied file. The file header and product provenance must therefore be checked before normalization.

## Classify the artifact before import

| Artifact | Intake treatment | Essential limitation |
| --- | --- | --- |
| Report PDF, image or saved web report | Preserve as an original report; extract dated provider claims, units, methods, limitations and source locations into a separate private summary | A report is an interpretation snapshot; it does not contain the complete underlying genotype or sequencing data. Do not invent a PDF download feature if the account only offers web results |
| Ethnicity estimate, haplogroup, DNA-match or shared-segment output | Label as ancestry/genealogy; retain model version and export date where available | These outputs are not clinical diagnoses, and match files may disclose relatives' information |
| SNP raw TXT/TSV/CSV | Inspect comments, headers, delimiter, allele representation and stated reference build; preserve the exact input before parsing | The extension alone does not establish schema, coverage, accuracy or clinical suitability |
| VCF or compressed VCF | Record fileformat, reference assembly, sample selection, REF/ALT, genotype, filters and available quality metadata | VCF describes variant calls; it does not establish WGS coverage or a negative finding at an absent position |
| FASTQ or CRAM | Inventory privately and refer processing to an appropriate bioinformatics workflow | These are sequencing reads or alignments, not ready-made clinical interpretations; this skill does not align reads or perform variant calling |

The categories above are operational intake rules. Provider export availability is limited to the specific documentation below; no availability of BAM, gVCF, PDF or universal CSV export is inferred.

## MyHeritage: current documentation and mixed generations

The raw-data help article describes tab-separated text with five fields: variant identifier, chromosome, position and two alleles. It states that SNP alleles use the forward reference strand and that its indel representation uses I/D. Keep I/D tokens without converting them into sequence-resolved REF/ALT. Two allele columns do not identify parent of origin. The article does not establish the genome build for every file. [S214]

The WGS help article, dated July 21, 2026, describes new laboratory samples from January 2026 as WGS, subject to its Health-product exception. Previously processed kits are not automatically resequenced. It calls the ordinary download CSV/TXT and describes CRAM downloads as still being developed. Its comparison table mentions CRAM, but the availability paragraph is conditional: do not promise that an account can currently download it. Health reports are described as GSA-based and incompatible with the WGS processing route. Verify the supplied header rather than assigning technology from purchase date. [S215]

These pages use different descriptions of the ordinary file. Accept a historical CSV only after observing its actual delimiter and fields; do not describe a four-column CSV as the sole current official schema. Preserve any single genotype field and document a validated split into alleles only in a derived copy. No official historical CSV-version specification was verified during this review. [S214, S215]

The download help requires published results and the kit manager. Its documented workflow uses Manage DNA kits, Download, consent and an emailed link valid for 24 hours. Uploaded kits from another provider must be obtained from their original provider. Credentials and email links are not source metadata for the public package. [S216]

The chromosome-browser download is a CSV of shared/triangulated segments, not a SNP raw-genotype file. Keep its genealogy classification even if its extension matches a raw file. [S217]

## Genotek: product-specific exports

The public laboratory-process article describes microarray analysis and a downloadable VCF in the personal account. Consequently, a Genotek VCF must not be classified as WGS merely because it is a VCF. The article is product-process documentation, not an independent validation of clinical accuracy or a complete VCF schema. [S218]

The current Full Genome product FAQ explicitly offers VCF and FASTQ downloads and says that conversion to 23andMe v3/v5 is available on request. Treat a converted TXT as a derived consumer format with original provider provenance; its format name does not mean the specimen was tested by 23andMe. Retain the primary VCF/FASTQ and conversion provenance privately where the owner has supplied them. The page describes sharing processed results through an account link; this review did not verify PDF export. [S219]

The official genealogy page's indexed FAQ lists VCF, 23andmeV5 TXT and 23andmeV3 TXT. Direct retrieval returned almost no usable body, so this is a provider search-index excerpt, not a fully read or account-tested export specification. Verify the available choices in the owner's supplied documentation before relying on this detail. No universal Genotek TSV/CSV schema, reference build or variant count is established here. [S220]

## Private intake and safe explanation workflow

1. Resolve owner authorization, exact input and private destination. Preserve the original byte content and record a checksum, export date, provider, product, laboratory method and visible format/version. Keep identifiers only in the private archive.
2. Examine a minimal local header/sample when authorized; never paste real alleles or identifiers into public web queries, tests or repository examples. Classify archives before extraction and reject ambiguous or unexpected contents.
3. Record unknown build, strand, sample identity, conversion method or quality as unknown. Do not guess these from an rsID, provider name or filename. Separate observed calls, missing/no-calls and absent loci.
4. Keep report assertions, raw observations, ancestry outputs and any later annotations in separate provenance-linked records. Preserve disagreement between providers or generations without choosing a clinically correct answer from a simple majority.
5. Explain coverage and evidence limitations before discussing a finding. An rsID is a lookup identifier; it is not a clinical interpretation. Do not manufacture a diagnosis, drug dose, pathogenicity claim or negative disease screen from it. Apply module 30's confirmation and clinician-review boundaries.
6. If the format or analysis cannot be handled with available tools, complete the inventory and clearly state the unperformed operation. This documentation does not claim live provider access, parser execution, sequencing analysis or clinical validation.

## Sources and remaining uncertainty

Source IDs in brackets identify the accompanying source records. MyHeritage pages and Genotek's laboratory-process and Full Genome pages were read as accessible official HTML. The Genotek genealogy claim was read only through a search-index excerpt. No provider account UI, historical CSV specification or CRAM rollout was verified in the public documentation review. Keep these limitations in any downstream answer about actual file support.

## Optional offline staging helper

The import skill bundles genetic_staging.py. With an available Python host, run `python genetic_staging.py SOURCE NEW_PRIVATE_DIRECTORY`. Output must be outside the public checkout. The helper preserves exact original bytes, a payload checksum, raw rows and source-line locators in staging.sqlite, plus metadata.json. It makes no network request, clinical annotation or medical-ledger write.

Supported schemas are explicit: four-column CSV with RSID/CHROMOSOME/POSITION/RESULT; five-column tab-separated rsID/Chromosome/Position/Allele1/Allele2 with normalized header spacing; standard textual VCFv4 with exactly one sample and FORMAT. A ZIP must contain exactly one supported text file and meet bounded size/compression/path checks. Compressed VCF gzip, 23andMe four-column TSV, multiselect/multisample VCF, FASTQ and CRAM are not handled by this helper. Inventory those inputs and choose an appropriately reviewed tool rather than silently converting them.

Missing calls, malformed rows, symbolic I/D and duplicate/conflicting loci retain flags. Assembly and strand remain unknown normalized fields, with source declarations preserved verbatim. Read back row counts, metadata and checksums before archiving. Synthetic parser tests establish these mechanics, not vendor-wide compatibility, sequencing completeness or clinical validity.

Saved web reports may use MHTML: parse MIME locally, decode HTML using the declared or embedded charset, and preserve the exact original. Extract text without executing scripts or loading remote assets. Verify headings and provider statements against the source; hidden tabs are not present merely because their labels appear. Keep report dates unknown if no date is stated. Record risk estimates as dated provider claims, with denominator/time horizon and missing coverage, not as a new medical diagnosis.
