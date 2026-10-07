# Health Evidence Companion

An English-language, skills-based plugin for adult medical information in ChatGPT. It helps people understand health questions, navigate primary sources, explain medicines and interactions, assess research and prepare useful questions for a healthcare professional. It answers in the user's language.

[Download latest plugin ZIP](https://github.com/Osintsevse/health-evidence-companion/releases/latest/download/health-evidence-companion.zip) | [Browser quick start](docs/quick-start.md) | [All releases](https://github.com/Osintsevse/health-evidence-companion/releases)

The core requires no local Codex installation, local server or paid medical API. A supported ChatGPT plugin surface and its own plan/workspace permissions are still required. This is an informational assistant: it does not establish diagnoses, prescribe, change treatment or replace clinical care.

## Skills

| Skill | Purpose |
|---|---|
| `health-explain` | Adult health questions, possible causes, tests, prevention and source navigation |
| `health-medicine-info` | Ingredients, mechanisms, exact product labels, interactions and uncertainty |
| `health-research` | Guideline and research retrieval with critical appraisal |
| `health-mental-health` | Psychiatry and psychiatric medicine information |
| `health-record-design` | General private-archive rules and blank templates |
| `health-contribute` | Sourced general knowledge contributions for maintainer review |

Examples: "What do doctors consider when an adult cough persists?", "How does benzydamine work?", "What does the evidence say about zinc for colds?", "Explain the interaction mechanisms of SSRIs and NSAIDs", "Show a blank medicine-history template." Ask in any language the host supports; no method selection is needed.

## Browser installation and distribution

Send a friend this repository link and direct them to the **Browser quick start** above. Before directory publication, they can use the ZIP as reference material to create a personal copy through Plugin Creator if their account supports it. The guide includes a copy-and-paste prompt, access checks and update instructions. This guided creation route is not a universal ZIP installer and has not been tested in a separate friend's account.

Use the **plugin ZIP release asset**, not GitHub's automatically generated source-code ZIP. After public platform approval/publication, users can install from the directory on supported browser surfaces. Authorized sharing/workspace import options depend on account access. An arbitrary GitHub URL does not automatically install a plugin into every ChatGPT account.

See [installation](docs/installation.md) and [publication](docs/publication.md). This repository contains an upload candidate, not evidence of platform approval. Skills are installed snapshots: new knowledge needs a new package upload/update, not merely a GitHub merge.

## Knowledge and privacy

The English library retains the original general modules and adds allergy, laboratory literacy, vaccination and treatment-evidence/homeopathy modules. It has 128 registered sources, including three marked secondary discovery lists, additional free-tool research and five blank template files. It prioritizes Serbian ALIMS, Russian GRLS/clinical guidelines, WHO and relevant international primary sources. Reading status and gaps are explicit; this is not a completed medical degree or validated diagnostic model.

The medicine workflow checks evidence for the exact indication before endorsing efficacy. It separates unsupported claims, guideline recommendations against, uncertain effects and pending appraisal rather than treating a brand list as a universal ban. See the [knowledge index](knowledge/00_INDEX.md), [treatment watchlist](knowledge/18_TREATMENT_EVIDENCE_AND_HOMEOPATHY.md) and [repository review](docs/review-2026-10-06.md).

**Only general knowledge and blank forms are allowed.** Never contribute actual histories, anonymized real cases, identifiable documents, private links or personal medicine lists. The public plugin does not maintain patient records, solicit PHI or connect to a clinical archive. General record rules are included so people can design a separate private system. See [knowledge policy](knowledge/00_KNOWLEDGE_POLICY.md), [privacy](PRIVACY.md) and [security](SECURITY.md).

No third-party interaction dataset, medical model weights or copyrighted textbook corpus is bundled. Free integrations and the earlier optional licensed DrugBank adapter are research examples, excluded from the plugin ZIP.

## Contributing

Fork, create a branch, add original English knowledge with primary sources and explicit scope/limitations, run checks and open a pull request. The maintainer reviews evidence and approves changes. See [CONTRIBUTING.md](CONTRIBUTING.md). CI does not validate clinical accuracy.

## Developer commands

Python 3.11+ and its standard library suffice for the core build:

```sh
python3 scripts/update_registry.py
python3 scripts/sync_references.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s examples/drugbank -v
python3 scripts/build.py
```

`dist/` receives versioned plugin/source ZIPs, the stable `health-evidence-companion.zip` download, `SETUP.md`, `SETUP_PROMPT.txt`, checksums and a build report. CI runs checks on PRs/main. After a `plugin.json` version change reaches reviewed `main`, the release workflow validates/builds and creates `vX.Y.Z` plus a public GitHub Release automatically. Workflow changes bootstrap a missing release; manual runs on `main` can retry. Existing published versions are retained without overwrites. No local execution is needed by browser end users. See [maintainer setup](docs/maintainer-setup.md) for required repository protection.

MIT applies to original project code/instructions/notes. External sources retain their rights. See [NOTICE.md](NOTICE.md).
