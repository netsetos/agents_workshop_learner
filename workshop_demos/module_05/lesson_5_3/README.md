# Lesson 5.3: Rerank and inspect retrieved candidates

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_answer_pool_and_reranker.py](demo_01_answer_pool_and_reranker.py) | Compare top_k answers, then reconstruct and rerank their candidate pool. |
| 3 | [demo_02_fallback_and_stage_latency.py](demo_02_fallback_and_stage_latency.py) | Run the saved-pool fallback, force a candidate timeout and inspect usage rows. |
| 4 | [demo_03_retrieval_origins_and_packing.py](demo_03_retrieval_origins_and_packing.py) | Join citations to retrieval origins, run smoke and inspect the packed evidence set. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The loaded HR/PDF corpus and Ranking API access. Saved answer/pool files are produced in this lesson.

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

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine. Temporarily disable an enabled answer cache for this retrieval/generation experiment and save its prior value. This changes the shared API; finish restores it. Cache lessons in Module 9 are unaffected.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

**`step_02_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index endpoint and the deployed index are for step 4's pool; the reranker's settings say what the API is running with, and an empty value means the setting's default. Step 4's rank call and the in-process calls in steps 5 and 7 need the API's Ranking client in the venv at the API's own pin; the pip line is harmless if it is already there. A name the service does not set is unset here rather than exported empty, because the kit's settings class reads an empty variable as a value, not as an absence, and a cell that imports the kit would refuse it.

Operation: bash — run in the operator shell, once per shell.

IDE adaptation: Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape, not a promised result:

```text
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
backend: vector  mode: dense (default)  top_k_retrieve: 20 (default)
rerank timeout: 5.0 (default)  answer cache: off (default)
```

### demo_01_answer_pool_and_reranker.py

Compare top_k answers, then reconstruct and rerank their candidate pool.

**`step_01_the_same_question_at_top_k_5_and_top_k_20(session)` — One answer, read end to end: the citations, their scores, the stages / Do it: the same question at top_k 5 and top_k 20**

The cell asks the notice-period question twice and prints, for each answer, the stages block on one line and every citation with its score, its chunk position, its source and the start of its quote. The second answer offers the model twenty chunks instead of five.

Operation: bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees).

IDE adaptation: Reject semantic-cache hits or a fallback-only pool before comparing top_k/reranker behavior.

Expected shape, not a promised result:

```text
top_k 5: pool 20 | from the index 20 | retrieve 6xx + rerank 3xx + generate 17xx ms of 28xx | rerank_fallback 0 | cache_hit none
   3 citations: the sources the model used, in the order it used them; [N] in the answer is the packed position
   [1] score 0.9xxx  #  1  hr_policy_2026.md          p.-  'NP-03 ...'
   [2] score 0.8xxx  #  4  hr_policy_2026.md          p.-  '...'
   [3] score 0.6xxx  #  2  hr_policy_2026.md          p.-  '...'
   sorted by score, the ranker's order among them: ['#1', '#4', '#2']

top_k 20: pool 20 | from the index 20 | retrieve 6xx + rerank 3xx + generate 3xxx ms of 4xxx | rerank_fallback 0 | cache_hit none
   4 citations: ...
   sorted by score, the ranker's order among them: ['#1', '#4', '#2', '#7']

saved /tmp/ans53_5.json and /tmp/ans53_20.json for steps 4, 7 and 8
```

**`step_02_embed_pool_rank_compare(session)` — The Ranking API by hand: the API's pool, the API's request, the API's order / Do it: embed, pool, rank, compare**

Do it: embed, pool, rank, compare

Operation: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding and one rank request, well under a rupee).

Expected shape, not a promised result:

```text
pool: 20 current ids from the index in 9xx ms, every one found_by vector
ranker: 20 of 20 back in 2xx ms, 20 records sent, model semantic-ranker-fast-004
   rank 1  score 0.9xxx  pool # 1  NP-03     hr_policy_2026.md
   rank 2  score 0.xxxx  pool # x  ...       hr_policy_2026.md
   ...
the API's cited ids, by score: ['#1', '#4', '#2'] | by hand, first 5: ['#1', '#4', '#2', '#7', '#3']
every citation is in the by-hand top 5: True | in the same relative order: True
saved /tmp/pool53.json for steps 5, 7 and 8
```

### demo_02_fallback_and_stage_latency.py

Run the saved-pool fallback, force a candidate timeout and inspect usage rows.

**`step_01_offline_the_kit_s_fallback_on_the_pool_you(session)` — The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, offline: the kit's fallback on the pool you saved**

Do it, offline: the kit's fallback on the pool you saved

Operation: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).

Expected shape, not a promised result:

```text
rerank_fell_back: True | every chunk marked: True
the pool by retrieval score, what the caller gets while the ranker is down:
   score 0.7xxx  pool # 1  NP-03     hr_policy_2026.md
   score 0.7xxx  pool # 2  ...       hr_policy_2026.md
   ...
the ranker's five (step 4): ['NP-03', '...', '...', '...', '...']
kept by the fallback: x of 5 | first is the same: True
```

**`step_02_on_a_candidate_a_deadline_no_call_can_meet(session)` — The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, on a candidate: a deadline no call can meet**

Do it, on a candidate: a deadline no call can meet

Operation: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read).

Expected shape, not a promised result:

```text
candidate: rerank_fallback 1 | rerank_ms 1x | pool 20 | answerable True
   score 0.7xxx  #1  hr_policy_2026.md
   score 0.7xxx  #4  hr_policy_2026.md
   score 0.6xxx  #2  hr_policy_2026.md
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	DeadlineExceeded
```

**`step_03_on_a_candidate_a_deadline_no_call_can_meet(session)` — The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, on a candidate: a deadline no call can meet**

Do it, on a candidate: a deadline no call can meet

Operation: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live service asked once).

Expected shape, not a promised result:

```text
live: rerank_fallback 0 | rerank_ms 3xx | first score 0.9xxx
100;documind-api-00044-xyz
```

**`step_04_the_selftest_then_the_lane_s_last_day_then(session)` — make usage: where the time went, p95 per stage, and the view behind it / Do it: the selftest, then the lane's last day, then its rows into the reader**

Do it: the selftest, then the lane's last day, then its rows into the reader

Operation: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the selftest touches nothing, and reading the log is free).

Expected shape, not a promised result:

```text
selftest: by tenant
tenant                 answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
zeta                         1      1500      120    0.0332      2.82    5200   0.00
acme                         2      3800      450    0.0091      0.77    1400   0.50

selftest: where the time went (p95 per stage, by tenant)
tenant                 answers  p95 ms  retrieve  rerank  generate   pool
-------------------------------------------------------------------------
zeta                         1    5200       200     120      4800   20.0
acme                         2    1400       220     130       990   20.0

selftest OK - grouped like tenant_daily: dearest tenant first, tokens summed, p95 the 95th latency, unanswerable a rate, p95 per stage and the pool beside it
```

**`step_05_the_selftest_then_the_lane_s_last_day_then(session)` — make usage: where the time went, p95 per stage, and the view behind it / Do it: the selftest, then the lane's last day, then its rows into the reader**

Do it: the selftest, then the lane's last day, then its rows into the reader

Operation: bash — run in the operator shell (the rows themselves, one JSON line each, for the reader in step 1).

Expected shape, not a promised result:

```text
NN rows; 1 with rerank_fallback 1; 0 with an empty pool
{"event": "query", "tenant": "acme", "user": "documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com", "tokens_in": xxxx.0, "tokens_out": xxx.0, "cached_tokens": 0.0, "cost_usd": 0.00xxxx, "latency_ms": 2xxx.0, "answerable": true, "retrieve_ms": 6xx.0, "rerank_ms": 3xx.0, "generate_ms": 1xxx.0, "pool": 20.0, "rerank_fallback": 0.0, ...
```

### demo_03_retrieval_origins_and_packing.py

Join citations to retrieval origins, run smoke and inspect the packed evidence set.

**`step_01_the_join_then_the_kit_s_own_retrieval_in_y(session)` — found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Operation: bash — run in the operator shell (a Python cell; Rs 0: two files on disk).

Expected shape, not a promised result:

```text
the answer's counts: pool 20 | vector_chunks 20 | graph_chunks 0 | managed_chunks 0 | retrieval_backend vector
a citation's fields: ['chunk_id', 'end', 'kind', 'media_url', 'page', 'quote', 'score', 'source_uri', 'start']
   #  1 hr_policy_2026.md          found_by vector   (by the join)
   #  4 hr_policy_2026.md          found_by vector   (by the join)
   #  2 hr_policy_2026.md          found_by vector   (by the join)
```

**`step_02_the_join_then_the_kit_s_own_retrieval_in_y(session)` — found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Operation: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read).

Expected shape, not a promised result:

```text
20 chunks in the pool, found_by: {'vector': 20}
first three: [('NP-03', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx)]
```

**`step_03_the_join_then_the_kit_s_own_retrieval_in_y(session)` — found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Operation: bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee).

IDE adaptation: Run with the page's pipeline status (no pipefail). The cell filters make smoke for the lines this lesson reads; a check failing elsewhere in the smoke shows in those lines instead of stopping the cell before its later lines.

Expected shape, not a promised result:

```text
[PASS] health  {"status":"ok"}
  [PASS] ready  ...
  [PASS] query  answerable=True citations=3  '...'
  [PASS] vector tier  20 of 20 chunks came from the index
  [PASS] no token refused  status=403
  ...
```

**`step_04_the_api_s_packer_offline_then_a_pool_of_ac(session)` — What the funnel costs, its knobs, and the packed set the citations come from / Do it: the API's packer offline, then a pool of Act pages on the lane**

The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

Operation: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: pure Python over the saved pool and a file in the kit).

Expected shape, not a promised result:

```text
the budget: 7,832 tokens for the chunks, 168 for the fixed prompt, 2,048 reserved for the answer
your ranked pool, top_k 5    packed  5, dropped  0, context   7xx tokens
your ranked pool, top_k 20   packed 20, dropped  0, context  2xxx tokens
twenty full CGST Act pages   packed 15, dropped  5, context  7633 tokens
the first header the model reads: [Source 1] hr_policy_2026.md
```

**`step_05_the_api_s_packer_offline_then_a_pool_of_ac(session)` — What the funnel costs, its knobs, and the packed set the citations come from / Do it: the API's packer offline, then a pool of Act pages on the lane**

The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

Operation: bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read).

Expected shape, not a promised result:

```text
pool 20 | citations 2 | generate_ms 3xxx | tokens_in 8xxx | sources ['cgst_act_2017.pdf']
2026-09-2xT1x:xx:xx.xxxxxxZ	1x	x
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs. Restore the saved answer-cache value and tenant backend, including after a failed experiment.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the lesson's main page, `Netsetos_GCP_Capstone_5.3_Rerank_WIX.html`. All 46 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `57bf349b566019103069ed16a192beac3c631f19`.
