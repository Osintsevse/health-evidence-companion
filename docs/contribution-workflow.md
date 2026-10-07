# Ask the assistant to add a study

GitHub calls a merge request a **pull request (PR)**. The maintainer is `@Osintsevse`; contributors and assistants never approve or merge their own proposals.

## Copyable requests

- "Review this study [public DOI or URL]. Add an original evidence summary to Health Evidence Companion, update the source register and prepare a pull request for Osintsevse. Include limitations and whether it changes the existing conclusion. Do not merge."
- "Add a general module about [topic], using current primary guidelines and original studies. Update related skills and tests and open a PR for the maintainer. Keep personal cases out."
- "Correct [claim/source] using this guideline [URL/version]. Prepare a small PR with the changed conclusion and evidence."

These are explicit authorization to create the contribution branch/fork and submit its PR when the user's connected GitHub account has the necessary permissions. Asking only to explain or summarize a study is not authorization to publish it. Asking to add it authorizes preparation; ask whether to submit only when publication was not requested. Never ask for a token in chat.

## Assistant workflow

1. Retrieve the canonical repository/default branch and applicable instructions. Locate related knowledge before editing; installed references are snapshots. Do not assume the user can write upstream.
2. Inspect the actual study/guideline. Record DOI/URL, version/date, sections read, PICO, design, outcomes, absolute effects when supported, harms, uncertainty and applicability. Abstract-only access must be labeled; an unseen full text is not fully appraised. A positive study alone does not settle a disputed treatment claim.
3. Write original English prose; preserve opposing evidence and existing useful material. Never include the user's story, documents, prescription or identifying metadata. Never copy a full article without rights.
4. Edit canonical `knowledge/` files and `knowledge/sources.json`, preserving source IDs. If adding a module, update the index, applicable SKILL.md links and `scripts/sync_references.py` map. Run registry generation, reference synchronization, project validation, tests and build. Generated copies are not independent sources.
5. Use a new contribution branch. With upstream write permission, push that branch, not main. Otherwise use an authorized fork and branch. Inspect base/head/repository before submitting; preserve unrelated changes. Never force-push, enable auto-merge or edit repository protection.
6. Open a PR into `Osintsevse/health-evidence-companion` with the problem, changed conclusion, primary sources/reading limits, validation and unresolved questions. Request owner review when the tool supports it. Return the verified PR URL. Do not claim clinician review or approval.
7. If GitHub tools, fork permissions or code execution are unavailable, provide a reviewable evidence card and PR draft or direct the user to the research-request issue form. State exactly which operations/checks were not done. Never claim a submitted PR, merged change or installed update without confirmation.

## Review and updates

The maintainer accepts, requests changes or rejects the contribution. CI checks structure/privacy heuristics and packaging, not medical truth. CODEOWNERS identifies the reviewer; branch protection/rules must enforce approval separately. A submitted PR does not change the installed plugin. After reviewed changes are merged with a new manifest version, the release workflow publishes a ZIP and setup files; manually installed copies must be updated explicitly. Supported workspace GitHub sync has its own controls.

Use [the repository](https://github.com/Osintsevse/health-evidence-companion) for proposals and [issues](https://github.com/Osintsevse/health-evidence-companion/issues/new/choose) when unable to submit code. Public issues accept only general questions and public research links.
