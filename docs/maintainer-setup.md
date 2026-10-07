# Repository and release setup

Owner: `Osintsevse`. Source repository: [health-evidence-companion](https://github.com/Osintsevse/health-evidence-companion). The public repository, owner CODEOWNERS entry and an initial successful Actions artifact build were verified on 2026-10-06. Settings such as branch protection require separate administrative verification; the owner has reported enabling protection.

## After repository creation

The initial English source tree is already on `main`, with GitHub Actions enabled. Make further changes on branches through PRs and keep `CODEOWNERS` set to `@Osintsevse`. The `validate-and-build` check creates candidate artifacts; the separate **Publish plugin release** workflow publishes permanent release downloads.

Configure protection/rules for `main`: require a PR, require code-owner review with one approval, dismiss stale approvals, require `validate-and-build`, block force pushes/deletion and resolve conversations. Review bypass settings deliberately. CODEOWNERS alone requests review; it does not enforce it. The repository administration operation must actually complete before describing the branch as protected.

This owner-review arrangement is for contributor PRs. A maintainer cannot approve their own authored PR. Do not manufacture a second reviewer; decide and document a narrow maintainer exception or obtain an independent reviewer where required.

Allow only approved Actions; use read-only default workflow permissions. The release workflow has contents-write permission only in its reviewed-main/tag job. Manual publication accepts `main` only. Fork PR code is never executed with publisher secrets or `pull_request_target`. Review workflow modifications as carefully as content.

Optional: enable private vulnerability reporting, issues and discussions as desired. Do not claim private reporting works until enabled. Public discussion must never contain real patient data.

## Contributions and releases

Contributors fork and open PRs. Owner review checks evidence, limits, license and privacy in addition to CI. Include a higher `plugin.json` version and the matching changelog section in the reviewed PR. When it reaches `main`, the workflow validates/tests/builds, creates the matching `vX.Y.Z` tag and publishes a GitHub Release. No manual tag step or extra token secret is required. A failed run does not establish publication.

Release-workflow/script changes also trigger a run on `main` to bootstrap a missing release, and **Actions -> Publish plugin release -> Run workflow -> main** retries a failed publication. Existing version tags and published assets are never moved/replaced. A failed upload stays a draft; reruns may add missing assets only when existing bytes and the source commit match. Mismatches require maintainer inspection or a new version, not `--clobber`. Manually pushed version tags remain supported only if they match the manifest and point into reviewed `main` history.

Release assets include the versioned plugin and source ZIPs, identical stable-name `health-evidence-companion.zip`, setup instructions/prompt, checksums and a build report. `/releases/latest/download/health-evidence-companion.zip` is the fixed download link. Latest-release selection uses GitHub's date/semantic-version policy, so an older-version retry does not explicitly force itself as latest.

GitHub Releases require no OpenAI developer verification. They publish no plugin to the ChatGPT directory automatically. Upload the plugin ZIP through the separate verified publisher process when ready. Test the friend setup in the recipient's real account; creation/install permissions are not granted by the source repository. If GitHub tag/release rules restrict the Actions token, the release run will fail visibly; inspect those rules rather than adding a personal token or bypass as an incidental fix.

## Administrative automation

`scripts/configure_github.py` provides an explicit maintainer CLI route for creating the public repository, pushing the source and applying branch protection. It requires a separately authenticated `gh` CLI with repository administration rights. Use `--execute` only after reviewing its printed plan; it never prompts for or writes a token. This is developer tooling, not a browser-user requirement. Availability/permissions/plan restrictions can prevent administrative operations; inspect returned errors and verify settings.

Sources: [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
