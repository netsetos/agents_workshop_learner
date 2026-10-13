# Lesson 4.5: Check the LLM judge against people

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

The number after `demo_` is the visible HTML section number, not the demo count or Level number. Gaps mean the intervening section is reading/UI-only. Unnumbered HTML setup stays in `setup/prepare.py`. At lesson end, `setup/finish.py` runs the numbered cleanup sections and restores saved settings; completed cleanup sections are skipped.

| HTML section | File | What it demonstrates |
|---|---|---|
| setup | [setup/prepare.py](setup/prepare.py) | Before you run anything: set up the shell |
| 3 | [demo_03_label_the_frozen_rows_yourself_blind.py](demo_03_label_the_frozen_rows_yourself_blind.py) | Label the frozen rows yourself, blind |
| 4 | [demo_04_two_people_on_the_same_rows_cohen_s_kappa.py](demo_04_two_people_on_the_same_rows_cohen_s_kappa.py) | Two people on the same rows: Cohen's kappa |
| 5 | [demo_05_the_judge_on_the_same_rows_true_pass_false_pass_and_the_cut.py](demo_05_the_judge_on_the_same_rows_true_pass_false_pass_and_the_cut.py) | The judge on the same rows: true-pass, false-pass and the cut |
| 7 | [demo_07_kappa_by_hand_and_the_judge_s_own_reasons.py](demo_07_kappa_by_hand_and_the_judge_s_own_reasons.py) | Kappa by hand, and the judge's own reasons |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from a previous layout, run the lesson's finish file first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures. Old progress is never silently treated as completion of the new section files.

## Optional extensions

- [optional/demo_06_your_lane_s_judge_on_the_frozen_rows_optional.py](optional/demo_06_your_lane_s_judge_on_the_frozen_rows_optional.py) — Do it

## Finish and restore

- [setup/restore_settings.py](setup/restore_settings.py) — At lesson end: DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 2 compares the four stores; Module 7 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.
- [setup/finish.py](setup/finish.py) — Run the listed cleanup sections in order, even after a failure; retain evidence and restore saved settings.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 2 compares the four stores; Module 7 studies the mirrors.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 2 compares the four stores; Module 7 studies the mirrors.

Operation: bash — run in the operator shell now, before the lesson's first step.

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

### demo_03_label_the_frozen_rows_yourself_blind.py

Do it: your sheet Open evals/reports/judge_labels.csv in a spreadsheet or a text editor. For each row, read the context first, then the answer, then the question again, and write yes or no under both label columns. Write a note on any row you hesitate over, now: step 4 prints it beside the other reader's. Here is one filled row of the kit's fixture, as a sheet holds it: The answer refuses, so it claims nothing: grounded, yes. But the context holds the cap, so a refusal does not answer the question: no. The reader's note says why: "the cap is in the context". Save the sheet as CSV with every column kept and in the same order. A spreadsheet may add a byte-order mark, Windows line endings or a capitalised YES; the check reads all three. Then check it:

**`step_01_your_sheet(session)` — Label the frozen rows yourself, blind / Do it: your sheet**

Do it: your sheet

Operation: bash — run in the operator shell, in the kit (Rs 0: a blank sheet of the frozen rows for you; it never overwrites one).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.json]
```

**`step_02_your_sheet(session)` — Label the frozen rows yourself, blind / Do it: your sheet**

Open evals/reports/judge_labels.csv in a spreadsheet or a text editor. For each row, read the context first, then the answer, then the question again, and write yes or no under both label columns. Write a note on any row you hesitate over, now: step 4 prints it beside the other reader's. Here is one filled row of the kit's fixture, as a sheet holds it: The answer refuses, so it claims nothing: grounded, yes. But the context holds the cap, so a refusal does not answer the question: no. The reader's note says why: "the cap is in the context". Save the sheet as CSV with every column kept and in the same order. A spreadsheet may add a byte-order mark, Windows line endings or a capitalised YES; the check reads all three. Then check it:

Operation: bash — run in the operator shell, in the kit (Rs 0: holds a filled sheet to the frozen set).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.json]
```

### demo_04_two_people_on_the_same_rows_cohen_s_kappa.py

Do it: the worked table, and the kit's own tests Do it: you against the author, then the author against the peer

**`step_01_the_worked_table_and_the_kit_s_own_tests(session)` — Two people on the same rows: Cohen's kappa / Do it: the worked table, and the kit's own tests**

Do it: the worked table, and the kit's own tests

Operation: bash — run in the operator shell, in the kit (Rs 0: the worked table, then the kit's own tests of the arithmetic).

Expected shape, not a promised result:

```text
selftest: the worked table of 50 rows (20 both yes, 5 and 10 split, 15 both no) agrees on 35/50 = 70.0% [56.2%, 80.9%], 0.50 by chance, kappa 0.40; identical labels 1.00; one label throughout undefined; a reader with one label against one with two 0.00
Ran 18 tests in ...s

OK
```

**`step_02_you_against_the_author_then_the_author_aga(session)` — Two people on the same rows: Cohen's kappa / Do it: you against the author, then the author against the peer**

Do it: you against the author, then the author against the peer

Operation: bash — run in the operator shell, in the kit (Rs 0: two sheets, kappa per rubric).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.json]
```

### demo_05_the_judge_on_the_same_rows_true_pass_false_pass_and_the_cut.py

Do it: the judge against you, then against the author CUT=3 passes the second metric at 3 or more, and SWEEP=1 adds every cut from 1 to 5 under the two blocks, the current one marked. There is nothing to restore: a run without CUT is back at 4.

**`step_01_the_judge_against_you_then_against_the_aut(session)` — The judge on the same rows: true-pass, false-pass and the cut / Do it: the judge against you, then against the author**

Do it: the judge against you, then against the author

Operation: bash — run in the operator shell, in the kit (Rs 0: the judge's ratings of the same rows against one sheet).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.json]
```

**`step_02_change_it_move_the_cut(session)` — The judge on the same rows: true-pass, false-pass and the cut / Change it: move the cut**

CUT=3 passes the second metric at 3 or more, and SWEEP=1 adds every cut from 1 to 5 under the two blocks, the current one marked. There is nothing to restore: a run without CUT is back at 4.

Operation: bash — run in the operator shell, in the kit (Rs 0: the Change-it; nothing to restore, because CUT is not a setting).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.json]
```

### optional/demo_06_your_lane_s_judge_on_the_frozen_rows_optional.py

Do it

**`step_01_your_lane_s_judge_on_the_frozen_rows_optio(session)` — Your lane's judge on the frozen rows (optional) / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (optional: 40 Vertex AI Evaluation requests, two a row; nothing asked of the API).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_frozen.txt]
```

### demo_07_kappa_by_hand_and_the_judge_s_own_reasons.py

Two standard-library cells over the files themselves, with no kit function between you and the count. The first cell reads your sheet and the author's with Python's csv module, counts p_o and p_e by hand, and checks the result against the kit's cohen_kappa(). It is this lesson's arithmetic in a screenful, and it runs anywhere Python does. The first cell reads your sheet and the author's with Python's csv module, counts p_o and p_e by hand, and checks the result against the kit's cohen_kappa(). It is this lesson's arithmetic in a screenful, and it runs anywhere Python does. The second reads the judge's ratings file directly and prints each row where the judge and you disagree, with the judge's score and its own explanation. It is lesson 4.2's advice made concrete: where they disagree, read the row. It skips judge_agree.py's row_sha check, because both files come from the same frozen set.

**`step_01_kappa_by_hand_and_the_judge_s_own_reasons(session)` — Kappa by hand, and the judge's own reasons / Kappa by hand, and the judge's own reasons**

Two standard-library cells over the files themselves, with no kit function between you and the count. The first cell reads your sheet and the author's with Python's csv module, counts p_o and p_e by hand, and checks the result against the kit's cohen_kappa(). It is this lesson's arithmetic in a screenful, and it runs anywhere Python does.

Operation: bash — run in the operator shell, in the kit (a Python cell; Rs 0: it reads two sheets).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_labels.L1.csv]
```

**`step_02_kappa_by_hand_and_the_judge_s_own_reasons(session)` — Kappa by hand, and the judge's own reasons / Kappa by hand, and the judge's own reasons**

The first cell reads your sheet and the author's with Python's csv module, counts p_o and p_e by hand, and checks the result against the kit's cohen_kappa(). It is this lesson's arithmetic in a screenful, and it runs anywhere Python does. The second reads the judge's ratings file directly and prints each row where the judge and you disagree, with the judge's score and its own explanation. It is lesson 4.2's advice made concrete: where they disagree, read the row. It skips judge_agree.py's row_sha check, because both files come from the same frozen set.

Operation: bash — run in the operator shell, in the kit (a Python cell; Rs 0: it reads your sheet and the judge's ratings).

Expected shape, not a promised result:

```text
[awaiting the author's run: data/judge_set.ratings.jsonl]
```

### setup/restore_settings.py

At lesson end: DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 2 compares the four stores; Module 7 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 2 compares the four stores; Module 7 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

### setup/finish.py

Run the listed cleanup sections in order, even after a failure; retain evidence and restore saved settings.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_4.5_Judge_Vs_People_WIX.html`. All 44 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `7e8b44daf16b794b654f1785a85dbb416d542676`.

Source line numbers refer to the teaching HTML before generated IDE-link blocks. Use the numbered section anchor/heading to find the example in the rendered page; its link opens this same learner file.
