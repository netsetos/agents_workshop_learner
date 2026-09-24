# Lesson 7.3: Compare one controlled change against a baseline

**Summary:** a pairwise verdict and the rupee delta. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html); Git blob `26b60d600a32c21f22d0a2778fe03515b0235248`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it_the_candidate.py](demo_03_01_do_it_the_candidate.py) | bash — run in the operator shell, in the kit (a new revision with no traffic; nothing moves for users) |
| s3 · window 10 | [demo_03_02_do_it_prove_it_is_one_change.py](demo_03_02_do_it_prove_it_is_one_change.py) | bash — run in the operator shell, in the kit (reads both revisions; changes nothing) |
| s4 · window 14 | [demo_04_01_do_it_the_gate_on_the_live_revision_then_on_the.py](demo_04_01_do_it_the_gate_on_the_live_revision_then_on_the.py) | bash — run in the operator shell, in the kit (the 10 rows that cite the handbook, on each revision: a few minutes) |
| s4 · window 16 | [demo_04_02_do_it_the_gate_on_the_live_revision_then_on_the.py](demo_04_02_do_it_the_gate_on_the_live_revision_then_on_the.py) | bash — run in the operator shell, in the kit (reads the two reports; changes nothing) |
| s5 · window 21 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (twenty rows on each revision, then the Evaluation service) |
| s6 · window 24 | [demo_06_01_the_rupee_delta_from_the_usage_rows.py](demo_06_01_the_rupee_delta_from_the_usage_rows.py) | bash — run in the operator shell, in the kit (the last hour of usage rows, by model) |
| s8 · window 26 | [demo_08_01_do_it_remove_the_candidate_s_tag.py](demo_08_01_do_it_remove_the_candidate_s_tag.py) | bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed; the live revision is untouched) |

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

### demo_03_01_do_it_the_candidate.py

**HTML: The candidate: a new revision with no traffic, and the proof that one setting differs / Do it: the candidate**

Do it: the candidate

Run instruction: bash — run in the operator shell, in the kit (a new revision with no traffic; nothing moves for users).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.1-flash-lite|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|..." --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_prove_it_is_one_change.py

**HTML: The candidate: a new revision with no traffic, and the proof that one setting differs / Do it: prove it is one change**

The cell finds the revision serving traffic and the one tagged candidate, reads both revisions' settings, and prints every setting that differs.

Run instruction: bash — run in the operator shell, in the kit (reads both revisions; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
live documind-api-000NN-xxx   candidate documind-api-000NN-yyy
  GENERATOR_MODEL        gemini-3.6-flash           -> gemini-3.1-flash-lite
1 setting(s) differ
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_gate_on_the_live_revision_then_on_the.py

**HTML: The scoped gate on both revisions, and the rows that moved / Do it: the gate on the live revision, then on the candidate**

Do it: the gate on the live revision, then on the candidate

Run instruction: bash — run in the operator shell, in the kit (the 10 rows that cite the handbook, on each revision: a few minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://documind-api-NUMBER.asia-south1.run.app

  report: evals/reports/base73.json
  All thresholds met.
>> https://candidate---documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate       100.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 10 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 10 rows)
  [PASS] must_contain_rate      90.0%  (threshold 85%; 10 rows)
  [PASS] correct_rate           90.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  [ -- ] media_kind_rate         0.0%  (threshold 80%; no rows in scope; 0 rows)
  [ -- ] isolation_403_rate      0.0%  (threshold 100%; no rows in scope; 0 rows)
  [info] quote_support_rate      ...  (quoted words found in the tenant's corpus text; not a threshold - a Doc AI extraction and a pypdf mirror hyphenate differently)

  shape        rows   ok   pass
  lookup          9    9      8
  version         1    1      1
  latency ms  p50   ...  p95   ...   (round trip, 10 rows)
  retrieve_ms p50   ...  p95   ...
  rerank_ms   p50   ...  p95   ...
  generate_ms p50   ...  p95   ...
  pool        avg   ...   semantic cache hits ...

  rows that cost a point (1):
    lk-04  lookup    acme    answered without ['15'] | 'the documents cover this [1].'

  report: evals/reports/cand73.json
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_gate_on_the_live_revision_then_on_the.py

**HTML: The scoped gate on both revisions, and the rows that moved / Do it: the gate on the live revision, then on the candidate**

Now set the two reports side by side: each judged threshold on both revisions, every row whose verdict changed, and the median round trip of each.

Run instruction: bash — run in the operator shell, in the kit (reads the two reports; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
live  candidate  needs
  request_success_rate   100.0%     100.0%   100%
  answerable_rate        100.0%     100.0%    80%
  citation_rate          100.0%     100.0%    95%
  citation_valid_rate    100.0%     100.0%   100%
  must_contain_rate      100.0%      90.0%    85%
  correct_rate           100.0%      90.0%    68%
  lk-04: pass on live, fail on the candidate (answered without ['15'])
  1 row(s) changed verdict; median round trip ... ms live, ... ms candidate
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The pairwise judge: which answer is better, row by row / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (twenty rows on each revision, then the Evaluation service).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://documind-api-NUMBER.asia-south1.run.app
  20/20 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  20/20 candidate answers from https://candidate---documind-api-NUMBER.asia-south1.run.app
  context: .../... cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-vs-candidate-tcd7070:
    groundedness/mean                                ...
    groundedness/mean[join]                          ...
    groundedness/mean[lookup]                        ...
    groundedness/std                                 ...
    instruction_following/mean                       ...
    instruction_following/std                        ...
    pairwise_question_answering_quality/baseline_model_win_rate ...
    pairwise_question_answering_quality/candidate_model_win_rate ...
    row_count                                        20.000

  the gate (run_eval.py) still decides; this judge explains. Where they disagree, read the row.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_the_rupee_delta_from_the_usage_rows.py

**HTML: The rupee delta, from the usage rows / The rupee delta, from the usage rows**

Every answer of the last hour, grouped by the model that gave it, and the difference per answer. The API priced every answer on its usage row with cost.price(), at the rates of the model that answered. The gate's runs and the judge's collections asked both revisions the same questions, so the two groups are like for like. The cell groups the last hour's rows by model and divides.

Run instruction: bash — run in the operator shell, in the kit (the last hour of usage rows, by model).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gemini-3.6-flash          ... answers  Rs ...  Rs ... an answer
  gemini-3.1-flash-lite     ... answers  Rs ...  Rs ... an answer
  the candidate costs Rs ... less an answer: Rs ... per 1,000 answers
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_do_it_remove_the_candidate_s_tag.py

**HTML: Deciding, the confounds that fake a result, and removing the candidate / Do it: remove the candidate's tag**

This ends the experiment. The candidate revision stays in the service's history with no traffic and no URL. Removing the tag is not enough on its own: make promote refuses only when the tag points at another revision, and otherwise flips traffic to the revision named in .candidate-revision. Deleting that file makes make promote stop with an error instead.

Run instruction: bash — run in the operator shell, in the kit (the candidate's tag and its recorded name removed; the live revision is untouched).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
the candidate URL now: HTTP 404
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

27 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 17 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
