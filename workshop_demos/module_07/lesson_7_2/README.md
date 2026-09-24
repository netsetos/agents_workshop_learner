# Lesson 7.2: Separate offline checks, live scoring and LLM judgment

**Summary:** `make eval` green; live numbers; judge scores. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.2-live-judge/Netsetos_GCP_Capstone_7.2_Live_Judge_WIX.html); Git blob `035b7ce9098bd5e839d3c9896e605aacda3edf63`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py](demo_03_01_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py) | bash — run in the operator shell, in the kit (the offline half, as CI runs it) |
| s3 · window 10 | [demo_03_02_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py](demo_03_02_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py) | bash — run in the operator shell, in the kit (one unauthenticated call to GitHub's public API) |
| s4 · window 18 | [demo_04_01_do_it_the_live_gate_with_a_report.py](demo_04_01_do_it_the_live_gate_with_a_report.py) | bash — run in the operator shell, in the kit (every row as the member, every isolation row as the outsider: about ten minutes) |
| s4 · window 20 | [demo_04_02_do_it_the_live_gate_with_a_report.py](demo_04_02_do_it_the_live_gate_with_a_report.py) | bash — run in the operator shell, in the kit (reads the report; changes nothing) |
| s4 · window 22 | [demo_04_03_do_it_the_live_gate_with_a_report.py](demo_04_03_do_it_the_live_gate_with_a_report.py) | bash — run in the operator shell, in the kit (the usage rows of the last hour, priced) |
| s5 · window 31 | [demo_05_01_do_it_the_judge_s_venv_and_its_self_test.py](demo_05_01_do_it_the_judge_s_venv_and_its_self_test.py) | bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test) |
| s5 · window 33 | [demo_05_02_do_it_the_judge_on_your_lane.py](demo_05_02_do_it_the_judge_on_your_lane.py) | bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them) |
| s6 · window 35 | [demo_06_01_where_the_gate_and_the_judge_disagree_read_the_r.py](demo_06_01_where_the_gate_and_the_judge_disagree_read_the_r.py) | bash — run in the operator shell, in the kit (reads both files; changes nothing) |
| s7 · window 38 | [demo_07_01_the_judge_s_other_two_modes_trajectories_now_pai.py](demo_07_01_the_judge_s_other_two_modes_trajectories_now_pai.py) | bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise) |

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

### demo_03_01_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py

**HTML: The offline half: on every push, and CI's verdict on the commit you run / Do it: the gate as CI runs it, and CI's result on your commit**

Do it: the gate as CI runs it, and CI's result on your commit

Run instruction: bash — run in the operator shell, in the kit (the offline half, as CI runs it).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
python evals/run_eval.py
== eval gate: OFFLINE (no credentials, no cost) ==
  65 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_the_gate_as_ci_runs_it_and_ci_s_result_on.py

**HTML: The offline half: on every push, and CI's verdict on the commit you run / Do it: the gate as CI runs it, and CI's result on your commit**

The next cell asks GitHub's public API which commits the dry run has judged, and marks the one your clone is at.

Run instruction: bash — run in the operator shell, in the kit (one unauthenticated call to GitHub's public API).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
your kit is at b89bbd8
  b89bbd8  push  success  2026-09-23  <- the commit you run
  6999d24  push  success  2026-09-22
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_live_gate_with_a_report.py

**HTML: The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Do it: the live gate, with a report

Run instruction: bash — run in the operator shell, in the kit (every row as the member, every isolation row as the outsider: about ten minutes).

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

  report: evals/reports/lesson72.json
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_live_gate_with_a_report.py

**HTML: The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point.

Run instruction: bash — run in the operator shell, in the kit (reads the report; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_03_do_it_the_live_gate_with_a_report.py

**HTML: The live half: every row, two identities, nine rates, three exit codes / Do it: the live gate, with a report**

Now take the report apart. The cell recounts the four rates whose denominators people misread, from the report's own rows, then prints all nine with their verdicts and the rows that cost a point. Last, what the run cost. The API priced every answer on its usage row; make usage groups the last hour of those rows. Run it straight after the gate, before step 5 asks the lane again.

Run instruction: bash — run in the operator shell, in the kit (the usage rows of the last hour, priced).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
65 answers from documind-api in the last 1 h; USD_INR=85

by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
----------------------------------------------------------------------------------
acme                        47       ...      ...       ...       ...     ...    ...
zeta                        10       ...      ...       ...       ...     ...    ...
globex                       8       ...      ...       ...       ...     ...    ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_the_judge_s_venv_and_its_self_test.py

**HTML: The judge: the lane's own answers, read with the context they cite / Do it: the judge's venv and its self-test**

Do it: the judge's venv and its self-test

Run instruction: bash — run in the operator shell, in the kit (a second venv for the judge, then its offline self-test).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
selftest: the cited chunk's text replaces its quote as the context and a miss keeps the quote; the prompt the judge reads carries the context then the question; the frame carries the six judge columns plus the baseline; the trajectory maths is right on the three cases
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_the_judge_on_your_lane.py

**HTML: The judge: the lane's own answers, read with the context they cite / Do it: the judge on your lane**

--reuse keeps the collected answers in a file. If the Evaluation step stops, the rerun judges the same answers without asking the lane again.

Run instruction: bash — run in the operator shell, in the kit (the lane answers every row again, then Vertex AI Evaluation reads them).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_where_the_gate_and_the_judge_disagree_read_the_r.py

**HTML: Where the gate and the judge disagree: read the row / Where the gate and the judge disagree: read the row**

Four ways the two can meet, and the gate's misses read against the judge's answers. judge.py prints its summary and writes no per-row ratings, so "read the row" means reading the answers. The cell takes each row the gate failed and prints what the judge's own collection received for it.

Run instruction: bash — run in the operator shell, in the kit (reads both files; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
2 row(s) cost the gate a point. The judge's own run answered them:
  jn-06  gate: answered without ['EMEA', '11.4']
         judge's answer: 'EMEA revenue fell in FY2026 [1].', 1 cited
         EMEA present; 11.4 absent
  lk-27  gate: refused
         judge's answer: 'The documents do not say.', 0 cited
         twenty per cent absent
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_the_judge_s_other_two_modes_trajectories_now_pai.py

**HTML: The judge's other two modes: trajectories now, pairwise in lesson 7.3 / The judge's other two modes: trajectories now, pairwise in lesson 7.3**

The chat service's tool calls against the one grounded path, and why the pairwise judge needs a candidate. With CHAT_URL, the judge sends a few answerable acme rows to each of the chat service's three brains, langchain, langgraph and adk. It compares the tool calls each brain returns with the reference path: one retrieve, then the answer. The three matches are computed in judge.py: exact, in order and any order. A brain that answers without retrieving scores 0 on all three, whatever its answer says. --no-vertex skips the Evaluation service, and --reuse skips asking the API again, so this costs only the chat turns.

Run instruction: bash — run in the operator shell, in the kit (nine chat turns if your lane has the chat service; nothing otherwise).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
no documind-chat service on this lane: trajectories need one
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

40 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 28 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
