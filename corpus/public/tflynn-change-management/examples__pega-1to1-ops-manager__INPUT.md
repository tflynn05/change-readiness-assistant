---
title: Rollout description (as handed to the skill)
source_id: tflynn-change-management
source_title: Change management skill (references and Pega case study)
author: Tim Flynn
license: MIT
source_url: https://github.com/tflynn05/change-management-skill/blob/main/examples/pega-1to1-ops-manager/INPUT.md
source_path: examples/pega-1to1-ops-manager/INPUT.md
source_commit: afc2dc6d926ea836128fba6e0558d3ec1015c2bc
---

# Rollout description (as handed to the skill)

This is the description a program lead could have written at the planning stage, before any assessments were run. It is the only input the skill received for the blind test. Nothing from the actual assessments or outcomes is included.

---

**Project.** Enterprise rollout of Pega 1:1 Operations Manager, the business-user layer on top of Pega Customer Decision Hub, at a large US financial services company. The platform replaces manually built, segment-based marketing campaigns with AI-driven next-best-action decisioning. Campaigns are no longer authored as audience segments plus offers; instead, marketers define actions, treatments, and eligibility, and the decisioning engine selects the next best action for each member in real time across channels. The rollout spans multiple lines of business (LOBs) and is sequenced LOB by LOB rather than as a single cutover. I lead operations for the rollout with a core team of five, coordinating program activity across the LOBs.

**Purpose.** Personalized, real-time decisioning instead of batch targeting; faster speed to market for campaigns; stronger revenue outcomes from marketing; and one governance and measurement model across LOBs that today run different processes and tools.

**What changes in the work.** The platform and tools change. The way actions are built, approved, and deployed changes: a new workflow with new roles in the approval chain. And the relationship with targeting changes most of all: experienced marketers who built and owned their own segment logic are now asked to trust the model's recommendation over their own targeting judgment. Measurement changes too, since campaign results are now attributed through the decisioning engine rather than to a hand-built segment.

**Who is impacted.**
- Marketing channel managers, who own campaigns in a channel and today build the targeting themselves.
- Campaign operations, who build, QA, and deploy campaigns.
- Marketing analysts, who measure campaign performance and report to LOB leadership.
- LOB marketing leads, whose teams adopt and who are accountable for their LOB's marketing results.
- Compliance approvers, who review and approve marketing content and targeting before it goes out.

Group sizes are not large per LOB (tens, not hundreds), but the groups repeat in each LOB.

**Sponsorship.** A senior marketing executive sponsors the program. The LOB marketing leads report into their own LOB structures, not to the sponsor.

**Timeline.** Program kickoff, then the first LOB goes live around month 6, with further LOBs following in waves. Business outcomes are expected to show around month 12.

**History.** The organization has run several large marketing-technology implementations before, with mixed adoption. Teams have working methods they built themselves and are proud of.

**Success measures the business already uses.** Campaign throughput and speed to market, campaign lift and conversion, and marketing-driven revenue by LOB.

**What is algorithmic.** The selection of which action a member sees, when, and in which channel, previously decided by the marketer through segment design, is now decided by the decisioning engine's models and arbitration rules. People still define the actions, treatments, eligibility rules, and objectives.
