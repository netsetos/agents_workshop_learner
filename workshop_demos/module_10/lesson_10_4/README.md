# Lesson 10.4: Compare the LangChain and ADK adapters

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

The number after `demo_` is the visible HTML section number, not the demo count or Level number. Gaps mean the intervening section is reading/UI-only. Unnumbered HTML setup stays in `setup/prepare.py`. At lesson end, `setup/finish.py` runs the numbered cleanup sections and restores saved settings; completed cleanup sections are skipped.

| HTML section | File | What it demonstrates |
|---|---|---|
| setup | [setup/prepare.py](setup/prepare.py) | Before you run anything: set up the shell |
| 3 | [demo_03_two_adapters_over_one_tool_side_by_side.py](demo_03_two_adapters_over_one_tool_side_by_side.py) | Two adapters over one tool, side by side |
| 4 | [demo_04_four_brains_on_health_and_the_module_s_gate.py](demo_04_four_brains_on_health_and_the_module_s_gate.py) | Four brains on /health, and the module's gate |
| 5 | [demo_05_four_cost_lines_as_rag_api_s_rows_draw_them.py](demo_05_four_cost_lines_as_rag_api_s_rows_draw_them.py) | Four cost lines, as rag-api's rows draw them |
| 6 | [demo_06_the_half_the_rows_cannot_see.py](demo_06_the_half_the_rows_cannot_see.py) | The half the rows cannot see |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The deployed chat lane and access to the example models; adapters use a separate framework venv.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from a previous layout, run the lesson's finish file first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures. Old progress is never silently treated as completion of the new section files.

## Finish and restore

- [setup/restore_settings.py](setup/restore_settings.py) — At lesson end: DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.
- [setup/finish.py](setup/finish.py) — Run the listed cleanup sections in order, even after a failure; retain evidence and restore saved settings.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Operation: bash — run in the operator shell now, before the lesson's first step.

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

### demo_03_two_adapters_over_one_tool_side_by_side.py

Do it: the venv Do it: side by side

**`step_01_the_venv(session)` — Two adapters over one tool, side by side / Do it: the venv**

Do it: the venv

Operation: bash — run in the operator shell, in the kit (lesson 10.2's venv, with google-adk added).

Expected shape, not a promised result:

```text
graph-venv ok: google-adk 2.8.0 langchain 1.4.0
```

**`step_02_side_by_side(session)` — Two adapters over one tool, side by side / Do it: side by side**

Do it: side by side

Operation: bash — run in the operator shell, in the kit (the two adapters side by side; no model, no network beyond your machine).

Expected shape, not a promised result:

```text
1. what each model is shown for retrieve (* = required)
   langchain query*, doc_type, top_k                                481 characters
   adk       query*, tenant_id*, top_k, doc_type, assertion, brain  2,572 characters
   langchain tools: retrieve, calculate_processing_cost, get_usage_stats
   adk tools:       retrieve, calculate_processing_cost
2. one retrieve(); the ADK model writes tenant_id "globex" and assertion "anything"
   langchain rag-api got tenant acme, brain langchain, assertion header None
             the model read: citations, answerable, confidence
   adk       rag-api got tenant acme, brain adk, assertion header 'anything'
             the model read: citations, answerable, confidence, answer
3. three calls that go wrong
   delete_document(doc="x")
     langchain [error] {"error": "delete_document requires manual approval"}
               refusals ['delete_document']
     adk       the turn raises ValueError: Tool 'delete_document' not found.
   calculate_processing_cost(total_pages="many")
     langchain [error] Error invoking tool 'calculate_processing_cost' with kwargs
               {'total_pages': 'many'} with error: total_pages: Input should be a valid
               [...]
               refusals ['calculate_processing_cost']
     adk       the turn raises TypeError: '<=' not supported between instances of 'str' and
               'int'
   calculate_processing_cost(total_pages=10, processing_type="express")
     langchain [success] {"num_documents": 1, "total_pages": 10, "processing_type":
               "express", "rate_per_page": 0.05, "cost_usd": 0.5, "cost_inr": 42.5}
               refusals []
     adk       the turn raises ValueError: unknown tier 'express'; expected one of ['bulk',
               'priority', 'standard']
4. ADK's sessions with no CHECKPOINT_DSN: InMemorySessionService, at most 12 model calls a turn
```

### demo_04_four_brains_on_health_and_the_module_s_gate.py

Do it

**`step_01_four_brains_on_health_and_the_module_s_gat(session)` — Four brains on /health, and the module's gate / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (/health, then the module's gate).

Expected shape, not a promised result:

```text
{"status":"ok","profile":"gcp","brains":["langchain","langgraph","adk","direct"],"default_brain":"langchain"}
  DocuMind chat - live smoke test
  target: https://documind-chat-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] health  profile=gcp default=langchain
  [PASS] brain direct  3120 ms  tools=['retrieve']  'Gratuity becomes payable after not less than five years of c'
  [PASS] brain langchain  11840 ms  tools=['retrieve']  'Gratuity becomes payable once you have rendered at least fiv'
  [PASS] brain langgraph  9730 ms  tools=['retrieve']  'Gratuity is payable after at least five years of continuous '
  [PASS] brain adk  14260 ms  tools=['retrieve']  'After five years of continuous service, gratuity becomes pay'
  [PASS] outsider refused  status=403 not a member of any tenant
  --------------------------------------------------------
  6 passed, 0 failed
```

### demo_05_four_cost_lines_as_rag_api_s_rows_draw_them.py

Do it

**`step_01_four_cost_lines_as_rag_api_s_rows_draw_the(session)` — Four cost lines, as rag-api's rows draw them / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).

Expected shape, not a promised result:

```text
direct    1 retrieve()  in  2,561  out   68  Rs 0.3699
  langchain 1 retrieve()  in  2,498  out   64  Rs 0.3593
  langgraph 1 retrieve()  in  2,504  out   66  Rs 0.3613
  adk       1 retrieve()  in  2,537  out   71  Rs 0.3687
```

### demo_06_the_half_the_rows_cannot_see.py

Do it

**`step_01_the_half_the_rows_cannot_see(session)` — The half the rows cannot see / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted).

Expected shape, not a promised result:

```text
langchain 2 model calls  in  1,451  out    51 (thinking     0)  Rs 0.2175
  langgraph 2 model calls  in  1,451  out    51 (thinking     0)  Rs 0.2175
  adk       2 model calls  in  2,477  out    47 (thinking     0)  Rs 0.3458
the four cost lines, whole: the brain's own model calls + rag-api's, from step 5
  direct    Rs 0.0000 + Rs 0.3699 = Rs 0.3699
  langchain Rs 0.2175 + Rs 0.3593 = Rs 0.5768
  langgraph Rs 0.2175 + Rs 0.3613 = Rs 0.5788
  adk       Rs 0.3458 + Rs 0.3687 = Rs 0.7145
```

### setup/restore_settings.py

At lesson end: DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

### setup/finish.py

Run the listed cleanup sections in order, even after a failure; retain evidence and restore saved settings.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_10.4_Adapters_WIX.html`. All 20 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `f3598f8936669b98d54a99f356e98faea20a469a`.

Source line numbers refer to the teaching HTML before generated IDE-link blocks. Use the numbered section anchor/heading to find the example in the rendered page; its link opens this same learner file.
