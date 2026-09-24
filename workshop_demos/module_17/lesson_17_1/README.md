# Lesson 17.1: Decide whether tuning is justified and prepare data

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_tuning_decision.py](demo_01_tuning_decision.py) | Establish whether tuning is justified using the lesson's actual baseline evidence. |
| 3 | [demo_02_prepare_training_examples.py](demo_02_prepare_training_examples.py) | Prepare the dataset and inspect its schema/content before uploading. |
| 4 | [demo_03_validate_splits_and_contamination.py](demo_03_validate_splits_and_contamination.py) | Check split quality and contamination before any managed tuning job. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

Baseline evaluation evidence and the kit's sanitized training examples; no tuning job is submitted here.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

Prepare this lesson's saved settings and dependencies before its live experiments.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Operation: bash — run in the operator shell now, before the lesson's first step.

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

### demo_01_tuning_decision.py

Establish whether tuning is justified using the lesson's actual baseline evidence.

**`step_01_example(session)` — The kit's rules, and the file it ships, audited / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the rules on fixtures, then the kit's own v1; no network).

Expected shape, not a promised result:

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

### demo_02_prepare_training_examples.py

Prepare the dataset and inspect its schema/content before uploading.

**`step_01_example(session)` — The evidence, and the verdict / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (every golden row, as in 7.2: about ten minutes).

Expected shape, not a promised result:

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

**`step_02_example(session)` — The evidence, and the verdict / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (reads only: the report, a week of logs, the price table).

Expected shape, not a promised result:

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

### demo_03_validate_splits_and_contamination.py

Check split quality and contamination before any managed tuning job.

**`step_01_example(session)` — Your training file, as v2 / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (about twenty minutes: one flash call a chunk).

Expected shape, not a promised result:

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

**`step_02_example(session)` — The frozen file, read back / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (reads only).

Expected shape, not a promised result:

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

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_17.1_Tuning_Decision_WIX.html`. All 22 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `055368732655b9c9c490603445fb3ef0f506e36b`.
