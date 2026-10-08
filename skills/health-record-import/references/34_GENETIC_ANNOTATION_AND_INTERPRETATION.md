# Consumer genetic annotation and interpretation

Status: draft for maintainer review. Evidence checked: 2026-10-08. General educational knowledge only; no patient records, genotypes, identifiers, or individualized risk estimates. This module helps interpret consumer SNP arrays and third-party reports; it does not establish a diagnosis or authorize treatment.

## Start with the decision, not a list of diseases

Separate three questions: was the allele measured correctly; is its association credible; would knowing it change an evidence-based clinical decision? A technically credible common association may still have little clinical utility. A frightening rare call may be an array error. Prioritize potentially useful confirmation, medication discussions and appropriate symptom/family-history evaluation; keep weak associations in an optional appendix rather than presenting an undifferentiated risk inventory.

FDA guidance explains that consumer tests have different coverage and evidence. A negative selected-variant result does not exclude disease; a risk-associated allele is not a diagnosis. Authorized report claims do not validate every raw-data probe or a third-party interpretation of another company's file. See [FDA consumer testing guidance](https://www.fda.gov/medical-devices/in-vitro-diagnostics/direct-consumer-tests).

## Technical safeguards for a build37 forward-strand file

These are analysis safeguards, not claims that every MyHeritage export uses the same format. Read the actual header and vendor metadata. Preserve the original locally. Record file checksum, export date, declared assembly, strand, platform if available, parsing version and annotations date. Treat an explicitly declared GRCh37/build37 forward file as such; never silently substitute GRCh38 positions or reverse-strand alleles.

Match the exact variant by assembly, chromosome, position and normalized alleles, with rsID as an additional identifier. An rsID alone may have merged mappings, multiple alleles, or indel representation differences. Account for complements (A/T and C/G pairs are especially ambiguous without reliable orientation). No-call, absent probe, reference genotype and failed mapping are distinct states. Do not convert missing data to a normal result. Preserve duplicates/conflicts for review rather than choosing the convenient line.

An array samples selected sites; it is not a negative gene panel, exome or genome. Do not infer unmeasured repeat expansions, deletions, duplications, copy number, mitochondrial heteroplasmy, balanced rearrangements or full HLA types. Phase is usually unavailable. Imputation is a probabilistic estimate and must remain labelled separately from observed calls.

## Choose annotation tools appropriate to the data

[GATK germline short-variant discovery](https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels) expects preprocessed sequencing BAM files and derives calls from sequence reads. A consumer array text export has no reads to realign, no sequencing depth, and no genotype likelihoods for unmeasured sites. Converting its measured calls into VCF does not make it whole-genome sequencing and does not justify applying sequencing discovery or recalibration steps.

[Ensembl VEP cache documentation](https://www.ensembl.org/info/docs/tools/vep/script/vep_cache.html) describes local cache-based annotation and offline operation. Local annotation can avoid transmitting personal variants to remote services, but requires compatible assembly, cache and tool versions and any necessary local reference FASTA. Consequence annotation describes effects on transcripts; it does not establish analytical validity, clinical pathogenicity or actionability. Archive versions and access failures must remain explicit.

## Rare pathogenic candidates and clinical confirmation

In a selected clinical referral series, 40% of variants reported in submitted DTC raw data were false positives on clinical confirmation; some others were misclassified by interpretation services. This does **not** mean 40% of all array genotypes or all users are wrong. Referral selection and the concentration of rare disease variants limit generalization. The practical lesson is to confirm consequential raw-data findings using an appropriate clinical laboratory before screening changes, surgery, reproductive decisions or family cascade testing. See [Tandy-Connor et al., 2018](https://pubmed.ncbi.nlm.nih.gov/29565420/).

Confirmation should match the variant class: targeted sequencing can verify many SNVs, but a suspected deletion, duplication, repeat, HLA allele or complex pharmacogene may require a different assay. A clinician should decide whether a targeted assay or a broader diagnostic panel fits symptoms and family history. A concerning family history can justify clinical evaluation despite a negative consumer file.

## ClinVar, ACMG/AMP and ClinGen mean different things

[ACMG/AMP sequence-variant guidance](https://pmc.ncbi.nlm.nih.gov/articles/PMC4544753/) defines pathogenic, likely pathogenic, uncertain significance, likely benign and benign for Mendelian disease interpretation. A VUS should not drive clinical decisions. Common complex-disease risk alleles cannot simply be promoted to Mendelian pathogenic variants because an association is statistically significant. Pathogenic classification is about a specific variant and disease mechanism; it is not a statement that every carrier currently has the disease. Consider inheritance, zygosity, penetrance and condition context.

[ClinVar review status](https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/) reflects review and agreement, not severity or certainty of an individual's disease: four stars denote a practice guideline; three an expert panel; two multiple submitters with criteria and no conflicts; one commonly a single submitter with criteria or conflicting aggregate submissions; zero several forms of absent criteria/classification. Read the text as well as the stars. Record accession/version, specific condition, current aggregate classification, conflicting submissions, last evaluation dates and evidence. Do not equate a somatic cancer therapeutic assertion with a germline inherited-risk classification.

[ClinGen gene-disease validity](https://www.clinicalgenome.org/docs/gene-disease-validity-classification-information/) asks whether the gene causes the specified disorder; variant pathogenicity asks whether a particular change does so. [Clinical actionability](https://www.clinicalgenome.org/curation-activities/clinical-actionability/browse-curations/) evaluates whether an intervention can improve an outcome. Neither a gene name on an actionable list nor a database hit validates an unconfirmed array call. Refresh relevant expert-panel evidence rather than treating database classifications as permanent.

## APOE and Alzheimer's disease

APOE is susceptibility information, not a stand-alone dementia diagnosis or a reliable forecast of age at onset. Absence of epsilon4 does not exclude Alzheimer's disease. Epsilon4-associated risk varies with age, ancestry, sex, family history and other factors; do not turn an odds ratio into an individual's lifetime probability. [NIA genetics guidance](https://www.nia.nih.gov/health/alzheimers-disease-genetics-fact-sheet) supports discussing interpretation with a clinician or genetic counselor.

Common APOE isoform inference uses rs429358 and rs7412 together; missing calls and unusual/unphased combinations should remain unresolved rather than forcing an epsilon genotype. A single nearby proxy is not full clinical APOE testing. Interpretation of severe neurodegenerative risk merits explicit consent about disclosure. If APOE becomes relevant to an actual anti-amyloid treatment discussion, use clinician-directed testing and the current drug label; do not extrapolate treatment eligibility or safety from a consumer report.

## AMD: ARMS2 and CFH

ARMS2/CFH associations reflect susceptibility to age-related macular degeneration, not evidence of retinal disease. They do not justify preventive high-dose supplements in an unaffected person. [NEI AREDS/AREDS2 guidance](https://www.nei.nih.gov/eye-health-information/clinical-trials/age-related-eye-disease-studies-aredsareds2/aredsareds2-frequently-asked-questions) explains that eye examination is more useful for management, that genotype does not determine supplement selection, and that the studied supplements did not benefit people with no AMD or early AMD. Treatment follows retinal findings and clinical stage. Do not recommend genotype-specific zinc omission or an AREDS regimen from raw SNPs. The [AREDS report 38 analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC4253656/) found no clinically significant CFH/ARMS2 interaction supporting genotype-guided supplement management.

## Celiac HLA tags

A tag SNP marks an associated haplotype in a population; it is not complete HLA-DQA1/DQB1 typing. Linkage patterns and performance may vary by ancestry. Selected tags can miss relevant haplotypes, so a negative tag result cannot inherit the exclusion value of comprehensive clinical HLA typing. FDA describes an authorized selected-variant celiac report as reporting a variant associated with HLA-DQ2.5, not all celiac-related variation.

[NIDDK diagnostic guidance](https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/diagnosis) notes that DQ2/DQ8 presence is not a diagnosis and many carriers never develop celiac disease. Clinical absence makes disease very unlikely, but must be interpreted against the assay's actual coverage. Symptoms, family history, serology and appropriate biopsy pathways matter. Do not start a gluten-free diet before diagnostic testing solely because of a genetic tag; gluten avoidance can interfere with testing.

## CCR5: resistance is not immunity

CCR5 delta32 is a 32-base-pair deletion, not interchangeable with an arbitrary nearby SNP. Even a clinically confirmed homozygous deletion cannot establish immunity to HIV: infection through CXCR4-using virus has been documented. A proxy or an ambiguous array indel warrants additional caution. See the [primary report of infection in a homozygous individual](https://pubmed.ncbi.nlm.nih.gov/9621067/). Genetic information does not remove the need for ordinary HIV prevention, testing or post-exposure clinical assessment.

## Pharmacogenomics: incomplete alleles are not complete phenotypes

A measured functional SNP can be a useful discussion lead, but clinical star alleles/diplotypes may require additional variants, phase and structural information. An untested allele must not default automatically to *1 or normal metabolizer. CYP2D6 is particularly complicated by deletions, duplications and hybrid genes; see [CPIC structural-variant discussion](https://files.cpicpgx.org/data/guideline/publication/atomoxetine/2019/30801677-supplement.pdf). Report observed variants separately from provisional allele or phenotype inference.

Use the current gene-drug CPIC guideline and clinically validated genotype when a real medicine decision arises. Enzyme inhibition, co-medications and organ function can change the practical phenotype. Pharmacogenomics does not explain every treatment failure or adverse effect. The [2023 CPIC serotonin-reuptake inhibitor guideline](https://files.cpicpgx.org/data/guideline/publication/serotonin_reuptake_inhibitor_antidepressants/2023/37032427.pdf) distinguishes supported CYP recommendations from weaker pharmacodynamic-marker claims. Do not tell a person to start, stop or alter treatment from consumer raw data.

## Polygenic scores and ancestry

A disease percentile is a position in a specified reference distribution, not the chance of developing disease. A raw score cannot be interpreted without its exact model, variant weights, effect-allele alignment, assembly, handling of missing/imputed data, reference cohort and validation. Sparse collections of popular SNPs are not interchangeable with a validated PRS. Report ancestry portability, discrimination and calibration; combine appropriately validated genetic estimates with clinical factors rather than replacing them.

[NHGRI's 2024 account of multi-ancestry validation](https://www.genome.gov/news/news-release/researchers-optimize-genetic-tests-for-diverse-populations-to-tackle-health-disparities) describes the need to improve transfer across populations. Genetic ancestry estimates depend on reference panels and analytical choices; do not use ethnicity labels as exact biological predictors or fabricate precise nationality percentages. Do not claim a score is clinically actionable solely because it is published.

## Useful reporting pattern

For each prioritized finding record: observed call and coverage; technical confidence; confirmed versus inferred state; exact variant/condition; source date and review status; what the evidence supports; what it does not establish; practical next discussion; and urgency grounded in symptoms rather than database language. Keep an audit appendix for unreviewed candidates. Explicitly distinguish not tested, not detected and clinically ruled out.

## Source reading ledger

All access attempts below: 2026-10-08. Source IDs are in the canonical sources.json register and source map. Search-result excerpts are not full-text review. Tool access failures are stated rather than concealed.

| Source | URL | Read scope | Limitation |
|---|---|---|---|
| [S221] GATK germline short-variant discovery | https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels | Opened extracted official page; expected BAM input and read-based calling reviewed | Sequencing workflow, not array validation |
| [S222] Ensembl VEP cache documentation | https://www.ensembl.org/info/docs/tools/vep/script/vep_cache.html | Opened extracted official documentation; redirected to June 2026 archive | Tool annotation documentation, not clinical interpretation |
| FDA DTC tests | https://www.fda.gov/medical-devices/in-vitro-diagnostics/direct-consumer-tests | Opened full extracted page; limitations, authorized examples and FAQ inspected | US regulatory examples; authorization does not transfer to other vendors or raw exports |
| [S223] NCBI ClinVar review status | https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/ | Opened extracted documentation; star definitions and aggregation read | Documentation, not review of any individual variant |
| [S224] ACMG/AMP 2015 sequence interpretation | https://pmc.ncbi.nlm.nih.gov/articles/PMC4544753/ | Search excerpt for categories and VUS rule; direct open hit CAPTCHA | Full guideline not read; gene-specific current specifications need separate review |
| [S225] Tandy-Connor et al. 2018 | https://pubmed.ncbi.nlm.nih.gov/29565420/ | Search abstract/excerpts, including publisher result for 40% statistic; PubMed open empty and PMC CAPTCHA | Selected referral study; not a population-wide error estimate |
| [S226] NIA Alzheimer's genetics | https://www.nia.nih.gov/health/alzheimers-disease-genetics-fact-sheet | Search excerpt on APOE prediction and counseling; direct open failed 405 | No detailed numerical risk tables reviewed |
| [S227] NEI AREDS FAQ | https://www.nei.nih.gov/eye-health-information/clinical-trials/age-related-eye-disease-studies-aredsareds2/aredsareds2-frequently-asked-questions | Detailed search excerpts: no/early AMD and genetic-testing sections | Full page not opened |
| [S228] AREDS report 38 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4253656/ | Search excerpts on supplement interactions/conclusions | Full text not read |
| [S229] NIDDK celiac diagnosis | https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/diagnosis | Opened extracted page; genetic-testing and pre-diet testing guidance | Not a complete current specialist diagnostic guideline |
| [S230] CCR5/CXCR4 primary infection report | https://pubmed.ncbi.nlm.nih.gov/9621067/ | Search abstract excerpt | Historical mechanistic counterexample; not an estimate of current HIV risk |
| [S231] CPIC atomoxetine supplement | https://files.cpicpgx.org/data/guideline/publication/atomoxetine/2019/30801677-supplement.pdf | Search excerpt on CYP2D6 structural/hybrid variants | Historical supplement; current gene-drug page must be checked before application |
| [S232] CPIC antidepressants 2023 | https://files.cpicpgx.org/data/guideline/publication/serotonin_reuptake_inhibitor_antidepressants/2023/37032427.pdf | Search excerpts on guideline scope, modest proprietary-panel evidence and supported CYP markers | Full tables not read; no dosing advice derived |
| [S233] ClinGen gene-disease validity | https://www.clinicalgenome.org/docs/gene-disease-validity-classification-information/ | Search excerpts of framework and definitions | No individual gene-condition curation reviewed |
| [S234] ClinGen actionability | https://www.clinicalgenome.org/curation-activities/clinical-actionability/browse-curations/ | Search excerpt of protocol and intervention-outcome purpose | No individual actionability score reviewed |
| [S235] NHGRI diverse-population risk testing | https://www.genome.gov/news/news-release/researchers-optimize-genetic-tests-for-diverse-populations-to-tackle-health-disparities | Opened extracted release on 2024 multi-ancestry work | Agency research summary, not model-specific validation |

Maintenance: review variant-level annotations at use time; refresh guideline/label statements when a real clinical decision arises. Technical safeguards and the suggested report structure are editorial recommendations for an auditable workflow, not laboratory validation or a completed clinical interpretation.

## Reusable implementation and current source refresh

Use the bundled genetic-analysis-workflow.md guidance, staging, MHTML extraction, marker inventory, local ClinVar download/index/annotation and candidate-summary helpers. Reuse existing private SQLite observations and a public reference cache rather than regenerating extraction code. `recheck --source --output` reapplies current candidate policies to stored observations/INFO without repeating a complete reference join; it cannot refresh the reference itself. Reference changes require a new local annotation and dated comparison.

Coordinate and identifier must be reviewed together for arrays. A mismatched rs identifier is a flag, not permission to correct the source or infer a complement. Compare known reference coordinates locally when an identifier is absent; aliases may be missing from the partial SNP index. No-call, absent identifier, reference-only call and a clinically negative condition are different statements. A repeated allele token on X/Y does not establish two biological copies, ploidy or a chromosome diagnosis; retain the representation and seek assay clarification where consequential.

The optional Genetics sidebar renders separately reviewed private text, source metadata and searchable/paginated candidate records. Classification, review status and technical flags remain distinct; priorities are operational review signals, not numerical disease probabilities. The entire per-person model and outputs stay outside the public checkout. Full raw calls and all annotation records remain in separate private databases, rather than time-series clinical observations.

WHO released a second edition of dementia-risk guidance on July15 2026. Its overview and official announcement were read [S247,S248]; not every guideline table was reviewed. General risk-factor management does not establish an APOE-specific prevention percentage. The announcement advises against preventive vitamin/omega-3/multivitamin supplementation without a diagnosed deficiency. Refresh exact guidance for an actual clinical decision. Common MTHFR variants do not establish inability to process folic acid [S240], and lactase-persistence markers are distinct from present symptoms or secondary disease [S241,S242].
