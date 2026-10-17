# Grounded knowledge review — 2026-10-17

Candidate version 0.9.0. The change adds bounded original explanations and an answer-construction workflow; it does not establish a completed curriculum, learned model weights or improved clinical outcomes. Twelve skills explicitly load the workflow and its supporting references. The initial eight were extended after a static loading audit to prevention, mental-health information, nutrition and care navigation.

## Question, reading scope and recheck trigger

| Question | Source and actual scope | Limit and recheck trigger |
|---|---|---|
| What do sampling and assignment support? | psychology:S104, OpenIntro Statistics 4e, screen-reader copy updated 2022-10-21; sections 1.2.5, 1.3.1, 1.3.3–1.3.4 and 1.4–1.4.1; selected PDF pp. 20, 24–28, 36 read 2026-10-16; metadata checked 2026-10-17 | Introductory concepts only. Read design-specific methods before judging a consequential causal estimate. |
| What can behavior reveal about a mental process? | psychology:S103, E. Bruce Goldstein, fifth edition, copyright 2019; printed pp. 5–9 read 2026-10-16 and pp. 10–12 read 2026-10-17; relevant figures visually checked | Historical conceptual examples, not diagnostic standards. Check the validity of a particular task and alternatives before strengthening a construct claim. |
| How do innate/adaptive responses and IgE sensitization work? | medical:S641, Abbas, Lichtman and Pillai, seventh edition (2012); printed pp. 2–3 read 2026-10-16 and pp. 426–428 read 2026-10-17; relevant figures checked | Mechanism only. Recheck current evidence for molecular details, diagnostic accuracy, treatment effects or immune interventions. |
| Why record gestational age and birthweight separately? | medical:S642, Nelson Textbook of Pediatrics, nineteenth edition (2011); printed pp. 552–553 read 2026-10-16 | Historical concept only. No cohort graph, numerical prognosis or current classification is reproduced. Use current pediatric standards for clinical assessment. |
| What does a positive peanut test establish? | medical:S643, AAAAI 2020 parameter; PDF pp. 1–3 and 30 read 2026-10-17 | Peanut-specific, conditional recommendations and limited certainty. Directory status is not a new systematic review. Recheck for other allergens, methods or clinical decisions. |
| What can selected endometriosis recommendations support? | medical:S363, ESHRE 2022; additional PDF/printed pp. 9, 11, 21–22, 27, 29, 31–32, 35–36, 67–68, 125–126 read 2026-10-17; four pages visually checked | Selected passages only. Individual cited studies were not independently appraised. New biomarkers, approvals and individual care require newer applicable evidence. |

Canonical registers retain earlier source identities and reading history. The scoped NICE NG73 record remains bibliographic under the current source-use policy; the revised endometriosis passages use independently read ESHRE sections. This is not an audit or refresh of every historical source in the project.

## Attribution and content boundary

These are short original factual syntheses and workflows. No book files, chapters, page images, extracted full texts, licensed test instruments, tables or source figures are included. External copyrights and file-specific licenses remain with their owners. The MIT license covers original project material, not the cited books. No permission to redistribute a source follows from access to it. OpenIntro attribution and its resource-specific ShareAlike conditions remain recorded in psychology:S104; no source passage, exercise or figure is adapted here.

A separate source review checked the changed endometriosis and peanut-test assertions against the enumerated official sections and found no substantive mismatch. This is a bounded source check, not independent professional clinical validation. Selected older textbook reading is never presented as a current treatment standard.

## Executed fresh-context response checks

Two fresh-context agents received the selected skill and relevant bundled references plus the four fictional questions below. They did not receive implementation history, diffs, evaluation fixtures or expected answers. Neither agent performed a new web review. Outputs are preserved below in their original English. Review found the four responses retained the requested inference limits; there was no comparison with the previous version or estimate of real-world accuracy.

The seven separate prompts in evals/grounded-reasoning.json remain unexecuted fixtures. They are not these four observed responses. Structural/unit checks and these limited response checks do not establish clinical validation, emergency handling, live source retrieval or behavior in an installed host.

### A — Positive peanut-specific IgE

**Fictional request:** In a fictional example, someone has a positive peanut-specific IgE result but has never noticed symptoms after eating peanut. Does the number prove a dangerous peanut allergy, and can it tell how severe a future reaction would be?

**Actual response:**

A positive peanut-specific IgE result shows sensitization; by itself, it does not prove that eating peanut causes a clinical allergy. The result also cannot predict how severe a future reaction would be. Interpretation depends on the exposure history and symptoms. Do not test this with a home food challenge; a clinician can advise whether further assessment, including a supervised challenge, is appropriate.

Informational tool, not intended for use as a medical device; not a diagnosis or prescription and not a substitute for clinical care.

### B — Normal ultrasound and pain relief

**Fictional request:** In a fictional example, an adult has ongoing pelvic pain and a normal ultrasound. Does that rule out endometriosis, and should they automatically arrange laparoscopy? They also ask whether pain relief with an analgesic would prove endometriosis.

**Actual response:**

A normal ultrasound does not rule out endometriosis, especially superficial disease. Laparoscopy can be considered when imaging is negative and other evaluation or treatment makes it appropriate, but a normal scan does not make surgery automatic; that decision should be discussed with a clinician. Relief from an analgesic can help with pain, but it does not prove endometriosis or show that the disease has changed.

Informational tool, not intended for use as a medical device; not a diagnosis or prescription and not a substitute for clinical care. The endometriosis guidance notes that its review of the 2026 ACOG announcement did not include the full clinical practice guideline, so detailed recommendations from that guideline were not checked.

### C — Random assignment in a volunteer sample

**Fictional request:** A fictional study recruited 40 volunteers from one club and randomly assigned them to two learning tasks. Since assignment was random, can we say this represents all adults? If task A did better, what causal claim is justified?

**Actual response:**

Random assignment and representative sampling answer different questions. Because the 40 volunteers came from one club, the study does not establish that they represent all adults. If assignment was carried out properly and the comparison was analyzed appropriately, a better result for task A could support a causal claim that **assignment to task A improved the measured learning outcome, on average, among these volunteers under the study conditions**. The sample is small, so the size of that effect may be uncertain. The result alone does not show that task A would work the same way for all adults.

### D — Memory performance and an unanswered message

**Fictional request:** A fictional person was slow in a memory task and did not reply to one message. Does this prove a memory disorder or that they are deliberately avoiding someone? Explain what the observations do establish and how to investigate without diagnosing.

**Actual response:**

The observations establish that the person was slow on that memory task under the conditions in which it was given, and did not reply to one message. They do not establish a memory disorder or deliberate avoidance. Task performance can vary with context and other factors; silence can have several explanations, and its function cannot be inferred from the action alone.

To investigate, first describe the observations precisely, including the task, conditions and timing. If the concern continues, look for a pattern across tasks or situations and ask the person neutrally about context. A qualified professional can assess persistent memory difficulties using a broader history and appropriate evaluation. For the message, a calm, direct check-in is more informative than assuming a motive.

The clinical context read health-explain and its grounded-reasoning, allergy, endometriosis and symptom-reasoning references. The methods context read psyops-research and its evidence-triage, evidence-methods, foundations and grounded-reasoning references.

## Required review and remaining study

Maintainer review remains required before merge. The next literature work should target current permitted diagnostic guidance for endometriosis, pediatric age-specific assessment, allergy test validation and respiratory-infection evidence. These additions do not imply those areas or any entire book have been fully studied. Each future contribution needs a question, exact source/edition, actual reading scope, uncertainty and recheck trigger.

## Technical validation

Initial candidate full run: 288 repository tests, 285 passed and 3 skipped (two unavailable Windows symlink privileges and one optional browser runtime); 8 offline adapter tests passed separately. Structure/content validation and the release-candidate build passed. The citation and amendment tests use synthetic registers/files and check real rejection paths. Generated references, qualified source metadata and the explicit package manifest were synchronized. These results establish software checks only; they do not convert the four response checks or the authored fixtures into clinical validation.

## Follow-up source and loading audit

See [the open-source shortlist](open-source-audit-2026-10-17.md). The four additional entrypoints have an explicit reading hook and matching bundled references; one follow-up context exercised prevention with two fictional questions recorded in the shortlist report; the other three additions have static checks only. The original four observed responses remain the initial response evidence. A brief separately sourced serum-model example was added to distinguish internal validation from external clinical validation and from saliva-test evidence. OpenStax is now an explicit bibliographic-only rule in the source-use policy.
