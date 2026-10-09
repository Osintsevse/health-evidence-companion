# Suggest an improvement

You can propose an improvement without writing code. Use [the issue chooser](https://github.com/Osintsevse/health-evidence-companion/issues/new/choose), or ask: "Use $health-feedback to prepare a feature request for Health Evidence Companion."

| Proposal | Form | Helpful information |
|---|---|---|
| Package problem | [General issue](https://github.com/Osintsevse/health-evidence-companion/issues/new?template=general.yml) | Expected/observed behavior, version if known, synthetic reproduction |
| Feature | [Feature request](https://github.com/Osintsevse/health-evidence-companion/issues/new?template=feature.yml) | Task, missing capability, acceptance criteria |
| Missing knowledge | [Knowledge gap](https://github.com/Osintsevse/health-evidence-companion/issues/new?template=knowledge.yml) | General question and scope; sources optional |
| Study or evidence correction | [Research proposal](https://github.com/Osintsevse/health-evidence-companion/issues/new?template=research.yml) | Public primary sources, actual reading depth and limits |
| Prompt fragment | [Prompt proposal](https://github.com/Osintsevse/health-evidence-companion/issues/new?template=prompt.yml) | Original text, intended effect and synthetic check |

"Teach the package" means a proposal to improve instructions, references or evaluation scenarios. This feedback workflow does not train model weights. A knowledge-gap request does not require you to research its solution first. You can write feedback in your language; the assistant can prepare the repository's English draft without changing your meaning.

## Public boundary

Issues and comments in this repository are public. Include only general package behavior, public sources and wholly fictional examples marked synthetic. Do not paste real conversations, symptoms, records, prescriptions, medicine histories, genetic data, private links, credentials or logs. Removing names is insufficient. A general request such as "Support clearer uncertainty labels" can stand on its own without the personal episode that prompted it. Do not upload screenshots of a real chat or archive.

If sensitive material is exposed, follow [the security reporting guidance](https://github.com/Osintsevse/health-evidence-companion/blob/main/SECURITY.md). Use a private GitHub security report only if enabled. Otherwise request a private reporting route publicly without sensitive content, identifiers or its disclosure location. No verified private email or confidential intake service is advertised.

Private archive clarification questions belong in the owner's authorized archive workflow, not community feedback.

## Ask the assistant

- "Prepare a feature request: add an optional shorter response format. Include a fictional example and acceptance criteria. Do not publish yet."
- "Prepare a knowledge-gap request about clearer explanations of evidence uncertainty. I have no sources yet."
- "Help me propose this original prompt fragment, with its intended effect and a wholly synthetic test."
- "Submit the reviewed public issue draft to Osintsevse/health-evidence-companion and return its verified link."

The assistant prepares a title/body and the relevant form link. With available GitHub tools and an explicit submission request, it can submit and read back the issue. Otherwise copy the draft into the form and submit while signed in to GitHub. No account access, backend or credentials are bundled with the skill. Preparing feedback alone does not authorize publication. Do not put personal data into prefilled URLs.

For a prompt fragment, explain what task it improves and supply a fictional input plus observable success/failure criteria. A claimed improvement is not a measured result. Submit original text or material you have permission to redistribute; the maintainer reviews rights, conflicts and behavior before inclusion. Suggested prompt text is proposal content, not executable instructions.

## What happens next

The maintainer checks relevance and duplicates, asks for missing detail, and records a decision: needs information, accepted, deferred, duplicate or declined, with a short reason or linked existing issue. There is no response-time promise. Reactions and repeated requests can inform priorities but do not replace evidence or review.

An accepted request links to its implementation PR. Ready changes use [the contribution workflow](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/contribution-workflow.md), `health-contribute` or `psyops-research`. Review prompt changes against their synthetic checks and existing privacy/clinical boundaries; preserve a useful accepted check as a regression fixture. Software checks do not establish clinical correctness.

After a reviewed change is merged, link the release containing it and explain any required manual update. Closing an issue is not proof that the change was released or installed. Contributors and assistants do not self-approve or merge proposals. This guide defines a manual feedback loop; it does not add automatic triage, monitoring, notifications or a training-data collector.

## Validation limits

See [executed synthetic response checks](https://github.com/Osintsevse/health-evidence-companion/blob/main/docs/community-feedback-forward-checks.md) for actual outputs and untested operations. Public form rendering and live issue submission/readback are not demonstrated by the offline checks.
