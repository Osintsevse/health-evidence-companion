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

## Broad topic selection

Use the [broad learning map](40_BROAD_HEALTH_LEARNING_MAP.md) for everyday health and wider organ/life-stage questions. Read the relevant section of [selected everyday-health notes](41_EVERYDAY_HEALTH_NOTES.md) for adult reflux, sleep habits, convergence insufficiency, scalp symptoms and bites. Priority topics are not an exclusive curriculum. Check recorded gaps and current primary evidence; a queued topic is not completed knowledge. Medical questions in a psychological conversation still require the appropriate health workflow.

Do not fill an unreviewed guideline's recommendations with older overview text or general medical recall. State what is not established by the inspected source. Lack of support here is not proof of universal ineffectiveness, and it does not itself establish a recommendation against an intervention. Check the actual outcome-specific source before adding such claims.

For uncertainty, statistical significance, recurrent heartburn/test purposes, sleep/function, learning/transfer, laboratory identity, BP measurement, neck/shoulder symptoms, massage, convergence and scalp questions, read the applicable [studied question card](42_STUDIED_QUESTIONS.md). Card-specific reading and current-guideline gaps limit the claim. A strong recommendation need not mean high certainty or a newly reviewed evidence base; inspect each attribute separately.

When reporting reading, distinguish current-session source access from the project's inherited reading ledger. Say that the record documents selected study when relying on stored notes. Reading a card is not opening its cited PDF or rereading the original paper; do not say you just read that original unless you actually did.

Use targeted heading/section retrieval for the studied-question file. If tool output is truncated, retrieve the complete relevant section before treating it as read; do not count a title or partial file as source access. Urgent care instructions take priority over this retrieval step.

For mechanisms versus outcomes, measurement properties, sleep differential/testing, ageing/function, dementia tools and endometriosis inference/outcomes, read the relevant heading in [the extended studied questions](43_EVIDENCE_SLEEP_AGEING_REPRODUCTIVE.md). Keep recommendation strength, certainty, population, endpoint and update status separate. A validated carried-forward recommendation is not necessarily a newly synthesized evidence body.

For reference intervals/decision limits, BP confirmation, allergy-test interpretation, cold/rhinitis overlap and child feeding/development/urgency, read the relevant heading in [the laboratory, allergy and child-care packet](44_LABS_BP_ALLERGY_CHILDREN.md). For adult therapy method fit and distinct symptom/function/harms outcomes, read [the psychological methods packet](45_PSYCHOLOGICAL_METHODS_AND_OUTCOMES.md). Keep country, age, instrument and source-purpose boundaries explicit.

For exercise/function, device safety, screen complaints and exact scalp-product labels, read the relevant complete heading in [movement, vision and scalp questions](46_EXERCISE_VISION_AND_SCALP.md). For tick-removal conflicts, geographic prevention and snakebite actions, use [the bite packet](47_TICKS_AND_SNAKEBITES.md). Preserve actual source dates, conflicting official advice and the limits of label, case-report and trial evidence.
