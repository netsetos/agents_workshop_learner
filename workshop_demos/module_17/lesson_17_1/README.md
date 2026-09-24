# Lesson 17.1: Decide whether tuning is justified and prepare data

**Summary:** the frozen manifest and its row count. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.1-tuning-decision/Netsetos_GCP_Capstone_17.1_Tuning_Decision_WIX.html); Git blob `9dd628268229d1f2f125a0bd5f6abb9d42ce92cb`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the rules on fixtures, then the kit's own v1; no network) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (every golden row, as in 7.2: about ten minutes) |
| s4 · window 14 | [demo_04_02_do_it.py](demo_04_02_do_it.py) | bash — run in the operator shell, in the kit (reads only: the report, a week of logs, the price table) |
| s5 · window 18 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (about twenty minutes: one flash call a chunk) |
| s6 · window 21 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (reads only) |

## Finish and restore settings

- [finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) — bash — run in the operator shell when you finish the lesson, not now

## Checkpoints and explanation

### demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Run instruction: bash — run in the operator shell now, before the lesson's first step.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=vector
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### finish_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Run instruction: bash — run in the operator shell when you finish the lesson, not now.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Run at lesson end despite its early HTML position, as the source label explicitly instructs.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it.py

**HTML: The kit's rules, and the file it ships, audited / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the rules on fixtures, then the kit's own v1; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
selftest: the evidence rule dropped jn-06's chunk and kept EMEA elsewhere and lk-09's 8, the question rule dropped lk-06's twin, the PAN row dropped, two formats agree, ModelDraft parses, the batch round trip holds
the manifest: v1, built 2026-09-10, 317 rows (30 refusals) from 12 documents; dropped 13 for the golden set, 0 for PII
the two formats agree row by row: True; targets that parse as ModelDraft: 317 of 317; SYSTEM is the generator's: True
quotes: 287; in their chunk as written: 22, once line breaks are spaces: 282; over twenty-five words: 17
answers that mark their source with [N], as SYSTEM's rule 2 asks: 0 of 287
rows from the handbook: 58, every one from a generated GEN- section: its clauses are all under 400 characters
today's golden set (65 rows) would drop 0 of v1's rows
the prompt v1 trains on shows a chunk as: '[Source 1] CHAPTER XIV INSPECTION, SEARCH, SEIZURE AND ARREST \n '...
the prompt the generator serves shows it as: '[Source 1] cgst_act_2017.pdf\nCHAPTER XIV INSPECTION, SEARCH, SEI'...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The evidence, and the verdict / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (every golden row, as in 7.2: about ten minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  65 rows (47 answerable, 18 not) against https://documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 65 rows)
  [PASS] answerable_rate        97.9%  (threshold 80%; 47 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 46 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 46 rows)
  [PASS] must_contain_rate      97.8%  (threshold 85%; 46 rows)
  [PASS] correct_rate           95.7%  (threshold 68%; 47 rows)
  [PASS] refusal_rate          100.0%  (threshold 90%; 18 rows)
  [PASS] media_kind_rate       100.0%  (threshold 80%; 3 rows)
  [PASS] isolation_403_rate    100.0%  (threshold 100%; 11 rows)
  [info] quote_support_rate      ...  (quoted words found in the tenant's corpus text; not a threshold - a Doc AI extraction and a pypdf mirror hyphenate differently)

  shape        rows   ok   pass
  lookup         34   34     33
  join           11   11     10
  refusal         8    8      8
  isolation      11   11     11
  version         1    1      1
  latency ms  p50   ...  p95   ...   (round trip, 65 rows)
  retrieve_ms p50   ...  p95   ...
  rerank_ms   p50   ...  p95   ...
  generate_ms p50   ...  p95   ...
  pool        avg   ...   semantic cache hits ...

  rows that cost a point (2):
    jn-06  join      acme    answered without ['EMEA', '11.4'] | 'emea revenue fell in fy2026 [1].'
    lk-27  lookup    acme    REFUSED conf=low cites=0 | What is the maximum rate of central tax the CGST Act allows?

  report: /home/YOU/gate171.json
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it.py

**HTML: The evidence, and the verdict / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads only: the report, a week of logs, the price table).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. the gate: 65 rows, 2 missed
   jn-06  join     answered without ['EMEA', '11.4']            -> knowledge (retrieval, the corpus, or the row)
   lk-27  lookup   refused                                      -> knowledge (retrieval, the corpus, or the row)
2. the grammar, last 7 days: 1 repaired, 0 invalid, 0 unparsed, in 360 answers (0.3%)
3. the price at this lane's tokens (7,389 in and 211 out an answer, 1,543 answers a month):
   gemini-3.6-flash         Rs 1.08 an answer, Rs 1,662 a month
   tuned flash-lite, 1.5 x  Rs 0.28 an answer, Rs 426 a month
4. the data: 1,542 chunks of 400 characters or more in acme's corpus mirrors
verdict: not for quality - the misses are knowledge, and the grammar holds.
         for price, only as an experiment: gemini-3.6-flash cannot be tuned; a tuned gemini-3.1-flash-lite would save
         Rs 1,236 a month at this traffic, if it passes the same gate (lesson 17.3)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Your training file, as v2 / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (about twenty minutes: one flash call a chunk).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python evals/make_trainset.py --project documind-ai-YOUR-ID --tenant acme --rows ${ROWS:-300} \
  --upload gs://documind-ai-YOUR-ID-datasets/sft/ --version v2
  300 chunks sampled from acme's corpus mirrors
  315 rows (30 refusals) from 12 documents; dropped 15 for golden overlap ['jn-10', 'jn-11', 'lk-14', 'lk-17', 'lk-18', 'lk-23', 'lk-24', 'lk-26', 'lk-28'] and 0 by the PII scan
  wrote /home/YOU/deploy_module_rag/evals/sft/documind_sft_v2.{vertex,chat}.jsonl + .manifest.json (sha ac73343d2550)
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.chat.jsonl
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.manifest.json
  uploaded gs://documind-ai-YOUR-ID-datasets/sft/documind_sft_v2.vertex.jsonl
  review the rows before you commit them: a generated question inherits the generator's blind spots (4.7)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The frozen file, read back / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the frozen manifest, from gs://documind-ai-YOUR-ID-datasets/sft/: v2, built 2026-09-24, 315 rows (30 refusals) from 12 documents; generator gemini-3.6-flash
  dropped 15 for the golden set {'evidence': 10, 'question': 5} (jn-10, jn-11, lk-14, lk-17, lk-18, lk-23, lk-24, lk-26, lk-28), 0 for PII
  vertex documind_sft_v2.vertex.jsonl: 315 rows, sha256 as the manifest says
  chat   documind_sft_v2.chat.jsonl: 315 rows, sha256 as the manifest says
the rows, checked again: the golden set would drop 0 of 315
  quotes in their chunk, line breaks as spaces: 285 of 285; over twenty-five words: 0
  answers that mark their source with [N]: 0 of 285
  rows from the handbook's generated GEN- sections: 58
  acme:cgst_act_2017#p1-0: What does the CGST Act, 2017 say about its scope?
  acme:code_on_social_security_2020#p57-0: Does the Code on Social Security, 2020 set a time limit for the employer?
  acme:industrial_relations_code_2020#p16-2: What does the Industrial Relations Code, 2020 say about registration?
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

22 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 14 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
