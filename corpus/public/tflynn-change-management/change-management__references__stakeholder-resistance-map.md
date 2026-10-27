---
title: 'Stakeholder and resistance map: reference'
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/change-management/references/stakeholder-resistance-map.md
source_path: change-management/references/stakeholder-resistance-map.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# Stakeholder and resistance map: reference

Use this when building Step 1 of the plan.

## Impacted groups are defined by type of impact, not by org chart

Two people in the same department can be in different impacted groups if the change hits their work differently. Two people in different departments can be in the same group if it hits them the same way. Start from "whose daily work changes, and how," then name the groups.

Typical groups on a platform rollout:

| Group pattern | Usual impact |
|---|---|
| Primary users who do the core work in the platform | Workflow, tools, skills; often decision authority |
| Approvers and reviewers (compliance, legal, finance, brand) | New workflow and tooling for review; sometimes new rules |
| Analysts and reporting | New data sources and definitions; old reports break |
| Business-unit leads whose teams adopt | Sponsorship role, measurement, resourcing |
| Upstream suppliers of inputs (data, content, creative) | New format, timing, or quality bar |
| Downstream consumers of outputs (sales, service, operations) | Different volume, timing, or kind of output |
| People managers of any group above | Must coach the change while adopting it themselves |

## Impact dimensions

For each group, say what changes on each dimension and name the biggest one.

| Dimension | Question to answer |
|---|---|
| Workflow | What steps change, disappear, or get added? |
| Tools | What systems do they use now versus after? |
| Decision authority | What decisions move from a person to a rule, a model, a different role, or a committee? |
| Skills | What must they be able to do that they cannot today? |
| Role identity | What did their expertise mean before, and what does it mean after? |
| Measurement and incentives | What are they measured and rewarded on, and does that change? |
| Relationships | Who do they work with, hand off to, or escalate to, and does that change? |

**Decision authority and role identity are the dimensions most often underestimated on AI and automation rollouts.** A tool change that leaves authority and identity alone is a training problem. A change that moves authority to a model is a trust problem, even if the screens are easy.

## Stance today

| Stance | Signal |
|---|---|
| Supporter | Asked for the change, helped design it, or has a clear win from it |
| Neutral | Aware, not yet engaged; will follow their manager and peers |
| Skeptic | Open questions about whether it works or is worth it; can be converted with evidence |
| Likely resistor | Loses authority, status, a valued workflow, or an incentive; or has a history of changes done to them |

Most groups start Neutral. Predict Skeptic or Likely resistor only with a reason tied to an impact dimension.

## Resistance patterns and root causes

Resistance shows up as behavior. Name the behavior, then the probable root cause, because the action depends on the cause.

### General patterns

| Observed behavior | Probable root cause | First action |
|---|---|---|
| "We weren't told" even after announcements | Awareness messages came from the wrong sender or lacked the why | Sponsor delivers the why in person; manager repeats it |
| Vocal objection in meetings | Job impact not acknowledged; no involvement in design | Manager holds the job-impact conversation; give the person a design or pilot role |
| Quiet compliance, no real use | Weak personal benefit; no reinforcement | Make usage visible; manager follow-up; recognize early use |
| Reverting to the old method after go-live | Ability gap under real conditions, or the old path still works | Side-by-side support; retire the old path on a date |
| "This is not how we do things here" | Perceived conflict with culture or values | Name the conflict; adjust the change or expand scope to include the culture shift |
| Workarounds and parallel spreadsheets | Platform does not fit a real need, or trust is low | Capture the need; fix it or explain why not; publish the fix |
| Change fatigue, disengagement | Saturation from concurrent changes | Sponsor sequences or delays; combine changes into one program |
| Managers not coaching | Managers have their own barrier and no toolkit | Equip managers first; resolve the manager's own Desire before asking them to lead |

### AI- and automation-specific patterns

These are the ones that an experienced practitioner population produces when a model, rule, or automation takes a decision they used to make.

| Observed behavior | Probable root cause | First action |
|---|---|---|
| "The model is wrong" with anecdotes | Low trust; no transparency into how it decides | Explain the decision logic in plain language; run a side-by-side period where they can see model versus their own results |
| Overriding the model by default | Loss of control; override is free and unreviewed | Define when override is appropriate, review overrides, and show override outcomes versus model outcomes |
| Building the old segments inside the new tool | Role identity: expertise was the targeting logic | Redefine the role explicitly (judgment moves to strategy, objectives, guardrails, and evaluation); give the person authority there |
| "Who is accountable when it's wrong?" | Accountability for model decisions is undefined | Publish the accountability model before go-live |
| Approvers reject or slow everything | Review workflow was designed for human-authored items, not model-generated ones | Redesign review for the new volume and kind of output; involve approvers in design |
| Analysts dispute the results | Measurement changed and nobody reconciled old to new | Reconcile definitions; publish a crosswalk; agree the new source of truth |
| Enthusiasm at the demo, silence at go-live | Ability gap: the demo was easy, the real work is not | Hands-on practice with real cases before go-live; super-users on the floor |

## Sponsor coalition map

A multi-unit rollout has one primary sponsor and a coalition of unit leaders. Adoption tracks the coalition, not the primary sponsor.

For each leader whose unit must adopt, record:

| Field | Values |
|---|---|
| Unit | |
| Stance | Supporter / Neutral / Skeptic / Resistor |
| Visibly active | Yes / Partly / No. "Active" means they show up, speak about the change to their own people, and resolve issues; a kickoff appearance does not count |
| Aligned on success | Yes / No. Do they measure success the same way as the primary sponsor? |
| Access for the change lead | Adequate / Inadequate |
| Risk flag | Flag any leader who is Neutral or worse, not visibly active, or not aligned |

The three things a sponsor must do, and that the plan must ask of them: participate actively and visibly throughout; build and hold the coalition of other leaders; communicate the business case directly to employees.

If the description names one sponsor for a rollout across several units, the coalition is missing from the plan, and that is the first judgment call to raise.
