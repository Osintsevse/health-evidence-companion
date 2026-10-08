# Readable private archive views

Use with module 20 and the row contract when an owner asks to browse a medical archive or to maintain reusable views. This module defines presentation and update quality, not clinical recommendations. Keep actual records, paths, account IDs, exports and generation logs outside the public package.

## One accepted history, several readable views

Choose one accepted-history ledger: the existing native Sheet, SQLite database or explicitly selected store. Do not create competing editable masters. Received originals and committed import receipts remain evidence. HTML, Markdown, spreadsheets and clinician handoffs are derived views with an as-of date, included record IDs and a generation receipt. A view edit does not silently amend history; accept an explicit source-linked correction first, then regenerate.

Preserve an existing archive. Older summary structures may contain facts not yet in the ledger. Inventory them before replacing a catalog with a dashboard. A private context table or immutable source snapshot can preserve their mixed provenance until an explicit reviewed row migration is completed. Label that context as previously recorded; do not promote an old summary, discussion or uncertain dose into a newly verified fact.

## Reader and system areas

Use one obvious entry point and a clearly named reader folder. Keep current summaries, vaccination views, investigation matrices, clinical timelines, medicines, allergies, uncertainty lists and source-detail pages together. Put databases, contracts, configuration, import snapshots, received originals, scripts, technical logs and backups in a clearly marked system area. Folder names and language are configurable, not prescribed universally. Retain an owner's intended restricted psychiatric/psychotherapy boundaries; a combined dashboard must not broaden access.

Reorganization is a migration: resolve absolute source/target paths within the authorized archive; inventory hashes and current row IDs; serialize writes; record old-to-new locations; preserve immutable import receipts and source IDs; repair reader links; read back rows, bytes and navigation before completion. Old journal paths remain historical, with the migration map resolving current locations. Do not delete originals, rebuild received images, move outside the selected archive or silently discard older summaries. Preserve provider IDs and actual inherited access where possible. Back up changed generated files and the accepted ledger. Do not claim cross-device concurrency or complete cloud synchronization from a local filesystem operation alone.

## Useful views

Build the views justified by available data. A practical set includes an overview; vaccinations; laboratory history; vital measurements; visits/reports and imaging conclusions; conditions/allergies; medicines; source documents; and unresolved items. Empty sections say information is unavailable, not that a condition or treatment is absent. Show historical dates and last reconciliation; avoid automatically turning every abnormal result into a diagnosis, score or alert.

An overview can show dated reported state, documented historical assessments and reported medicines. Keep historical prescriptions elsewhere in the medicine view. Explain source certainty in ordinary language; expose technical IDs when they help locate evidence. Preserve doctor's source wording separately from translations and summaries. Do not display technical JSON dumps as the normal way to read symptoms or measurements.

### Vaccinations

When a native reference exists, copy the whole workbook before adapting the separate view, following the host's Google Sheets workflow. Preserve the familiar history columns: infection, vaccine/product, type, date, dose, result, comment, batch and manufacturer as present. Add source/event-date/review information without guessing units, doses, certificates or protection duration. A private details table keyed to each clinical entry may preserve these columns alongside the accepted event.

Distinguish vaccinations, tuberculin tests and reported disease history. A placeholder or conflicting date may remain visible verbatim, while the accepted event date is unknown. Do not infer one event per source row when source duplicates or underlying transcriptions disagree. Preserve those disputes. Source notes about immunity/recommendations are not verified clinical status; label them as unreviewed source notes. No table edit establishes vaccination completion without evidence.

### Laboratory matrix

By default put analytes in rows and dated investigation events in columns, with chronological dates, laboratory, specimen and source references. Preserve an explicitly chosen owner orientation. Group pages of the same established report/accession, not all tests sharing a calendar date. Different collections in one day remain distinct; missing collection time stays unknown. Keep blood, urine and stool contexts in distinct views when grouping would confuse interpretation.

Retain every value if a cell has multiple accepted results; never use a first/last overwrite, average or fabricated zero. Preserve raw decimal precision, inequality signs, qualitative results, source flags, units and the contemporary reference interval. Keep unknown-date reviewed results visible in an undated section rather than assigning a date or dropping them. Needs-review results remain available in an uncertainty view and must not become numerical chart points.

Display translations or aliases must not collapse different raw analytes, units or specimens. An explicitly reviewed equivalence/conversion registry can support a further derived comparison, retaining the original identities, source units, conversion formula and review authority. Unreviewed spelling similarity, missing specimen or a display-unit label is insufficient. A side-by-side display does not establish assay comparability. Graph selection still follows module 20: reviewed values, genuine dates, verified compatible context, and explicit handling/exclusion of detection limits.

Freeze the analyte column and date/source header rows, with scannable headers, normal-sized text and bounded formatting. A search/filter should expose the selected analyte's actual cases rather than forcing the reader through many blank rows. Show reference intervals and source locators per cell or in one accessible detail view. Avoid using newly invented global ranges or color as a diagnosis.

### Measurements, reports and medicines

Preserve each measurement's date/time precision, method, unit, source and uncertainty, including repeat measurements at the same time. Missing pages and conclusions remain visible. Visits, investigations, clinician diagnoses, recommendations and planned actions have separate meanings; a plan is not evidence of completion. In medicines show orders separately from explicit use events and retain regimen/dose uncertainty, benefit and adverse-effect reports. A receipt or old prescription does not establish current use.

Only committed, row-verified imports can feed accepted views. Resolve reviewed corrections using the target table and replacement eligibility. A staged or unreadable replacement must not hide the accepted prior value. A completed correction chain is history, not a pending dispute merely because an intermediate replacement no longer appears in the current view.

## Private scripts and repeatable generation

When scripts materially improve repeatability, save the actual generator, template, adapter, configuration and reproduction command in the authorized private system area. Record version/hash, inputs, output paths, generation time, included/excluded rows and native-view file IDs. Configuration binds one owner to one ledger and its managed views. Keep actual configuration out of the plugin repository.

The import skill provides an optional standard-library SQLite generator and offline HTML template; the spreadsheet adapter requires the host's available Artifact Tool runtime. They do not perform OCR, upload files, connect accounts, implement access control or run automatically. Hosts without code execution can implement the same views with available authorized tools. Follow relevant document/spreadsheet skills; save only the requested private destination. Do not require a new server, public website, third-party OCR provider or paid dependency for a local view.

HTML should work from a local file with embedded data/assets and no external requests. Google Drive is storage, not an assumed HTML application host: native Sheets can be opened directly in Drive, while an offline HTML file may require a local synchronized path or download. A dashboard snapshot contains sensitive information and inherits its storage/sharing boundary. Do not publish it to demonstrate the plugin.

## Update and verify

1. Read current configuration, accepted markers, source IDs and managed view IDs. Confirm the authorized owner and effective access. Reuse the standing authorization and current layout.
2. Import new material through module 20. Preserve unresolved rows and immutable sources. Do not append on an unknown result or infer clinical facts from filenames.
3. Generate into private staging from accepted rows and preserved context; resolve eligible corrections without premature exclusions. Write literal spreadsheet cells and escape document text in HTML. Neutral source IDs must not become traversal paths. Generated outputs must stay outside public source.
4. For a new layout, generator change or requested full rebuild, verify every populated view and important desktop/mobile interactions. For a routine delta, verify affected views and their navigation; retain prior verification for unchanged outputs against current hashes/versions. Verify row coverage, dates, units, qualitative/limit values, repeated/undated results, source links, uncertainty and prescription/use separation. For Sheets inspect native cell values/features and layout according to the host workflow. A local XLSX preview alone does not prove native Google rendering.
5. Update only managed view files/ranges; preserve unrelated inputs, comments, formulas and source workbooks. Read back material values and output hashes, then finalize a generation receipt. Keep import completion separate from human uncertainty and from publication or clinical approval.

Save the chosen rules with the personal archive so a later authorized assistant can reproduce it. Do not promise unseen-chat retrieval, monitoring or background refresh. Schedule future imports only when explicitly requested.

## Owner clarification and laboratory row families

Use module 22 for a separate questions/feedback page with stable IDs, private source links, persistent answer fields and correction acceptance. Preserve user answer columns during native refreshes; an offline browser draft requires export and ingestion. For date-by-analyte matrices, reviewed display aliases may share a row while source specimens, methods, values and references remain inspectable. Only reviewed compatible transformations support quantitative comparison; browsing grouping alone does not.

## Parsed sources and original documents

Every displayed fact and clarification needs both its parsed-source link and the preserved original link, including laboratory result details and report headings. Resolve local paths inside the authorized archive and reuse verified private cloud URLs when available. Do not invent accessible originals or silently substitute extracted text for a scan.

Show document-photo previews immediately beside questions, with a click target for the full original. Embed verified local image bytes in offline HTML so previews survive downloading one file; label a resized preview and retain the untouched original and checksum. Plain source text may use a labeled text panel. Native tables and unsupported formats get an explicit original link, not a fabricated scan. PDF page rendering needs an available local renderer and a separate verified implementation; the optional helper does not render PDF pages.

The optional local preview helper needs an explicitly configured private `originals_root`, `embed_question_originals: true`, and available Pillow for image thumbnails. It makes no network requests and requires matching source checksums. Hosts may implement equivalent local rendering with available tools. Never make a private image public to satisfy a spreadsheet IMAGE formula. Native question sheets can use rich original links while the offline HTML supplies immediate previews. Preserve owner answer cells during these changes and verify full-original URLs, source hashes, image loading and standalone HTML behavior.

For incremental refresh, compare output hashes and follow [module 24](24_INCREMENTAL_ARCHIVE_SAVES.md). Avoid embedding a fresh generation timestamp in an otherwise unchanged view solely to force its upload; retain its last generation timestamp when source rows/configuration are unchanged. A refresh failure does not undo a separately verified ledger commit, and it must remain explicit.
