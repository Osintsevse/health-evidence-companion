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
