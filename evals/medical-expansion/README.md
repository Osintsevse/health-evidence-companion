# Medical expansion behavioural fixtures

`cases.json` contains wholly synthetic prompts and explicit review criteria across the twelve clinical reference modules. Some prompts combine later-turn changes to test whether an initial explanation is revised when new danger or contradictory evidence appears. They are authored fixtures, not recorded patient histories.

Every reusable fixture retains `execution_status: not_executed_fixture`. This file is not a model response log or a clinical validation dataset. A separate forward-check record identifies the limited prompts actually presented to fresh-context agents, the instructions they read, observed answers, reviewer findings and limits. Never infer that all fixtures passed from schema or packaging checks.

For meaningful execution, give a fresh evaluator only the user prompt and the actual selected skill and bundled references; withhold this rubric, packet notes and expected answers. Assess the answer before providing the next fictional turn. Use no real history, private record, outbound contact or irreversible action. A later-turn change must be evaluated against the new evidence, with urgency and uncertainty recalibrated.

Checks should include action-first emergency replies, age/jurisdiction-specific sequences, exact medicine identity, uncertain units, symptom resolution that does not clear a TIA, optional history fields, nutrition estimates with missing portions, regulated test/therapy versions, respectful calibrated risk, and verification of facility capability. Passing a few examples does not establish sensitivity, specificity, clinical benefit or safe autonomous triage.
