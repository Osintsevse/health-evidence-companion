# Publication and platform review

This release is a portable Agent Plugins package: root `plugin.json`, immediate `skills/` directories and bundled relative references. It contains no MCP server, app mapping or lifecycle hooks. The core requires no user-run server or paid medical API.

## Current route

The publisher uses the OpenAI Plugins upload process with the owning organization/project and verified developer identity. Upload the plugin ZIP, inspect metadata/skill scan findings, resolve them, submit for review and publish only after approval. Use public links that are accessible and match the publisher; confirm the dashboard category and developer identity rather than assuming the working metadata is approved.

This repository cannot confer publisher verification, directory acceptance or account installation rights. An archive passing local tests is only an upload candidate. Do not bypass findings by disguising medical purpose. Earlier informational health skills in this project were rejected by a server safety scan without detailed reasons; those attempts do not establish approval for this package.

## Medical scope and privacy

The reviewed guidelines prohibit collecting, soliciting or processing PHI. This public package therefore provides general education, research, product explanations and blank record design, without an individual archive or identifiable-document workflow. It does not diagnose, prescribe or manage psychiatric treatment. Whether the platform accepts its specific medical scope remains a review decision; no eligibility guarantee is made.

Keep real data and secrets out of metadata, examples, test materials and ZIPs. No publisher backend receives conversations through package code. The host's own privacy controls remain applicable.

## Versions and extensions

GitHub release publication and OpenAI plugin publication are separate. Changed metadata/skills need a new complete ZIP and the platform update flow. Do not promise automatic synchronization from GitHub.

The current submission documentation does not support adding an MCP server to an already created skills-only plugin. A future source-access/backend integration should be planned as a separate plugin/submission unless that platform limitation changes. It needs its own transport, data-handling and review work; no external service is connected by this release.

## Before submission

- Version 0.2.1 uses **Healthcare**, an accepted category matching the medical-information purpose. The 0.2.0 dashboard questioned Productivity and requested a privacy-policy review. The expanded policy now explicitly covers data categories, purposes, recipients, retention and user controls. Upload 0.2.1 and check actual findings again; source edits do not clear dashboard findings or establish approval.
- Verify repository, privacy, terms and support URLs are genuinely public and identify the publisher.
- Confirm name/subtitle lengths, version, included square icon and every relative path.
- Run project checks and inspect synthetic workflow outputs; state limits honestly.
- Inspect actual automated findings and resolve them substantively.
- Confirm required verification and policy attestations in the publisher dashboard.

Official primary sources, checked 2026-10-07: [packaging](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission), [accepted categories and upload errors](https://developers.openai.com/plugins/deploy/submission-errors), [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines). Re-read before publishing because rules may change.
