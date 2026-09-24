# Lesson 13.1: Debug a wrong answer through the complete pipeline

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_inspect_debugging_instruments.py](demo_01_inspect_debugging_instruments.py) | Read the available trace instruments and establish the question's baseline. |
| 3 | [demo_02_introduce_and_trace_wrong_answer.py](demo_02_introduce_and_trace_wrong_answer.py) | Introduce the lesson's version change and follow the resulting answer trace. |
| 4 | [demo_03_restore_and_verify_answer.py](demo_03_restore_and_verify_answer.py) | Put version 1 back and verify recovery through the same pipeline. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The original HR fixture; the controlled version change is undone before completion.

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

### demo_01_inspect_debugging_instruments.py

Read the available trace instruments and establish the question's baseline.

**`step_01_example(session)` — The trail, as the kit writes it down / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network).

Expected shape, not a promised result:

```text
the envelope on every answer, beyond the contract (schemas.py, RAGResponse):
  model, backend, cost_usd, tokens_in, tokens_out, cached_tokens, latency_ms, stages, cache_hit
stages, as query() fills them (main.py):
  generate_ms, graph_chunks, managed_chunks, policy_fallback, pool, rerank_fallback, rerank_ms, retrieval_backend, retrieve_ms, vector_chunks
found_by, the rung that put a chunk in the pool (retriever.py):
  firestore, graph, rag_engine, vector, vertex_search
GET /version, what is serving (main.py):
  model_backend, generator_model, prompt, retrieval_mode, retrieval_backend, retrieval_graph, graph_backend, embedding, retrieval_current_only, semantic_cache, git_sha
the events a degraded answer leaves in documind-api's log:
  routing_fallback         main.py:96
  retrieval_pin_ignored    main.py:135
  rag_engine_fallback      retriever.py:200
  rag_engine_fallback      retriever.py:212
  vertex_search_fallback   retriever.py:302
  vector_search_fallback   retriever.py:382
  rerank_fallback          retriever.py:503
  tier_exhausted           generator.py:304
  generation_truncated     generator.py:402
  tier_exhausted           generator.py:493
  cache_stale              cache_manager.py:119
```

**`step_02_example(session)` — A right answer, and its trail / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the question, the answer and its trail).

Expected shape, not a promised result:

```text
A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  [1] hr_policy_2026.md  version 497809ffbaa6  chunk 1  'serves a notice period of 60 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-before.json
```

### demo_02_introduce_and_trace_wrong_answer.py

Introduce the lesson's version change and follow the resulting answer trace.

**`step_01_example(session)` — Break it: a version reaches the lane / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (revision 2 re-issued, then the same question).

Expected shape, not a promised result:

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_5560308823a62dc8...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
From 1 October 2026, a confirmed employee at grade E3 or above serves a notice period of 90 days [1].
  [1] hr_policy_2026.md  version 5560308823a6  chunk 1  'serves a notice period of 90 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-after.json
```

**`step_02_the_trace(session)` — Trace it, name the cause, put it back / Do it: the trace**

Do it: the trace

Operation: bash — run in the operator shell, in the kit (the trace: reads only).

Expected shape, not a promised result:

```text
serving: COMMIT, gemini-3.6-flash via vertex, prompt documind-rag@v3, text-embedding-005@1, current-only off, answer cache off
events since the break: none
the trail of ~/ask131-after.json, in the order the answer was made:
  1 the answer cache         clean  cache_hit none: retrieval ran
  2 the store and its rungs  clean  vector: 20 of the pool's 20 from its own index; no fallback event
  3 the pool                 clean  20 of the 20 the ablation decided
  4 the reranker             clean  the Ranking API ordered the pool
  5 the version              OFF    acme/hr_policy_2026.md: the ledger's current since 2026-09-23T10:41 is 5560308823a6, not the golden set's 497809ffbaa6; it declares effective_from 2026-10-01
  6 the model                clean  answered from 1 citation; groundedness is make judge's
CAUSE: a version (link 5) - every link before it is clean
```

**`step_03_the_versions_view_and_the_two_probes(session)` — Trace it, name the cause, put it back / Do it: the versions view and the two probes**

Do it: the versions view and the two probes

Operation: bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only).

Expected shape, not a promised result:

```text
source                                       status                  gen chunks reused embed retired effective  embedding              indexed_at
acme/hr_policy_2026.md                       indexed    1758624067215604    283    283     0     283 -          text-embedding-005@1   2026-09-23T10:41:07
Project: documind-ai-YOUR-ID (NUMBER)
Terraform index: projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
Terraform endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321
API index: projects/NUMBER/locations/asia-south1/indexes/1234567890123456789
API endpoint: projects/NUMBER/locations/asia-south1/indexEndpoints/9876543210987654321
Index dimensions: 768; update method: STREAM_UPDATE
Global vector count: 1745
Deployment: documind_chunks_v1
Deployment sync time: 2026-09-23T10:42:18.000Z
PASS: the expected index is attached to the expected endpoint.
This verifies attachment and configuration; ingestion and query checks are separate.
{"project": "documind-ai-YOUR-ID", "collection": "chunks", "source_uri": "gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md", "source_status": "indexed", "source_doc_key": "acme_5560308823a62dc812a39ca44b777bd73ccd12146b02f1f9506a3d15ed208c71"}
STOP: HR source ledger does not match the selected local HR file; review the source version.
```

### demo_03_restore_and_verify_answer.py

Put version 1 back and verify recovery through the same pipeline.

**`step_01_put_version_1_back(session)` — Trace it, name the cause, put it back / Do it: put version 1 back**

Do it: put version 1 back

Operation: bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again).

Expected shape, not a promised result:

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  [1] hr_policy_2026.md  version 497809ffbaa6  chunk 1  'serves a notice period of 60 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-restored.json
PASS: both Firestore filter modes verified. Evidence: operator-evidence/firestore-combined-filters.json
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html). All 21 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `c7abb19efcfadcbf3543f389b135fca680b1166c`.
