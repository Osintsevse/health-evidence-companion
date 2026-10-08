# Health and PsyOps unification

Version 0.6.0 combines the two public packages in Health Evidence Companion. The repository/package identity and the six psyops-* skill names remain stable. There are 15 entry skills: nine medical/archive/research skills and six psychology skills. No personal archive is migrated by installing this release.

## Preserved content

PsyOps canonical knowledge, blank forms, source register, original evaluation samples and historical audit documents are retained under psychology subdirectories. Their upstream commit and file hashes are recorded in [import provenance](psychology/import-provenance.json). The transfer preserves reading dates and limitations; it does not re-appraise the referenced clinical literature. The original PsyOps repository remains available for historical snapshots.

## Install and migrate

Install the combined Health package, verify that all 15 skills are present, then remove or disable the separate PsyOps installation through the host's normal plugin controls if desired. Avoid two enabled copies of the same psyops-* skills. This repository change does not install, remove or reconnect a plugin automatically. Existing medical and psychological archives keep their destinations and permissions.

## Use and private sharing

Read [routing and boundaries](../knowledge/35_UNIFIED_HEALTH_AND_PSYCHOLOGY.md). The optional Psychology tab accepts an explicitly selected private summary rather than a diary dump. Keep full psychological notes in their own store. Exports must choose whether psychology is included; a collapsed tab does not remove embedded text. Existing archives without the psychology config retain their medical views.

## Source maintenance

[Unified source catalog](../knowledge/source-catalog.json) qualifies IDs by domain. The medical and psychological canonical schemas remain unchanged. Duplicate URLs are reported as aliases rather than silently losing distinct access histories. Run python scripts/update_registry.py and python scripts/sync_references.py after edits. Run python scripts/source_review.py --domain all --as-of YYYY-MM-DD for an offline recheck queue; it never refreshes check dates by itself.
