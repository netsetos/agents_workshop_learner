# Lesson 4.2: Reindex a changed section and measure embedding reuse

**Summary:** `reused=281 embedded=2 retired=283`; the answer moves. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html); Git blob `04da291943e43a6795223f296f39e4dafd0a5d8c`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it_the_offline_gate_scoped_to_the_handbook_rs.py](demo_03_01_do_it_the_offline_gate_scoped_to_the_handbook_rs.py) | bash — run in the operator shell, in $DEMO_ROOT (no credentials, no cost) |
| s4 · window 13 | [demo_04_01_do_it_the_six_edits_through_the_worker_s_planner.py](demo_04_01_do_it_the_six_edits_through_the_worker_s_planner.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s5 · window 15 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in $DEMO_ROOT (writes the revision to your home directory, then one re-issue) |
| s6 · window 17 | [demo_06_01_read_the_three.py](demo_06_01_read_the_three.py) | bash — run in the operator shell (the ledger row from the API, then the claims and the vectors from Firestore) |
| s7 · window 21 | [demo_07_01_do_it_the_live_gate_red.py](demo_07_01_do_it_the_live_gate_red.py) | bash — run in the operator shell, in $DEMO_ROOT (ten questions; a few rupees) |
| s7 · window 23 | [demo_07_02_the_undo_then_the_gate_green.py](demo_07_02_the_undo_then_the_gate_green.py) | bash — run in the operator shell, in $DEMO_ROOT (the undo, then ten questions again) |

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

### demo_03_01_do_it_the_offline_gate_scoped_to_the_handbook_rs.py

**HTML: The gate: the golden set, scoped to one document / Do it: the offline gate, scoped to the handbook, Rs 0**

Do it: the offline gate, scoped to the handbook, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (no credentials, no cost).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
== eval gate: OFFLINE (no credentials, no cost) ==
  65 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.

  rows citing hr_policy_2026.md: 10 - the scoped live gate judges these
    lk-01  lookup    What is the per-trip cap on domestic travel reimbursement?
    lk-02  lookup    By when is Form 16 issued?
    lk-03  lookup    How many days of earned leave can I carry forward?
    lk-04  lookup    What notice period applies during probation?
    lk-05  lookup    Are USB drives allowed on a company laptop?
    lk-06  lookup    What is the notice period for a confirmed E3?
    lk-07  lookup    At what rate does earned leave accrue?
    lk-08  lookup    Who approves a purchase of Rs 3,00,000?
    lk-09  lookup    How many days a month can I work remotely?
    vr-01  version   What is the notice period for a confirmed E3?
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_six_edits_through_the_worker_s_planner.py

**HTML: Measure reuse: six kinds of edit, Rs 0 / Do it: the six edits through the worker's planner**

Do it: the six edits through the worker's planner

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
a figure in NP-03 (60 to 90)         chunks 283 -> 283  reused 282  embedded  1    234 chars  ['NP-03']
a figure in PB-02 (15 to 20)         chunks 283 -> 283  reused 282  embedded  1    212 chars  ['PB-02']
NP-03 re-wrapped (whitespace only)   chunks 283 -> 283  reused 283  embedded  0      0 chars  []
NP-03's heading renamed              chunks 283 -> 283  reused 282  embedded  1    250 chars  ['NP-03']
a clause inserted before PB-02       chunks 283 -> 284  reused 283  embedded  1     84 chars  ['NP-04']
NP-03 and PB-02 swapped              chunks 283 -> 283  reused 283  embedded  0      0 chars  []
wages: a sentence added on page 2    chunks  65 ->  65  reused  63  embedded  2   3261 chars  ['p2-0', 'p2-1']
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Do it: revision 3 of the handbook, on the lane / Do it**

Do it

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (writes the revision to your home directory, then one re-issue).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
/home/you/hr_policy_2026_rev3.md | version key acme_54337b4ba3f0...
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_ok	acme_54337b4ba3f0109a...	283	281	2	283	2026-11-01
>> retired (doc_keys, chunks, expire days): [u'acme_497809ffbaa603c4...']	283	30
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_read_the_three.py

**HTML: Inspect: the ledger row, the claims, the vectors / Read the three**

Read the three

Run instruction: bash — run in the operator shell (the ledger row from the API, then the claims and the vectors from Firestore).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme/hr_policy_2026.md chunks 283 reused 281 embedded 2 retired 283 effective 2026-11-01 text-embedding-005@1
3 claims (versions) for hr_policy_2026.md, oldest first
  acme_497809ff...  superseded chunks 283  reused 0  embedded 283  superseded_by acme_54337b4b...  reactivated once
  acme_55603088...  superseded chunks 283  reused 281  embedded 2  superseded_by acme_497809ff...
  acme_54337b4b...  indexed    chunks 283  reused 281  embedded 2
rows: 849 | current: 283 | retired: 566
  LV-01  current hash ff463cede286  version 1's hash ff463cede286  same vector: True
  NP-03  current hash 876232171dec  version 1's hash f4512754ae41  same vector: False
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_the_live_gate_red.py

**HTML: The gate goes red, and the two ways back to green / Do it: the live gate, red**

Ten questions to the API, each a generation call: a few rupees at most. The target mints two identity tokens, the UI's account as the member and the outsider's for the isolation rows, which is why it takes a moment to start.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (ten questions; a few rupees).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> https://documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate       100.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 10 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 10 rows)
  [FAIL] must_contain_rate      80.0%  (threshold 85%; 10 rows)
  [PASS] correct_rate           80.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  ...

  shape        rows   ok   pass
  lookup          9    9      8
  version         1    1      0
  latency ms  p50  2410  p95  3980   (round trip, 10 rows)

  rows that cost a point (2):
    lk-06  lookup    acme    missing '60' | What is the notice period for a confirmed E3?
    vr-01  version   acme    missing '60' | What is the notice period for a confirmed E3?

  required rows that did not pass (1) - each one blocks on its own:
    vr-01: missing '60'

  Blocked: must_contain_rate: 80% < 85%; required: 1 mandatory row(s) did not pass
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_the_undo_then_the_gate_green.py

**HTML: The gate goes red, and the two ways back to green / The undo, then the gate, green**

Version 1's bytes again, through the same release command. The offline gate passes, the upload lands, and the worker finds a version it has retired within the window: ingest_reactivated, nothing embedded, revision 3 retired in turn. The live gate then passes with the rows as they are.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the undo, then ten questions again).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
...
  [PASS] must_contain_rate     100.0%  (threshold 85%; 10 rows)
  ...
  shape        rows   ok   pass
  lookup          9    9      9
  version         1    1      1
  All thresholds met.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

26 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 17 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
