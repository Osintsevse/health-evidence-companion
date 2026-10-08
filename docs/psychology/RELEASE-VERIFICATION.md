# Release verification

## English edition 0.1.1 — 2026-10-08

All public package prose is in English, including canonical knowledge, source metadata, synthetic examples and generated references. Each of the six skills and the ChatGPT Project instructions explicitly preserves the user's current language or stated language preference. These rules do not establish efficacy or validated scale equivalence across languages.

Comparison with the preceding published commit confirmed unchanged IDs, URLs, evidence types, reading depth and check dates for all 102 source records, and unchanged card/citation IDs and table-row counts in numbered modules. Dates in prose were standardized to ISO format. Clinical terminology and misleading literal translations were edited. No new source review or independent clinical evaluation was performed.

The package validator, six standard skill-format checks, archive-content checks and six synthetic negative checks passed. The negative checks cover the four publication invariants below, untranslated Cyrillic prose and removal of the Project user-language rule. They verify structural behavior, not actual multilingual conversation performance. Generated references and Project files match canonical material; the previous release remains available.

## Initial release 0.1.0 — 2026-10-08

Performed a structural/content check of the common database, an explicit check of the list of distributed files, source IDs, local links, consistency of manifests, emptiness of forms and matches of generated references. All six SKILL.md passed the standard quick_validate from skill-creator with PyYAML 6.0.3.

Three ZIPs were built from an explicit list and are open for composition inspection. Project ZIP contains general knowledge, source register, instructions, START_HERE, LICENSE, PRIVACY and TERMS. SHA-256 are stored separately. The scan does not use the contents of your personal archive.

Four synthetic checks confirmed failure for an unknown file, a private Drive link, a completed form, and an stale reference copy. These are meaningful tests of the publication boundary, but the heuristic search is not guaranteed to detect any possible leak in future changes.

The addresses of all 102 sources were checked for transport accessibility: 64 responded with HTTP 200, 38 gave an error/access restriction. Full log - source-link-check-2026-10-08.json. A successful answer does not imply scientific validity, and an error does not refute the source. Meaningful rereading was targeted, see evidence-rechecks-2026-10-08.json.

12 responses to fully synthetic queries generated and verified by the current assistant; independent skill triggering and peer clinical assessment not completed. Historical reports from previous versions are saved with an explicit status. The effectiveness of treatment, long-term safety, and the qualifications of the psychologist have not been established by this release.
