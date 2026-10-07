# Changelog

## 0.2.2 - 2026-10-07

- Use the release ID returned by GitHub's draft creation response instead of immediately looking for the new draft in the release listing.
- Add a regression test for a draft that exists but has not appeared in that listing; retain checked uploads, recovery and published-asset immutability.
- Version 0.2.1 was successfully published by retrying the failed main workflow. Medical knowledge and runtime skill instructions are unchanged by this delivery fix.

## 0.2.1 - 2026-10-07

- Initial GitHub delivery: automatic release/tag creation after a reviewed main version bump, a permanent latest-ZIP link and browser friend setup instructions/prompt.
- Draft-first, checksum-verified release uploads with retry handling and no published-asset replacement.
- Updated contributor release instructions and their generated skill reference.
- Healthcare listing category and explicit privacy-policy data categories, purposes, recipients, retention and user controls following the 0.2.0 dashboard findings. Platform rechecks remain required; no approval is claimed.

## 0.2.0 - 2026-10-06

- Review of canonical knowledge, six skills, source register, policies, contribution/release files, packaging and the optional offline adapter.
- New allergy, laboratory literacy, vaccination and treatment-evidence/homeopathy modules with explicit reading limits.
- Forty new source entries (128 total), preserving original IDs; three supplied secondary medicine lists used only for discovery.
- Indication-specific efficacy checks before recommendations, a dated watchlist and verified exceptions to blanket medicine bans.
- Access audit for original sources/documentation, corrected repository/CI status and clearer artifact/browser installation instructions.
- Offline adapter tests added to CI/release checks; synthetic workflow fixtures expanded. No new paid API or patient-data processing.

## 0.1.0 - 2026-10-06

- English migration of fourteen general medical modules, source register and blank templates.
- Six skills for adult medical information, medicines, evidence, psychiatry, record design and contributions.
- Skills-only portable plugin package with user-language responses and no mandatory medical API.
- Contribution review, privacy policy, deterministic packaging and synthetic evaluation fixtures.
- Local validation is separate from clinical validation and platform approval.
