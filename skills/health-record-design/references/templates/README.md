# Blank health record templates

Copy a form into a separate private archive before entering any information about a person. Never save a filled copy in the general repository.

- `patient_card.template.md`: concise summary and archive starting point.
- `patient_record.template.json`: blank project data structure, not a FHIR resource.
- `medication_entry.template.json`: medicine entry separating prescription from actual use.
- `episode_entry.template.json`: sourced event with uncertainty fields.

See module 14. Null, unknown and empty lists mean information has not been entered; empty allergy/medicine lists do not establish absence. Keep event and recording dates separate. Do not use real people, results or regimens as sample entries.

## Document import and longitudinal tables

Module 20 and `archive_tables.json` define the Drive-first/private row contract. The original patient/episode/medicine forms remain version-1 summary designs; they are not silently migrated into a table database. The new entirely blank forms are:

- `archive_config.template.json`: owner/destination IDs and storage policy, filled privately.
- `archive_import.template.json`: staged operation and empty table lists.
- `source_document.template.json`: received file, date/page metadata and storage readback.
- `lab_result.template.json`: raw/typed results, comparators, units, intervals and review/mapping states.
- `clinical_entry.template.json`: visit, assessment, recommendation, allergy/reaction or vaccine statement with source wording.
- `medication_order.template.json`: prescribed/recommended plan; actual use remains unknown.
- `medication_use_event.template.json`: explicitly evidenced use/change/missed-dose/effect event.
- `correction_entry.template.json`: version/correction links, reason and authority.

These eight forms are generated from the public contract by `scripts/generate_archive_templates.py`; use `--check` to detect stale copies and synchronize skill references after generation. Remove the `is_blank_template` marker from private active rows/bundles, then populate stable IDs and required statuses/dates according to the contract. Null cells are not negative findings or measured zero. The marker is not an authorization to ingest real data into the repository.

Keep received originals immutable and the configured ledger as the accepted-history master. Import JSON is an audit snapshot; summaries and charts are derived views. Private writes need explicit owner/material/destination authorization and readback. The package contains no person's Drive IDs and no automatic provider connection.

For reader/system layout, vaccination views and investigation matrices, use module 21. View configuration and generated records remain private; these blank forms do not prescribe an owner identity or storage path.
