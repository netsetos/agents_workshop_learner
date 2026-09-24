# Lesson 10.3: Diagnose tool arguments, access failures and timeouts

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_tool_failure_cases.py](demo_01_tool_failure_cases.py) | Exercise the five argument/refusal/budget/timeout failures in the actual harness. |
| 3 | [demo_02_chat_access_failures.py](demo_02_chat_access_failures.py) | Test access failures at the chat service's admission and identity gates. |
| 4 | [demo_03_unanswerable_arguments.py](demo_03_unanswerable_arguments.py) | Send an argument the corpus cannot satisfy and inspect its returned failure. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The deployed chat lane; the framework failure harness runs in its own lesson venv.

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

**`step_02_the_venv(session)` — Five failures through the kit's LangChain brain / Do it: the venv**

Do it: the venv

Operation: bash — run in the operator shell, in the kit (the venv from lesson 10.2, made if it is missing).

Expected shape, not a promised result:

```text
graph-venv ok: langchain 1.4.0
```

### demo_01_tool_failure_cases.py

Exercise the five argument/refusal/budget/timeout failures in the actual harness.

**`step_01_five_failures(session)` — Five failures through the kit's LangChain brain / Do it: five failures**

Do it: five failures

Operation: bash — run in the operator shell, in the kit (five failures through the kit's LangChain brain; no model, no network beyond your machine).

Expected shape, not a promised result:

```text
blocked     0.0 s  refusals ['delete_document']
              result [error] {"error": "delete_document requires manual approval"}
  bad args    0.0 s  refusals ['calculate_processing_cost']
              result [error] Error invoking tool 'calculate_processing_cost' with kwargs {'total_page
  no such     0.0 s  refusals ['summon_rain']
              result [error] Error: summon_rain is not a valid tool, try one of [retrieve, calculate_
  timed out   0.5 s  refusals []
              result [success] {"error": "document search is unavailable", "citations": [], "answerable
  over budget 0.0 s  refusals []
              result [success] {"num_documents": 1, "total_pages": 283, "processing_type": "priority", 
  the log lines, from the guard, the adapter and the one retrieve():
    WARNING refused delete_document (blocked list)
    INFO    calculate_processing_cost took 0.00s (budget 10s)
    INFO    summon_rain took 0.00s (budget 30s)
    WARNING retrieve failed: HTTPConnectionPool(host='127.0.0.1', port=PORT): Read timed out. (
    INFO    retrieve took 0.51s
    INFO    retrieve took 0.51s
    WARNING rag-api query failed: document retrieval is unavailable
    INFO    retrieve took 0.51s (budget 30s)
    WARNING calculate_processing_cost took 0.00s (budget 0s)
```

### demo_02_chat_access_failures.py

Test access failures at the chat service's admission and identity gates.

**`step_01_example(session)` — Access failures at the chat service's door / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (three identities at the chat service's door).

Expected shape, not a promised result:

```text
403  {"detail":"not a member of any tenant"}
  401  {"detail":"the bearer token carries no verified email"}
  200  {"answer":"Gratuity becomes payable after not less than five years of continuous service [1].","tool
```

### demo_03_unanswerable_arguments.py

Send an argument the corpus cannot satisfy and inspect its returned failure.

**`step_01_example(session)` — An argument the corpus cannot honour / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (one question with and without a doc_type filter, then rag-api's rows).

Expected shape, not a promised result:

```text
doc_type None     5 citations | answerable True | The total payable on invoice INV-2026-0412 is Rs 1,84,500 
  doc_type invoice  0 citations | answerable False | The corpus holds nothing near this question: no passage of
  pool 20  answerable True   backend vertex  Rs 0.2831
  pool  0  answerable False  backend none    Rs 0.0000
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.3-tool-failures/Netsetos_GCP_Capstone_10.3_Tool_Failures_WIX.html). All 18 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `8c8650c57c7da57795b534e5c7b86462f1357233`.
