# Installation and updates

Start with [manual quick setup](quick-start.md) and its [setup prompt](setup-prompt.txt). The target is GitHub distribution with manual personal/workspace installation where the host allows it. Public-directory publication is not planned for this edition.

## Which download to use

- [Latest plugin ZIP](https://github.com/Osintsevse/health-evidence-companion/releases/latest/download/health-evidence-companion.zip): stable asset name for friends.
- [GitHub Releases](https://github.com/Osintsevse/health-evidence-companion/releases): fixed `health-evidence-companion-X.Y.Z.zip`, source archive, setup files, SHA256SUMS.txt and build report.
- [GitHub Actions](https://github.com/Osintsevse/health-evidence-companion/actions): successful Package checks candidate artifacts for proposed versions; extract the artifact wrapper to obtain the inner plugin ZIP. GitHub sign-in may be required; artifacts expire after fourteen days.

The stable and versioned plugin ZIPs have identical bytes in a release. GitHub's generic source ZIP and the project's `-source.zip` are contributor files, not the plugin package. `plugin.json` is at archive root; SKILL.md/UI YAML are skill metadata, not import commands.

## Routes and limitations

Personal copy: use Plugin Creator with attached reference material or a direct import/upload control only if the account offers it. Verify version, included relative references and actual install confirmation. The setup prompt describes the medical purpose honestly and retains all safety/privacy rules. No universal browser ZIP-import button or guaranteed recreation is claimed.

Workspace: an eligible admin can import the root marketplace catalog from GitHub and configure roles/sync. `.agents/plugins/marketplace.json` references the root portable package. This does not grant GitHub contribution permissions or clinical-data authorization.

Local Codex: use the available skill installer for this repository's nineteen `skills/` folders or the documented user `.agents/skills/` location. Preserve references and unrelated installed skills. Local installation does not create a browser plugin.

Supported ordinary Project reference use is described in the quick setup. It is not a plugin installation and must not be used to bypass a medical-policy rejection. All routes remain subject to host policies, scans, account availability and permissions. No separate friend's account/workspace installation has been verified.

## Updates and contributions

For personal snapshots, download a new released ZIP and update through the copy's permitted edit workflow, then verify version and a sample response. GitHub merge/release does not update installed copies automatically. Workspace GitHub sync has separate controls; fixed tags do not follow new versions.

See [contribution workflow](contribution-workflow.md) for adding studies with PR review. A successful PR is a proposal, not a merged change, installed update or clinical approval.

Official sources checked 2026-10-07: [Build plugins](https://learn.chatgpt.com/docs/build-plugins), [Plugins](https://learn.chatgpt.com/docs/plugins), [GitHub workspace import](https://learn.chatgpt.com/docs/enterprise/plugin-management), [Local skills](https://learn.chatgpt.com/docs/build-skills).

Version 0.6.0 also includes the six psyops-* psychology skills. Read [combined-package migration](unification.md) before replacing a standalone PsyOps installation. Existing private archives are not moved or connected by package installation.
