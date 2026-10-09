# Contributing general knowledge

Contributions are welcome through GitHub pull requests (PRs). The maintainer, `@Osintsevse`, reviews and accepts changes. Do not merge your own contribution or describe it as clinically approved without an actual review.

## Allowed changes

Original general medical explanations, current primary-source metadata, corrections, blank templates, skill workflows and synthetic evaluation tasks. Write names, instructions and content in English. Runtime answers remain in the user's language. Native source titles may be translated; do not mistranslate a product name or ingredient.

Never submit a real person's story, filled record, results, prescription, document/photo, medicine history, private link, query log or credentials. Removing names is insufficient. Use a wholly fictional, explicitly synthetic exercise if necessary. Do not bundle copyrighted books/full articles, vendor datasets or weights without verified redistribution rights. DDInter's data license is not this project's MIT license.

## Feedback before implementation

Use [the feedback guide](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/feedback.md) or `health-feedback` for bugs, features, knowledge gaps and prompt proposals. Knowledge-gap sources are optional; researched claims use the research form. Prompt proposals include original text, intended effect and a wholly synthetic behavioral check. Record a decision with reasons, then link accepted requests to the implementation PR and eventual release. An issue is not implementation authorization or evidence of an installed update.

## Ask an assistant to contribute

See [study-to-PR workflow](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/contribution-workflow.md) for copyable requests, connected-account/fork requirements and a draft fallback. Explicitly asking to open a PR authorizes submission; it never authorizes merge or approval. Submit only general knowledge, never the personal question that motivated it.

## Add a knowledge card

1. Define one general question and scope (age group, country/setting and exclusions).
2. Read current primary sources: applicable guideline, exact local medicine label, relevant review/study. Prefer ALIMS for Serbian products and GRLS for Russian products. ICD classifies conditions rather than choosing treatment.
3. Write original concise English prose. Include evidence, benefit/harm, exceptions, uncertainty and what is not established. Distinguish recommendation from interpretation and mechanism from outcome.
4. Add each new source to `knowledge/sources.json`: `id`, `title`, `url`, `region`, `retrieval_status`, `use`, `checked_on`. Use the next unused stable `S` identifier; do not renumber existing IDs. Record the actual reading depth and version in the title/status. A date does not imply full reading or live API testing.
5. Cite source IDs next to supported statements and link URLs where useful. Update the relevant module; a new module needs an index entry and an applicable skill/reference-map entry in `scripts/sync_references.py`.
6. Regenerate derived material and run the README developer commands. Do not manually edit generated CSV, source map or skill reference copies. Inspect the complete ZIP contents.
7. Open a PR using the template. Describe the general problem, change, sources, limitations and validation. Clinical checks need substantive maintainer review; passing CI is not proof of medical truth.

For treatment claims, apply module 18's evidence gate. Identify the indication, comparator, outcome, certainty and guideline direction. Drug lists/Wikipedia/popular articles can supply search leads, not a final classification. Preserve legitimate indication-specific exceptions. Do not infer that weak-evidence products are harmless or exclude a trial solely because of its funding. For calendars/laboratories, record jurisdiction, internal version, units/method and reading scope; a lookup date does not establish a new guideline edition.

## Code changes

Keep browser runtime skills free from local-code or mandatory paid-API dependencies. Packaging scripts are developer tooling, not runtime features. Use standard-library tooling where practical. Test meaningful failure modes: path traversal, stale reference copies, unfilled/filled templates, private links, missing source IDs, version mismatch and archive allowlisting.

`scripts/source-files.txt` lists every reviewed distributable source file, including itself and generated references. Add or remove exact paths in the same PR as intentional file changes. Do not regenerate it from an uninspected working directory; unexpected files stop validation/build rather than enter source ZIPs. Temporary build output belongs in `dist/` or outside the source tree. A clean source ZIP can be built without Git or installed dependencies.

Markdown forms are pinned to reviewed blank-content digests in `scripts/validate.py`; JSON forms have field-level blank checks. A deliberate Markdown layout change needs review of the entirely blank form and its updated digest, followed by reference synchronization. Never update the pin to accept a populated form. Both canonical and archive copies are checked.

Do not introduce external data transmission, a record store, MCP connection or paid provider as an incidental change. Such functionality needs explicit scope, license/privacy review and the applicable host review. GitHub/manual distribution does not exempt integrations from host rules or data protection.

## Review and release

The owner checks evidence applicability, safety limits, citations, intellectual property, privacy and actual tests. CODEOWNERS requests owner review; repository branch protection must also require it. Contributions are not automatically merged. For changed skills, perform fresh-context synthetic forward checks and inspect actual output; do not supply expected answers to the executing agent.

Include a higher stable `X.Y.Z` version in `plugin.json` and a matching changelog section in the PR. After review and merge to `main`, the release workflow validates/tests/builds and automatically creates `vX.Y.Z` with permanent plugin/source ZIP downloads, browser setup files and checksums. Existing published versions are not overwritten; a failed release may be retried on `main`. GitHub/manual installation is the distribution target. GitHub publication does not approve or update an installed ChatGPT copy; host controls still apply. See the repository's distribution guide.

## Psychology namespace

The combined package also maintains knowledge/psychology/sources.json using its original schema and S identifiers. Add psychological sources there with actual access, checked_at, supported claim and limitations. Qualify cross-domain references as medical:Sxx or psychology:Sxx; IDs are not interchangeable. Regenerate the unified source catalog and skill references. Public psychological material, original practices and synthetic evaluations follow the same no-private-record and maintainer-review rules. Transfer does not refresh evidence dates.
