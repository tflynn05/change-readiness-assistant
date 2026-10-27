# Retrieval evaluation

_Generated 2026-10-26 23:55 UTC by `cra eval --retrieval-only`. Knowledge base: 101 documents, 479 chunks, 48,908 words._

## Does the right source come back?

For each answerable question, the rank of the first chunk from an expected source.

| Retrieval | Questions | Hit@1 | Hit@3 | Hit@6 | Hit@10 | MRR@10 |
|---|---|---|---|---|---|---|
| bm25 | 28 | 61% | 93% | 100% | 100% | 0.78 |

## Grounding gate calibration

The gate declines before any model call when the best keyword match is weaker than the threshold. A good threshold lets every answerable question through and stops as many off-topic ones as possible.

Lowest score among answerable questions: **0.140**. Highest score among off-topic questions: **0.184**. Recommended threshold: **0.14** (configured: 0.14).

| Threshold | Answerable let through | Off-topic stopped | On-topic-but-uncovered stopped |
|---|---|---|---|
| 0.10 | 100% | 0% | 0% |
| 0.14 | 100% | 67% | 0% |
| 0.18 | 93% | 67% | 17% |
| 0.22 | 89% | 100% | 50% |
| 0.26 | 86% | 100% | 100% |
| 0.30 | 75% | 100% | 100% |
| 0.34 | 64% | 100% | 100% |
| 0.38 | 50% | 100% | 100% |
| 0.42 | 36% | 100% | 100% |
| 0.46 | 18% | 100% | 100% |
| 0.50 | 11% | 100% | 100% |

On-topic questions the knowledge base does not cover usually pass the gate because they share vocabulary with it. Declining those is the model's job, and stage 2 measures it.
