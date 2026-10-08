# Separate records and selected Psychology summaries

The full medical ledger and psychological journal retain their existing private stores and permissions. This optional view loads one preselected summary file. It does not enumerate a diary, authenticate an owner, validate clinical claims or authorize sharing. Resolve the human owner's scope, purpose, recipient and destination before preparing it.

## Summary contract

Use schema psychology-sharing-summary-v1, selection_scope owner_selected_summary, an opaque owner_key and summaries containing unique record_id, title and text. Optional fields are label, source_ref and as_of. Source references are rendered as plain text. No external hyperlink or diary attachment is created. Extra fields such as full_conversation or private_diary are dropped by the projection. Dates remain supplied provenance strings, not clinical assertions.

The helper reads one explicit local JSON file, refuses duplicate JSON keys and IDs, limits input and output to 2 MiB and requires the exact expected owner_key. A matching string detects configuration mistakes; it is not authentication or evidence of consent. Selected text must already be suitable for the intended recipient. Do not assume an unselected source journal is deidentified.

## Synthetic configuration example

The following paths and identity are wholly fictional. Actual values stay in the private archive configuration:

```json
{
  "psychology": {
    "summary_path": "/private/selected-summary.json",
    "owner_key": "synthetic-owner"
  }
}
```

The summary file uses the same owner_key. Omit the psychology configuration when making a medical-only export. The conditional sidebar is added only when the extension is present; existing archives remain compatible. Exported HTML contains all selected summaries, even when the tab is closed.

## Reuse the local helper

psychology_records.py is bundled in health-record-import and psyops-private-records. The CLI accepts only an already selected summary, never a full diary:

```sh
python psychology_records.py --input /private/selected-summary.json --output /private/summary-for-view.json --owner-key synthetic-owner
```

It publishes atomically without replacement and refuses output inside the public plugin or installed skill. Use a new private filename for each revision, retain source provenance, verify the output and configure the matching-owner projection. It makes no network calls and changes no medical or psychological fact ledger. Storage encryption, recipient access and host processing remain governed by the owner and services used.
