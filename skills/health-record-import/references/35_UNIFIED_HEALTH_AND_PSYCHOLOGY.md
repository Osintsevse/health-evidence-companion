# Unified health and psychology routing

One Health Evidence Companion package includes medical education and the adult psychology skills formerly distributed as PsyOps. Select references for the current request; importing a larger library is not model training or a professional qualification.

## Choose the task

| Request | Route |
|---|---|
| Physical symptoms, tests or immediate medical urgency | health-explain; health-family-care for children, pregnancy and reproductive contexts |
| Medicine ingredients, interactions or label checks | health-medicine-info |
| Psychiatric diagnosis concepts, medication monitoring or clinician preparation | health-mental-health; use current primary clinical sources |
| Adult emotions, meaning, everyday difficulties and supportive reflection | psyops-dialogue |
| Optional structured CBT, ACT or MCT self-help | psyops-cbt-act-mct |
| Relationships, boundaries or an actually shared conversation | psyops-relationships |
| Sport performance and preparation | psyops-sport; physical injury or clearance questions use the medical route |
| Medical studies and clinical guidance | health-research |
| Psychology/sport evidence and psychological method comparisons | psyops-research |
| Private medical archive, imports, history and graphs | health-record-import; design-only requests use health-record-design |
| Owner-authorized psychological notes | psyops-private-records |
| General public knowledge contributions in either domain | health-contribute, with domain-specific evidence appraisal |

The six psyops-* skill names remain stable. Psychological support coverage is adult-only unless a separately reviewed child pathway applies. General pediatric medical coverage does not establish child psychotherapy competence. Joint conversations retain each person's scope and consent; one participant cannot authorize reading another person's diary. Follow the relevant risk/referral guidance before an exercise when clinical safety is affected. Do not infer a psychological cause from an unexplained bodily symptom, nor diagnose from a diary or questionnaire.

When the user asks simply to get started, briefly explain the relevant routes and respond to their actual request. Do not demand a method choice, biography or entire record. Read the minimum needed topic references. Medical symptom, medicine, test and treatment answers use module 19's informational disclaimer; ordinary supportive dialogue follows the psychological boundary guidance without repetitive medical boilerplate. No skill conveys licensure or validated AI treatment.

## Two private record domains

Keep the configured medical ledger and psychological journal separate. Installing the combined package, authorizing one archive, or using a common computer does not authorize the other archive. Reuse an existing authorized destination and permissions; do not migrate personal files merely because the plugins were combined. Shared indexing must honor domain scope before reading private content, not retrieve everything and hide it after retrieval.

A medical record may contain a clinician's psychiatric diagnoses or medication orders under the usual medical provenance rules. A psychological note distinguishes reported experience, a working hypothesis, a practice and its observed effect. It does not automatically become a diagnosis, medication event or laboratory observation. Quantitative self-report scales require their original instrument, date and interpretation limits; correlations with sleep or medicines do not establish causation.

For a shared view or clinician handoff, resolve owner, purpose, recipients, exact selected records and destination. Produce the smallest useful owner-selected summary. Sharing a summary does not expose the source diary or authorize future summaries. Preserve the source privately and version corrections. Relationship notes involving other people require their relevant consent and scope. Permission flags in a JSON file describe a workflow choice; they are not independent proof of human authorization.

The optional Psychology sidebar loads only a deliberately configured summary projection. It never discovers or reads a full psychological journal automatically. A combined HTML file includes everything embedded in it even when tabs are collapsed. Export the medical-only view by omitting the psychology extension, or export an explicitly selected psychological summary for the intended recipient. Separate tabs and namespaces are not encryption or access control. The chosen storage service and model host retain their own controls; the plugin adds no author backend or telemetry.

## Public source namespaces and reuse

Medical source records remain in sources.json with their original S IDs. Psychology records remain in psychology/sources.json with their original S IDs and richer historical access/limitations metadata. S01 in one domain is not S01 in the other. The generated source-catalog.json uses medical:S01 and psychology:S01; repeated URLs are explicitly linked without merging distinct reading dates or claims. The import provenance inventory records original file hashes and the upstream snapshot. Transfer is not a fresh review of the papers.

Use the bundled source_review.py offline planner for one or both domains. It does not visit sources, schedule work, update reading dates or claim clinical review. Reuse the existing medical parsing, genetic, chart and save helpers for their supported schemas. Their output formats do not imply that raw psychological notes can be placed in the medical ledger. General reusable mechanics belong in the plugin; actual owners, private paths, diary contents and shared summaries remain outside the public checkout.
