# Source-grounded reasoning

Reviewed 2026-10-17. This is an answer-construction workflow, not a diagnostic algorithm or a claim of validated clinical performance. Read it with `EVIDENCE_METHODS.md` (installed as `evidence-methods.md`), `27_FOUNDATIONS_AND_LEARNING_INDEX.md`, the relevant topic module and the current source-use policy. These supporting references are bundled with the skills that use this workflow.

## Match support to the question

| Question | Support to inspect | Inference to avoid |
|---|---|---|
| What does a concept mean? | Exact textbook edition and section or an authoritative educational source | Treating a definition or mechanism as evidence that an intervention works |
| What does a measurement show? | What was measured, how, in whom and under what conditions | Equating a proxy, positive test or observed behavior with the condition or process of interest |
| Does an intervention help? | Applicable current guidance and outcome-specific studies; comparator, benefits, harms and uncertainty | Inferring benefit from plausibility, improvement without a comparator, or a surrogate alone |
| Does this apply here? | Age, anatomy, setting, formulation, baseline risk and relevant alternatives | Transferring an adult result to a newborn or a group average to an individual prediction |
| What can this source support? | Actual sections read, access limits, version and applicable rights | Treating a search hit, abstract, bibliography or recent retrieval date as full current appraisal |

The evidence and scope rules come from **evidence methods**, **medical source maintenance** and **psychological evidence triage**. The examples below connect those rules to bounded concepts; they are not additional clinical decision rules.

## Construct an answer

1. Address immediate danger first under the applicable emergency skill. For a nonurgent question, identify the actual question and one missing detail that would materially change the answer. Do not ask for an entire history by default.
2. Separate reported observations, measured results, source-supported explanations and working interpretations. Preserve an important plausible alternative when the available evidence does not distinguish it.
3. Select the exact source section for each consequential claim. A background textbook can explain a mechanism; diagnosis, treatment, dose and safety claims need current applicable evidence. If the needed source is unavailable or restricted, narrow the claim and state what remains unchecked.
4. Check the inferential step: could selection, confounding, measurement error, a different mechanism or a population mismatch explain the observation? A named possibility is not itself evidence that it occurred.
5. Explain the supported conclusion in plain language, the practical limit and what observation or professional assessment could reduce uncertainty. Match confidence to support. Do not invent a probability, causal story or treatment recommendation to make the answer sound complete.

## Bounded concept links

- Random sampling concerns inclusion from a population; random assignment concerns allocation to conditions. Neither guarantees the purpose served by the other. See **study design**.
- A behavioral task measures performance under specified conditions; the proposed mental process is an interpretation requiring justification. See **psychological foundations**.
- Innate and adaptive responses interact. This framework does not identify an individual's immune defect or justify an immune treatment. See **immune foundations**.
- Gestational age and birthweight describe different dimensions. One value does not reconstruct the other or supply a current individual risk estimate. See **newborn foundations**.
- Sensitization is not the same conclusion as clinical allergy; negative imaging has condition-specific limits. See **allergy** and **endometriosis**.

## Source identity and learning status

Use `medical:Snn` or `psychology:Snn` for cross-domain citations: the same numeric ID can identify different sources in the two registers. An unqualified ID inherits the document's domain and must not silently switch registers. Bibliographic metadata, abstract-only reading, selected sections and full-text reading remain distinct. A newly read section extends only that section's recorded scope.

Store short original explanations with a question, scope, source edition/section, actual reading date, uncertainty and a recheck trigger. Do not reconstruct chapters, reproduce protected figures/tables or infer that technical validation is substantive scientific review. Changes remain subject to maintainer review; these instructions do not train model weights or establish improved patient outcomes.
