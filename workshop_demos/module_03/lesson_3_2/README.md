# Lesson 3.2: Parse documents and compare chunk boundaries

**Summary:** 65 identical chunks from both chunkers. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html); Git blob `5b333c8a6d51ef5416793e5ae594068511fda01e`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_call_it_which_reader_does_your_lane_have.py](demo_03_01_call_it_which_reader_does_your_lane_have.py) | bash — run in the operator shell |
| s4 · window 12 | [demo_04_01_do_it_count_the_corpus_rs_0.py](demo_04_01_do_it_count_the_corpus_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s4 · window 14 | [demo_04_02_prove_it_on_the_lane_one_small_pdf_four_pages.py](demo_04_02_prove_it_on_the_lane_one_small_pdf_four_pages.py) | bash — run in the operator shell, in $DEMO_ROOT (costs about four pages of Document AI) |
| s5 · window 17 | [demo_05_01_do_it_cut_the_handbook_rs_0.py](demo_05_01_do_it_cut_the_handbook_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s5 · window 19 | [demo_05_02_read_it_on_the_lane.py](demo_05_02_read_it_on_the_lane.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 22 | [demo_06_01_do_it_cut_the_code_on_wages_rs_0.py](demo_06_01_do_it_cut_the_code_on_wages_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 24 | [demo_06_02_read_it_on_the_lane_and_ask_a_question_that_land.py](demo_06_02_read_it_on_the_lane_and_ask_a_question_that_land.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 25 | [demo_06_03_read_it_on_the_lane_and_ask_a_question_that_land.py](demo_06_03_read_it_on_the_lane_and_ask_a_question_that_land.py) | bash — run in the operator shell (acme pinned to vector, see the setup) |
| s7 · window 27 | [demo_07_01_see_it_page_by_page.py](demo_07_01_see_it_page_by_page.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |

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

### demo_03_01_call_it_which_reader_does_your_lane_have.py

**HTML: Parse: Document AI, chosen by residency / Call it: which reader does your lane have?**

Two read-only calls. The first prints the worker's environment, where the residency and the processor id live. The second asks the Document AI API to list the processors in each of the two possible locations; exactly one location will list documind-parser.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{'name': 'RESIDENCY', 'value': 'us'}
{'name': 'DOCAI_PROCESSOR_ID', 'value': 'a1b2c3d4e5f6a7b8'}
== us ==
documind-parser LAYOUT_PARSER_PROCESSOR ENABLED
== asia-south1 ==
(none)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_count_the_corpus_rs_0.py

**HTML: Count pages first: slices, and the 250-page line / Do it: count the corpus, Rs 0**

The same count, on the PDFs in your kit folder, with the same library. The cell prints pages and slices per PDF, then the totals and what one parse of the whole corpus would cost at each processor's list price - the rates as the course reads them on the pricing page, to re-verify before quoting.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme/cgst_act_2017.pdf                           pages= 236 slices= 16 inline
acme/code_on_social_security_2020.pdf            pages= 116 slices=  8 inline
acme/code_on_wages_2019.pdf                      pages=  29 slices=  2 inline
acme/maternity_benefit_amendment_act_2017.pdf    pages=   4 slices=  1 inline
acme/posh_act_2013.pdf                           pages=  13 slices=  1 inline
...
zeta/osh_code_2020.pdf                           pages=  86 slices=  6 inline

1065 pages in 79 Document AI requests
one full parse: OCR Rs 136   Layout Parser Rs 905
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_prove_it_on_the_lane_one_small_pdf_four_pages.py

**HTML: Count pages first: slices, and the 250-page line / Prove it on the lane: one small PDF, four pages**

The amendment Act is four pages and globex does not hold it, so ingesting it there is a fresh source, one Document AI request, and a few paise. Then read the worker's line for it, which carries the page count as pages.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (costs about four pages of Document AI).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
globex_e7a1c0...    4    5    5
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_cut_the_handbook_rs_0.py

**HTML: Chunk by section: the handbook becomes 283 clauses / Do it: cut the handbook, Rs 0**

Do it: cut the handbook, Rs 0

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
283 chunks from 282 headings
  preamble   section=None                               chars=   97  hash=903e2b39ee92
  NP-03      section=NP-03 — Notice period              chars=  234  hash=f4512754ae41
  PB-02      section=PB-02 — Probation                  chars=  212  hash=bb65ccc2494c
  LV-01      section=LV-01 — Earned leave               chars=  189  hash=ff463cede286
  LV-07      section=LV-07 — Leave on exit              chars=  167  hash=7b5538b88f78
sections windowed within themselves: []
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_read_it_on_the_lane.py

**HTML: Chunk by section: the handbook becomes 283 clauses / Read it on the lane**

The worker cut the same file with the same rule when the corpus was loaded. Its rows for the handbook should be the same 283 locators in the same order.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lane: 283 local: 283 same locators in the same order: True
same hashes: True
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_cut_the_code_on_wages_rs_0.py

**HTML: Chunk by window: an Act becomes page windows / Do it: cut the Code on Wages, Rs 0**

Your kit has a text mirror of every Act, made by pypdf when the corpus was fetched, with a form feed between pages. Cut the mirror of the Code on Wages and look at one seam.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
pages in the mirror: 29
65 windows; the first six locators: ['p1-0', 'p2-0', 'p2-1', 'p3-0', 'p3-1', 'p4-0']
p2-0 is 2000 chars; p2-1 is 1201 chars
end of p2-0 -> 'th or without the knowledge of the\nprincipal employer and includ'
start of p2-1 -> 'in or\nin connection with the work of an establishment when he'
the overlap: the last 200 characters of p2-0 reappear at the start of p2-1 -> True
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_read_it_on_the_lane_and_ask_a_question_that_land.py

**HTML: Chunk by window: an Act becomes page windows / Read it on the lane, and ask a question that lands on a page**

Read it on the lane, and ask a question that lands on a page

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_read_it_on_the_lane_and_ask_a_question_that_land.py

**HTML: Chunk by window: an Act becomes page windows / Read it on the lane, and ask a question that lands on a page**

Read it on the lane, and ask a question that lands on a page

Run instruction: bash — run in the operator shell (acme pinned to vector, see the setup).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
67 windows on the lane; first six: ['p1-0', 'p2-0', 'p2-1', 'p3-0', 'p3-1', 'p4-0']
pages seen: [1, 2, 3, 4, 5] ... 29
Under the Code on Wages, wages must be paid within seven days after the end of the wage period ... [Source 1]
19 code_on_wages_2019.pdf page 9 | (iv) monthly basis, before the expiry of the seventh day of the succ
20 code_on_wages_2019.pdf page 9 | ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_see_it_page_by_page.py

**HTML: Compare the boundaries: two parsers, one document / See it, page by page**

See it, page by page

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lane 67 windows, mirror 65 windows
pages with a different number of windows: [(7, 3, 2), (23, 3, 2)]
p2-0 on the lane: 2000 chars, hash 4c19e0b7a2d8
p2-0 in the mirror: 2000 chars, hash 6a3f7e9c01b5
lane text starts: 'THE CODE ON WAGES, 2019\nCHAPTER I\nPRELIMINARY\n1. (1) This Code may be called ...'
mirror text starts: 'THE CODE ON WAGES, 2019 CHAPTER I PRELIMINARY 1. (1) This Code may be called ...'
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

29 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 17 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
