# Responsible AI notes

What this assistant is for, what it is not for, how it can fail, and what is in place to catch that.

## Intended use

Helping people who plan and lead platform and AI rollouts find and apply guidance on change management,
sponsorship, communications and training, adoption measurement, and product delivery. Every answer is
drawn from a curated knowledge base and cites the passages it used, so the reader can check it.

## Not intended for

- Decisions about individual employees: performance, discipline, compensation, or selection.
- Legal, HR, labor-relations, or regulatory advice.
- Questions the knowledge base does not cover. The assistant is built to decline those rather than
  answer from the model's general knowledge.

## Data

| Knowledge base | What it contains | Where it lives |
|---|---|---|
| Public | Openly licensed guidance (18F, U.S. Digital Service, CC0) and the author's own writing (MIT). Sources, licenses, and pinned commits are in [SOURCES.md](SOURCES.md). | This repository, `corpus/public/` |
| Private | Whatever a user adds: course materials, internal playbooks. | The user's machine only, `corpus/private/`, git-ignored |

**What leaves the machine.** Retrieval runs locally. When a question is answered, the question and the
retrieved passages (up to six, public or private) are sent to the Claude API. Users adding private
material should confirm its license and their organization's policy allow that. Embeddings, if enabled,
are computed locally.

**Representativeness.** The public knowledge base reflects U.S. federal digital-delivery practice and one
practitioner's experience in a large U.S. financial services company. Advice that depends on culture,
labor law, unions or works councils, or industry regulation is outside what it can speak to.

## How it can fail, and what catches it

| Failure | Mitigation | How it is measured |
|---|---|---|
| Answers from general knowledge instead of the sources | System rules restrict answers to the search results; a decline path (`INSUFFICIENT_SOURCES`) | Grounding: a judge model checks each claim against the retrieved passages; unanswerable questions should be declined |
| Answers an off-topic question | Grounding gate: if no passage matches well enough, decline without calling the model | Off-topic decline rate; gate calibration table |
| Cites something that does not support the claim | Citations come from the API's search-result citation feature, which ties each cited sentence to a specific passage, not from model-written reference numbers | Citation coverage per answer; grounding judge |
| Uncited claims slip in | Post-check computes the share of answer text with a citation and flags answers below 60% | Citation coverage, reported per answer |
| Prompt injection, in the question or in a document | Passages go in as data blocks, and the rules say passages are reference material, not instructions; questions are scanned for injection phrasing and flagged | Adversarial questions in the evaluation set |
| Reproducing licensed text | Rules require paraphrase; a check flags any answer that shares more than 25 consecutive words with a private passage | Verbatim-run check on the adversarial reproduction question |
| Retrieval misses the right passage | Six passages per question; embedding and hybrid retrieval available; misses listed in the retrieval report | Hit@k and MRR per retrieval mode |
| The judge is wrong | The judge is a different, larger model than the one answering, it sees only the question, answer, and passages, and every verdict is stored with the claim it judged so a person can audit it | Per-question claims are saved in `eval/results/*.json` |

## Known limitations

- Keyword retrieval misses paraphrases: a question about "early adopters" may not find a passage that only
  says "pilot team." Hybrid retrieval reduces this; the retrieval report shows by how much.
- The grounding gate is a cheap first filter, not a classifier. On-topic questions the knowledge base does
  not cover share its vocabulary and pass the gate; declining those is the model's job.
- The evaluation set is small (39 questions) and was written by the person who built the system. It is a
  regression test and a demonstration of method, not a benchmark.
- Results vary between runs. Two runs of the same pipeline both passed 37 of 39, but failed on different
  questions. Compare runs on the claim-level counts, and repeat a run before trusting a small difference.
- The remaining grounding failure is the model adding a conclusion or step of its own that no source states
  (2 of 26 answers in the latest run, both with low citation coverage). Uncited sentences deserve the
  closest reading.
- An LLM judge can be lenient or strict in ways a person would not. Spot-check its verdicts.

## Human oversight

The assistant drafts; a person decides. Answers are inputs to a change plan written and owned by a
practitioner who knows the organization. The judgment calls that matter most (which leaders are passive,
which unit should pilot, what the organization's history with change has been) are not in any knowledge base.
