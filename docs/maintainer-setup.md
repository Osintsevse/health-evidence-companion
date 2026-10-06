# Repository and release setup

Owner: `Osintsevse`. Source repository: [health-evidence-companion](https://github.com/Osintsevse/health-evidence-companion). The public repository, owner CODEOWNERS entry and an initial successful Actions artifact build were verified on 2026-10-06. Settings such as branch protection require separate administrative verification; the owner has reported enabling protection.

## After repository creation

The initial English source tree is already on `main`, with GitHub Actions enabled. Make further changes on branches through PRs and keep `CODEOWNERS` set to `@Osintsevse`. The `validate-and-build` check creates downloadable candidate artifacts; version tags use the separate release workflow.

Configure protection/rules for `main`: require a PR, require code-owner review with one approval, dismiss stale approvals, require `validate-and-build`, block force pushes/deletion and resolve conversations. Review bypass settings deliberately. CODEOWNERS alone requests review; it does not enforce it. The repository administration operation must actually complete before describing the branch as protected.

This owner-review arrangement is for contributor PRs. A maintainer cannot approve their own authored PR. Do not manufacture a second reviewer; decide and document a narrow maintainer exception or obtain an independent reviewer where required.

Allow only approved Actions; use read-only default workflow permissions. The release workflow has write permission only in its tag-triggered job. Fork PR code is never executed with publisher secrets or `pull_request_target`. Review workflow modifications as carefully as content.

Optional: enable private vulnerability reporting, issues and discussions as desired. Do not claim private reporting works until enabled. Public discussion must never contain real patient data.

## Contributions and releases

Contributors fork and open PRs. Owner review checks evidence, limits, license and privacy in addition to CI. Include the version/changelog increment in the reviewed PR. After merging that release, create a matching version tag such as `v0.2.0`; the tag must refer to the reviewed source on `main`.

The tag workflow builds the installable ZIP and source archive, checks the version/tag match and creates a GitHub release with checksums. It publishes no plugin to OpenAI automatically. Upload that release's plugin ZIP through the publisher process. If the GitHub action is disabled or fails, inspect the run; do not describe the pipeline as verified from a local test alone.

## Administrative automation

`scripts/configure_github.py` provides an explicit maintainer CLI route for creating the public repository, pushing the source and applying branch protection. It requires a separately authenticated `gh` CLI with repository administration rights. Use `--execute` only after reviewing its printed plan; it never prompts for or writes a token. This is developer tooling, not a browser-user requirement. Availability/permissions/plan restrictions can prevent administrative operations; inspect returned errors and verify settings.

Sources: [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
