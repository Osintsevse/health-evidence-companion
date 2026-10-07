# Offline private archive staging helpers

`record_tools.py` validates already extracted rows against the public table contract and can export literal, formula-escaped CSV staging files. It does not perform OCR, upload originals, connect to Drive/Sheets, commit an archive, reconcile a remote journal, or make clinical decisions. The installed skill uses whatever explicitly authorized storage capabilities its host actually provides; this optional example is excluded from the plugin ZIP.

Keep actual input and exports outside this repository, including ignored directories. Run locally with an already extracted private JSON bundle:

```sh
python examples/private_archive/record_tools.py /private/path/import.json --record-id OWNER_ID
python examples/private_archive/record_tools.py /private/path/import.json --record-id OWNER_ID --export-dir /private/path/new-staging-snapshot
```

These paths and the owner ID are placeholders. The input must follow [the table contract](../../knowledge/archive_tables.json) and [the blank import form](../../knowledge/templates/archive_import.template.json), with its blank-template marker removed. An optional `is_synthetic: true` marker identifies teaching fixtures. All row columns must be present; unknown values remain null. Decimal numbers are strings, exact dates have explicit precision, and factual records retain source text and page locators.

Exporting CSV is a staging operation, not a second editable master or a successful Drive commit. Import literal values into a bounded, authorized Sheet range and read them back using the [private import workflow](../../knowledge/20_PRIVATE_DOCUMENT_IMPORT_AND_HISTORY.md). Preserve raw JSON separately: an apostrophe prefix in the CSV is an export escape, not part of the medical source text. The CLI refuses existing CSV destinations.

`validate_bundle` checks structural invariants and source/row links. It cannot verify that claimed remote IDs, hashes, readback states or transcription-review labels are true. The real storage/visual review must establish those facts. `known_ids` allows references to prior rows but is not a duplicate-reconciliation engine.

`chart_candidates` requires import IDs with committed, row-verified journal markers and an explicit set of obsolete/error row IDs resolved from eligible reviewed corrections and replacements. It excludes censored values, incomplete dates and unverified comparisons; it groups exact values conservatively by analyte, unit, specimen, method and laboratory. The caller still needs to sort dates, handle timezones, label limitations and plot the returned points. It does not infer units, standard terminology, medication adherence or causation.

Run wholly synthetic offline checks:

```sh
python -m unittest discover -s tests -p 'test_record_tools.py' -v
```
