# Free medical tools: APIs, GitHub, models and databases

Documentation and license review dated 2026-10-06. General information only; no personal health information was used.

## Project decision and verification status

The core browser plugin requires no paid medical API. The earlier DrugBank adapter remains optional research code. Use official labels for products, interaction references with explicit coverage, and public bibliographic resources for research. A local medical model is an optional experiment.

Free code/data access does not make computers, electricity, hosting or maintenance free. Code licenses do not automatically cover data or model weights.

Documentation, READMEs and terms were reviewed; PharmExpert dependencies were also inspected. Repositories were not installed, models were not run and independent clinical validation was not performed. Trial GET results from DailyMed, openFDA and Interaction Checker could not be obtained through the research interface. This limits verification and does not prove the services are broken. MCP handshakes and live endpoints remain unverified.

## Medicines and interactions

| Resource | Access | License/cost and conclusion |
|---|---|---|
| [DDInter 2.0](https://ddinter2.scbdd.com/) | Interaction mechanisms, severity, website and CSV | Data CC BY-NC-SA 4.0: noncommercial, attribution, ShareAlike. Candidate local reference; verify pair coverage |
| [PharmExpert](https://github.com/AnnaKazarian13/pharmexpert-drug-interactions) | RU/EN UI, local SQLite, DDInter and additional rules | MIT code; DDInter data separately restricted. Useful implementation pattern, not audited clinical software |
| [PillChecker API](https://github.com/SPerekrestova/pillchecker-api) | OCR ingredient extraction and DDInter/openFDA pairs | MIT code; data/models separate; requires hosting. Confirm extracted product identity |
| [Interaction Checker](https://interaction-checker.com/api) | Documented public REST pair search with label citations | Vendor says no key/fee, ten requests/minute/IP, up to ten items. Citation-search candidate only |
| [DailyMed](https://www.dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm) | SPL labels, metadata and versions via GET v2 JSON/XML | Public information API; not comprehensive interaction assessment |
| [openFDA](https://open.fda.gov/apis/authentication/) | Labels and other FDA datasets | Free keys; documentation describes 1,000 requests/day/IP without a key. Check current access terms and limits |
| [RxNorm/RxNav](https://lhncbc-portal.lhcaws-prod-pub.nlm.nih.gov/RxNav/information/FAQs.html) | Medicine-name/identifier normalization | Main APIs need no license, with a proprietary-endpoint exception. Interaction API ended 2024-01-02 |

### DDInter limits

The documented download lists groups A, B, D, H, L, P, R and V and is not equivalent to the complete website database. Absence of separate N/C downloads does not mean no pairs involving those drugs: they can appear as the other participant. Do not assume complete psychiatric/cardiovascular coverage.

If importing into a separate licensed system, retain version, license, retrieval date, IDs and covered groups. Do not generate missing interactions. A documented public DDInter REST API was not confirmed; do not invent endpoints or treat internal website calls as a stable contract.

References: [terms](https://ddinter2.scbdd.com/terms/), [download](https://ddinter2.scbdd.com/download/), [explanation](https://ddinter2.scbdd.com/explanation/). This MIT project does not bundle DDInter data or sublicense it as MIT.

### PharmExpert and PillChecker audit questions

PharmExpert describes Russian/English normalization, a local index and the principle that not found does not mean safe. It does not model dose, route or individual risk factors. Review manual FDA overrides, matching, data currency and failure handling before reuse. Its inspected requirements list Streamlit without a paid LLM dependency.

PillChecker describes local extraction and an API. Its DeBERTa fallback classifies severity from text: distinguish this generated estimate from DDInter's source classification. A hosted test URL does not establish permanent free access or permission to send personal documents.

### Documented remote MCP candidate

Interaction Checker advertises `https://interaction-checker.com/mcp`, Streamable HTTP, no authentication, eight tools and 60 requests/minute/IP. The owner documents connectivity; handshake/tools-list were not verified. It is an independent service, not FDA/NIH software. Open-source engine code was not confirmed.

Severity uses text rules/class matching; the owner notes false positives and formulation differences. Use retrieved citations to open the original label, not as a final clinical verdict. Browser-side privacy claims do not extend automatically to API calls: an API sends the submitted list to the server. Its privacy page discusses analytics/logs, so "no trackers" elsewhere is not a verified assurance.

References: [MCP](https://interaction-checker.com/mcp), [method](https://interaction-checker.com/about), [privacy](https://interaction-checker.com/privacy).

## Source-access MCP servers

| Repository | Purpose | Conditions and assessment |
|---|---|---|
| [RowanErasmus/dailymed-mcp-server](https://github.com/RowanErasmus/dailymed-mcp-server) | SPL search, metadata and history | MIT, Node/TypeScript, local execution; upstream unauthenticated. Narrow candidate for code review |
| [GoogleCloudPlatform/hcls-mcp-servers](https://github.com/GoogleCloudPlatform/hcls-mcp-servers) | RxNorm/DailyMed, PubMed, MedlinePlus, ClinicalTrials and other modules | Apache-2.0, Python, local path documented; some modules need keys. Select necessary modules |
| [danielk-am/clinical-evidence-mcp](https://github.com/danielk-am/clinical-evidence-mcp) | PubMed/Europe PMC, ClinicalTrials, labels and FAERS | MIT, Node, optional NCBI key; hosted service needs token. Hosted free access unconfirmed |

Google Cloud branding does not make local execution paid. Cloud Run deployment requires billing and is outside the no-paid-hosting path. Review deployment/logging configurations rather than copying them blindly.

These expose sources, not validated diagnosis. FAERS report counts are neither adverse-event rates nor proof of causality. Trial registration does not establish efficacy.

[Europe PMC REST API](https://dev.europepmc.org/RestfulWebService) supports public bibliography search. Searchable metadata is distinct from reusable full text: include only material with appropriate rights, not every DOI result.

## Models and retrieval

| Project | Pattern | Cost/limits |
|---|---|---|
| [Google-Health/medgemma](https://github.com/Google-Health/medgemma) | Local text/image/document processing | Apache-2.0 code, HAI-DEF weights. Local access is not a free hosted API |
| [gzxiong/MedRAG](https://github.com/gzxiong/MedRAG) | Retrieve passages before generation; compare retrieval approaches | Public Domain Notice for code. Commercial model examples need paid APIs; local models need compute. Corpus rights are separate |

MedGemma 1.5 4B is a manageable experiment scale, not proven superior medical advice. The reviewed 1.5 model card describes a 4B variant; do not mix it with earlier 27B models. Russian/Serbian output, dose extraction and reliability need separate testing. [Model card](https://developers.google.com/health-ai-developer-foundations/medgemma/model-card) requires adaptation/validation; a model must not fill missing interaction records. [MedRAG license](https://github.com/gzxiong/MedRAG/blob/main/LICENSE).

## Records and synthetic evaluation

- [OpenEMR](https://github.com/openemr/openemr): GPL electronic records system with API/FHIR; may be excessive for one archive. Deployment needs separate access control, updates and backups. Real records remain outside general knowledge.
- [Synthea](https://github.com/synthetichealth/synthea): Apache-2.0 synthetic-history/FHIR generator for import testing, not treatment evidence.

## Possible future free stack

Official ALIMS/GRLS labels, DailyMed for supplementary ingredient/form information, a separately licensed local DDInter lookup, Europe PMC/PubMed research search and selected source-access adapters. MedGemma/MedRAG only if an evaluated local component adds value. The distributed browser package requires none of these deployments.

No free complete substitute with guaranteed coverage equivalent to licensed professional interaction references was found. Open GitHub code does not itself establish clinical reliability.

Before any future integration, pin a commit and inspect code/data licenses, dependencies and outgoing requests. Use synthetic inputs first. Test network failure, unknown names, ambiguous salt/form, multi-ingredient products, stale data and missing pairs. Preserve citations/source severity and label model estimates separately. Never place medical records, real medicine lists, keys or private query logs in this repository.
