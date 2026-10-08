# Health Evidence Companion

A community-maintained adult health knowledge base and seven AI skills, distributed through **GitHub Releases and manual installation**. English source content; answers in your language. No required medical API, local server or paid backend.

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
| `health-contribute` | Add studies/topics/corrections through owner-reviewed GitHub PRs |

Examples: "Compare possible causes of these symptoms and what would distinguish them", "What can I safely check at home and when should I seek care?", "Explain these non-identifying laboratory values", "Check this medicine combination and the unknown ingredients", "Review this study and open a PR for the maintainer". Ask naturally; no method selection required.

## Extend the project

**[Contribution workflow and copyable prompts](docs/contribution-workflow.md)** · **[Contribution rules](CONTRIBUTING.md)** · **[Propose research](https://github.com/Osintsevse/health-evidence-companion/issues/new/choose)**

Ask the assistant to review a public study/guideline, update the general knowledge and open a pull request (GitHub's name for a merge request). A connected GitHub account and appropriate tools/permissions are needed to submit it. Without them, the assistant prepares an evidence card and PR draft. `@Osintsevse` reviews and approves; there is no automatic merging or self-approval. CI checks files, not clinical truth.

## Knowledge, sources and privacy

All existing modules are retained: 140 registered sources, allergy, laboratory literacy, dated Serbia/Russia vaccination landmarks, pharmacology, interaction evidence and the indication-specific treatment/homeopathy watchlist. Module 19 adds practical symptom/self-care workflows; module 20 adds an owner-authorized private document/history workflow with eight new data/storage references. Primary sources are checked for consequential claims; reading status, source dates, uncertainty and remaining coverage gaps stay explicit. See [index](knowledge/00_INDEX.md), [watchlist](knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md) and [validation](docs/validation.md).

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
