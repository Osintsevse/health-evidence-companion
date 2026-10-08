# Private intake queues for external chats

This is an operational handoff, not a second medical ledger or a clinical service. Checked 2026-10-09. Use the owner's existing archive and currently available host tools. Ordinary reports, files and manual entry work without a wearable, smart home or home server.

## Choose the supported persistence route

1. A host with the authorized accepted-ledger adapter may commit a small reviewed delta, serialize writes, preserve originals, read back rows and refresh affected views under module 24.
2. A host with an authorized file upload but no safe ledger access should preserve a source package in the configured private inbox. State **queued; not yet in the medical ledger**. Do not download/replace a complete remote SQLite blob for every conversation update.
3. A host without durable upload should provide a downloadable JSON, Markdown or UTF-8 text file, state **prepared locally; manual placement required**, and name the configured inbox. A temporary sandbox link alone does not establish persistence.

Skills carry instructions; connected tools supply actions and access. Installation does not grant account/file permissions, and tools available in one chat/project are not proof that another chat has them. OpenAI documents supported app actions and custom MCP servers as separate integration capabilities [S251, S252]. Availability and effective permissions must be checked in the actual host. No connection, OAuth flow, hosted backend, schedule or publisher access is installed by these local helpers.

## Private inbox and source envelope

Keep the inbox ID/link, archive owner key, accepted-ledger location, generation commands and receipts in private configuration. Verify ancestry and effective access once and after relevant changes. Preserve existing sharing; do not broaden it to make an upload or preview work. A queue file is sensitive even before review. Queue access follows the owner's chosen storage responsibility.

Use a unique producer operation ID and stable file name for each update. A small package states its schema, owner/archive key, conversation title/date, available message coverage, literal user statements, uncertainty, source references and pending status. JSON transcripts accepted by the local statement helper use `turns`, each with `items`, each containing `role` and `text`. Assistant interpretations may be preserved in the transcript but cannot serve as user evidence. Markdown/text sources are treated as explicit owner reports only after manual source review; mixed-role transcripts should use JSON. Missing attachment bytes, unclear audio transcription and inaccessible older messages remain explicitly missing.

Retain clinical event dates separately from message/capture dates. Preserve a relative's relationship, approximate age and reported-versus-documented diagnosis. Do not copy relatives into the owner's diagnosis/allergy lists or chart their measurements as the owner's. Use `family_history_report` rows and the dedicated reader section. Do not turn a medicine question into actual use, character descriptions into psychiatric diagnoses, or missing information into a negative history.

## Upload and unknown outcomes

Use the connector's documented input shape and authenticated file/materialization route. Never send a local path to a remote-only service unless that host explicitly supports it. After upload, read the exact created file metadata and content/bytes as available; bind the observed ID, parent, operation ID and hash to a private receipt. On unknown outcome, inspect the exact stable operation/file identity before retrying. Hash matching is source-byte deduplication, not proof that two clinical events are identical. Repeating a 403 download or changing arbitrary user-agent headers is not recovery. Fall back to the inbox or downloadable package and retain the status.

## Local processing with bundled helpers

The helpers use Python's standard library and local filesystem/SQLite only. All actual paths, sources and outputs must be outside every plugin checkout. JSON/Markdown/text sources are bounded to 8 MiB. Larger documents, images, PDF and fitness/genetic datasets use their existing specialized intake workflows; do not silently convert or truncate them.

- `intake_queue.py --queue <private-inbox> init --record-id <owner>` creates `incoming`, immutable `packages` and `receipts`.
- `... stage --record-id <owner> --input <private-source> --title <title>` archives exact source bytes with SHA-256/readback and leaves `pending_review`.
- `... scan --record-id <owner>` stages supported files in `incoming`; it does not accept facts. Original incoming files remain in place, so a repeated scan resolves to the same source package. Unsupported files remain for the relevant workflow. Inventory errors never mean all inputs were processed.
- `... status` reports source packages and incoming files. `processed` is a recorded verification result, not a live freshness claim about every future database/view version.

For a manually reviewed owner report, `accept_owner_report.py --queue <inbox> --queue-id <id> accept --review <private-review.json> --archive-root <archive> --db <existing.sqlite> --system-root <existing-service-directory>` preserves sources, exact review and a SQLite backup, uses an exclusive archive lock and a database transaction, checks the current owner/schema/version, inserts new reported clinical rows and reads every material field back. It creates no schema, performs no OCR, quantitative import, clinical diagnosis, correction or cloud upload. A changed accepted review must use the existing correction workflow; it cannot overwrite a previous import. All archive writers/generators must honor the same lock; cloud blob concurrency still needs an adapter.

The private review contains `record_id`, `source_sha256`, `expected_db_sha256`, `review_status: reviewed_from_source`, `coverage_note`, optional `source_language`, and a nonempty `facts` list. Every fact has exactly `statement_raw`, `source_text`, `source_locator`, `event_date`, `event_date_precision`, `uncertainties`, `entry_kind`. Supported kinds are `owner_reported_symptom`, `owner_reported_history`, `family_history_report`, `record_reconciliation`. For JSON, locators are `turns[n].items[n]` and each quote must literally occur in that user message. For Markdown/text the locator is `source`. Reviewed transcription never confirms a medical diagnosis. The source reviewer must reconcile existing facts, preserve unknowns and state omissions; syntactic validation cannot establish medical completeness.

After ledger acceptance the receipt is `ledger_verified_views_pending`. Reuse the configured generator, preserve unaffected sections and originals, inspect reader outputs, then run `... verify-views --model <current-view_data.json> --view <reader.html> [--view <reader.md>]`. The model must match the current ledger fingerprint; every accepted row must match the database and embedded HTML. Only then is the package marked `processed`. A subsequent ledger change requires new generation/verification for current views. Failed verification retains the source and accepted rows with the pending status. Do not claim cloud synchronization from a local receipt.

## Optional direct MCP adapter

An owner-controlled connected write service can expose narrow actions such as stage an update, inspect operation status and retrieve accepted facts. Its storage adapter must enforce owner identity, idempotency, serialized transactions, source provenance, bounded input and readback; never expose arbitrary SQL/path execution or accept unreviewed model guesses as clinical facts. OAuth/authorization, access deployment and an end-to-end host test are separate work. This package describes the interface and includes an offline fallback; it does not deploy a remote MCP server. A desktop or another chosen service can host it; a Raspberry Pi, Home Assistant and a named wearable are optional.

## Validation limits

Wholly fictional tests exercise byte preservation, repeat staging, owner/path/hash checks, source-role/quote checks, database version changes, locks, schema rejection, transaction readback, changed-review rejection, staged-operation recovery and stale/missing HTML rejection. These are mechanical checks, not clinical validation, universal connector compatibility or a measured cloud-latency guarantee. Re-check actual host action permissions after installing a reviewed release.
