# Use the same archive workflow in Codex and Claude

Instructions checked against official host documentation on 2026-10-08. This skills-only package connects to no account, creates no publisher patient store and installs no background service. A host still needs access to the owner's chosen private documents and storage. Local helpers need an available Python runtime; photo previews optionally use Pillow. Use that host's spreadsheet/PDF tools when its runtime differs. The Artifact Tool spreadsheet adapter is optional and is not assumed available in Claude.

## Codex CLI and desktop

Register the repository marketplace and install its root package:

```sh
codex plugin marketplace add Osintsevse/health-evidence-companion
codex plugin add health-evidence-companion@health-evidence-companion-community
```

The second command was checked against the installed Codex CLI help. Restart the desktop app after local package changes. The repository's `.agents/plugins/marketplace.json`, portable `plugin.json` and `.codex-plugin/plugin.json` compatibility overlay declare the same skills and identity. For a contribution preview, add `--ref codex/archive-graphs-review-0.4.4` to the marketplace-add command; use main or a reviewed release tag after merge. Do not assume GitHub changes update an installed snapshot.

A skills-only fallback is to copy each complete `skills/<name>/` directory into a private project's `.agents/skills/` or the user's `~/.agents/skills/`, preserving references/assets/scripts and unrelated existing skills. Do not copy actual records into this repository. A supported workspace GitHub import remains available as described in [manual setup](quick-start.md).

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) and [Codex local skills](https://learn.chatgpt.com/docs/build-skills). Native installation in a separate account is not claimed.

## Claude Code

Install from this repository's Claude marketplace:

```sh
claude plugin marketplace add Osintsevse/health-evidence-companion
claude plugin install health-evidence-companion@health-evidence-companion-community
```

For local development, clone the reviewed branch or extract the plugin ZIP, then launch:

```sh
claude --plugin-dir /absolute/path/to/health-evidence-companion
```

The `.claude-plugin/plugin.json` overlay discovers the same root `skills/` folders. No Codex-only connector, hook or authentication is bundled. After installation invoke `/health-evidence-companion:health-record-import`, or describe the task naturally. If Claude Code is unavailable, local manifest and package checks cannot establish a native installation; test in the target host before relying on it.

Sources: [Claude plugin overview](https://code.claude.com/docs/en/plugins), [marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) and [manifest reference](https://code.claude.com/docs/en/plugins-reference).

## Claude chat and Cowork

Download the release asset `health-evidence-companion-claude-skills.zip`. Extract it: it contains fifteen individual skill ZIPs. In Claude, open **Customize > Skills**, choose **Create skill > Upload a skill**, and upload the needed individual ZIPs. Each contains one named skill folder with `SKILL.md` and its resources. The enclosing bundle is not itself one uploadable skill.

For an archive, start with `health-record-import.zip` and `health-record-design.zip`. Enable other skills for health explanation, medicine information, mental-health education, research and general contributions when needed. Code execution/Skills availability and organization permissions vary. Installation does not grant file or Drive access. Account uploads and Cowork operation were not exercised by the package's local tests.

Sources: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) and [custom skill ZIP layout](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## First archive request and updates

Example request: "Organize these selected reports in my existing private archive at [chosen location]. Preserve originals and source links. Create the standard reader views, a medication-use timeline and a separate clarification page."

The assistant follows modules 20-23, chooses a supported store and keeps one authoritative ledger. It preserves dates, raw values, uncertainty, separate orders/use and corrections. The default reader interface supplies analyte-by-date labs, diagnosis summaries, allergies, medication events, original previews and explicit answer transfer. Existing owner layouts and authorization take precedence. Missing capabilities are reported rather than silently switching storage or claiming a successful write.

When updating, verify the installed version and required resources. Perform a wholly synthetic forward check with an uncertain result, a prescription without use evidence, an explicit use report, and an accepted unknown answer. Confirm sources and uncertainty remain visible; do not use a real archive as a public test. Public distribution and maintainer review are separate from private record maintenance.

Version 0.6.0 also includes the six psyops-* psychology skills. Read [combined-package migration](unification.md) before replacing a standalone PsyOps installation. Existing private archives are not moved or connected by package installation.
