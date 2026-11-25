# Medical AI, models, APIs and architecture

Documentation review dated 2026-10-06. No accounts were created and no personal record was sent to providers. Product claims do not establish comparative clinical accuracy.

## Existing systems

| System | Intended use and useful pattern | Limit for this project |
|---|---|---|
| Ada | Patient symptom interview and possible next steps | Not a final diagnosis or comprehensive interaction check |
| Isabel | Patient navigation, possible causes and urgency; Russian advertised | A long differential list does not select treatment |
| AMBOSS AI Mode | Professional learning and cited search of its reference/guideline/drug content | Access/subscription and jurisdiction need checking |
| OpenEvidence | Professional literature questions; Mount Sinai adoption documented | Ordinary-user access from Serbia not confirmed; local labels still matter |
| UpToDate Expert AI | Professional decision support with UpToDate/Lexidrug content | Access not established; professional product |
| Lexidrug | Specialized medicine, dosing and interaction reference | Not a patient diagnostic AI |

Sources: S33-S38. Do not repeat advertising superlatives as facts.

## Research context

The 2024 RCT involving 50 physicians did not find a statistically significant diagnostic-reasoning improvement from access to the tested LLM over usual resources: medians 76% versus 74%, adjusted difference two percentage points, 95% CI -4 to 8. This was a specific model and limited case experiment, not evidence about every current system or the safety of self-treatment. [S39]

## X-ray images, local viewers and clinical AI

Documentation and evidence checked 2026-11-25. The workflow starts with plain radiography. For CT or MRI, a radiologist needs the complete study with its series or sequences and the clinical question. Use a written report or selected images for explanation within their scope. Module 30 covers private source handling and scope limits.

### Prepare a study for review

1. Keep the original DICOM study and radiologist's report in the authorized private location. Request the complete study from the imaging service for a medical second opinion. For a child's study, seek a radiologist experienced in pediatric imaging when available.
2. Use a local DICOM viewer to open the study, inspect the available projections and adjust display contrast. [Weasis](https://weasis.org/en/index.html) is a free, open-source option with offline viewing and PNG export. [RadiAnt](https://www.radiantviewer.com/) is a commercial Windows viewer. Their documentation describes file handling. No viewer was installed or tested for this review. [S959, S960]
3. For a report explanation in an image-capable chat, share only the relevant, authorized material. Provide the report text, age, body area and the question. If images are needed, export each relevant projection as a full, labeled PNG or JPEG. Check filenames, visible labels and any identifiers burned into the pixels. Preserve useful side and projection markers while hiding personal identifiers. A display export is a derivative with a chosen contrast and framing. A masked overlay alone does not clean all pixels or metadata. [S956, S957, S959, S963]
4. Ask the assistant to identify the supplied views when labels are readable, explain the radiologist's wording, compare dated written reports and draft follow-up questions. Qualify missing views or uncertain labels. If the report is unavailable, ask for it and explain what information would help the reader. The clinical interpretation and any decision to rule out a finding belong to the treating team. [S957, S958]

### Interpret evidence about an AI reader

OpenAI documents PNG and JPEG input in Codex and medical limitations for ChatGPT image inputs. An image attachment establishes a way to provide visual context. In Lacaita et al.'s 2025 experiment, ChatGPT-4o identified pneumothorax in 21 of 51 selected cases. The authors used a curated teaching-case dataset and a specific model, so the fraction cannot estimate current chat performance, performance on a particular child or accuracy in a clinic's population. Article CC BY 4.0. This summary uses results and study methods, without redistributing images. [S956–S958]

| Example | Documented purpose | Scope to check before clinical use |
|---|---|---|
| Gleamer BoneView 1.1-US | Highlights possible fractures for the clinician while reading radiographs. | The US filing includes specified anatomy, with selected pediatric and adolescent sites for ages 2 through 21. Verify the exact version, site, projection and local authorization. [S961] |
| Annalise Enterprise CXR Triage Pneumothorax | Prioritizes adult chest radiographs for clinical review when pneumothorax or tension pneumothorax is suspected. | The US filing covers adult worklist triage. A negative alert cannot exclude pneumothorax. [S962] |

Check device version, country, modality, anatomy, age group, target finding, clinical workflow and independent evidence before relying on a product claim. The examples describe particular US filings. Individual availability in other jurisdictions and local deployment were not checked. The package supplies this workflow as guidance. DICOM parsing, inference and connections to clinical imaging systems require separate tools.

## General care workflow design

A separately authorized private environment can preserve originals and dated reports; maintain a current concise summary of conditions, allergies and actual medicine use; assess urgency; consult guidelines/local labels and interaction sources; prepare questions and follow-up; record actual clinical outcomes. This is a project design choice, not a comparative trial result. The distributed skills package supplies general explanations and blank templates only.

AI cannot continuously see other chats. Private updating requires available material and authorized working access. External services should receive only necessary information after a separate informed decision; the public plugin does not transmit patient data.

## Open weights and code

| Project | Access | Use and limits |
|---|---|---|
| MedGemma | HAI-DEF weight terms; code has a separate license | Version 1.5 is a 4B multimodal developer component for text/images/extraction; adaptation and validation are required |
| BioMistral-7B | Public weights; Apache-2.0 in model card | Research text model; authors limit real clinical use |
| gzxiong/MedRAG | Retrieval-generation code; Public Domain Notice in LICENSE | Research retrieval pattern; corpus rights must be checked separately |

Sources: S43-S49. MedGemma is more accurately called open-weight rather than entirely open-source. Do not confuse 1.5 4B with earlier 27B variants. Self-hosting and Vertex AI infrastructure are not a free ready-made hosted medical API. Runtime memory also includes context/cache/load beyond weight size. Russian/Serbian performance and clinical outcomes were not measured here. [S43-S46]

## Documented APIs

| Provider | Function | Access and limitations |
|---|---|---|
| Infermedica | Engine/Platform symptom interview and navigation | Public docs; access agreed with provider. An endpoint called diagnosis is not a final clinical diagnosis |
| Isabel | Self-Triage and differential support | Documentation/sandbox requested from vendor; access not obtained or tested |
| Ada Health | Partner API/SDK integration | Official help directs partnership inquiries; unrestricted individual access not confirmed |
| EvidenceMD | REST medical questions with retrieval and citations | Dashboard keys described; accuracy/citation quality not independently assessed |
| DrugBank | Drug data and drug-drug interactions | Appropriate license and local-product coverage checks required; not mandatory |

Sources: S50-S58. No API connection, account or key was established. Recheck pricing and actual availability before integration.

Infermedica distinguishes present, absent and unknown evidence. Stateless Engine workflows carry accumulated interview evidence: not asked must not become absent. [S51]

EvidenceMD documents `https://evidencemd.ai/api/v1/chat/completions`; retention and infrastructure claims are vendor statements, not an audit. The existence of an API does not justify sending a medical archive. [S55-S56]

DrugBank documents `/ddi` severity, rationale, management and references under the relevant request. First map every ingredient to a verified identifier. Results do not replace ALIMS/GRLS labels or clinical assessment. [S58]

No unrestricted public API for an ordinary developer was confirmed for OpenEvidence or AMBOSS in this investigation. This does not prove that corporate integrations do not exist. Unofficial wrappers/private endpoints are not verified public APIs. [S35, S38, S57]

## Information APIs

DailyMed supplies SPL labels/metadata; openFDA supplies structured drug-label data with FDA warnings about limitations and use. Neither is a universal interaction engine. [S59-S60]

RxNorm/RxNav supports US name/identifier normalization. The former RxNav interaction API ended on 2024-01-02; a working normalization endpoint does not restore it. [S61-S62]

## Patterns to adopt

Retrieve relevant primary-source passages, explain with exact links and dates, verify product identity separately, then assess interaction evidence and preserve uncertainty. Use wholly synthetic evaluations. Distinguish urgency from diagnosis, product from class, unknown from absent and vendor claims from validation. Do not silently fill gaps in an interaction database with generated text.

## Free path

No paid medical subscription is required by the core package. Optional research candidates include DDInter for local interaction lookup with coverage/license limits; ALIMS/GRLS/DailyMed for labels; and public bibliography APIs for evidence. Documentation reviewed is not a working integration.

See `docs/research/free-medical-tools.md` for licenses and candidates including PharmExpert, PillChecker, MedGemma, MedRAG, OpenEMR and Synthea. Interaction Checker's documented free API/MCP is an additional citation-search candidate, not a validated clinical engine. The core browser plugin does not install, host or call these services automatically.
