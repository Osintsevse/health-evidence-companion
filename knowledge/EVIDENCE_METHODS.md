# Evidence appraisal methods

Frame population, intervention, comparator and outcomes. Start with applicable current guidelines, then systematic reviews and primary research for unresolved questions. Distinguish recommendations, evidence and interpretation.

Record design, sample, baseline risk, comparator, follow-up, patient-relevant outcomes, absolute/relative effects, intervals, missing data, bias, funding and applicability. Mechanisms, surrogates, uncontrolled reports, vendor benchmarks and trial registration do not establish clinical benefit.

Randomized evidence can support many efficacy questions; observational studies can inform rare harms with confounding limits. Evidence level does not resolve a population mismatch. Do not combine incompatible endpoints or invent numbers from qualitative abstracts.

## Sampling, assignment and the inference being made

Sampling determines which cases enter a study from a target population. Random selection can reduce some selection bias, but an incomplete sampling frame or selective nonresponse can still limit generalization. Random assignment allocates enrolled cases to experimental conditions and helps make groups comparable on average. It does not make the recruited sample representative; representative sampling does not itself assign exposure or establish causation. [psychology:S104]

In observational data, an exposure-outcome association can reflect several processes. A factor related to both can create or distort the relationship, including when that factor was not measured. Association alone therefore does not identify a causal effect. Describe what the design supports before making a causal explanation; simply naming a possible confounder does not establish that it explains the result. [psychology:S104]

For a wholly synthetic example, imagine volunteers randomized between two learning tasks. Random allocation can support an experimental comparison within those volunteers, but it does not establish that the volunteers represent every age or clinical population. Conversely, a representative survey that records task choice does not randomize that choice. These invented scenarios illustrate different inferential questions; they contain no observed treatment effect. Source for the underlying distinctions: [psychology:S104].

Reading scope: *OpenIntro Statistics*, fourth edition, screen-reader version updated 21 October 2022, sections 1.2.5, 1.3.1, 1.3.3-1.3.4 and 1.4-1.4.1. Only the listed introductory sections were read; this is not a complete causal-inference method or a review of an intervention.

Preserve URL, publication/version, section actually read, check date and limits. Identify conflicts, corrections/retractions and uncertainty. A source merely mentioning a topic cannot substantiate a specific outcome claim.

Create original cards: question, scope, explanation, benefits/harms, exceptions, sources and remaining uncertainty. Do not reproduce articles, commercial chapters or datasets without permission. These procedures do not claim a completed systematic review or clinical validation.

## Efficacy checks and discovery lists

Use module 18 for the indication-specific gate and watchlist. Secondary catalogues identify candidates; their labels, publication counts and foreign-registration comparisons cannot replace primary evidence. Insufficient evidence, demonstrated little/no effect for a particular outcome, a guideline recommendation against and uncertain benefit are different conclusions. Pending appraisal gets no positive efficacy endorsement.

Inspect whether the outcome matches the claim: symptom relief need not reduce mortality, while a surrogate cannot establish prevention of complications. Funding/conflicts prompt scrutiny, not automatic exclusion. Record absolute effects when available, uncertainty, missing meaningful outcomes, replication and the relevance of age, country, formulation and timing. Check corrections/retractions and newer reviews; an older review's publication date is separate from its search end date.

Report guideline disagreements with their scope and reasoning. For example, WHO's 2024 influenza recommendations and CDC's inspected US clinician guidance differ for some non-severe treatment decisions. Do not silently substitute one country's policy or flatten all antivirals into a single verdict. [S111, S128]

For each new consequential question, recheck current local labels, vaccine calendars/outbreak orders and interaction sources. Review general summaries when new guidance emerges and at a documented periodic content audit. This is a maintainer procedure, not an implemented background monitor. Access errors remain errors; they never become proof of safety or ineffectiveness.

## STAT-F1 — Pairing changes the analysis unit, not causal identification

Pairing means that each observation has a meaningful counterpart, for example two measurements on the same participant. For a paired mean comparison, take one difference per pair in a consistent direction: twenty people measured twice provide twenty differences, not forty independent observations. Uncertainty uses variation among those differences and the number of pairs. Dependence within a pair is expected; independence between pairs and the adequacy of the differences for the chosen method still need assessment. Repeating readings does not create independent participants. [psychology:S104]

An unpaired mean comparison instead concerns two groups without that correspondence, with uncertainty reflecting both groups and appropriate independence/distribution checks. Choose the method from the design; selecting whichever produces a smaller p-value changes the question. A pre/post difference describes change, while pairing handles dependence. It does not supply an untreated comparison or random assignment: time and other influences remain alternative explanations. The causal limit combines this selected reading with the earlier design sections. [psychology:S104]

**Original invented arithmetic:** four fictional puzzle times change from [40,55,70,85] to [38,52,69,79] seconds. Second minus first gives [-2,-3,-1,-6], with descriptive mean -3 seconds over four pairs. No p-value, interval, distributional adequacy or treatment effect is inferred. Practice is a possible explanation, not an established cause.

**Actual additional reading:** Diez, Çetinkaya-Rundel and Barr, *OpenIntro Statistics*, fourth edition, screen-reader copy updated2022-10-21, pp295–297 and301:7.2/7.2.1, selected7.2.2 opening/calculation and7.3/7.3.1 opening. These four pages are not the full sections or a repeated-measures/causal-inference course. Exact file licence and current provider terms were checked. The source textbook is [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); these are original factual notes and invented data, with no copied source example, figure or exercise. Clustering, serial correlation, missing pairs, crossover designs and clinical interpretation need further evidence.

## STAT-F4 — What varies when an estimate has sampling uncertainty?

An individual observation, a sample statistic and a population parameter are different objects. A sampling distribution describes how a chosen statistic would vary across samples generated by the specified sampling process. It is not the distribution of the individual observations in one sample. Standard error describes the spread of that estimator distribution; it is neither raw-data spread nor the known realized error of a particular estimate. Substituting an observed proportion for an unknown population proportion estimates uncertainty under a model; it does not reveal the population value. [psychology:S104]

For the introductory independent single-proportion model, a normal approximation concerns sample proportions, while individual responses remain binary. Both outcome categories must be adequately represented for that approximation; a large total alone can leave one category sparse. The sampling proportion remains discrete even when a smooth approximation is useful. Increasing sample size can reduce sampling variability under the model, while leaving selection and measurement bias unresolved. [psychology:S104]

**Original synthetic contrast:** a hypothetical study records one yes/no observation per independently sampled item; a different file records the same items repeatedly. Equal row counts do not establish equal numbers of independent items. This design interpretation combines the new sampling-model reading with STAT-F1; it is not a new clustered or repeated-measures estimator. Random assignment to conditions does not by itself remove every source of within-person or group dependence.

**Actual additional reading:** Diez, Çetinkaya-Rundel and Barr, *OpenIntro Statistics*, fourth edition (2019), screen-reader copy updated 2022-10-21: pp. 190–193,195–196,199, selected 5.1.1–5.1.6 prose/openings. Root and researcher read these seven pages; root visually checked 192–193. The book's broad independence statements on 193 are not exported as universal rules; its finite-population caveat also requires design-specific interpretation. Pages 194,197–198 and later methods were not newly appraised. No exact approximation cutoff, source example, code, dataset, chart or exercise is reproduced.

**Rights/limits:** source textbook [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/), with author/title/edition attribution above; current resource licence and website terms checked 2026-10-17. These are original factual explanations and an invented illustration, not reproduced source expression or a relicensing of source material under MIT. Any expressive adaptation must retain applicable attribution/ShareAlike. Survey weighting, finite-population methods, clustering, resampling, missingness and a full statistical-inference course remain further study.

## STAT-F5 — A fitted average is not an individual or causal guarantee

A fitted straight line describes a modeled average outcome as the predictor varies. Its slope concerns an estimated average difference per predictor unit; identify both units, population and setting. An observational slope alone does not identify the effect of changing that predictor. The intercept concerns the modeled average at predictor zero, which needs meaningful zero and model support there. [psychology:S104]

A line can return a number beyond the observed range without evidence that its form continues there. Inspect curvature, changing spread, unusual points and dependence before trusting the simple model and its uncertainty. Repeated rows from one person or a time series do not become independent because a line was fitted. The introductory source groups near-normal residuals with its chapter conditions; this selected account does not establish a universal prerequisite for computing coefficients or the correct remedy for every unsuitable model. [psychology:S104]

**Original fictional contrast:** repeated sleep durations and puzzle scores from the same volunteers produce a fitted average. The coefficient does not guarantee one volunteer’s score, prove an extra hour caused improvement, or validate prediction beyond the observed range. These are distinct design, model and prediction questions; no physiological threshold or prediction interval is invented.

**Actual reading/limits:** Diez, Çetinkaya-Rundel and Barr, OpenIntro Statistics 4e (2019), screen-reader update 2022-10-21. Researcher read 8.2.3/8.2.5 on 356/360; root independently read and visually checked 356/360 and additionally 8.2.6 on 361. Three distinct substantive pages, not five readings counted as pages. Root directly checked file identity/current licence/terms. Page357 practice and the 8.2.7 opening encountered during extraction are not newly appraised units. Source examples, quotation, exercises, figures, code and data excluded. Source [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/), attribution retained; expressive adaptations would retain ShareAlike. Robust, clustered/time-series inference, prediction intervals and clinical model validation remain further study.
