# Private knowledge base

Put licensed or internal material here: training manuals, certification course materials,
your organization's change playbooks. Git ignores everything in this folder except this file,
so nothing you add here can be committed or pushed.

**Formats:** `.md`, `.txt`, `.csv`, and, with `pip install -e ".[files]"`, `.pdf`, `.docx`,
`.pptx` (slide text, tables, and speaker notes), and `.xlsx` (each sheet as a table).
Images are skipped. Subfolders are fine. A markdown file can start with front matter
(`title:`) to set its title. PDF passages are cited by page and slides by slide number.

**Or leave your files where they are.** Set `CRA_PRIVATE_DIR` in `.env` to any folder, for
example `CRA_PRIVATE_DIR=../Certifications/Prosci`, and it is read in place. Nothing is copied
into the project, so there is nothing that could be committed. `cra index` lists every private
file it read, with chunk and word counts, and any it skipped.

**How it is used:** `cra index` picks these files up automatically, and answers can cite them.
Private sources show as `private:<file name>` and are marked `[private]` in search results.

**Before you add anything, know two things:**

1. **Retrieved passages are sent to the Claude API** when you ask a question, the same as
   public passages. Check that the material's license and your organization's policy allow
   that. Anthropic's commercial terms do not use API data for training by default, but your
   license terms are what decide whether you may send the text at all.
2. **Answers are kept from quoting private sources at length.** The model is told to
   paraphrase, and a check flags any answer that repeats more than 25 consecutive words
   from a private passage (`CRA_MAX_PRIVATE_QUOTE_WORDS`). Treat flagged answers as
   internal only.

**Evaluation:** `cra eval` uses the public knowledge base only, so published results are
reproducible. To test with your private files, put your own questions in
`eval/questions.private.yaml` (also git-ignored) and run
`cra eval --include-private --questions eval/questions.private.yaml`.
