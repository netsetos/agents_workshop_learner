# Lesson 13.1: Debug a wrong answer through the complete pipeline

**Summary:** a wrong answer traced to its cause. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.1-debug-wrong-answer/Netsetos_GCP_Capstone_13.1_Debug_Wrong_Answer_WIX.html); Git blob `c7abb19efcfadcbf3543f389b135fca680b1166c`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network) |
| s4 · window 11 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the question, the answer and its trail) |
| s5 · window 13 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (revision 2 re-issued, then the same question) |
| s6 · window 15 | [demo_06_01_do_it_the_trace.py](demo_06_01_do_it_the_trace.py) | bash — run in the operator shell, in the kit (the trace: reads only) |
| s6 · window 17 | [demo_06_02_do_it_the_versions_view_and_the_two_probes.py](demo_06_02_do_it_the_versions_view_and_the_two_probes.py) | bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only) |
| s6 · window 20 | [demo_06_03_do_it_put_version_1_back.py](demo_06_03_do_it_put_version_1_back.py) | bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again) |

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

### demo_03_01_do_it.py

**HTML: The trail, as the kit writes it down / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the trail as the kit writes it down; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: A right answer, and its trail / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the question, the answer and its trail).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  [1] hr_policy_2026.md  version 497809ffbaa6  chunk 1  'serves a notice period of 60 days'
  cache_hit none | backend vertex | answerable True
  store vector | vector_chunks 20 | pool 20 | rerank_fallback 0 | policy_fallback 0
  kept in ~/ask131-before.json
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Break it: a version reaches the lane / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (revision 2 re-issued, then the same question).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_trace.py

**HTML: Trace it, name the cause, put it back / Do it: the trace**

Do it: the trace

Run instruction: bash — run in the operator shell, in the kit (the trace: reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_the_versions_view_and_the_two_probes.py

**HTML: Trace it, name the cause, put it back / Do it: the versions view and the two probes**

Do it: the versions view and the two probes

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the versions view and the two probes; reads only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_do_it_put_version_1_back.py

**HTML: Trace it, name the cause, put it back / Do it: put version 1 back**

Do it: put version 1 back

Run instruction: bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

21 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 12 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
