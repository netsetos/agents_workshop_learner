# Lesson 17.3: Compare the tuned candidate with an uncontaminated baseline

**Summary:** the pairwise verdict and the rupee delta. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html); Git blob `c02ada0a08be5b1c1cbcc4ad94b1b7ced4a3e0b3`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the kit's own functions; no network) |
| s4 · window 12 | [demo_04_01_do_it_the_candidate.py](demo_04_01_do_it_the_candidate.py) | bash — run in the operator shell, in the kit (a revision with no traffic; nothing is billed until it answers) |
| s4 · window 14 | [demo_04_02_do_it_the_audit.py](demo_04_02_do_it_the_audit.py) | bash — run in the operator shell, in the kit (reads both revisions, ~/tune172.log, the bucket and Firestore) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (every golden row, on each revision: about twenty minutes) |
| s5 · window 18 | [demo_05_02_do_it.py](demo_05_02_do_it.py) | bash — run in the operator shell, in the kit (reads the two reports) |
| s6 · window 21 | [demo_06_01_do_it_the_verdict.py](demo_06_01_do_it_the_verdict.py) | bash — run in the operator shell, in the kit (the judge's venv from lesson 7.2: 65 answers from each revision, then Vertex AI Evaluation) |
| s6 · window 23 | [demo_06_02_do_it_the_delta.py](demo_06_02_do_it_the_delta.py) | bash — run in the operator shell, in the kit (reads the last two hours of usage rows) |
| s6 · window 26 | [demo_06_03_the_decision_and_the_candidate_s_tag.py](demo_06_03_the_decision_and_the_candidate_s_tag.py) | bash — run in the operator shell, in the kit (removes the candidate's address; the revision stays, with no traffic) |

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

**HTML: What the kit does with a tuned candidate / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the kit's own functions; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
an answer gemini-3.6-flash cached, looked up for the tuned endpoint: alive True
cost.py with RAG_MODEL_BASE=gemini-3.1-flash-lite  Rs 0.1764 an answer of 7,400 tokens in, 150 out
cost.py with RAG_MODEL_BASE=gemini-3.6-flash       Rs 1.0391 an answer of 7,400 tokens in, 150 out
Google, a tuned endpoint at 1.5 x its base          Rs 0.2646

make usage's model column
model                  answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
gemini-3.6-flash             1      7400      210    0.0127      1.08    2100   0.00
projects/NUMBER/loca         1      7400      150    0.0021      0.18    1000   0.00
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_candidate.py

**HTML: The candidate, audited / Do it: the candidate**

Do it: the candidate

Run instruction: bash — run in the operator shell, in the kit (a revision with no traffic; nothing is billed until it answers).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=projects/NUMBER/locations/us/endpoints/9136961803583303949|RAG_MODEL_BASE=gemini-3.1-flash-lite|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=off|RETRIEVAL_CURRENT_ONLY=off|RETRIEVAL_GRAPH=off|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_audit.py

**HTML: The candidate, audited / Do it: the audit**

The cell makes the four checks from step 1:

Run instruction: bash — run in the operator shell, in the kit (reads both revisions, ~/tune172.log, the bucket and Firestore).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. one change: 2 settings differ between documind-api-000NN-xxx (live) and documind-api-000NN-yyy
   GENERATOR_MODEL  gemini-3.6-flash -> projects/NUMBER/locations/us/endpoints/9136961803583303949
   RAG_MODEL_BASE   gemini-3.6-flash -> gemini-3.1-flash-lite
   the model and the base it is priced at, and nothing else
2. the answer cache: off on the live revision, off on the candidate
3. the test set: the endpoint was tuned on documind_sft_v2.vertex.jsonl, 315 rows; building it dropped 15 for the golden set, and today's golden set would drop 0 more
4. the context cache: none for acme, so both revisions pay full price for their input
verdict: uncontaminated - one change, no answer cache, a training file the test set never entered, the same input price
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The gate on both revisions / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (every golden row, on each revision: about twenty minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
report: /home/YOU/base173.json
  All thresholds met.
>> https://candidate---documind-api-NUMBER.asia-south1.run.app
  65 rows (47 answerable, 18 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 65 rows)
  [PASS] answerable_rate        97.9%  (threshold 80%; 47 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 46 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 46 rows)
  [PASS] must_contain_rate      95.7%  (threshold 85%; 46 rows)
  [PASS] correct_rate           93.6%  (threshold 68%; 47 rows)
  [PASS] refusal_rate          100.0%  (threshold 90%; 18 rows)
  [PASS] media_kind_rate       100.0%  (threshold 80%; 3 rows)
  [PASS] isolation_403_rate    100.0%  (threshold 100%; 11 rows)
  [info] quote_support_rate      ...  (quoted words found in the tenant's corpus text; not a threshold - a Doc AI extraction and a pypdf mirror hyphenate differently)

  shape        rows   ok   pass
  lookup         34   34     33
  join           11   11      9
  refusal         8    8      8
  isolation      11   11     11
  version         1    1      1
  latency ms  p50   ...  p95   ...   (round trip, 65 rows)
  retrieve_ms p50   ...  p95   ...
  rerank_ms   p50   ...  p95   ...
  generate_ms p50   ...  p95   ...
  pool        avg   ...   semantic cache hits ...

  rows that cost a point (3):
    jn-03  join      acme    answered without ['45', '60'] | '45 days of the earned leave are encashed.'
    jn-09  join      acme    answered without ['8.33', 'twenty per cent'] | 'the minimum bonus is 8.33% of the salary or wage.'
    lk-27  lookup    acme    REFUSED conf=low cites=0 | What is the maximum rate of central tax the CGST Act allows?

  report: /home/YOU/cand173.json
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it.py

**HTML: The gate on both revisions / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the two reports).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
live  candidate  needs
  request_success_rate   100.0%     100.0%   100%
  answerable_rate         97.9%      97.9%    80%
  citation_rate          100.0%     100.0%    95%
  citation_valid_rate    100.0%     100.0%   100%
  must_contain_rate       97.8%      95.7%    85%
  correct_rate            95.7%      93.6%    68%
  refusal_rate           100.0%     100.0%    90%
  media_kind_rate        100.0%     100.0%    80%
  isolation_403_rate     100.0%     100.0%   100%
  jn-03: pass on live, fail on the candidate (answered without ['45', '60'])
  jn-06: fail on live, pass on the candidate (ok)
  jn-09: pass on live, fail on the candidate (answered without ['8.33', 'twenty per cent'])
  3 row(s) changed verdict; median round trip ... ms live, ... ms candidate
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_verdict.py

**HTML: The verdict and the delta / Do it: the verdict**

Do it: the verdict

Run instruction: bash — run in the operator shell, in the kit (the judge's venv from lesson 7.2: 65 answers from each revision, then Vertex AI Evaluation).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://documind-api-NUMBER.asia-south1.run.app
  65/65 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  65/65 candidate answers from https://candidate---documind-api-NUMBER.asia-south1.run.app
  context: 46/46 cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070:
    groundedness/mean                                1.000
    groundedness/mean[isolation]                     1.000
    groundedness/mean[join]                          1.000
    groundedness/mean[lookup]                        1.000
    groundedness/mean[refusal]                       1.000
    groundedness/mean[version]                       1.000
    groundedness/std                                 0.000
    instruction_following/mean                       4.877
    instruction_following/std                        0.600
    pairwise_question_answering_quality/baseline_model_win_rate 0.031
    pairwise_question_answering_quality/candidate_model_win_rate 0.015
    row_count                                        65.000

  the gate (run_eval.py) still decides; this judge explains. Where they disagree, read the row.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_the_delta.py

**HTML: The verdict and the delta / Do it: the delta**

The gates and the judge asked both revisions the same questions, so their usage rows are like for like. The cell prints make usage's model table, groups the rows by model, and prices the endpoint's rows at 1.5 times what they log.

Run instruction: bash — run in the operator shell, in the kit (reads the last two hours of usage rows).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
by model and backend (what answered, through which door)
model                 model_backend          answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------------------------------
gemini-3.6-flash      vertex                     130    952849    28030    1.6395    139.36    2100   0.00
projects/NUMBER/loca  vertex                     130    970907    17751    0.2694     22.89    1000   0.00

  live        130 answers  Rs 1.0720 an answer
  candidate   130 answers  Rs 0.1761 an answer as logged, Rs 0.2641 as Google bills it
the rupee delta: the tuned endpoint costs Rs 0.8079 less an answer, Rs 808 per 1,000 answers
  (the usage rows alone say Rs 0.8959: they log the endpoint at its base's rate)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_the_decision_and_the_candidate_s_tag.py

**HTML: The verdict and the delta / The decision, and the candidate's tag**

The decision is yours, and it reads the three results in order. The gate must pass. The judge says how often the tuned model gives the worse answer where the two differ. The delta says what that is worth at your volume. With a candidate that passes, there are three ways forward:

Run instruction: bash — run in the operator shell, in the kit (removes the candidate's address; the revision stays, with no traffic).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
the candidate URL now: HTTP 404
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

27 code windows mapped: 10 IDE demo files, 1 shared setup blocks, 16 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
