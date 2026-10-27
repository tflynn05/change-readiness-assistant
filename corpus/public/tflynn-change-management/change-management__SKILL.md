---
title: Change management for platform rollouts
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/change-management/SKILL.md
source_path: change-management/SKILL.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

Build a change management plan for a platform, tool, or AI rollout. Given a description of the rollout, produce (1) a stakeholder and resistance map, (2) an ADKAR-style readiness assessment with the barrier point for each group, (3) a communications and training plan sequenced to that assessment, (4) the adoption metrics to track, and (5) a short list of judgment calls only an insider can make. Use this whenever someone describes a system implementation, migration, new tool, automation or AI adoption, process change, or asks about adoption, resistance, sponsorship, readiness, go-live risk, or "getting people to actually use" something, even if they never say "change management."

# Change management for platform rollouts

This skill turns a rollout description into a working change plan. It encodes two things: the structure of a widely used individual-change model (Awareness, Desire, Knowledge, Ability, Reinforcement) and the practitioner lessons from an enterprise AI decisioning rollout where the technology worked and adoption was the hard part.

Read `references/` files only when the step below says to. Write the final deliverable using `templates/change-plan.md`.

## Operating principles

Apply these in every output. They are the difference between a plan and a communications calendar.

1. **Adoption is the risk, not the technology.** A platform returns nothing until the people in the impacted groups do their jobs the new way. Size the plan to that, not to the delivery schedule.
2. **Diagnose before you prescribe.** Do not write a single message or training session until you have a readiness score per group and know its barrier point.
3. **Change is sequential within a person.** Fix the first element scoring 3 or below before spending on later ones. Training people who have not decided to participate produces attendance, not adoption.
4. **Awareness is rarely the barrier on an AI or automation rollout.** Experienced practitioners usually know the change is coming. They stall at Desire (trust, control, role identity) and Ability (doing the new job under real conditions). Start there unless the evidence says otherwise.
5. **Sponsor consistency across units is the strongest predictor of adoption.** Where several business units adopt the same platform, adoption will be uneven in exactly the places where the local leader is passive. Map that explicitly and treat gaps as the top risk.
6. **Business messages come from the sponsor; personal-impact messages come from the direct manager.** A project team email is the wrong sender for both.
7. **Define "adopted" in observable terms before go-live.** Otherwise go-live gets reported as success while teams quietly revert to the old method.
8. **Start at kickoff, not at go-live.** If the rollout is already underway, say so and front-load the diagnostic steps.
9. **Separate what you know from what you assumed.** Every plan ends with the list of judgment calls that only someone inside the organization can settle.

## Step 0: Collect the inputs

Pull these from the description. If something is missing, make a labeled assumption and keep going; do not stall the plan on questions. Ask at most three questions, and only when a wrong guess would change the plan's shape (for example, whether use of the platform is mandated or optional).

| Need | Why it matters |
|---|---|
| **Project**: what is being rolled out, scope, phasing | Determines the size of the change and whether units go live together or in waves |
| **Purpose**: the business reason and the cost of not changing | Awareness and sponsor messaging are built from this |
| **Particulars**: what changes in each group's daily work | The stakeholder map is built from *type of impact*, not the org chart |
| **People**: impacted groups, approximate sizes, their managers | Readiness is assessed per group |
| **Sponsor** and other senior leaders whose units are affected | Sponsor coalition map |
| **Timeline**: kickoff, pilots, go-live(s), when outcomes are expected | Sequences the plan and the metric cadence |
| **History**: how past changes went in this organization | Sets the Desire prior and the trust assumptions |
| **Success measures** the business already has | Adoption metrics must ladder up to these |
| **What is algorithmic or AI-driven** about the change | Triggers the AI-specific resistance patterns and metrics |

Then write the **Change at a glance** block (template section 1): project, purpose, particulars, people, in a few lines each. Everything downstream must be traceable to it.

When the requester supplies the list of impacted groups, record it as "as provided; confirm each group is impacted on at least one dimension." Score only groups whose impact the description actually states; list the rest under judgment calls as "possible impacted group, impact not described" rather than giving them a readiness row built on nothing.

## Step 1: Stakeholder and resistance map

Read `references/stakeholder-resistance-map.md` before this step.

For each impacted group, produce one row in the map (template section 2):

- **What changes for them**, using the impact dimensions in the reference (workflow, tools, decision authority, skills, role identity, measurement and incentives, relationships). Name the dimension with the biggest change.
- **Degree of impact** (High / Medium / Low) and **group size** if known.
- **Likely stance** today (Supporter / Neutral / Skeptic / Likely resistor) with one line of reasoning.
- **Predicted resistance pattern** and its **probable root cause**, chosen from the reference. For AI-driven changes, check the AI-specific patterns first.
- **Preferred sender** for personal-impact messages (normally the direct manager) and the **leader whose sponsorship this group reads from**.
- **Confidence** (High / Medium / Low) in the row, with what evidence would raise it.

Then build the **sponsor coalition map**: primary sponsor, and every leader whose unit must adopt. For each: unit, current stance, whether they are visibly active, whether they have bought into the same definition of success. Flag any unit whose leader is passive or unaligned as a named risk. If the description gives you only one sponsor for a multi-unit rollout, say so and flag the missing coalition.

Finish with the **top three resistance risks** in ranked order, each tied to a group, a root cause, and a first action.

## Step 2: ADKAR-style readiness assessment

Read `references/adkar-assessment.md` before this step.

Score each impacted group 1 (low) to 5 (high) on the five elements. For every score, give the evidence from the description or the assumption you made. Then:

- **Barrier point** = the first element scoring 3 or below. State it in one sentence per group.
- For each barrier point, list the **two to four most likely root causes** (from the reference) and a **mitigating action with an owner**. Owners are: primary sponsor, coalition leader, people manager, project team, or change lead. Prefer the easiest-to-resolve root causes first.
- Note which elements score low *after* the barrier and say explicitly that they are deferred until the barrier is cleared, so the reader does not spend on them yet.
- Rate **confidence** per group. If the scores are inferred rather than measured, recommend the fastest way to measure them (a five-question pulse survey, manager interviews, a focus group) and when.

Default priors when the description gives little evidence: for an AI or automation rollout among experienced practitioners, Awareness 4, Desire 3, Knowledge 2, Ability 2, Reinforcement 1 is a reasonable starting profile. State that it is a prior, not a finding. Depart from the prior by more than one point only on direct evidence (a quoted statement, a described incident, a survey result), never on the tone of the description. Vivid prose about pride or frustration is a signal to investigate, not a score.

## Step 3: Project health check

Read `references/health-check.md` before this step.

Score the four corners of project health (Success definition, Leadership and sponsorship, Project management, Change management) using the questions in the reference, each 1 to 3. Report the four totals, the risk band, and the three lowest-scoring conditions overall. Keep this to half a page; its job is to show where the project, not just the people, is exposed. If the description cannot support a score, score it 1 and label it "not evidenced," which is usually the honest answer at planning stage.

## Step 4: Communications and training plan

Read `references/comms-training-plan.md` before this step.

Build the plan **from the readiness assessment**, not from a calendar. The sequence for each group is the element order, starting at that group's barrier point:

- **Awareness**: the why, the risk of not changing, and what is and is not changing, from the sponsor.
- **Desire**: the job-impact conversation and the honest "what's in it for me," from the direct manager; involvement in design and pilot; visible leader participation.
- **Knowledge**: role-based training timed close to first use (two to four weeks before, not months), with the new process and decision rules, not just the screens.
- **Ability**: hands-on practice under real conditions, side-by-side support, super-users or change agents, a feedback path for problems that would otherwise become reasons to revert.
- **Reinforcement**: usage metrics visible to managers, recognition, corrective conversations, and the formal handoff to whoever owns the change after the project team leaves.

Produce the table in template section 4: audience, element, message or activity, sender or owner, channel or format, timing relative to go-live, and the resistance risk it addresses. Include the **sponsor roadmap** (what the sponsor does, when, visibly) and the **people-manager toolkit** (what each manager needs in hand before they talk to their team).

For AI-driven changes, add the **trust-building track**: how the model decides, in plain language; when a person may override it and how overrides are reviewed; a side-by-side comparison period where people can see model results against their own; and an explicit statement of what the role becomes once the model makes the decision.

## Step 5: Adoption metrics

Read `references/adoption-metrics.md` before this step.

Define, per group where it differs, the three dimensions that make adoption measurable:

- **Speed of adoption**: how quickly people start using the new way.
- **Utilization**: how many of the people who should be using it are, and how much of the work goes through it versus the old path.
- **Proficiency**: how well they use it, against a defined standard.

Name a **headline three** the sponsor sees every month, and cap the full table at eight. A small team cannot report more, and a long table hides the ones that matter. For each metric: definition, data source, baseline, target, review cadence, owner, and the business outcome it is a leading indicator for. Where no baseline exists, write the target as "to be set from the first-wave baseline by [date]," not as a number; a placeholder number in a table reads as a recommendation. Write the **definition of adopted** as one unambiguous sentence per group. For AI-driven changes, include override or reversion rate and a quality proxy for the model's decisions as experienced by the people using them. Include the two or three business outcomes the sponsor already cares about, and state how adoption connects to each.

## Step 6: Risks, assumptions, and judgment calls

Close with template section 6. List every assumption you made, each marked with what the reader should check. Then list the **judgment calls**: decisions the plan depends on that only an insider can make, such as which unit leader is actually passive, whether use is mandated, what the real history with past changes is, and which group should pilot first. Do not hide these in the body; a plan with unmarked assumptions is more dangerous than no plan.

## Output

Write the deliverable using `templates/change-plan.md`. Keep section order. Use tables where the template has them. The plan has two readers: the sponsor reads the one-page summary (section 0) and stops; the change lead reads the rest and acts on it tomorrow. Write the summary last, after the plan, and keep it to one page: barrier point per group, top three risks, the ask of the sponsor, next three actions. Do not pad with framework explanation; the reader wants the plan.

If the user asks for only one component (for example, "just the stakeholder map"), still run Step 0 and the readiness scoring in your head, because the component depends on them, and deliver only the section requested.

## Validating the output

Run `scripts/validate_plan.py <output.md>` when a script runner is available. It checks that every required section is present, every impacted group in the stakeholder map has a readiness row, and the judgment-calls section is not empty.
