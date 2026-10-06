# Universal private health record rules

General design guidance for any owner. Filled records always remain outside this knowledge repository. The public plugin explains this design; it does not collect or maintain identifiable records.

## Creation

Copy a blank template into a separate private location. Establish owner, identifier, creation date and private access. Collect only necessary information; passport details and other people's contacts are usually irrelevant. Check every export before sharing.

Recommended sections: current summary, physical episodes, psychiatric monitoring, unified medicine history, allergies/adverse reactions, vaccinations, investigations, originals, questions/uncertainties and corrections. Psychotherapy notes can have separate storage and permissions.

## Provenance and certainty

For each fact, retain its source: owner report, medical document, test or other evidence. Distinguish reported, documented, inferred and unreadable. A document does not prove present-day status.

Keep event date, recording date and document date separately where needed. Preserve partial date precision; never invent the first day of a month. Missing information is not an explicit negative. These principles are informed by FHIR Provenance, but the project's simplified JSON format is not a FHIR resource. [S87]

## Conditions and investigations

Keep complaint, observation, hypothesis and clinician-established diagnosis separate. An owner-reported diagnosis without documentation remains reported. A relative's condition does not become the owner's diagnosis. Add ICD codes only for a justified match; a code does not confirm disease.

For investigations, retain analyte, value, unit, that laboratory's reference, date and known conditions. One abnormal value is not a final diagnosis. Preserve the original separately; a summary does not replace it. Never guess an unreadable dose or result from OCR or a photograph.

## Medicines

Separate prescribed treatment from actual use. An old discharge document does not establish current use. Retain source and status; this distinction is also reflected in FHIR MedicationStatement. [S85]

Fields: brand/INN, formulation, strength/concentration, route, dose/unit, regular or as-needed regimen, indication, dates, prescriber where necessary, actual-use status, source and last reconciliation. Record benefit, adverse effects, missed doses and changes separately.

Useful statuses: prescribed but not started; reported taking; as-needed; paused; completed; discontinued; unknown. Recommended, purchased and taken are not equivalent. Interaction work needs a single reconciled list across physical and psychiatric care, OTC products and supplements rather than disconnected partial lists.

## Allergies and adverse reactions

Retain substance, reaction, timing, severity, source, certainty and subsequent clarifications. Drowsiness or nausea is not automatically allergy. Distinguish unknown, not yet reviewed, no known allergies reported after review, and a reported/documented reaction. An empty list does not mean no allergies. [S86]

## Psychiatry and psychotherapy

Psychiatric records hold relevant symptoms, documented assessments, medicines, effects and follow-up. Do not transfer entire psychotherapy conversations automatically. Any necessary transfer uses a minimum relevant fact and source within an authorized private record, respecting owner permission and actual access.

## Updates and corrections in an authorized private system

1. Read the current summary and related records; verify the correct owner.
2. Add a dated sourced fact; check duplicates and contradictions.
3. Preserve old prescriptions; update current status only with confirmation.
4. Date corrections, explain the reason and reference the original entry. Mark an erroneous entry as such. Owner-requested deletion/access restriction is a separate operation including copies.
5. Update the concise summary and read back the saved version.

Show last reconciliation dates for medicines, allergies and significant conditions. Preserve unresolved source disagreement rather than silently picking a convenient version.

## Clinician handoff and AI

Prepare a minimum relevant summary: current question, trajectory, significant conditions, allergies, actual medicines, investigations and questions. Share with the selected recipient only under the owner's decision. Never publish records as part of the general corpus.

Do not claim access to unseen chats or background updates. A private update requires available source material and working authorized storage. An AI suggestion remains an informational hypothesis unless established by the appropriate clinical source.
