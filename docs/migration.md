# English migration coverage

The source general-knowledge folder and its template/integration folders were re-read on 2026-10-06. Individual medical archives and the unavailable personal document images were not used.

## Coverage

| Original general item | English destination | Handling |
|---|---|---|
| `00_INDEX.md` | `knowledge/00_INDEX.md` | Translated, package scope clarified |
| `00_KNOWLEDGE_POLICY.md` | Same path under `knowledge/` | Privacy rules preserved, Git-release cleanup added |
| `01_SOURCE_MAP.md` | Same path under `knowledge/` | All 88 entries and search rules in English; generated from canonical register |
| `02_PRIMARY_CARE.md` | Same path under `knowledge/` | Reasoning, urgency, context and treatment principles |
| `03_RESPIRATORY.md` | Same path under `knowledge/` | Adult scope, symptoms, cough, medicines and evidence limits |
| `04_MEDICATIONS.md` | Same path under `knowledge/` | Classes, identity, label examples and review workflow |
| `05_ALLERGY_SKIN_EYES.md` | Same path under `knowledge/` | Mechanisms and interpretation limits |
| `06_PSYCHIATRY.md` | Same path under `knowledge/` | Classes, monitoring, withdrawal and interactions |
| `07_LABS_PREVENTION_METABOLISM.md` | Same path under `knowledge/` | Tests, pressure, metabolism and vaccination |
| `08_MEDICAL_AI.md` | Same path under `knowledge/` | Systems, research, open weights, APIs and free path |
| `09_STUDY_LOG_AND_ROADMAP.md` | Same path under `knowledge/` | Learning status/gaps retained; private installation links/identifiers omitted |
| `10_WORKFLOW_AND_TEMPLATES.md` | Same path under `knowledge/` | General workflow design; private processing explicitly separate |
| `11_PHARMACOLOGY_FOUNDATIONS.md` | Same path under `knowledge/` | ADME, pharmacodynamics, formulations and ingredient-card structure |
| `12_DRUG_INTERACTIONS.md` | Same path under `knowledge/` | Mechanisms, synthetic pairs, sources and uncertainty categories |
| `13_MEDICAL_CURRICULUM.md` | Same path under `knowledge/` | All twenty discipline areas and study-status criteria |
| `14_PATIENT_RECORD_RULES.md` | Same path under `knowledge/` | General rules for any owner; no actual record handling by public plugin |
| `sources.json`, `sources.csv` | Same paths under `knowledge/` | 88 stable IDs/URLs retained; titles, status, region and purpose translated |
| Five blank template files | `knowledge/templates/` | Markdown translated; already-English JSON preserved without population |
| `Free_medical_tools_2026-10-06.md` | `docs/research/free-medical-tools.md` | Licenses, candidates, access/verification limits and future integration checks |
| `DrugBank_setup.md` | `docs/research/drugbank-connector.md` | English optional developer notes, excluded from browser runtime |
| Prior adapter source ZIP | `examples/drugbank/` | Original English source/tests retained; old README replaced by English integration guide |
| Prior knowledge PDF/ZIP | New English release ZIPs | Derived snapshots superseded; not imported as separate text or treated as additional evidence |

This is a translated and adapted general edition, rather than a byte-for-byte translation of operational storage instructions. It removes private locations, explains public-platform limitations and preserves substantive knowledge, reading depth and gaps. No private cases were converted into public examples.

Source-register identity was compared against the fresh original CSV (including its UTF-8 BOM) and the original JSON. All 88 IDs/URLs and original records matched before English field translation. Original Drive file IDs/URLs and private installation locations are not distributed as provenance identifiers; public primary-source URLs are retained.

Canonical content lives in `knowledge/`. Generated copies in skills make the installed ZIP self-contained. Research documentation and optional adapter code remain in the source archive. The public runtime contains neither developer scripts nor an API backend.
