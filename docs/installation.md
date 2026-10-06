# Installation in ChatGPT

For browser users, the intended distribution route is an approved directory plugin or an authorized workspace import. A GitHub checkout/local marketplace is a developer route and is not a universal browser installation mechanism. End users do not need Codex, Python or an MCP server for the skills-only core.

## Publisher or workspace importer

### Download the correct archive

For a stable version, open [GitHub Releases](https://github.com/Osintsevse/health-evidence-companion/releases) and choose the maintainer-created `health-evidence-companion-X.Y.Z.zip` under Assets. Releases appear only after a reviewed version tag has successfully run; a PR or merge alone creates no release.

For a candidate, open [GitHub Actions](https://github.com/Osintsevse/health-evidence-companion/actions), select a successful **Package checks** run for the intended PR or `main` commit, then download **health-evidence-companion-candidate** from Artifacts. GitHub sign-in may be required. This is an automatically generated artifact wrapper: extract it and use the inner `health-evidence-companion-X.Y.Z.zip`. The accompanying `-source.zip`, `SHA256SUMS.txt` and `build-report.json` are separate developer/verification files. Candidate artifacts expire after fourteen days; a newer successful run creates another one.

### Use the available publishing/import route

1. Download the versioned `health-evidence-companion-X.Y.Z.zip` release asset. Do not use the source archive or GitHub's generic source ZIP.
2. Check the accompanying SHA-256 checksum if desired.
3. Use the plugin upload/import controls available to your account/workspace. For public submission, follow `publication.md` and the current official publisher dashboard.
4. Inspect metadata/skill findings, resolve them and complete the applicable review. An upload candidate is not a directory-approved plugin.
5. Install/enable the resulting plugin on a supported ChatGPT surface and try a general question in your language. Browse availability and workspace policy affect behaviour; the package cannot grant those capabilities.

There is no documented universal ZIP/YAML import button available to every browser account. Public submission uses the publisher process. Workspace admins may import a GitHub marketplace where supported, which needs the applicable marketplace layout/catalog; this source repository currently contains a portable plugin package, not a configured team marketplace. If Plugin Creator is available in a personal/workspace account, use it to create/edit an eligible plugin through a conversation with the instructions/reference files. That availability is separate from accepting this ZIP as a public submission.

The package manifest is root `plugin.json`; the per-skill YAML files contain instructions/UI metadata. They are not themselves a marketplace installation file.

## Ordinary users after publication

Open ChatGPT's Plugins tab, find Health Evidence Companion if it is published and available to your account, open its details and select the plus/install button. Start a new chat and choose it with an @ mention under Plugins where supported. Ask naturally in your preferred language. Use general health questions and public product information; do not supply PHI or an identifiable archive for this public package to process. This repository does not establish directory publication.

## Updates

The knowledge and skills are snapshots. A GitHub merge does not update an installed plugin. The publisher uploads a new versioned ZIP, resolves findings and publishes the eligible reviewed version. A host may have its own update controls.

No remote interaction engine is connected by the core package. Research notes describe candidates; they are not installation steps for required services. Personal record management is outside this public release.

Official routes reviewed 2026-10-06: [package guide](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission), [skills](https://developers.openai.com/plugins/build/skills). Recheck these when the host changes.

Browser controls and permissions: [Plugins](https://learn.chatgpt.com/docs/plugins), [Build plugins](https://learn.chatgpt.com/docs/build-plugins).
