---
title: 'Adoption metrics: reference'
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/change-management/references/adoption-metrics.md
source_path: change-management/references/adoption-metrics.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# Adoption metrics: reference

Use this when building Step 5 of the plan.

## Why this section exists

Go-live is a project milestone. Adoption is a business result. If adoption is not measured, the project reports success at go-live while the benefit never arrives, because people kept doing the work the old way. Define the measures before go-live, baseline them, and put them in front of the sponsor and the managers.

## The three dimensions

| Dimension | What it measures | Typical metric |
|---|---|---|
| Speed of adoption | How quickly people start using the new way after it is available to them | Days from access to first real use; share of the group that has used it by week 2, 4, 8 |
| Utilization | How many of the people who should be using it are, and how much of the work goes through it | Active users over eligible users; share of work items created or processed in the new path versus the old |
| Proficiency | How well they use it against a standard | Error or rework rate; time per task; share of outputs meeting a quality bar; use of the capabilities that deliver the benefit, not just the basic ones |

Measure all three. Utilization alone hides the team that logs in and does nothing. Proficiency alone hides the team that is excellent and tiny.

## The vital few

Pick a headline three that the sponsor reviews monthly: usually share of work through the new path, one proficiency measure tied to the benefit, and, for AI changes, the override rate. Cap the full set at eight. Every metric needs someone to produce it and someone to act on it; a team that cannot name both for a metric should drop it.

## Define "adopted" per group

One sentence per group, observable, with a number. Examples of the form:

- Primary users: "Builds and launches at least 90 percent of new work items in the platform, with no parallel build in the legacy tool, for four consecutive weeks."
- Approvers: "Completes 95 percent of reviews in the new workflow within the agreed turnaround, with no email-based approvals."
- Analysts: "Reports from the new data source only; legacy reports retired."
- Managers: "Reviews the team adoption dashboard weekly and has held a corrective conversation where needed."

Agree these with the unit leaders. A definition the unit leader did not agree to will be disputed when it is missed.

## Leading and lagging

Adoption metrics are leading indicators for the business outcomes the sponsor already cares about. Show the link explicitly:

| Adoption metric (leading) | Business outcome (lagging) |
|---|---|
| Share of work through the new path | Throughput, speed to market |
| Proficiency on the capabilities that drive the benefit | Lift, conversion, cost per outcome |
| Approver turnaround in the new workflow | Cycle time |
| Legacy path retired | Cost, risk, governance |

If a business outcome has no adoption metric leading it, either the outcome does not depend on people, or the plan is missing a metric.

## Metric specification

For each metric, fill in:

| Field | Content |
|---|---|
| Name | |
| Definition | Numerator, denominator, inclusion rules |
| Group | Who it applies to |
| Data source | System, report, survey; name the owner of the data |
| Baseline | Value before go-live, or "to be baselined by [date]" |
| Target | Value and date |
| Cadence | Weekly to managers, monthly to the sponsor is the usual default |
| Owner | Who reports it and who acts on it |
| Leads to | The business outcome it predicts |

## AI-specific metrics

When a model takes decisions, add:

| Metric | Why |
|---|---|
| Override or reversion rate: share of model decisions changed by a person, by group and by reason | High and unexplained override rate is the signature of low trust or an unredefined role; zero override on a new model is also a warning sign |
| Share of decisions made through the model versus the legacy manual path | The direct measure of whether the old way is retiring |
| Model-decision quality as experienced by users: agreement rate in side-by-side review, complaint rate, correction rate | People trust what they can see performing |
| Time from model recommendation to action | Measures whether the new workflow is actually faster for people |
| Training coverage on the override process, not just the interface | Knowledge metric specific to AI changes |

## Pulse measures

Alongside system data, a short pulse per element (one question each, five-point scale) at kickoff, pilot, and go-live gives the readiness trend by group. Keep it to five questions; response rates fall with length.

## Reporting

- Weekly: managers see their own team's three dimensions against the adoption definition.
- Monthly: the sponsor sees adoption by unit, the lagging outcomes, and the units behind target, with the unit leader named.
- At handoff: the operational owner inherits the metrics, the targets, and the reporting.

A metric nobody reviews changes nothing. Put the review on calendars before go-live.
