---
title: 'Evaluation: where the skill was right, and where it needed my judgment'
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/examples/pega-1to1-ops-manager/EVALUATION.md
source_path: examples/pega-1to1-ops-manager/EVALUATION.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# Evaluation: where the skill was right, and where it needed my judgment

**Setup.** A fresh model instance was given only `SKILL.md`, its references, and `INPUT.md` (the rollout as it could have been described at planning stage). It was told not to read anything else. It produced `OUTPUT.md`, which passed the structural validator on the first run. I then compared it against `GROUND-TRUTH.md`: the health check and readiness assessment I ran on the rollout, and what I observed leading it.

Scores in the two documents are on different scales (the skill's health check is out of 15 per corner; the instrument I used is out of 30), so the comparison is on direction, ranking, and conclusions, not on numbers.

## Where it was right

### 1. It found the same barrier point for channel managers, for the same reasons

| | Blind run | Actual |
|---|---|---|
| Channel manager profile | A4 D2 K2 A1 R1 | A4 D3 K2 A2 R1 |
| Barrier point | Desire | Desire |
| Root causes named | Loss of decision authority, role identity, no transparency into the model, override free and unreviewed, incentives reward old behavior | Skepticism about the AI, discomfort with reduced control, uncertainty about the role |

The three resistance patterns I observed map one-to-one onto the skill's AI-specific patterns (low trust, loss of control, role identity). The skill also drew the conclusion I reached in the certification work: training channel managers before Desire clears produces attendance, not adoption. It scheduled training at G-3w, after the role statement, job-impact conversation, and override policy.

### 2. It identified sponsor consistency across LOBs as the top structural risk

The skill flagged that one sponsor was named for a multi-LOB rollout where the LOB leads report elsewhere, built a coalition table with every LOB lead flagged, and wrote: adoption will be uneven in exactly the LOBs where the lead is passive. That is the single clearest lesson from the rollout, and the skill got there from the org structure in the description alone. It also assigned LOB leads their own Desire barrier ("leaders not modeling the change, own barrier unresolved"), which is the root cause I featured in the certification deck.

### 3. The health check ranked the corners correctly and found the same three gaps

| Corner | Blind run (of 15) | Actual (of 30) | Rank match |
|---|---|---|---|
| Success | 7, high | 15, high | Yes |
| Leadership and sponsorship | 6, high | 14, high | Yes |
| Project management | 9, medium | 16, high (but highest) | Yes on rank, no on band |
| Change management | 6, high | 14, high | Yes |

The three lowest conditions the skill named (no coalition on one definition of success, no adoption targets separate from milestones, no owner after the project team leaves) are three of the items that scored lowest on my assessment. The skill also correctly scored "nature of the change defined by group" as partly in place, which was my strongest project-management item.

### 4. It recommended the same first move I chose for the certification presentation

The skill's "Next three actions" opens with a sponsor conversation carrying a specific ask: coalition, wave-1 LOB, legacy retirement authority, operational owner, standing weekly check-in. My presentation chose the primary sponsor as the audience and asked for commitment to the three sponsor roles. Same diagnosis, same audience, same shape of ask.

### 5. It separated what it knew from what it assumed

The plan ends with ten labeled assumptions and eight judgment calls. Every one of the judgment calls is a real question from the rollout (wave order, mandate, sponsor reach into LOBs, incentives, override authority, compliance posture, post-project owner). The skill did not pretend to know them. That is the behavior I most wanted from it.

## Where it needed my judgment

### 1. It treated my unconfirmed group list as fact

Four of the five impacted groups in the input were my working list, never assessed. The skill scored all five with equal structure and assigned Awareness barriers to analysts and compliance approvers. Those are plausible inferences from the description, but nobody measured them, and the skill's confidence ratings (Low for both) were the only signal. An insider knows which groups are real impacted groups and which are adjacent functions. **Skill change:** when the requester supplies the group list, the plan now records the list as "as provided; confirm each group is impacted on at least one dimension" and does not score a group whose impact is not stated.

### 2. It over-weighted the description's language in the Desire score

The skill scored channel-manager Desire at 2; I scored it 3. The input said teams "built themselves and are proud of" their methods, and the skill read that as a stronger signal than it was. Same barrier, but the severity came from prose, not evidence. **Skill change:** departures of more than one point from the stated prior now require direct evidence (a quote, an incident, a survey), not an inference from tone.

### 3. It credited project management for the existence of an operations lead

The description said I led operations with a core team of five. The skill scored "assigned project manager and schedule" as partly in place. My assessment scored it as not in place: leading operations across LOBs is not the same as a project manager owning a lifecycle with a schedule and a work breakdown. The skill cannot know that distinction from a sentence. **Skill change:** the health check now scores project-management items on evidence of the artifacts (a named PM, a schedule, a work breakdown), not on the presence of a lead.

### 4. It could not know which LOB leads were passive, or which LOB to pilot

The skill correctly flagged this as the first judgment call, but every downstream decision in the plan (wave order, where to run the side-by-side, which LOB's channel managers get design roles) depends on it. In the rollout, I knew which LOB sponsors were active from the first month; the skill can only say "find out." That is the right behavior and also the limit of what a description can produce.

### 5. Its metrics and targets were placeholders that look like decisions

Thirteen metrics, with targets like "override rate under 15 percent" and "50 percent cycle-time reduction," all labeled as assumed. The labels were honest, but a sponsor skimming the table would read them as recommendations. A team of five can sustain about five metrics, and the right override band is a business decision with data science and compliance, which the skill said itself in judgment call 5. **Skill change:** the metrics section now requires a "headline three" and caps the full table at eight; numeric targets without a baseline are written as "to be set from the wave-1 baseline," not as numbers.

### 6. It produced a plan the sponsor would not read

The output is excellent for a change lead and too long for a sponsor: a 29-row communications table and a 13-row metrics table, against the skill's own instruction to be readable in fifteen minutes. In practice the sponsor conversation is one page. **Skill change:** the template now opens with a one-page summary (barrier per group, top three risks, next three actions, the ask of the sponsor), and the full plan sits beneath it.

### 7. It could not know the rollout was already underway

The input was written as planning stage, so the skill planned from G-20w. On the actual rollout, people-side work was sequenced after technical delivery was already moving. The skill has no way to detect that from a description that does not say so, which is fine; but it means the honest use of this skill mid-rollout is to compress the diagnostic steps into weeks, and the plan now says what to do in that case (assumption 1 covers it).

## Scorecard

| Component | Verdict |
|---|---|
| Stakeholder and resistance map | Right on channel managers and LOB leads; plausible but unverified on the other three groups |
| Readiness assessment | Right barrier, right reasoning, scores one point too severe where the prose was vivid |
| Health check | Right ranking and right top-three gaps; over-credited project management |
| Comms and training plan | Right sequence and right senders; too long for its primary reader |
| Adoption metrics | Right dimensions and right link to business outcomes; too many, with placeholder targets that read as decisions |
| Judgment calls | The strongest section: every item is a question I actually had to answer |

## What this says about the skill

The skill reliably gets the shape of the problem right from a description: which group is the barrier, why, who the real sponsor risk is, and what to do first. It cannot replace three things only an insider has: who the people are and how they actually behave, what the real history is, and which numbers are real. The design decision that made it useful is forcing those three things into a visible list rather than hiding them inside confident-looking tables.

Changes 1, 2, 3, 5, and 6 above are applied in the skill as published. `OUTPUT.md` is left as the unedited blind run against the first version, so the evaluation stays honest. You can see the two structural changes directly: the current validator passes `OUTPUT.md` only with `--legacy`, and in strict mode fails it on exactly the two things this evaluation changed, the missing one-page summary and the thirteen-row metrics table.

```
$ python3 change-management/scripts/validate_plan.py examples/pega-1to1-ops-manager/OUTPUT.md
FAIL
  - missing section: ## 0. One-page summary
  - metrics table has 13 rows; cap is 8 (pick the vital few)
```
