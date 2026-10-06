# Repository and release setup

Target owner: `Osintsevse`. Target source repository: `health-evidence-companion`. The package uses these planned links; confirm actual repository creation before claiming they are live.

## After repository creation

Push the prepared English source tree to `main`. Enable GitHub Actions. Ensure the owner has the authority to review/merge and `CODEOWNERS` resolves to `@Osintsevse`. The first push should produce the `validate-and-build` check and downloadable artifacts.

Configure protection/rules for `main`: require a PR, require code-owner review with one approval, dismiss stale approvals, require `validate-and-build`, block force pushes/deletion and resolve conversations. Review bypass settings deliberately. CODEOWNERS alone requests review; it does not enforce it. The repository administration operation must actually complete before describing the branch as protected.

This owner-review arrangement is for contributor PRs. A maintainer cannot approve their own authored PR. Do not manufacture a second reviewer; decide and document a narrow maintainer exception or obtain an independent reviewer where required.

Allow only approved Actions; use read-only default workflow permissions. The release workflow has write permission only in its tag-triggered job. Fork PR code is never executed with publisher secrets or `pull_request_target`. Review workflow modifications as carefully as content.

Optional: enable private vulnerability reporting, issues and discussions as desired. Do not claim private reporting works until enabled. Public discussion must never contain real patient data.

## Contributions and releases

Contributors fork and open PRs. Owner review checks evidence, limits, license and privacy in addition to CI. After merging a reviewed release, increment `plugin.json` and changelog, then create a matching version tag such as `v0.1.0`.

The tag workflow builds the installable ZIP and source archive, checks the version/tag match and creates a GitHub release with checksums. It publishes no plugin to OpenAI automatically. Upload that release's plugin ZIP through the publisher process. If the GitHub action is disabled or fails, inspect the run; do not describe the pipeline as verified from a local test alone.

## Administrative automation

`scripts/configure_github.py` provides an explicit maintainer CLI route for creating the public repository, pushing the source and applying branch protection. It requires a separately authenticated `gh` CLI with repository administration rights. Use `--execute` only after reviewing its printed plan; it never prompts for or writes a token. This is developer tooling, not a browser-user requirement. Availability/permissions/plan restrictions can prevent administrative operations; inspect returned errors and verify settings.

Sources: [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
