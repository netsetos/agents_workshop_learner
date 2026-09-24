# Lesson 9.2: Test cache scope, configuration changes and freshness

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_cache_state_and_scope.py](demo_01_cache_state_and_scope.py) | Inspect both caches and vary request scope while keeping question words fixed. |
| 3 | [demo_02_reissue_and_refresh.py](demo_02_reissue_and_refresh.py) | Release revision 2, observe both cache reactions and refresh the context cache. |
| 4 | [demo_03_undo_and_compare_rows.py](demo_03_undo_and_compare_rows.py) | Restore revision 1 and explain how old answers relate to the restored fingerprint. |

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

### demo_01_cache_state_and_scope.py

Inspect both caches and vary request scope while keeping question words fixed.

**`step_01_the_two_caches(session)` — Both caches, and the corpus they follow / Do it: the two caches**

Do it: the two caches

Operation: bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on).

Expected shape, not a promised result:

```text
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  cache projects/NUMBER/locations/global/cachedContents/CACHE_ID
  location global (global or regional: the answer to CLAUDE.md's question)
  model gemini-3.6-flash | tokens 41259 | expires YYYY-MM-DD HH:MM:SS.ssssss+00:00 | corpus 75b21a03f12f | ledger fingerprint 1ef46119bd89b143
  the next /v1/query for acme carries cached_content; read cached_tokens in its usage row
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=on|..."
...
>> candidate revision: documind-api-00045-tqm (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

**`step_02_the_state_and_three_asks(session)` — Both caches, and the corpus they follow / Do it: the state, and three asks**

Do it: the state, and three asks

Operation: bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks).

Expected shape, not a promised result:

```text
ledger 1ef46119bd89b143 (17 versions, last ingest_ok) | context cache packed from 1ef46119bd89b143: current
  vertex none     in  43109 cached  41259  2480 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2530 ms | A confirmed employee at grade E3 or above serves a
  cache  semantic in      0 cached      0   170 ms | A confirmed employee at grade E3 or above serves a
```

**`step_03_example(session)` — Scope: the same words under other settings / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes).

Expected shape, not a promised result:

```text
vertex none     in  43349 cached  41259  2610 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2440 ms | A confirmed employee at grade E3 or above serves a
  scope as asked   7a0875abc72b0f7b
  scope top_k 8    bcc480117460bf66
  scope kind: text 8d8d4a1d9912dc52
  scope prompt v4  1d409edacc15c1d1
```

### demo_02_reissue_and_refresh.py

Release revision 2, observe both cache reactions and refresh the context cache.

**`step_01_the_release(session)` — The corpus moves: revision 2, and both caches react / Do it: the release**

Do it: the release

Operation: bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release).

Expected shape, not a promised result:

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_5560308823a62dc8...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
```

**`step_02_the_state_both_asks_and_the_log(session)` — The corpus moves: revision 2, and both caches react / Do it: the state, both asks, and the log**

Do it: the state, both asks, and the log

Operation: bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines).

Expected shape, not a promised result:

```text
ledger 1441fb4775d21e13 (17 versions, last ingest_reactivated) | context cache packed from 1ef46119bd89b143: STALE
  vertex none     in   1880 cached      0  2390 ms | From 1 October 2026 the notice period for a confir
  vertex none     in   1880 cached      0  2455 ms | From 1 October 2026 the notice period for a confir
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13
```

**`step_03_example(session)` — make cache again: attached again, and what it packed / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the pack again, under the new fingerprint).

Expected shape, not a promised result:

```text
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  cache projects/NUMBER/locations/global/cachedContents/CACHE_ID
  location global (global or regional: the answer to CLAUDE.md's question)
  model gemini-3.6-flash | tokens 41259 | expires YYYY-MM-DD HH:MM:SS.ssssss+00:00 | corpus 75b21a03f12f | ledger fingerprint 1441fb4775d21e13
  the next /v1/query for acme carries cached_content; read cached_tokens in its usage row
  ledger 1441fb4775d21e13 (17 versions, last ingest_reactivated) | context cache packed from 1441fb4775d21e13: current
  vertex none     in  43139 cached  41259  2575 ms | From 1 October 2026 the notice period for a confir
```

### demo_03_undo_and_compare_rows.py

Restore revision 1 and explain how old answers relate to the restored fingerprint.

**`step_01_the_corpus_comes_back_version_1_and_the_ol(session)` — The corpus comes back: version 1, and the old answer with it / The corpus comes back: version 1, and the old answer with it**

Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

Operation: bash — run in the operator shell, in the kit (version 1's bytes again: the undo).

Expected shape, not a promised result:

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
```

**`step_02_the_corpus_comes_back_version_1_and_the_ol(session)` — The corpus comes back: version 1, and the old answer with it / The corpus comes back: version 1, and the old answer with it**

Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

Operation: bash — run in the operator shell, in the kit (the state, and the candidate's ask).

Expected shape, not a promised result:

```text
ledger 1ef46119bd89b143 (17 versions, last ingest_reactivated) | context cache packed from 1441fb4775d21e13: STALE
  cache  semantic in      0 cached      0   165 ms | A confirmed employee at grade E3 or above serves a
```

**`step_03_every_row_of_the_walk(session)` — The corpus comes back: version 1, and the old answer with it / Every row of the walk**

Every row of the walk

Operation: bash — run in the operator shell, in the kit (every acme usage row since the start; reads only).

Expected shape, not a promised result:

```text
00041-kqz  vertex  in  43109  cached  41259  Rs 1.0201   2480 ms
  00045-tqm  vertex  in  43109  cached  41259  Rs 1.0201   2530 ms
  00045-tqm  cache   in      0  cached      0  Rs 0.0000    170 ms
  00045-tqm  vertex  in  43349  cached  41259  Rs 1.0507   2610 ms
  00045-tqm  vertex  in  43109  cached  41259  Rs 1.0201   2440 ms
  00041-kqz  vertex  in   1880  cached      0  Rs 0.4978   2390 ms
  00045-tqm  vertex  in   1880  cached      0  Rs 0.4978   2455 ms
  00041-kqz  vertex  in  43139  cached  41259  Rs 1.0239   2575 ms
  00045-tqm  cache   in      0  cached      0  Rs 0.0000    165 ms
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_clean_up(session)` — The corpus comes back: version 1, and the old answer with it / Clean up**

Clean up

Operation: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted).

Expected shape, not a promised result:

```text
Updating traffic...done.
Done.
URL: https://documind-api-...run.app
Traffic:
  100% documind-api-00041-kqz      (the live revision, as before; no candidate tag)
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  deleted acme's cache
```

**`step_02_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html). All 31 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `11e9ef8b32dc608b3b9fcb57cae1cd8145b29fa7`.
