# Lesson 10.4: Compare the LangChain and ADK adapters

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_compare_adapters.py](demo_01_compare_adapters.py) | Run the LangChain and ADK adapters over the same tool contract. |
| 3 | [demo_02_four_brains_and_gate.py](demo_02_four_brains_and_gate.py) | Inspect the four deployed brains and run the module's actual gate. |
| 4 | [demo_03_costs_and_missing_observability.py](demo_03_costs_and_missing_observability.py) | Compare recorded cost lines and identify work those rows do not measure. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The deployed chat lane and access to the example models; adapters use a separate framework venv.

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

**`step_02_the_venv(session)` — Two adapters over one tool, side by side / Do it: the venv**

Do it: the venv

Operation: bash — run in the operator shell, in the kit (lesson 10.2's venv, with google-adk added).

Expected shape, not a promised result:

```text
graph-venv ok: google-adk 2.8.0 langchain 1.4.0
```

### demo_01_compare_adapters.py

Run the LangChain and ADK adapters over the same tool contract.

**`step_01_side_by_side(session)` — Two adapters over one tool, side by side / Do it: side by side**

Do it: side by side

Operation: bash — run in the operator shell, in the kit (the two adapters side by side; no model, no network beyond your machine).

Expected shape, not a promised result:

```text
1. what each model is shown for retrieve (* = required)
   langchain query*, doc_type, top_k                                465 characters
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

### demo_02_four_brains_and_gate.py

Inspect the four deployed brains and run the module's actual gate.

**`step_01_example(session)` — Four brains on /health, and the module's gate / Do it**

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

### demo_03_costs_and_missing_observability.py

Compare recorded cost lines and identify work those rows do not measure.

**`step_01_example(session)` — Four cost lines, as rag-api's rows draw them / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).

Expected shape, not a promised result:

```text
direct    1 retrieve()  in  2,561  out   68  Rs 0.3699
  langchain 1 retrieve()  in  2,498  out   64  Rs 0.3593
  langgraph 1 retrieve()  in  2,504  out   66  Rs 0.3613
  adk       1 retrieve()  in  2,537  out   71  Rs 0.3687
```

**`step_02_example(session)` — The half the rows cannot see / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted).

Expected shape, not a promised result:

```text
langchain 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  langgraph 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  adk       2 model calls  in  2,477  out    47 (thinking     0)  Rs 0.3458
the four cost lines, whole: the brain's own model calls + rag-api's, from step 5
  direct    Rs 0.0000 + Rs 0.3699 = Rs 0.3699
  langchain Rs 0.2147 + Rs 0.3593 = Rs 0.5740
  langgraph Rs 0.2147 + Rs 0.3613 = Rs 0.5760
  adk       Rs 0.3458 + Rs 0.3687 = Rs 0.7145
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_10.4_Adapters_WIX.html`. All 20 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `4d85e128644454856f18a930ac9e3dfcec8d55e1`.
