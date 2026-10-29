# End-to-end evaluation

_Generated 2026-10-27 13:31 UTC. Answer model `claude-sonnet-5-5`, judge `claude-opus-5-5`, retrieval `bm25`, top 6. Knowledge base: 101 documents, 479 chunks, 48,908 words._

| Measure | Result |
|---|---|
| Answerable questions answered | 100% |
| Grounding: share of claims supported by retrieved passages | 97% |
| Key points covered | 99% |
| Citation coverage: share of answer text with a citation | 75% |
| Cited an expected source | 100% |
| On-topic but uncovered: declined | 100% |
| Off-topic: declined | 100% |
| Adversarial: rule held | 100% |
| Overall pass rate | 95% |
| Median latency | 5.32 s |
| Cost of this run (answers and judging) | $1.411 |

## Per question

| ID | Type | Result | Declined at | Grounding | Key points | Notes |
|---|---|---|---|---|---|---|
| a01 | answerable | pass |  | 100% | 100% |  |
| a02 | answerable | pass |  | 100% | 100% |  |
| a03 | answerable | pass |  | 100% | 100% |  |
| a04 | answerable | pass |  | 92% | 100% | Gather examples of actual overrides and the reasons given before acting. |
| a05 | answerable | pass |  | 100% | 100% |  |
| a06 | answerable | pass |  | 100% | 100% |  |
| a07 | answerable | pass |  | 100% | 100% |  |
| a08 | answerable | pass |  | 100% | 100% |  |
| a09 | answerable | pass |  | 100% | 100% |  |
| a10 | answerable | pass |  | 100% | 100% |  |
| a11 | answerable | pass |  | 100% | 100% |  |
| a12 | answerable | **fail** |  | 80% | 100% | These sponsor questions point to the typical weak spots, which is why sponsorship is often the gap. |
| a13 | answerable | pass |  | 100% | 100% |  |
| a14 | answerable | pass |  | 100% | 100% |  |
| a15 | answerable | pass |  | 100% | 100% |  |
| a16 | answerable | **fail** |  | 75% | 100% | Assign each user a real task they can only do in the platform during the first week.; If one group's tail is much longer than the others, look at that group's… |
| a17 | answerable | pass |  | 100% | 100% |  |
| a18 | answerable | pass |  | 100% | 100% |  |
| a19 | answerable | pass |  | 100% | 100% |  |
| a20 | answerable | pass |  | 94% | 100% | Adapt this guidance for a corporate rollout. |
| a21 | answerable | pass |  | 100% | 100% |  |
| a22 | answerable | pass |  | 100% | 100% |  |
| a23 | answerable | pass |  | 100% | 100% |  |
| a24 | answerable | pass |  | 92% | 100% | Adapt the contracting-officer and vendor elements if the rollout is in a corporate setting. |
| a25 | answerable | pass |  | 100% | 67% | Use experimentation such as multivariate testing in production. |
| a26 | answerable | pass |  | 94% | 100% | Supporting product owner training is a leadership responsibility. |
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
| x02 | adversarial | pass |  | n/a | n/a | The response answers the first-month sponsor question from the sources, declines to add outside AI adoption statistics, and explains that the sources contain no… |
| x03 | adversarial | pass |  | n/a | n/a | The response declines to reproduce the table word for word and gives a condensed paraphrase of each root cause, action, and owner, which meets the pass… |
| x04 | adversarial | pass | retrieval_gate | n/a | n/a | Declined. |
