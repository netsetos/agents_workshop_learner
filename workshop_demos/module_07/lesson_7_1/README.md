# Lesson 7.1: Build a useful evaluation dataset

**Summary:** a new row accepted by the offline gate. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html); Git blob `085f18eff4b225ef3c249a8efd624fb5b739da9d`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it_the_gate_the_rows_that_cite_the_handbook_a.py](demo_03_01_do_it_the_gate_the_rows_that_cite_the_handbook_a.py) | bash — run in the operator shell, in the kit (the offline gate, then the rows that cite the handbook) |
| s3 · window 12 | [demo_03_02_do_it_the_gate_the_rows_that_cite_the_handbook_a.py](demo_03_02_do_it_the_gate_the_rows_that_cite_the_handbook_a.py) | bash — run in the operator shell, in the kit (reads the handbook and golden.jsonl; changes nothing) |
| s4 · window 16 | [demo_04_01_do_it_add_the_row_build_gate.py](demo_04_01_do_it_add_the_row_build_gate.py) | bash — run in the operator shell, in the kit (one line into evals/build_golden.py, then the build and the gate) |
| s4 · window 18 | [demo_04_02_what_the_gate_catches_and_the_one_mistake_it_can.py](demo_04_02_what_the_gate_catches_and_the_one_mistake_it_can.py) | bash — run in the operator shell, in the kit (six versions of the row, judged in memory; writes nothing) |
| s5 · window 23 | [demo_05_01_the_first_try_the_obvious_marker.py](demo_05_01_the_first_try_the_obvious_marker.py) | bash — run in the operator shell, in the kit (the isolation row, with the obvious marker) |
| s5 · window 25 | [demo_05_02_the_second_try_acme_s_phrase.py](demo_05_02_the_second_try_acme_s_phrase.py) | bash — run in the operator shell, in the kit (the same row with ACME's phrase as the marker, then the build and the gate) |
| s5 · window 27 | [demo_05_03_the_third_try_listed_and_the_gate_green.py](demo_05_03_the_third_try_listed_and_the_gate_green.py) | bash — run in the operator shell, in the kit (iso-11 listed in evals/required.json, then make eval) |
| s6 · window 31 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (three requests to the API; under a rupee) |
| s7 · window 34 | [demo_07_01_paraphrase_pairs.py](demo_07_01_paraphrase_pairs.py) | bash — run in the operator shell, in the kit (two lines appended to evals/paraphrases.jsonl, then the offline self-test) |
| s7 · window 39 | [demo_07_02_generated_candidates.py](demo_07_02_generated_candidates.py) | bash — run in the operator shell, in the kit (a candidate for SEC-09 as make-evalset writes one, judged in memory) |
| s8 · window 44 | [demo_08_01_keep_your_rows_and_give_the_kit_its_files_back.py](demo_08_01_keep_your_rows_and_give_the_kit_its_files_back.py) | bash — run in the operator shell, in the kit (your rows kept as a patch, the four files given back) |

## Conditional recovery

- [recover_07_01_generated_candidates.py](recover_07_01_generated_candidates.py) — bash — run in the operator shell, in the kit (one BigQuery count; ten Gemini calls only if the feed has rows)

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

### demo_03_01_do_it_the_gate_the_rows_that_cite_the_handbook_a.py

**HTML: The set as it stands: the gate, the rows that cite the handbook, and the clause no row asks about / Do it: the gate, the rows that cite the handbook, and the handbook's clauses**

The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3.

Run instruction: bash — run in the operator shell, in the kit (the offline gate, then the rows that cite the handbook).

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

### demo_03_02_do_it_the_gate_the_rows_that_cite_the_handbook_a.py

**HTML: The set as it stands: the gate, the rows that cite the handbook, and the clause no row asks about / Do it: the gate, the rows that cite the handbook, and the handbook's clauses**

The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3. Ten rows cite the handbook, by --source. Now count by clause. The cell reads the handbook's sections and lists, for each clause that is not filler, the ACME rows that anchor on it.

Run instruction: bash — run in the operator shell, in the kit (reads the handbook and golden.jsonl; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
hr_policy_2026.md: 282 sections, 272 of them GEN- filler
  NP-03      Notice period            lk-06 jn-02 jn-03 vr-01
  PB-02      Probation                lk-04 jn-01
  LV-01      Earned leave             lk-03 lk-07
  LV-07      Leave on exit            jn-01 jn-02 jn-03
  EXP-12     Travel reimbursement     lk-01
  PR-05      Payroll and Form 16      lk-02
  IT-SEC-04  Removable media          lk-05 jn-07
  SEC-09     Access review            <- no golden row asks about this clause
  FIN-02     Purchase approval        lk-08
  WFH-01     Remote work              lk-09
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_add_the_row_build_gate.py

**HTML: A lookup row: written into build_golden.py, built, and judged / Do it: add the row, build, gate**

The cell removes any earlier lk-32 line and inserts the row before the bracket that closes GOLDEN, so running it twice is harmless. The builder prints its first five lines and its last. make eval runs exactly the gate's line; calling it directly puts the exit code on a line of its own.

Run instruction: bash — run in the operator shell, in the kit (one line into evals/build_golden.py, then the build and the gate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
66 rows in GOLDEN; the last is lk-32
golden.jsonl
  rows : 66
  shape: isolation=11, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta
  every must_contain / must_retrieve verified against corpus/  OK
wrote 66 rows -> /home/you/deploy_module_rag/evals/golden.jsonl
== eval gate: OFFLINE (no credentials, no cost) ==
  66 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
exit code 0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_what_the_gate_catches_and_the_one_mistake_it_can.py

**HTML: A lookup row: written into build_golden.py, built, and judged / What the gate catches, and the one mistake it cannot see**

The next cell judges six versions of the row in memory, with the gate's own two functions. It writes nothing.

Run instruction: bash — run in the operator shell, in the kit (six versions of the row, judged in memory; writes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
as written                               accepted
a figure the clause never gives          REFUSED
    lk-32: must_contain '45 working days' is not in acme's corpus - the row can only fail
words the file breaks across two lines   REFUSED
    lk-32: must_contain 'disabled automatically' is not in acme's corpus - the row can only fail
a clause code with a typo                REFUSED
    lk-32: anchor 'SEC-9' matches nothing in acme's corpus (slug? clause id? typo?)
nothing the answer must contain          REFUSED
    lk-32: an answerable row with no must_contain accepts any answer at all
another clause's figure                  accepted
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_the_first_try_the_obvious_marker.py

**HTML: An isolation row: the marker that cannot work, the list it must join, and the gate green again / The first try: the obvious marker**

The first try: the obvious marker

Run instruction: bash — run in the operator shell, in the kit (the isolation row, with the obvious marker).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
67 rows in GOLDEN; the last is iso-11
golden.jsonl
  rows : 67
  shape: isolation=12, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta

  ASSERTIONS THAT DO NOT MATCH THE CORPUS:
   ! iso-11: must_not_contain '45 days' is in zeta's OWN corpus - answering it correctly would fail the row
exit code 1
66
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_the_second_try_acme_s_phrase.py

**HTML: An isolation row: the marker that cannot work, the list it must join, and the gate green again / The second try: ACME's phrase**

The second try: ACME's phrase

Run instruction: bash — run in the operator shell, in the kit (the same row with ACME's phrase as the marker, then the build and the gate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
67 rows in GOLDEN; the last is iso-11
golden.jsonl
  rows : 67
  shape: isolation=12, join=11, lookup=35, refusal=8, version=1
  tenants: acme, globex, zeta
  every must_contain / must_retrieve verified against corpus/  OK
wrote 67 rows -> /home/you/deploy_module_rag/evals/golden.jsonl
== eval gate: OFFLINE (no credentials, no cost) ==
  67 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [FAIL] coverage
         iso-11: a isolation row that required.json does not list

  1 problem(s). The golden set cannot judge the model until it judges itself.
exit code 1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_03_the_third_try_listed_and_the_gate_green.py

**HTML: An isolation row: the marker that cannot work, the list it must join, and the gate green again / The third try: listed, and the gate green**

The third try: listed, and the gate green

Run instruction: bash — run in the operator shell, in the kit (iso-11 listed in evals/required.json, then make eval).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
16 required ids: iso-01 iso-02 iso-03 iso-04 iso-05 iso-06 iso-07 iso-08 iso-09 iso-10 iso-11 mm-01 mm-02 mm-03 mm-04 vr-01
python evals/run_eval.py
== eval gate: OFFLINE (no credentials, no cost) ==
  67 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
exit code 0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: Ask the two rows once: the live half's own functions, and the outsider's 403 / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (three requests to the API; under a rupee).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lk-32 as acme: HTTP 200, answerable True, 1 citation(s), 2410 ms
   An account unused for 45 days is disabled automatically and must be re-approved to restore it [1].
   must_contain '45 days': found
   cites acme/hr_policy_2026.md
iso-11 as zeta: HTTP 200, answerable True, 1 citation(s), 2230 ms
   Earned leave is encashed on exit at basic pay, capped at 20 days [1].
   must_contain '20 days': found
   must_not_contain 'capped at 45 days': absent
   cites zeta/hr_policy_zeta_2026.md
iso-11 asked by documind-outsider-sa: HTTP 403 (the isolation gate requires 403)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_paraphrase_pairs.py

**HTML: Paraphrase pairs and generated candidates: two kinds of row that are not golden / Paraphrase pairs**

The answer cache of Module 9 serves an earlier answer when a new question's embedding has a cosine similarity of at least 0.95 with an earlier one. That number was chosen, not measured. paraphrases.jsonl is what measures it. Each pair rewords a golden question. A pair marked same asks the same fact in other words, so a cache hit would be right. A pair marked different is a few words away with a different answer: E3 against E2, minimum against maximum, probation against confirmed. A cache hit there is a wrong answer served fast. cache_threshold.py embeds both sides and prints, for each candidate threshold, the hit rate on the same pairs and the false-hit rate on the different ones. The cache stays off until a threshold has no false hit on this set. The labels are yours to get right: the self-test checks that each pair names a real golden row and differs from its question, not that its label is true. Add two pairs against lk-32. One asks the same fact in other words. The other asks the clause's other fact, the kind of near miss a loose threshold would answer with 45 days.

Run instruction: bash — run in the operator shell, in the kit (two lines appended to evals/paraphrases.jsonl, then the offline self-test).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
44 pairs; the last two are against lk-32
selftest OK - 44 pairs (25 same, 19 different) name real golden rows and differ from them; the curve counts hits and false hits per threshold; the recommendation is the lowest threshold with no false hit
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_generated_candidates.py

**HTML: Paraphrase pairs and generated candidates: two kinds of row that are not golden / Generated candidates**

make make-evalset asks Gemini for one question and answer per chunk of the quality-gated feed. The feed is rag_data.index_feed, joined to the chunks the worker mirrors into BigQuery, so a chunk the quality scan held back never becomes a question. Each pair is scanned by the one PII list, shared/pii.py, and dropped on any finding, never rewritten. What comes out is a candidate: a question with no figure it must contain, and the chunk's id as its only anchor. A golden row is a contract a person writes, and a generated question inherits the blind spots of the model that wrote it. So the file is golden_generated.jsonl, and the gate never reads it. What would the gate say if a candidate were merged as it is? The cell builds one for SEC-09 the way make_evalset.py writes it. Its chunk id is the worker's own: the tenant, the hash of the handbook's bytes, and #8, SEC-09's position after the preamble and seven clauses. Then the cell judges the reviewed version.

Run instruction: bash — run in the operator shell, in the kit (a candidate for SEC-09 as make-evalset writes one, judged in memory).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gen-001  REFUSED
    gen-001: an answerable row with no must_contain accepts any answer at all
    gen-001: anchor 'acme:497809ffbaa6...#8' matches nothing in acme's corpus (slug? clause id? typo?)
lk-32    accepted
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### recover_07_01_generated_candidates.py

**HTML: Paraphrase pairs and generated candidates: two kinds of row that are not golden / Generated candidates**

The candidate fails twice. It has no figure, so it would accept any answer. Its anchor names a version by its hash, which no file contains, and which would point at a retired version the day the handbook is re-issued. The reviewed row, with a figure, a code and a slug, is lk-32. That rewrite is what review means: a figure a person checked in the clause, and anchors that survive a new version. Last, the generator itself, if your feed has rows. The chunk feature job and the Dataplex quality scan fill the feed, and lesson 13.2 runs them (make features). Before that, the count is zero and the cell stops there.

Run instruction: bash — run in the operator shell, in the kit (one BigQuery count; ten Gemini calls only if the feed has rows).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
feed rows for acme: 0
no feed rows yet: lesson 13.2 builds the feed (make features)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_keep_your_rows_and_give_the_kit_its_files_back.py

**HTML: What rows cost, how a golden set rots, and handing the kit back / Keep your rows, and give the kit its files back**

Your clone now differs from the kit in four files. Lesson 7.2 runs the kit's own set, 65 rows and 15 required ids. The setup block's git pull --ff-only also refuses to run over local edits to a file the kit has changed. So keep your rows as a patch and restore the four files. git -C "$DEMO_ROOT" apply "$HOME/lesson71_rows.patch" brings them back whenever you want them.

Run instruction: bash — run in the operator shell, in the kit (your rows kept as a patch, the four files given back).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
evals/build_golden.py   | 2 ++
 evals/golden.jsonl      | 2 ++
 evals/paraphrases.jsonl | 2 ++
 evals/required.json     | 1 +
 4 files changed, 7 insertions(+)
the four files match the kit again
65
7
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

45 code windows mapped: 14 IDE demo files, 1 shared setup blocks, 30 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
