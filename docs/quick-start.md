# Health Evidence Companion: manual setup

[Download latest plugin ZIP](https://github.com/Osintsevse/health-evidence-companion/releases/latest/download/health-evidence-companion.zip) | [Releases](https://github.com/Osintsevse/health-evidence-companion/releases) | [Setup prompt](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/setup-prompt.txt)

English instructions; answers in your language. No required local Codex, Python, server or medical API key for a supported browser installation. The target is a personal/workspace copy, not publication in the public directory. Account features and host medical/data policies still apply; manual installation may be scanned or refused. A ZIP cannot unlock features or bypass a refusal.

## Personal ChatGPT copy

1. Download the maintainer's `health-evidence-companion.zip`, not the generic GitHub source ZIP or `-source.zip`.
2. If your account/workspace offers **Plugin Creator**, start a new chat, select it with `@`, and attach the ZIP as reference material. If it offers a supported direct plugin upload/import control, use that instead.
3. Send the [setup prompt](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/setup-prompt.txt). Preserve all six skills, their references, the medical purpose, practical symptom/self-care workflows and limits. Review which files were actually included and the manifest version.
4. Complete the host's creation/install process only if permitted. In a new chat, select the resulting plugin with `@` and try: "Compare possible causes of an adult cough, safe home observations and when an examination helps; cite current primary sources and answer in my language."
5. To contribute, try: "Review this public study [URL] and open a knowledge PR for Osintsevse. Do not merge." Submission needs available connected GitHub tools and account permissions; otherwise obtain an evidence card and PR draft.

Official guidance documents creation with instructions/reference files. It does not establish a universal ZIP importer or faithful ZIP reconstruction for every account. If the ZIP cannot be inspected, attach extracted SKILL.md/reference files when asked. If host policy rejects the medical workflow, stop that installation attempt; do not disguise the purpose, strip safeguards or retry through another surface to evade the restriction. Personal setup has not been tested in a separate user's account.

## Workspace import

An eligible workspace admin can import this repository's marketplace: **Admin > Plugins > Add > Import marketplace**, repository `https://github.com/Osintsevse/health-evidence-companion`, root path (blank), chosen branch/tag (for example `v0.3.0`). The `.agents/plugins/marketplace.json` catalog references the root portable package. Review import findings and configure eligible roles. A tag pins a snapshot; main allows supported sync. Sharing/installation and access to a connected GitHub account remain separate controls. This import was not exercised in a separate workspace.

## If plugin creation is unavailable

Use supported ordinary ChatGPT Project instructions/reference-file features with the source material where the host permits this medical-information use; this is reference use, not an installed plugin or an exemption from restrictions. Upload only the needed general modules and preserve their policies/source map. Availability, file limits and citations depend on the host. Do not use this path to bypass an explicit policy refusal.

For local Codex, download/clone the repository and ask its skill installer to install the six `skills/` folders with their references. Alternatively, copy them to your local user's `.agents/skills/` directory using the documented local-skill mechanism, preserving existing unrelated skills. This is a local option; it does not install a browser plugin.

## Updating and privacy

Personal copies are snapshots. Download the new ZIP, open the copy's edit workflow, replace the instructions/references, verify version and rerun a sample question. A GitHub merge alone does not update it. Workspace GitHub sync uses its own controls.

Use only necessary symptom, medicine or non-identifying result details in an authorized host conversation. Actual cases must never enter public issues, PRs, releases or search queries. Remove identifiers from documents where practical. The package provides no publisher patient archive or secure storage. Every health-facing answer includes a short disclaimer; it cannot confirm diagnoses or change prescription treatment independently.

Sources checked 2026-10-07: [Build plugins](https://learn.chatgpt.com/docs/build-plugins), [Plugins](https://learn.chatgpt.com/docs/plugins), [Workspace GitHub import](https://learn.chatgpt.com/docs/enterprise/plugin-management), [Local skills](https://learn.chatgpt.com/docs/build-skills).
