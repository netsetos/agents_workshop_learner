# Lesson 15.1: Build graph evidence from source documents

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_graph_contracts.py](demo_01_graph_contracts.py) | Read graph evidence and the code that derives it from source documents. |
| 3 | [demo_02_build_and_inspect_graph.py](demo_02_build_and_inspect_graph.py) | Build the graph and inspect its nodes/edges against the source material. |
| 4 | [demo_03_graph_retrieval.py](demo_03_graph_retrieval.py) | Run the lane's graph retrieval example and inspect the evidence. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

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

### demo_01_graph_contracts.py

Read graph evidence and the code that derives it from source documents.

**`step_01_example(session)` — The rules, run / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the rules, run; no model, no network).

Expected shape, not a promised result:

```text
extraction: gemini-3.1-flash-lite, entity types person, org, product, policy, system, location, date
resolution: normalise(), then text-embedding-005 cosine >= 0.92
  normalise('ACME Pvt. Ltd.'        ) = 'acme'
  normalise('Acme Private Limited'  ) = 'acme'
  normalise('ACME Inc'              ) = 'acme'
  normalise('function head'         ) = 'function head'
  normalise('Function Head'         ) = 'function head'
  normalise('CFO'                   ) = 'cfo'
  normalise('Chief Financial Officer') = 'chief financial officer'
resolve_entities(), with an embedding that tells every name apart:
  'ACME Pvt. Ltd.'         -> 'ACME Pvt. Ltd.'
  'Acme Private Limited'   -> 'ACME Pvt. Ltd.'
  'ACME Inc'               -> 'ACME Pvt. Ltd.'
  'function head'          -> 'function head'
  'Function Head'          -> 'function head'
  'CFO'                    -> 'CFO'
  'Chief Financial Officer' -> 'Chief Financial Officer'
build_graph() on two passages:
  node 'CFO'                    person  id f3f1496ddec9...  cited by ['c1']
  node 'Purchase approval'      policy  id 36787430c7d6...  cited by ['c1']
  node 'Travel reimbursement'   policy  id 0cbc68db5bda...  cited by ['c2']
  node 'function head'          person  id b4468c254418...  cited by ['c1', 'c2']
  edge CFO -[APPROVES]-> Purchase approval  from c1, confidence 0.9
  edge function head -[APPROVES]-> Travel reimbursement  from c2, confidence 0.9
  2 relations dropped: 'board' is no entity (dangling), and Function Head -[IS]-> itself
```

### demo_02_build_and_inspect_graph.py

Build the graph and inspect its nodes/edges against the source material.

**`step_01_example(session)` — Build the handbook's graph / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build).

Expected shape, not a promised result:

```text
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --dry-run
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --rebuild
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 11}
tenant acme: 0 graph_edges deleted
tenant acme: 0 graph_nodes deleted
25 nodes, 15 edges written for tenant acme (Firestore)
{"event": "graph_built", "tenant": "acme", "backend": "firestore", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
```

**`step_02_example(session)` — Read it back: the counts, and one edge with its source / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (reads only).

Expected shape, not a promised result:

```text
tenant acme: 25 nodes, 15 edges in Firestore
the nodes the most chunks cite:
  Earned leave                     policy  3 chunk(s)
  Notice period                    policy  2 chunk(s)
  function head                    person  2 chunk(s)
  probation                        policy  2 chunk(s)
one edge, read back with its source chunk:
  CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval   confidence 0.9
  stated in acme:497809ffbaa6...#9 (FIN-02, hr_policy_2026.md):
    FIN-02 — Purchase approval
    Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
    approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  both names in the passage as written: CFO yes, Purchase approval yes
```

### demo_03_graph_retrieval.py

Run the lane's graph retrieval example and inspect the evidence.

**`step_01_example(session)` — Audit an extraction, and build again / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (one extraction against its passage; then the build again).

Expected shape, not a promised result:

```text
the extraction cached for FIN-02 (gemini-3.1-flash-lite), beside its passage:
  | FIN-02 — Purchase approval
  | Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
  | approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  entity   'Purchase approval'    policy  in the passage as written
  entity   'function head'        person  in the passage as written
  entity   'CFO'                  person  in the passage as written
  relation function head -[APPROVES_UP_TO_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
  relation CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
3 of 3 entity names are in the passage as written; 11 extractions cached for acme
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 0}
25 nodes, 15 edges written for tenant acme (Firestore)
{"event": "graph_built", "tenant": "acme", "backend": "firestore", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html`. All 17 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `d74daf0dbbc7f95660f0a56970362cc9c013c26a`.
