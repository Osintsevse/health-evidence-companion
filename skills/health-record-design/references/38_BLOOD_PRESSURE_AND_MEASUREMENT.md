# Blood pressure and measurement

Scope: general adult education and owner-authorized historical views. Not a diagnosis, treatment target, pregnancy/child algorithm or emergency monitor. Checked 2026-10-09. New explanations use original synthesis, not copied source tables; rights remain with linked sources.

## Parameters and devices

SYS/SBP and DIA/DBP are systolic and diastolic arterial pressure, in mmHg. Pulse is heart rate, in beats/min; pulse pressure is SBP minus DBP. Manual auscultation identifies first and disappearing Korotkoff sounds while cuff pressure falls. Electronic oscillometry estimates BP from cuff oscillations using an algorithm; hand inflation alone does not identify the measurement principle. Training, cuff fit and independent device validation matter. [S637]

## Interpreting ranges

AHA 2025 adult categories use the higher component: normal <120/<80; elevated 120–129 with <80; stage 1 130–139 or 80–89; stage 2 ≥140 or ≥90. This is a US category scheme, not a diagnosis from one reading or a universal treatment goal. The inspected official summary does not replace the full guideline. [S389]

NHS uses ≥140/90 in clinic and ≥135/85 at home for high BP; these setting-specific diagnostic thresholds should not be mixed with AHA category labels. ABPM needs period averages and its own interpretation, not a colour attached to every raw point. [S638, S637]

A low component (<90 systolic or <60 diastolic) is flagged independently in the educational UI: a high/low combination must show both explanations. Symptoms, usual baseline and repeated observations determine significance; the flag alone does not establish symptomatic hypotension. NHS low-pressure information supports context and dizziness/fainting review, not this plugin's colour design. [S391]

Resting adult pulse commonly spans 60–100/min; medicines, training, activity, temperature and emotions change interpretation. No pulse colour or combined health score is assigned from this interval. [S639]

For preparation and repeat measurements, follow the linked [AHA home instructions](https://www.heart.org/-/media/Files/Health-Topics/High-Blood-Pressure/How-to-Measure-Your-Blood-Pressure-Letter-Size.pdf). [S388]

Current severe BP with concerning symptoms needs emergency assessment; historical points cannot establish current urgency. The linked [AHA monitoring page](https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings/monitoring-your-blood-pressure-at-home) provides repeat-reading and urgent-action guidance. Do not change medicines from archive colours. [S640]

## Read-only archive contract

The `blood_pressure.py` helper projects committed, active, reviewed exact observations without changing the ledger. English and Russian exact aliases and explicit mmHg/bpm aliases are supported; no fuzzy naming, unit conversion, zeros or synthetic components are introduced. Other raw values stay visible. Use explicit locators such as `measurement[0]; SYS` and `measurement[0]; DIA` for one source-local measurement. Separate source-local measurement IDs are needed for repeats. Missing locators or duplicate components do not justify guessing pairs; ambiguous components stay separate with a warning.

Dates/times come from the event date or the existing ABPM `(1)HH:MM` / `(2)HH:MM` locator convention. Import timestamps are not measurement times. Missing time stays missing. Unknown, partial, invalid or future dates remain in a separately labelled source-order graph/table. All horizontal spacing is ordinal source order, not elapsed time; no interpolated trend is claimed. No adult categories are assigned to ABPM points.

The offline Measurements view starts with a collapsed, framed guide. The plot uses an up arrow for systolic, down arrow for diastolic and lightning for pulse, with separately labelled mmHg and pulse axes. Hover, focus, click or keyboard activation selects the entire reading with both pressure values, pulse, source links and component explanations. The initial filter is All measurements. Table columns retain date, time and all three numbers; a missing number is explicitly unrecorded.

Clinical colours default off. In a private generation configuration, set `blood_pressure_categories` to `aha_2025_adult` only after confirming adult applicability and exclusions. This opt-in is an explicit display convention, not automated age inference or clinical validation. Unknown/incomplete pairs are unclassified. General guidance does not replace a dated personal clinician assessment. All files and UI stay offline; the plugin sends no records or telemetry.

## Reading and validation limits

S637: AHA 2019 scientific statement (PMC author manuscript made available in 2024); selected BP component, auscultatory/oscillometric and technique sections read, not the whole statement. S389: 2025 official guideline summary rechecked, full guideline not read. S388: one-page home measurement instructions previously inspected; the current home page was rechecked as S640. S391: NHS low-pressure page rechecked. S638/S639/S640: the relevant public guidance sections inspected. Bibliography is not clinical approval, device certification or redistribution of publications. NHS adaptation attribution is in `medical-source-attribution.md`.

Synthetic regression cases cover repeats, language aliases, unclear pairing, missing components/time, date precision, incompatible units, non-exact/unreviewed values and mixed high/low explanations. Packaging/runtime checks establish implementation behaviour only. Maintainer and suitable clinical review remain necessary before release.
