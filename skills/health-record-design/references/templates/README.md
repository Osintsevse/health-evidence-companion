# Blank health record templates

Copy a form into a separate private archive before entering any information about a person. Never save a filled copy in the general repository.

- `patient_card.template.md`: concise summary and archive starting point.
- `patient_record.template.json`: blank project data structure, not a FHIR resource.
- `medication_entry.template.json`: medicine entry separating prescription from actual use.
- `episode_entry.template.json`: sourced event with uncertainty fields.

See module 14. Null, unknown and empty lists mean information has not been entered; empty allergy/medicine lists do not establish absence. Keep event and recording dates separate. Do not use real people, results or regimens as sample entries.
