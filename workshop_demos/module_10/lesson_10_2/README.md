# Lesson 10.2: Implement the main LangGraph workflow

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_inspect_langgraph.py](demo_01_inspect_langgraph.py) | Build and inspect the graph in its isolated framework environment. |
| 3 | [demo_02_force_refusal.py](demo_02_force_refusal.py) | Force the graph's refusal node and inspect its decision. |
| 4 | [demo_03_threads_and_delete_request.py](demo_03_threads_and_delete_request.py) | Compare one thread, a new thread and an unauthorized delete request. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The deployed chat lane from 10.1; framework dependencies are installed by this lesson's preparation.

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

**`step_02_the_venv(session)` — The graph, in a venv of its own / Do it: the venv**

Do it: the venv

Operation: bash — run in the operator shell, in the kit (a small venv with the chat image's LangChain pins; a minute or two).

Expected shape, not a promised result:

```text
graph-venv ok: langchain 1.4.0
```

### demo_01_inspect_langgraph.py

Build and inspect the graph in its isolated framework environment.

**`step_01_the_graph(session)` — The graph, in a venv of its own / Do it: the graph**

Do it: the graph

Operation: bash — run in the operator shell, in the kit (the kit's graph, built and listed; no network, no model).

Expected shape, not a promised result:

```text
nodes: __start__, agent, tools, refuse, __end__
  __start__ -> agent    
      agent -> __end__    (route decides)
      agent -> refuse     (route decides)
      agent -> tools      (route decides)
     refuse -> agent    
      tools -> agent
```

### demo_02_force_refusal.py

Force the graph's refusal node and inspect its decision.

**`step_01_example(session)` — The refuse node, forced to fire / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (three scripted turns through the kit's own graph; no network, no model).

Expected shape, not a promised result:

```text
plain    agent -> tools -> agent          tool_calls ['retrieve']  refusals []
           answer: After five years of continuous service [1].
  blocked  agent -> refuse -> agent         tool_calls ['delete_document']  refusals ['delete_document']
           error result for delete_document: {"error": "delete_document requires manual approval"}
           answer: I could not delete the invoice: deleting a document requires manual approval, so
  mixed    agent -> refuse -> agent         tool_calls ['retrieve', 'delete_document']  refusals ['retrieve', 'delete_document']
           error result for retrieve: {"error": "retrieve requires manual approval"}
           error result for delete_document: {"error": "delete_document requires manual approval"}
           answer: Nothing was done: that request needs manual approval.
```

### demo_03_threads_and_delete_request.py

Compare one thread, a new thread and an unauthorized delete request.

**`step_01_example(session)` — The graph on your lane: one thread, a new thread, and a request to delete / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (four turns to the LangGraph brain on your lane).

Expected shape, not a promised result:

```text
[lesson102] tool_calls ['retrieve']  refusals []  7310 ms
      Gratuity becomes payable after not less than five years of continuous service, under the Payment of Gratuity A
  [lesson102] tool_calls ['retrieve']  refusals []  6890 ms
      Under the Code on Social Security, 2020, a fixed-term employee is paid gratuity on a pro rata basis, without t
  [lesson102-new] tool_calls []  refusals []  2140 ms
      Could you tell me what you would like to know about? For example, gratuity or leave for fixed-term employees u
  [lesson102] tool_calls []  refusals []  1980 ms
      I can't delete documents - I can only search and read them. Removing the April invoice needs someone with acce
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.2-langgraph/Netsetos_GCP_Capstone_10.2_LangGraph_WIX.html). All 19 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `73498f3f2d62aedcf2bd29a83ca1c8a08c7fa43b`.
