# Start a private medical history

This guide prepares an owner-controlled archive. It does not create a publisher account, automatically connect Google Drive or establish that anything has been saved. Use an available authorized host and the `health-record-import` skill. The project carries the workflow and blank contract; your real files and values stay in private storage.

## Initial setup

1. Select the existing medical-card folder and verify its ID, ancestry, intended owner and effective access. Reuse an existing layout; do not create a duplicate history solely because the folder name differs from this guide. Store the IDs in a private copy of `archive_config.template.json`.
2. Inside the selected archive use logical areas for originals, immutable import snapshots/receipts, derived views and dated backups. Names can follow the owner's existing organization. Create one native Google Sheet for authoritative structured rows, using the `archive_tables.json` tab/column names. Create/import it through the available Google Sheets workflow and verify the resulting file/parents.
3. Record the ledger ID and schema version in private configuration. Check the actual original-upload, structured-write and readback capabilities. A successful folder search is not a successful import or OCR test.
4. Keep one writer per archive unless a tested locking/conditional-write mechanism exists. Back up before a schema migration; preserve older entries and unknown values. Version 1.0 of the older `patient_record.template.json` is a summary design, not an existing longitudinal table database. Never silently convert a real archive without inspecting it.

## Example user requests

- "Save these report photos in my selected private medical-card folder, preserve the originals and add their dated results to the history. Tell me which fields are unclear."
- "Add this visit report: record the doctor's conclusions, recommendations and prescriptions. Actual medicine use is not confirmed."
- "Record that I started/stopped this medicine on the date I state. Keep its prescription and my actual-use report separate."
- "Show the stored history of this laboratory test with dates, original units, lab references and source links. Explain exclusions before plotting."
- "Correct a misread value in this row using the clearer source image; preserve the prior entry and correction trail."

These authorize only the specified private operations when destination and tools are established. A report explanation does not implicitly authorize an upload or public contribution. Requests to share/export need an explicit recipient/destination. An owner can authorize a recurring import pattern; the assistant should retain that scope rather than ask again for every image.

## What happens after new photos

The assistant inventories pages, inspects the actual images, checks dates/table alignment/units and stages a source-linked extraction. It saves the bytes it actually received as originals, then maintains dated table rows and a private import receipt. It marks unclear fields pending and reads back completed writes before reporting success. Duplicate bytes can reuse an existing source; a second scan or an annual repeated result is not automatically a duplicate clinical fact.

The native Sheet contains Documents, Observations, ClinicalEntries, MedicationOrders, MedicationUseEvents, Corrections and Imports tabs. It is the accepted-history master. JSON import packages preserve each extraction/version; charts and summaries are derived, with source row IDs and an as-of date. No actual folder IDs, source images or values are stored in the public plugin.

## Local or other storage

The same contract can use private UTF-8 files or a local database outside the repository. The offline developer helper validates already extracted bundles and can produce safe CSV staging files; it does not recognize images or save to Drive. Do not treat CSV/JSON as a concurrent database or declare FHIR interoperability without mapping/profile validation.

For host-managed cloud storage, first verify durable retrieval, access, export and versioning in that host. This guide makes no assumptions about unnamed cloud products or conversation attachment retention. Use the owner's selected Drive/local destination until another one is explicitly chosen.

See [the full workflow](../knowledge/20_PRIVATE_DOCUMENT_IMPORT_AND_HISTORY.md), [table contract](../knowledge/archive_tables.json) and [blank templates](../knowledge/templates/README.md). Only general design and wholly synthetic tests belong in this repository.
