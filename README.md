# Health Evidence Companion

A community-maintained medical and adult psychology knowledge base and fifteen AI skills, distributed through **GitHub Releases and manual installation**. English source content; answers in your language. No required medical API, local server or paid backend.

Supports symptom reasoning, possible-diagnosis comparisons, checking self-diagnosis hypotheses, safe home observations, basic self-care and OTC label information, laboratory-result explanations, medicine interactions, psychiatry information, research appraisal and clinician preparation. Every health-facing answer includes a short disclaimer. It does not establish a diagnosis, independently prescribe/change prescription treatment or replace examination and clinical care. It is not intended for use as a medical device; no clinical validation or legal exemption is claimed.

## Install or send to a friend

**[Download plugin ZIP](https://github.com/Osintsevse/health-evidence-companion/releases/latest/download/health-evidence-companion.zip)** · **[Quick setup](docs/quick-start.md)** · **[Setup prompt](docs/setup-prompt.txt)** · **[Releases](https://github.com/Osintsevse/health-evidence-companion/releases)**

Use the maintainer's plugin ZIP, not GitHub's generic source archive. Create/import a personal or workspace copy only through controls available to your account. Manual installation can still be scanned or refused by ChatGPT; this project does not bypass platform policy and is not targeting public directory approval. The setup guide also describes local skill installation and using the material as ordinary project reference files when supported.

## Skills

| Skill | Purpose |
|---|---|
| `health-explain` | Symptom assessment, differential hypotheses, urgency, safe self-checks, self-care, laboratory and vaccine questions |
| `health-medicine-info` | Exact ingredients/forms, evidence, OTC labels, medicine-list and interaction checks |
| `health-research` | Guidelines, studies, systematic reviews and critical evidence appraisal |
| `health-mental-health` | Psychiatry concepts, symptom/medicine-effect explanations, monitoring and clinician questions |
| `health-record-design` | Blank private-record design, provenance, medicine reconciliation and unknown fields |
| `health-record-import` | Owner-authorized photo/PDF import, preserved originals, source-linked history, corrections, retrieval and charts in private storage |
| `health-family-care` | Child and pregnancy pathways, reproductive health, specialty navigation and rehabilitation |
| `health-prevention` | Screening, nutrition, healthy ageing, shared decisions and truthful insurance support |
| `health-contribute` | Add studies/topics/corrections through owner-reviewed GitHub PRs |
| `psyops-dialogue` | Adult supportive reflection, emotions and meaning |
| `psyops-cbt-act-mct` | Optional structured CBT, ACT and MCT self-help |
| `psyops-relationships` | Relationships, consent and genuinely shared conversations |
| `psyops-sport` | Sport and motorsport psychological preparation |
| `psyops-research` | Appraise psychology/sport methods and public evidence |
| `psyops-private-records` | Separately authorized private psychological notes |

Examples: "Compare possible causes of these symptoms and what would distinguish them", "What can I safely check at home and when should I seek care?", "Explain these non-identifying laboratory values", "Check this medicine combination and the unknown ingredients", "Review this study and open a PR for the maintainer". Ask naturally; no method selection required.

## Extend the project

**[Contribution workflow and copyable prompts](docs/contribution-workflow.md)** · **[Contribution rules](CONTRIBUTING.md)** · **[Propose research](https://github.com/Osintsevse/health-evidence-companion/issues/new/choose)**

Ask the assistant to review a public study/guideline, update the general knowledge and open a pull request (GitHub's name for a merge request). A connected GitHub account and appropriate tools/permissions are needed to submit it. Without them, the assistant prepares an evidence card and PR draft. `@Osintsevse` reviews and approves; there is no automatic merging or self-approval. CI checks files, not clinical truth.

## Knowledge, sources and privacy

All existing medical modules are retained: 250 medical source records, allergy, laboratory literacy, dated Serbia/Russia vaccination landmarks, pharmacology, interaction evidence and the indication-specific treatment/homeopathy watchlist. Module 19 adds practical symptom/self-care workflows; module 20 adds an owner-authorized private document/history workflow with eight new data/storage references. Primary sources are checked for consequential claims; reading status, source dates, uncertainty and remaining coverage gaps stay explicit. See [index](knowledge/00_INDEX.md), [watchlist](knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md) and [validation](docs/validation.md).

Relevant voluntarily supplied symptom/medicine/test details can inform the authorized host conversation. They never enter this public repository, PRs, releases, logs, web-search queries or a training corpus. Do not include identifiers or entire histories. The package has no publisher backend or automatic patient archive; private storage/sharing requires separate authorization. See [policy](knowledge/00_KNOWLEDGE_POLICY.md), [privacy](PRIVACY.md) and [security](SECURITY.md).

No copyrighted textbook corpus, third-party interaction dataset or medical model weights are bundled. Optional integration research and the licensed DrugBank example remain outside the plugin ZIP. MIT covers original code/instructions/notes; external sources retain their rights ([NOTICE](NOTICE.md)).

## Keep a private medical history

Use [private archive setup](docs/private-archive-setup.md) and [document/history rules](knowledge/20_PRIVATE_DOCUMENT_IMPORT_AND_HISTORY.md). The preferred Drive layout preserves received photos/PDFs separately and uses one native Google Sheet for dated laboratory results, visits/recommendations, prescriptions, actual medicine-use events, corrections and an import journal. Each fact links to its source/page; unclear fields remain pending. JSON import snapshots provide an audit/export trail, while charts and summaries are derived views.

The public project contains only general rules, the [row contract](knowledge/archive_tables.json), blank forms and wholly synthetic tests. The executing host needs available, explicitly authorized private storage tools; the package itself connects no account and stores no patient's files. Local storage can use the same contract. [Readable archive views](knowledge/21_READABLE_ARCHIVE_VIEWS.md) describe one reader entry point, a separate system area, vaccination tables, laboratory matrices and repeatable offline views. Optional generators are packaged in the import skill; they create private snapshots only and connect no account. No real patient archive or live upload is exercised by repository tests.

## Build and release

Python 3.11+ and the standard library suffice:

```sh
python3 scripts/update_registry.py
python3 scripts/generate_archive_templates.py --check
python3 scripts/sync_references.py
python3 scripts/sync_platforms.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s examples/drugbank -v
python3 scripts/build.py
```

PR/main CI produces candidate artifacts. After a reviewed version bump reaches main, release automation publishes versioned and stable-name plugin ZIPs, source ZIP, checksums, build report and setup files. Installed personal copies are snapshots and need an explicit update. GitHub publishing does not install or publish anything in ChatGPT. See [maintainer setup](docs/maintainer-setup.md) and [distribution boundaries](docs/publication.md).

- [22: Laboratory identity and owner feedback](knowledge/22_LAB_IDENTITY_AND_FEEDBACK.md) - multilingual display grouping, unit/scale distinctions and persistent clarification answers.

## Codex and Claude

See [platform setup](docs/platforms.md) for Codex CLI/desktop, Claude Code and individual Claude chat/Cowork skill ZIPs. All use the same general instructions. The default private archive now includes source-linked transposed labs, date-ordered diagnosis summaries, separate allergies, medication-use timelines and a clarification page with explicit transfer and collapsed accepted answers. Actual records remain outside this repository.

The medication timeline includes a horizontal scale, supported course bands, uncertain-date windows, contextual topic filters and source-linked details. Current-use panels require a dated accepted reconciliation; historical mentions stay separate.

## Small updates and save recovery

[Module 24](knowledge/24_INCREMENTAL_ARCHIVE_SAVES.md) defines an incremental path for conversation facts, corrections, save-status checks and unfinished operations. Keep the configured ledger authoritative, distinguish a supplement from a committed/read-back record, and refresh changed managed views only. The optional standard-library sync planner produces private candidates; it uploads nothing and provides no remote lock or background synchronization.

[Laboratory graphs and health review](knowledge/25_LAB_GRAPHS_AND_HEALTH_REVIEW.md) separates offline numeric flags from a substantive, dated source-grounded AI assessment. The optional adapter supports multi-category selection, original links, uncertainty and private follow-up questions; it transmits nothing automatically.

## Curriculum expansion and source maintenance

See [routing](knowledge/26_CLINICAL_ROUTING_AND_SCOPE.md), [learning index](knowledge/27_FOUNDATIONS_AND_LEARNING_INDEX.md), [specialty and life-stage guidance](knowledge/28_SPECIALTY_AND_LIFE_STAGE_ROUTING.md), [prevention](knowledge/29_PREVENTION_NUTRITION_AND_SHARED_DECISIONS.md), [private data boundaries](knowledge/30_PRIVATE_IMAGES_GENETICS_AND_ACTIVITY.md), [source maintenance](knowledge/31_SOURCE_MAINTENANCE.md) and [risk communication](knowledge/32_RISK_COMMUNICATION.md).

Generate a complete offline review queue with `python scripts/source_review.py --as-of 2026-10-08 --interval-days 90`. This plans rechecks; it makes no network requests, does not change reading dates and creates no scheduled monitor. See [expansion audit](docs/knowledge-expansion-2026-10-08.md) for coverage and validation limits.

## Genetic provider exports

[MyHeritage and Genotek intake](knowledge/33_GENETIC_PROVIDER_IMPORT.md) distinguishes health reports, genealogy outputs and raw calls. The optional import-skill helper stages supported CSV/TSV and single-sample textual VCF in a separate private SQLite dataset, with no network or clinical annotation. Actual provider compatibility depends on inspected headers; FASTQ/CRAM processing is not implemented. Raw genotypes are not laboratory time-series points.

Genetic analysis reuses bundled local helpers and a dated public ClinVar cache; see [workflow](docs/genetic-analysis-workflow.md). The optional Genetics sidebar keeps a private, reviewed explanation beside existing archive sections. No patient-specific report or reference database is distributed with the plugin.

## Unified psychology edition

Version 0.6.0 incorporates PsyOps: 102 psychological source records, the complete original knowledge and practice cards, and all six existing skill names. Medical and psychological registers retain separate IDs and actual reading dates. See [migration and provenance](docs/unification.md), [combined routing](knowledge/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md) and [source catalog](knowledge/source-catalog.json). These counts are metadata records, not independent studies or completed courses.

Medical records and full psychological journals remain separately authorized. The optional Psychology sidebar includes only an explicitly selected summary projection; omitting that config produces the medical-only view. Installing this package does not migrate any archive, authorize new recipients or access a diary. For psychological reflection use the relevant psyops-* skill; clinical psychiatric medication questions remain under health-mental-health and health-medicine-info.


### Saving from an external chat

Use [a private inbox](knowledge/36_PRIVATE_INTAKE_QUEUE.md) when this host lacks safe access to the accepted ledger. Connected file upload can queue a source package; otherwise download it and place it manually. Codex or another authorized local processor can review and accept it later. The inbox is not another medical database. No wearable, smart home or home server is required.
