---
title: 'ADKAR-style readiness assessment: reference'
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/change-management/references/adkar-assessment.md
source_path: change-management/references/adkar-assessment.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# ADKAR-style readiness assessment: reference

Use this when building Step 2 of the plan. ADKAR is a registered trademark of Prosci Inc. This reference describes the practitioner's application of the model's publicly described structure; it is not Prosci material.

## The five elements, in order

Change happens one person at a time, and within a person it happens in sequence.

| Element | The question the person is answering | Scored on |
|---|---|---|
| Awareness | Do I understand why this change is happening and what happens if we don't? | Can they state the business reason in their own words? |
| Desire | Have I decided to take part? | Are they choosing to engage, or waiting to see? |
| Knowledge | Do I know how to do my job the new way? | Can they describe the new process and their part in it? |
| Ability | Can I actually do it, under real conditions, at the required level? | Have they done it with real cases, and did it work? |
| Reinforcement | Is there anything keeping me from going back? | Are there consequences, measures, recognition, and an owner after go-live? |

## Scoring

Score each element 1 (low) to 5 (high) per impacted group. Give the evidence for every score. When the only evidence is the description, write "inferred" and say what you inferred from.

**Barrier point rule:** the barrier point is the first element scoring 3 or below. Fix that one first. Lower scores on later elements are expected and are not where the effort goes yet.

Example: Awareness 4, Desire 3, Knowledge 2, Ability 2, Reinforcement 1. The barrier is Desire. Scheduling training (Knowledge) or sandbox practice (Ability) now will not move adoption, because the people have not decided to participate. The plan starts with the actions that resolve Desire, then moves on.

## Root causes by element, with the action and the owner

Ordered within each element from easiest to hardest to resolve. Pick the two to four that fit the evidence.

### Awareness is the barrier

| Root cause | Action | Owner |
|---|---|---|
| The why was never stated, only the what | Sponsor states the business reason and the cost of not changing, in person | Primary sponsor |
| Message came from the project team, not leadership | Re-send through the sponsor and the direct manager | Sponsor, people managers |
| Messages described the tool, not the problem | Lead with the problem the change solves | Change lead drafts, sponsor delivers |
| Rumors filled the gap | Open a question channel and answer every question in public | Change lead |
| Credibility of the sender is low | Find the sender this group trusts; use peers and respected managers | Change lead, coalition |

### Desire is the barrier

| Root cause | Action | Owner |
|---|---|---|
| Individual job impact not acknowledged | Manager meets the team, confirms what changes for them, names the losses honestly, surfaces the opportunities | People managers |
| Leaders not modeling the change | Sponsor and unit leaders use the new way themselves and say so; resolve each leader's own barrier first | Primary sponsor, coalition |
| Low trust in management from past changes | Acknowledge what went wrong before and what will be different; enlist trusted peers as change agents | Sponsor, coalition |
| No involvement in design | Give the group real roles: design input, impact review, pilot, training design, peer support | Project team |
| Weak personal benefit | Communicate often; acknowledge downsides without overselling; explain the organizational and secondary benefits | People managers |
| Conflict with culture or values | Name the conflict; adapt the change where possible; otherwise include the culture shift in scope | Sponsor |
| Conflict with personal beliefs | One-on-one conversation; understand it; if unresolved, give clear choices and consequences | People manager |
| Disruption of valued relationships | Acknowledge the loss; support keeping the relationship or building new ones | People manager |
| Incentives reward the old behavior | Align performance measures and compensation to the new behavior | Sponsor, coalition, HR |
| Saturation from concurrent changes | Sponsor prioritizes, delays, or combines changes | Sponsor |

### Knowledge is the barrier

| Root cause | Action | Owner |
|---|---|---|
| Training too early or too late | Time role-based training two to four weeks before first use | Change lead, training |
| Training covers screens, not process and decisions | Teach the new workflow, the decision rules, and the person's part in it | Training, process owners |
| No role-specific content | Build per-group paths; approvers and analysts do not need the user curriculum | Training |
| No reference material at the moment of need | Job aids, quick-reference cards, an in-tool help path | Change lead |
| Nobody to ask | Super-users or change agents named and visible in each unit | Project team, coalition |

### Ability is the barrier

| Root cause | Action | Owner |
|---|---|---|
| No practice with real cases | Hands-on sessions with the group's own work, before go-live | Training, super-users |
| Old path still available and easier | Set a retirement date for the old path and hold it | Sponsor, project team |
| Unsupported at the moment of difficulty | Floor support in the first weeks; a fast fix path for blockers | Project team |
| The tool does not do something the job needs | Capture gaps; fix, workaround, or explain, and publish the answer | Project team |
| Time not given for the learning curve | Managers lower throughput expectations for a defined period | People managers, coalition |

### Reinforcement is the barrier

| Root cause | Action | Owner |
|---|---|---|
| No one owns the change after the project | Name the operational owner before go-live | Sponsor |
| Usage is invisible | Put adoption metrics in front of managers weekly | Change lead, analytics |
| No consequence for reverting | Managers hold corrective conversations; the old path is gone | People managers |
| No recognition | Recognize early adopters and teams that hit the adoption definition | Sponsor, coalition |
| Feedback goes nowhere | Visible loop: problems raised, what was fixed, what will not be and why | Project team |

## AI-specific notes by element

| Element | What changes when a model takes the decision |
|---|---|
| Awareness | People usually know; the gap is usually what the model does and does not decide |
| Desire | The three recurring causes are skepticism about the model, loss of control, and uncertainty about what the role becomes. All three are addressed by transparency into the decision logic, a defined override process, and an explicit redefinition of the role |
| Knowledge | Add: how the model decides, how to read its outputs, when and how to override, how performance is evaluated now |
| Ability | Add: a side-by-side period against the person's own results; practice reviewing model outputs rather than authoring from scratch |
| Reinforcement | Add: publish override outcomes; retire the manual path; make model performance visible to the people who have to trust it |

## Confidence and measurement

Inferred scores are a hypothesis. State the confidence per group and recommend the cheapest way to replace inference with evidence:

- A five-question pulse (one per element) sent through managers, two to three weeks before the plan is finalized.
- Manager interviews for groups under about thirty people.
- A focus group when the history with past changes is unknown.

Re-score at pilot and at go-live. A plan built on kickoff scores alone will be wrong by go-live.
