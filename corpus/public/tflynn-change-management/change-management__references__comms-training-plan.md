---
title: 'Communications and training plan: reference'
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/change-management/references/comms-training-plan.md
source_path: change-management/references/comms-training-plan.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# Communications and training plan: reference

Use this when building Step 4 of the plan.

## The plan follows the assessment

Each group's sequence starts at its barrier point. A group at Desire gets manager conversations and involvement before it gets a training invitation. A group at Ability gets practice and floor support, not another town hall. Build the table per group, then merge into one calendar.

## Senders

| Message type | Preferred sender | Why |
|---|---|---|
| Why the organization is changing, the business case, the cost of not changing | Primary sponsor, in person or on video, then repeated by unit leaders | People want to hear the business reason from the top |
| What this means for me, my team, my job | Direct manager, in conversation | People want to hear personal impact from the person they work for |
| How the new process works | Training and process owners | Content accuracy |
| How the project is going, what was fixed | Project team | Operational |
| Peer experience, "here is how I use it" | Super-users and change agents | Credibility |

A message from the project team about *why* the change matters is the most common sender error. A message from the sponsor about *how to click through the screens* is the second.

## Activities by element

### Awareness

- Sponsor message: the problem, the change, the cost of not changing, what is not changing, the timeline. Delivered live where possible.
- Unit leader repeats it to their own people within a week.
- A question channel that answers in public.
- A one-page "what is changing and what is not" by group.

### Desire

- **Job-impact conversation**: each manager meets their team, walks through what changes for them on the impact dimensions, names losses honestly, surfaces opportunities, and escalates impacts the project did not anticipate. Managers need a toolkit for this (below).
- **Involvement**: named roles for members of each group in design review, pilot, training design, and peer support. Involvement is the strongest single Desire lever for experienced practitioners.
- **Visible leader participation**: sponsor and unit leaders use the new way, attend sessions, and say what they see.
- **Honest WIIFM**: what gets easier, what gets harder, what the role becomes. Overselling costs trust later.
- **Early wins published**: from the pilot, with the pilot team as the voice.

### Knowledge

- Role-based training, timed two to four weeks before first use. Training months early is forgotten; training the week of go-live is too late to practice.
- Cover the new workflow, the decision rules, the person's part, and the handoffs. Screens are the smallest part.
- Separate paths for users, approvers, analysts, and managers.
- Job aids and quick references at the point of use.
- Managers trained before their teams, so they can coach.

### Ability

- Hands-on sessions using the group's real work, before go-live.
- Super-users or change agents in each unit, named, visible, and given time.
- Floor support for the first weeks after each go-live.
- A fast fix path for blockers, with a visible log of what was raised and what happened.
- Managers lower throughput expectations for a defined learning period.
- A retirement date for the old path, communicated early and held.

### Reinforcement

- Adoption metrics reviewed weekly by managers and monthly by the sponsor.
- Recognition for early adopters and for teams that meet the adoption definition.
- Corrective conversations when people revert; managers need to know this is expected of them.
- Formal handoff of the change to an operational owner before the project team leaves.
- A feedback loop that visibly produces fixes.

## AI trust-building track

Add this for any change where a model, rule, or automation takes a decision people used to make.

| When | Activity | Owner |
|---|---|---|
| Before Awareness messaging | Write the plain-language explanation of what the model decides, what it does not, and how it decides | Project team, data science |
| Desire stage | Publish the override policy: when override is allowed, how it is recorded, how outcomes are reviewed | Sponsor, process owner |
| Desire stage | State explicitly what the role becomes: where human judgment now sits (strategy, objectives, guardrails, evaluation, exceptions) | Sponsor, people managers |
| Knowledge stage | Train on reading model outputs and on the override process, not only on the interface | Training |
| Ability stage | Side-by-side period: people see model results against their own approach on real cases | Project team, analytics |
| Reinforcement | Publish model performance and override outcomes to the people who must trust the model | Analytics, sponsor |

## Sponsor roadmap

A short table of what the sponsor does and when. At minimum:

| Timing | Sponsor action |
|---|---|
| Kickoff | Deliver the why, live; name the coalition; set priority against other work |
| Monthly through go-live | Coalition meeting: stance, issues, adoption readiness by unit |
| Pre-pilot | Visit the pilot team; use the tool; say what they saw |
| Go-live | Message to all impacted employees; be present in the first week |
| Monthly after go-live | Review adoption metrics; recognize; address units that are lagging, directly with the unit leader |
| Handoff | Name the operational owner and say so publicly |

Also: a standing, short check-in between the sponsor and the change lead. Inadequate access to the sponsor is a common cause of plans that look fine and do nothing.

## People-manager toolkit

What every manager of an impacted group needs before they talk to their team:

1. The sponsor message, so they repeat it rather than reinterpret it.
2. The impact summary for their group, on the impact dimensions.
3. A conversation guide for the job-impact meeting, including how to handle "what happens to my role."
4. Answers to the likely questions, and where to send the ones they cannot answer.
5. What is expected of them at each stage: communicate, coach, hold corrective conversations, report adoption.
6. Their own barrier resolved first: a manager who has not decided to participate cannot lead the change.

## Calendar

Merge the per-group tables into one calendar keyed to the project milestones. Show timing relative to go-live (G minus weeks, G plus weeks) so the plan survives a date change. Every row has a sender or owner. Rows with no owner are not a plan.
