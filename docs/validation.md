# Validation status

Initial edition: 2026-10-06. This document distinguishes file checks, workflow evaluation and clinical/platform review.

## Limited independent workflow checks

Three fresh-context agents read the actual skill files and relevant bundled references, then answered ordinary requests. They received the prompt and skill location rather than the rubric or intended answer. No files or external systems were modified.

| Task | Observed behaviour | Limit |
|---|---|---|
| Adult cold/cough general question, Russian | Russian explanation, current CDC/NICE routes, no established diagnosis | One educational question; not triage accuracy testing |
| Synthetic sertraline/ibuprofen/unknown powder question, Russian | Unknown ingredients retained, source access limits disclosed, mechanism and spacing explained without automatic withdrawal or whole-list safety verdict | One synthetic combination; no clinical accuracy estimate |
| Real record inclusion and blank-status question, Russian | Excluded real discharge data even after name removal; empty lists remained unknown; described separate private storage | Record design only; no storage/access-control implementation tested |

Additional reusable cases are in `tests/skill-cases.json`; only the three above were executed during this edition's forward check. Do not present the full case list as executed. These observations are not a medical-device validation, certification or clinician review.

## Local deterministic checks

The project validator checks listing limits, relative links, unique original source IDs/URLs, CSV/JSON agreement, synchronized skill references, English source content, blank JSON templates, icon paths and archive membership. Privacy/secret patterns are heuristic and do not prove absence of all sensitive data.

Mutation tests exercise reproducibility, stale/extra references, missing links/source IDs, filled/unknown templates, private-link handling, invalid metadata, archive traversal/duplicates/unexpected members and symlink rejection. Build reports record actual results/version/checksums. Skill Creator's structural validator is also run on each skill during preparation.

## Version 0.2.1 distribution checks, 2026-10-07

Executed locally: project validation, 34 packaging/release tests, eight optional-adapter offline tests, deterministic package/source builds, release CLI dry run and whitespace checks. The release YAML parsed successfully; main/tag guards, main-only manual dispatch, pinned checkout and job-scoped contents-write permission were inspected. No live GitHub release was created by these tests.

The release tests simulate GitHub state and exercise draft creation, verified assets before publication, interrupted-upload recovery, retained published assets, conflicting commits/assets, failed lookups, missing server assets and rejection of fork/PR/feature-branch publication. They do not prove that the actual Actions token can satisfy repository tag/release rules; the first merged-main release run must verify that.

The plugin archive has 81 members, six skills and 128 registered sources. The stable ZIP is byte-identical to the versioned ZIP. Setup files match their source documents and all five download payloads have recorded checksums. Medical skill instructions are unchanged; the generated contribution reference now describes automatic reviewed-main releases. These are delivery checks, not new clinical evaluations. Personal-copy setup has not been tested in a separate friend's account, and OpenAI checks for the corrected metadata/privacy policy remain pending.

Previously, GitHub Actions run 7 for PR #3 completed successfully, including validation, packaging tests, offline adapter tests and the candidate build. The owner reported branch protection enabled; its administrative settings were not independently fetched.

## Not established

- Clinical accuracy, suitability for diagnosis, clinician-certified content or patient outcomes.
- Live access to optional medical APIs, hosted MCP handshakes or model performance.
- OpenAI metadata/skill scan success, directory acceptance or installation.
- Secure personal record storage or PHI-processing compliance.

Before release, inspect actual tests and build output. Re-run relevant checks after substantive changes, perform additional synthetic forward checks when needed, and obtain the platform's real review outcome.
