# Lesson 7.2: Separate offline checks, live scoring and LLM judgment

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_offline_gate_and_ci.py](demo_01_offline_gate_and_ci.py) | Run the offline gate and inspect the CI result for this kit commit. |
| 3 | [demo_02_live_gate_and_report.py](demo_02_live_gate_and_report.py) | Run the live gate, retain its actual exit code and inspect the row-level report. |
| 4 | [demo_03_judge_and_disagreements.py](demo_03_judge_and_disagreements.py) | Prepare the judge, run it on lane answers and compare disagreements/trajectory judgments. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The live deployed lane, the golden set, and the CI account/access needed by the source's optional CI inspection.

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

### demo_01_offline_gate_and_ci.py

Run the offline gate and inspect the CI result for this kit commit.

**`step_01_the_gate_as_ci_runs_it_and_ci_s_result_on(session)` — The offline half: on every push, and CI's verdict on the commit you run / Do it: the gate as CI runs it, and CI's result on your commit**

Do it: the gate as CI runs it, and CI's result on your commit

Operation: bash — run in the operator shell, in the kit (the offline half, as CI runs it).

Expected shape, not a promised result:

```text
python evals/run_eval.py
== eval gate: OFFLINE (no credentials, no cost) ==
  65 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
```

**`step_02_the_gate_as_ci_runs_it_and_ci_s_result_on(session)` — The offline half: on every push, and CI's verdict on the commit you run / Do it: the gate as CI runs it, and CI's result on your commit**

The next cell asks GitHub's public API which commits the dry run has judged, and marks the one your clone is at.

Operation: bash — run in the operator shell, in the kit (one unauthenticated call to GitHub's public API).

Expected shape, not a promised result:

```text
your kit is at b89bbd8
  b89bbd8  push  success  2026-09-23  <- the commit you run
  6999d24  push  success  2026-09-22
```

### demo_02_live_gate_and_report.py

Run the live gate, retain its actual exit code and inspect the row-level report.

**`step_01_the_live_gate_with_a_report(session)` — The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Do it: the live gate, with a report

Operation: bash — run in the operator shell, in the kit (every row as the member, every isolation row as the outsider: about ten minutes).

IDE adaptation: Retain the live gate's actual status and fresh structured report so the next functions can inspect a red result; missing reports remain errors.

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

  report: evals/reports/lesson72.json
  All thresholds met.
```

**`step_02_the_live_gate_with_a_report(session)` — The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point.

Operation: bash — run in the operator shell, in the kit (reads the report; changes nothing).

Expected shape, not a promised result:

```text
answerable_rate    46 answered          of 47 answerable rows
  must_contain_rate  45 with the figure   of 46 ANSWERED
  correct_rate       45 right             of 47 ANSWERABLE
  refusal_rate       18 refused           of 18 unanswerable rows
  pass  request_success_rate  100.0%  (needs 100%)
  pass  answerable_rate        97.9%  (needs 80%)
  pass  citation_rate         100.0%  (needs 95%)
  pass  citation_valid_rate   100.0%  (needs 100%)
  pass  must_contain_rate      97.8%  (needs 85%)
  pass  correct_rate           95.7%  (needs 68%)
  pass  refusal_rate          100.0%  (needs 90%)
  pass  media_kind_rate       100.0%  (needs 80%)
  pass  isolation_403_rate    100.0%  (needs 100%)
  cost a point: jn-06 (answered without ['EMEA', '11.4']), lk-27 (refused)
```

**`step_03_the_live_gate_with_a_report(session)` — The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point. Last, what the run cost. The API priced every answer on its usage row; make usage groups the last hour of those rows. Run it straight after the gate, before step 5 asks the lane again.

Operation: bash — run in the operator shell, in the kit (the usage rows of the last hour, priced).

Expected shape, not a promised result:

```text
65 answers from documind-api in the last 1 h; USD_INR=85

by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------
acme                        47       ...      ...       ...       ...     ...    ...
zeta                        10       ...      ...       ...       ...     ...    ...
globex                       8       ...      ...       ...       ...     ...    ...
```

### demo_03_judge_and_disagreements.py

Prepare the judge, run it on lane answers and compare disagreements/trajectory judgments.

**`step_01_the_judge_s_venv_and_its_self_test(session)` — The judge: the lane's own answers, read with the context they cite / Do it: the judge's venv and its self-test**

Do it: the judge's venv and its self-test

Operation: bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test).

Expected shape, not a promised result:

```text
selftest: the cited chunk's text replaces its quote as the context and a miss keeps the quote; the prompt the judge reads carries the context then the question; the frame carries the six judge columns plus the baseline; the trajectory maths is right on the three cases
```

**`step_02_the_judge_on_your_lane(session)` — The judge: the lane's own answers, read with the context they cite / Do it: the judge on your lane**

--reuse keeps the collected answers in a file. If the Evaluation step stops, the rerun judges the same answers without asking the lane again.

Operation: bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them).

Expected shape, not a promised result:

```text
>> https://documind-api-NUMBER.asia-south1.run.app
  65/65 answers collected from https://documind-api-NUMBER.asia-south1.run.app in ...s (model gemini-3.6-flash)
  context: .../... cited chunks read in full from the store
  trajectories: off (no --chat-url)
  pointwise: GROUNDEDNESS + INSTRUCTION_FOLLOWING  (templates cd7070; run api-GITSHA-YYYYMMDD-HHMM-tcd7070)
  pairwise: off (no --api-b)
  judge: the service default (pass --judge-model to pin one)

  Experiments run documind-eval/api-GITSHA-YYYYMMDD-HHMM-tcd7070:
    groundedness/mean                                ...
    groundedness/mean[isolation]                     ...
    groundedness/mean[join]                          ...
    groundedness/mean[lookup]                        ...
    groundedness/mean[refusal]                       ...
    groundedness/mean[version]                       ...
    groundedness/std                                 ...
    instruction_following/mean                       ...
    instruction_following/std                        ...
    row_count                                        65.000

  the gate (run_eval.py) still decides; this judge explains. Where they disagree, read the row.
```

**`step_03_where_the_gate_and_the_judge_disagree_read(session)` — Where the gate and the judge disagree: read the row / Where the gate and the judge disagree: read the row**

Four ways the two can meet, and the gate's misses read against the judge's answers. judge.py prints its summary and writes no per-row ratings, so "read the row" means reading the answers. The cell takes each row the gate failed and prints what the judge's own collection received for it.

Operation: bash — run in the operator shell, in the kit (reads both files; changes nothing).

Expected shape, not a promised result:

```text
2 row(s) cost the gate a point. The judge's own run answered them:
  jn-06  gate: answered without ['EMEA', '11.4']
         judge's answer: 'EMEA revenue fell in FY2026 [1].', 1 cited
         EMEA present; 11.4 absent
  lk-27  gate: refused
         judge's answer: 'The documents do not say.', 0 cited
         twenty per cent absent
```

**`step_04_the_judge_s_other_two_modes_trajectories_n(session)` — The judge's other two modes: trajectories now, pairwise in lesson 7.3 / The judge's other two modes: trajectories now, pairwise in lesson 7.3**

The chat service's tool calls against the one grounded path, and why the pairwise judge needs a candidate. With CHAT_URL, the judge sends a few answerable acme rows to each of the chat service's three brains, langchain, langgraph and adk. It compares the tool calls each brain returns with the reference path: one retrieve, then the answer. The three matches are computed in judge.py: exact, in order and any order. A brain that answers without retrieving scores 0 on all three, whatever its answer says. --no-vertex skips the Evaluation service, and --reuse skips asking the API again, so this costs only the chat turns.

Operation: bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise).

Expected shape, not a promised result:

```text
no documind-chat service on this lane: trajectories need one
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html`. All 40 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `035b7ce9098bd5e839d3c9896e605aacda3edf63`.
