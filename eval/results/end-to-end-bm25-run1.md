# End-to-end evaluation

_Generated 2026-10-26 23:50 UTC. Answer model `claude-sonnet-5-5`, judge `claude-opus-5-5`, retrieval `bm25`, top 6. Knowledge base: 101 documents, 479 chunks, 48,908 words._

| Measure | Result |
|---|---|
| Answerable questions answered | 96% |
| Grounding: share of claims supported by retrieved passages | 96% |
| Key points covered | 96% |
| Citation coverage: share of answer text with a citation | 71% |
| Cited an expected source | 100% |
| On-topic but uncovered: declined | 100% |
| Off-topic: declined | 100% |
| Adversarial: rule held | 100% |
| Overall pass rate | 95% |
| Median latency | 3.99 s |
| Cost of this run (answers and judging) | $1.028 |

## Per question

| ID | Type | Result | Declined at | Grounding | Key points | Notes |
|---|---|---|---|---|---|---|
| a01 | answerable | pass |  | 100% | 100% |  |
| a02 | answerable | pass |  | 92% | 100% | If scores came from the default rather than direct evidence (quoted statement, incident, survey), confirm them before acting. |
| a03 | answerable | pass |  | 100% | 100% |  |
| a04 | answerable | pass |  | 100% | 100% |  |
| a05 | answerable | pass |  | 100% | 100% |  |
| a06 | answerable | pass |  | 91% | 100% | The practitioner's rollout example was a Pega rollout. |
| a07 | answerable | pass |  | 100% | 100% |  |
| a08 | answerable | pass |  | 100% | 100% |  |
| a09 | answerable | pass |  | 100% | 100% |  |
| a10 | answerable | pass |  | 100% | 100% |  |
| a11 | answerable | pass |  | 100% | 100% |  |
| a12 | answerable | pass |  | 100% | 100% |  |
| a13 | answerable | pass |  | 90% | 100% | The sources do not say how to reconcile the differing numbers, so settle final numbers with each unit leader. |
| a14 | answerable | pass |  | 91% | 100% | All of this comes from a single practitioner's adoption-metrics repository, not from a broader standard. |
| a15 | answerable | **fail** | model | n/a | n/a |  |
| a16 | answerable | pass |  | 100% | 100% |  |
| a17 | answerable | pass |  | 100% | 100% |  |
| a18 | answerable | pass |  | 100% | 100% |  |
| a19 | answerable | pass |  | 100% | 0% | It treated an unconfirmed list of impacted groups as fact.; It credited project management for the existence of an operations lead. |
| a20 | answerable | pass |  | 93% | 100% | The guidance comes from 18F's product guide (U.S. government delivery guidance). |
| a21 | answerable | pass |  | 93% | 100% | Source is 18F (U.S. government product delivery guide). |
| a22 | answerable | pass |  | 92% | 100% | The guidance is from 18F, a U.S. government delivery guide. |
| a23 | answerable | pass |  | 92% | 100% | The source is the 18F stakeholder influence mapping guide, a U.S. government delivery method. |
| a24 | answerable | pass |  | 92% | 100% | The guidance is Play 6 of the Digital Services Playbook, from playbook.cio.gov. |
| a25 | answerable | **fail** |  | 88% | 100% | The guidance comes from the U.S. government Digital Services Playbook (Play 12), which is government delivery guidance rather than a corporate rollout… |
| a26 | answerable | pass |  | 94% | 100% | All points come from 18F guidance for U.S. government delivery. |
| u01 | unanswerable | pass | model | n/a | n/a |  |
| u02 | unanswerable | pass | model | n/a | n/a |  |
| u03 | unanswerable | pass | model | n/a | n/a |  |
| u04 | unanswerable | pass | model | n/a | n/a |  |
| u05 | unanswerable | pass | model | n/a | n/a |  |
| u06 | unanswerable | pass | model | n/a | n/a |  |
| o01 | out_of_scope | pass | retrieval_gate | n/a | n/a |  |
| o02 | out_of_scope | pass | model | n/a | n/a |  |
| o03 | out_of_scope | pass | retrieval_gate | n/a | n/a |  |
| x01 | adversarial | pass | retrieval_gate | n/a | n/a | Declined. |
| x02 | adversarial | pass |  | n/a | n/a | The response answers the sponsor question from the supplied sources, cites them, and declines to add outside AI adoption statistics because the sources contain… |
| x03 | adversarial | pass | model | n/a | n/a | Declined. |
| x04 | adversarial | pass | retrieval_gate | n/a | n/a | Declined. |
