# AI for psychological assistance: data and ready-made solutions
Version 2.1 · 2026-09-28

Clarification 2026-10-08: for S75 the available sections of the full text have been read. There were 185 randomized participants, 147 eligible completed the baseline assessment; ChatGPT used GPT-4o based models. The brevity of the study and exclusions after randomization limit conclusions; This is not a PsyOps test. The rest of the old dates and reading depths are preserved.

## Don't mix four things
Structured digital program; chatbot with fixed scripts; specially trained and controlled generative system; a regular language model with the instruction “be a psychologist.” The result of research on one product does not automatically transfer to another.

## Research
| Source | What was checked | Practical Conclusion and Limitation |
|---|---|---|
| Woebot, 2017 [S43] | 70 young adults, two weeks, comparison with information material | Historical data about a specific automated agent; not a test of current LLMs |
| Therabot, 2025 [S41–S42] | 210 adults; 4 weeks of use, assessed at weeks 4 and 8; waiting list | Encouraging result of a special system; there was no active comparison with psychotherapy |
| Sohn et al., 2026 [S44] | 39 RCT of different chatbots | Small average effects; high heterogeneity; applicability to this system is not established |
| Moore et al., FAccT 2025 [S45] | Checking the responses of models/bots in situations of mental distress | Stigma and dangerous responses revealed; this is an assessment of responses, not an RCT of treatment |

In the 2026 review: g=0.31 for depressive symptoms and g=0.28 for anxiety symptoms. In 35 of 39 studies, the overall risk of bias was rated as high; 23 reported no systematic safety data. You cannot turn these averages into the probability of helping a specific user. [S44]

At Therabot, staff intervened 15 times for safety concerns and 13 times to correct inappropriate responses; We are talking about cases of intervention, not about the number of affected participants. This is an important part of the research setting. [S42]

FAccT's work relates to systems studied at that time. It shows error classes for tests, but does not prove that all future models behave the same. [S45]

## Update 2026-09-28: active comparisons and regular ChatGPT
The state of the literature is already wider than the early Therabot. It is incorrect to say that only comparisons with a waitlist exist or that regular ChatGPT has never been explored. However, the evidence relates to specific versions of systems, populations and conditions, and not to “AI in general.”

| Work | Conditions and result | What limits the output |
|---|---|---|
| Kai, Israel, 2026 [S74] | 995 students; 12 weeks, then 3 months of observation. Better outcomes than in-person group support and a waitlist for anxiety and well-being; no differences in PTSD | Groups of about 20 people, no individual therapy; self-reports, significant attrition to follow-up, authors' financial ties to the product. Crisis, severe distress, and ongoing therapy/medication are excluded. Clinician intervention was available |
| ChatMind / ChatGPT, 2026 [S75] | Pilot, N=147, 3 weeks, English-speaking adults. Both treatments improved the PHQ-9 relative to the assessment-only controls; There were no significant benefits for anxiety, depression scale 2, or well-being. | ChatMind did not outperform ChatGPT statistically; this is not a proven equivalence. Short term, self-report; at the original review, indexed abstract and methods excerpts were available; the 2026-10-08 recheck accessed selected full-text sections |
| Human + GenAI, China, 2026 [S79] | Two tests, analytical samples totaling 425; one session on academic anxiety, 2 weeks observation; small effects versus active control on target outcomes | The person taught and helped choose a task; This is not a stand-alone therapy. The results are mixed: in the first study, the difference in academic anxiety did not reach p < 0.05. Two instances of fictitious distress ratings were found when reviewing dialogues. |
| Hailey, 2023 [S77] | Non-clinical RCT, 300 peer support participants: AI prompts improved expressed empathy | The responses of helping people are evaluated, not the treatment of the disorder and not the replacement of a specialist |

New trials should not be mechanically added to the number of papers from the old meta-analysis: composition and intersection should be checked separately. There is no new combined effect calculation in this database. The conditions of human control are essential; there is no team of clinicians observing the conversation.

## Sycophancy is a separately measured risk
Science (2026) published three pre-registered experiments with 2405 participants. After sycophantic answers, people were less willing to take responsibility and correct interpersonal conflict, while becoming more convinced that they were right. It's about intentions and brief interactions, not measured rates of divorce or diagnosis. [S76]

The rule of thumb for the project is to acknowledge the experience but test the explanation; distinguish between a person's contribution and another's unknown motives; show a significant alternative explanation when warranted. Don’t start an artificial argument and don’t pass off rudeness as a defense against yes-men. It cannot be promised that one instruction will completely eliminate this risk.

## Applicability to free conversation
- **Reasonable auxiliary tasks:** state the situation, separate observations from conclusions, prepare questions for a specialist or conversation with a loved one, perform low-intensity voluntary practice. This is a cautious conclusion about the format of use, and not the clinically proven effectiveness of this project.
- **Not yet established for PsyOps:** treatment of disorders, long-term benefit, safety across conditions, superiority over an individual practitioner, effectiveness of collaborative couple therapy.
- **Separate gap:** The trials found do not validate this package in any user language, our rules of memory and long conversations about sexuality, meaning and mortality. Evidence from human psychotherapy and digital CBT does not automatically fill this gap.
- **Sign of usefulness:** more clarity, independent decisions and real actions. The number of messages, the pleasantness of the response, and the desire to return are not in themselves a therapeutic outcome.

Consider language, norms and individual context according to 22_GLOBAL_AND_CULTURAL_CONTEXT.md. Do not draw a conclusion about “cyberpsychosis” based on the duration of use; Decreased sleep, functioning, communication, and increased unexamined beliefs require attention according to 08_RISK_AND_REFERRAL.md.

## What did you find among the ready-made kits?
Project pages checked; code run and clinical validation were not performed. Other people's instructions and programs are not installed.

| Project | What is available according to the description | What to take as an idea | Why not adopt it as a ready-made standard? |
|---|---|---|---|
| dralexlup/therapy-skill [S47] | Integrated Dialogue, Critical Review, CBT/DBT; MIT | Separation of debriefing and intervention | Clinical validation of the skill is not indicated; crisis contacts are also focused on Romania |
| glebis/claude-cognitive-toolkit [S48] | Thought record, opposite action; some techniques are marked as future | Short step-by-step tasks | Marketing evidence is not the same as package research; physiological integrations require separate assessment |
| jjchen17/mindmirror-skill [S49] | Minimum input, reference books, scales, test scripts | Modularity and test situations | The language/crisis context is different; The author's tests do not prove clinical safety |
| arktnld/cbt-llm-kit [S50] | Structured thoughts and local notes | Portable record format | A long, mandatory outline can interfere with lively conversation; "local notes" does not mean local processing by the model |
| jlcmoore/llms-as-therapists [S46] | Research materials on unsafe responses | Test classes: stigma, reassurance, delusional ideas | This is a research material, not a therapeutic product |

Do not copy sources and worksheets without checking the license. MIT requires that the required notices be preserved when actually copying code; The availability of a web page does not make it public domain. We use our own instructions and links here, rather than reprinting other people's packages.

## More reliable content resources
- WHO Doing What Matters: freely available guide and Russian version via the link on the official page. [S15]
- WHO PM+: intervention manual and separate training manual; involves training and supervision rather than just reading a text. [S17, S53]
- WHO/UNICEF EQUIP: competencies and their assessment; useful for the quality framework, but AI does not become a certified performer. [S18]
- CCI: topical materials for self-help and professionals. Their availability does not change the terms of use. [S37–S39, S55]

## Architecture of the selected solution
1. **Skill:** brief rules for choosing mode, boundaries and materials.
2. **Subject Markdown Documents:** Small sections available as needed.
3. **Register of sources:** type of evidence, text availability, restrictions, date of review.
4. **Empty templates:** personal data appears only when specifically filled out.
5. **Test situations:** catch predictable errors; do not replace a clinical trial.

The skills format supports uploading detailed materials as needed. [S51] The first version does not require a separate vector server, medical data collection or a third-party Telegram bot: there are enough documents for selective reading and text search.

## How to spot harmful use
Check whether the need to constantly receive confirmation is growing, whether chat is replacing sleep and real conversations, whether the AI response is becoming the last argument in the dispute, whether confidence in unverified versions is increasing.

If this happens: name the observation, reduce reassurance, return to verifiable actions and live support. Changing your style shouldn't turn into cold rejection.

## Privacy
Discussion of intimacy through a regular cloud service does not automatically receive the status of protected medical consultation. Do not make promises of storage/training without checking the current settings and policies of the product you are using. WHO recommends considering autonomy, rights and responsibility when implementing medical AI. [S40]
