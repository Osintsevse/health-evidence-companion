# Drug interactions and compatibility

General educational module, 2026-10-06. No entry describes an actual individual's treatment.

## What compatibility means

Distinguish drug-drug interactions, drug-condition suitability and duplicate ingredients. Physical compatibility of solutions for mixing/infusion is separate: evidence about taking tablets together does not answer it.

Interactions can increase, decrease or change toxicity. Some combinations are intentional. Clinical consequence, evidence strength and manageability matter; a database alert is not always a prohibition. No entry in a single source does not establish safety. [S66, S88]

## Mechanisms

| Mechanism | Change | Interpretation |
|---|---|---|
| Pharmacodynamic | Additive or opposing effects | Assess total sedation, bleeding and other shared effects |
| Absorption | Binding, intestinal environment or transport | A source-specific interval sometimes helps |
| Metabolism/transport | CYP enzymes or transporters | Consider inhibitor, inducer, substrate and metabolites |
| Excretion | Removal rate | Important with impaired renal function or a narrow therapeutic range |

Sources: S66-S67, S69, S88. Prodrugs may reverse the simplistic "inhibition increases effect" assumption. Effects may persist after discontinuation. There is no universal two-hour separation rule. [S67]

## Synthetic educational combinations

| Combination | Important concern | Sources |
|---|---|---|
| Paracetamol + a cold product containing paracetamol | Duplicate ingredient and overdose risk | S10 |
| Ibuprofen + another NSAID such as naproxen | Additional adverse effects and hidden duplication | S11 |
| Sertraline + NSAID/anticoagulant | Increased bleeding risk; indication and other risks matter | S27, S72, S75 |
| Serotonergic antidepressant + tramadol/dextromethorphan | Serotonin toxicity; check cough-product ingredients | S79 |
| Opioid + benzodiazepine/alcohol | Additive CNS and respiratory depression | S71 |
| Sedating antihistamine such as chlorphenamine + alcohol | Increased drowsiness and driving impairment | S73 |
| Multiple QT-risk medicines | Arrhythmia risk; electrolytes, conditions and metabolic interactions matter | S74 |
| Grapefruit + certain medicines | Increased exposure through CYP3A4 in some cases; fruit juice can instead reduce fexofenadine absorption | S70 |
| St John's wort + psychotropic/other medicines | Pharmacodynamic and enzyme interactions; natural does not mean risk-free | S67, S72, S75 |

This is not exhaustive and does not direct automatic medicine withdrawal. Do not apply one serotonergic warning equally to every antidepressant or analgesic. Verify severity and management for the exact ingredients and labels.

## Source hierarchy

1. Exact local product: ALIMS SmPC/PIL for Serbia or GRLS for Russia. SmPC sections 4.3-4.5, 4.8 and 5.2 are useful. [S12-S16, S76]
2. A professional interaction reference if legitimately available: Stockley's, BNF or Lexidrug. NHS SPS discusses resource selection. Full paid databases were neither studied nor copied here. [S37, S68]
3. FDA enzyme/transporter tables, NHS SPS mechanism resources and a QT guide support mechanism checks, not a complete clinical conclusion. [S69, S74]
4. Licensed DrugBank API may support automation after terms, coverage and identification checks. Vendor severity and citations require interpretation. It is not a mandatory dependency. [S58]
5. DailyMed/openFDA provide US labelling, not a universal interaction verdict. RxNorm supports identity normalization; the former RxNav interaction API ended on 2024-01-02. [S59-S62]

DDInter is an optional research candidate with separate noncommercial data licensing and limited downloadable coverage. No DDInter dataset is bundled. See module 08 and the free-tools review.

## General review workflow

Establish ingredients, form, route, dose range and timing relevant to the question; include regular, as-needed, OTC, supplement, herbal and alcohol exposures. Keep unknown composition unknown. Factors such as indication, pregnancy, allergies, kidney/liver function, bleeding, electrolytes or ECG may change interpretation; ask only relevant non-identifying context and respect the public plugin's PHI boundary.

Check duplicate ingredients/classes, then pairs and cumulative effects across the list. For recently stopped drugs, use the source's persistence information. Compare alerts with local labelling. Preserve conflicting sources and uncertainty.

Explain: combination -> mechanism -> potential outcome -> evidence strength -> clinical relevance -> question/next step -> source URL/version/check date.

Use distinct outcomes: contraindicated in the exact label; needs clinician/pharmacist review or monitoring; permitted under stated conditions; no clinically important interaction found in the consulted sources; insufficient data. The last two differ. An incomplete list cannot establish the safety of a whole regimen.

## Workflow exercises

All are wholly synthetic: unknown cold-product ingredients plus paracetamol (establish ingredients first); sertraline plus ibuprofen (explain bleeding risk without automatically stopping the antidepressant); codeine plus a CYP2D6 inhibitor (consider reduced activation); separating an enzyme inhibitor from a substrate (do not declare the interaction resolved). These test information handling, not diagnostic accuracy.
