# Health Evidence Companion: browser setup

[Download the latest plugin ZIP](https://github.com/Osintsevse/health-evidence-companion/releases/latest/download/health-evidence-companion.zip) | [All releases](https://github.com/Osintsevse/health-evidence-companion/releases) | [Setup prompt](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/setup-prompt.txt)

The ZIP contains English instructions and general medical references. Answers use your language. You do not need local Codex, Python, a server or a medical API key. Your ChatGPT account must support the creation or installation route you choose. A public GitHub repository does not grant ChatGPT plugin access.

## Use a personal copy before public directory publication

1. Download `health-evidence-companion.zip` using the link above. Keep it as a ZIP; do not use GitHub's generic source-code download or the `-source.zip` asset.
2. Open a new ChatGPT conversation, preferably Work for inspecting the archive. Type `@` and select **Plugin Creator** if it is available to your account/workspace.
3. Attach the ZIP as reference material. Copy the [setup prompt](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/setup-prompt.txt) into the conversation and send it.
4. Ask the creator to preserve the six bundled skills and their relative references. Review its actual output and complete any creation/install prompts. Ask it to report the package version and any omitted or inaccessible files.
5. Open a new conversation, select **Health Evidence Companion** with an `@` mention, and try a general question such as "Explain why antibiotics usually do not help an adult viral cold. Cite current primary sources and answer in Russian."

This is a guided personal-creation workflow using the package as input. Official documentation supports creating plugins with reference files; it does not document a universal ZIP importer for every browser account or guarantee a byte-for-byte recreation of this repository. If the creator cannot inspect the ZIP, extract it and attach the requested `SKILL.md` and reference files. If Plugin Creator is missing or creation is denied, the repository cannot unlock that feature; use an authorized shared/workspace plugin or wait for public publication. The friend setup has not been tested in a separate user's account.

## Use a plugin shared by its creator

If the maintainer supplies a ChatGPT plugin link, open it in the intended account/workspace and install the plugin if permitted. Access sharing and installation are separate. Workspace sharing requires the relevant permissions and does not imply availability to unrelated personal accounts. A GitHub URL is a source/download link, not this installation link.

## Use the public directory after publication

If Health Evidence Companion has been approved and published to the ChatGPT Plugins directory, open its listing and select the plus/install button. GitHub release publication alone does not create a directory listing. Public directory submission requires developer identity verification and platform review; personal creation is a separate route.

## Updates

Installed personal copies are snapshots. To update, download the new ZIP, open the plugin's **Edit Plugin** conversation and ask Plugin Creator to replace its instructions/reference files from that version while preserving the six workflows. Check the reported version and repeat the sample question. A GitHub release does not automatically update those copies.

Use general health questions and public product information. This distributed package contains only general knowledge and blank forms; personal medical archives belong in a separate private system.

Sources checked 2026-10-07: [Build plugins](https://learn.chatgpt.com/docs/build-plugins), [Use and install plugins](https://learn.chatgpt.com/docs/plugins), [Package and workspace distribution](https://developers.openai.com/plugins/build/plugins), [Public submission](https://developers.openai.com/plugins/deploy/submission).
