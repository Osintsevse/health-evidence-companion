# Medication timelines and complete archive defaults

General owner-authorized record workflow. Actual documents, dates, medicine histories, configuration and feedback remain private. This is a display and reconciliation method, not prescription guidance or clinical validation.

## Start without requiring layout coaching

Reuse the chosen archive and its single authoritative ledger. For a new archive, put originals, database, import journals, backups, configuration, generators and derived JSON in a system area. Put all current reader documents in one reader area with an entry point and navigation. Use one accepted source model to generate HTML, human-readable summaries and optional native Sheets. Keep the selected folder names, schema, commands and version with that owner's archive; do not transplant another person's paths or configuration.

Default readable views start with summaries, then source-linked details: overview; preserved vaccination layout; analytes in rows and dated laboratory events in columns; measurements; visits/reports; diagnoses sorted by date with first/last mentions; separate allergies/reactions; medication-use timeline; originals/parsed documents; and clarification. Module 22 governs safe display aliases and feedback. Generate static assets without external requests. A native Sheet can be used directly in Drive, while HTML may need a local synchronized file or download.

These defaults apply to setup, a requested complete archive or a rebuild. Routine small saves use [module 24](24_INCREMENTAL_ARCHIVE_SAVES.md) and refresh only affected managed views, with exact partial/completed status.

## Reconstruct actual use without losing an ingredient or brand

Keep medicine orders and actual-use events distinct, as in MedicationRequest and MedicationStatement. Preserve who reported each fact and its timing; a historical mention does not establish today's use. [S85, S87, S132]

Read the whole supplied medication-related conversation or document set, then reconcile existing rows before adding anything. Specific actual-use reports take precedence over vague context. An owner's explicit later confirmation of taking the identifiable prescribed regimens supports new source-linked use events. Preserve explicit exceptions such as never starting one proposed medicine. A list of alternative brands is not evidence that every alternative was taken. Broad confirmation does not supply missing doses, exact transition dates, adherence or completion of a planned course.

Save the new confirmation separately and link the associated order/context, including any source uncertainty. Do not rewrite an old order's `actual_use_status`; append a use event. Link brand and ingredient names only when the owner/source or a verified product mapping supports that identity. Display aliases belong in private configuration and never prove equivalent formulations, concentrations or release profiles. Keep a source containing several medicines as a combined report unless the evidence supports separate fields.

## Timeline semantics

Show chronological event points, sorted by their genuine date precision, with product, dose/regimen, event type, source and uncertainty. Month/year dates stay month/year dates. A dated message can report earlier use; a prescription date is not automatically a start date. Unknown dates sit in a labeled unknown-date area. Display starts, changes, stops, effects and explicit non-initiation distinctly. Show prescriptions in a separate layer/filter, initially displaying use events.

Do not draw a continuous exposure bar between disconnected mentions or close an interval at the next prescription by assumption. Approximate periods and known gaps remain explicit. Tablet strength is not the taken dose, a tablet count cannot be converted using an old unconfirmed strength, and a planned duration is not completed use. Reported improvement or adverse effects remain reports without asserting causation. Current use includes its last reconciliation date and never follows merely from a historical order.

The optional medication-timeline helper creates event rows without calculating exposure intervals or doses. Save it with the actual private generator/template and config. The view should let an owner filter by medicine and record type, open originals, and see the evidence behind a date or dose.

## Clarification lifecycle

Stable questions show the exact uncertainty and immediately available original preview where possible. Native Sheets bind answers by question ID and preserve owner cells. Offline HTML warns prominently at both ends that drafts are not sent or accepted automatically and provides working export controls at both ends. Use an archive-specific draft namespace to avoid mixing owners. Preserve all answers in downloads, including collapsed completed questions.

On receipt, preserve the answer file and hash, compare against current answers, append only new feedback, and validate known/unique question IDs. A collector stages feedback for review; it does not alter clinical facts. Review source-linked corrections through the accepted import/correction chain. Show both the answer and review outcome.

Move reconciled accepted questions, accepted unknowns and owner-closed requests into an answered section collapsed by default. Keep new, pending and partial questions open. An owner may decide a missing detail is not worth pursuing: close the question while preserving the unknown value or missing-page note. Closing a question does not make an unreadable result or incomplete document verified.

## Verify and publish only general improvements

Verify unchanged originals and prior source rows, accepted import markers, included row IDs, dose/date precision, separate orders/use, original links, rendered controls, export/import idempotency and answer preservation. Save a private receipt; passing software checks does not establish medical truth.

General contributions include these rules, portable helpers and wholly synthetic tests. Never copy an actual conversation, schedule, timeline, document or filled configuration into source, a PR or release. Platform manifests and per-skill upload ZIPs distribute the same general knowledge; they do not create storage, authentication, monitoring or automatic ingestion.
