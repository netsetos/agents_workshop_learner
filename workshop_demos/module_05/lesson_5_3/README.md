# Lesson 5.3: Rerank and inspect retrieved candidates

**Summary:** p95 rerank in `make usage`; `found_by` on a citation. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html); Git blob `57bf349b566019103069ed16a192beac3c631f19`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once per shell |
| s3 · window 10 | [demo_03_01_do_it_the_same_question_at_top_k_5_and_top_k_20.py](demo_03_01_do_it_the_same_question_at_top_k_5_and_top_k_20.py) | bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees) |
| s4 · window 13 | [demo_04_01_do_it_embed_pool_rank_compare.py](demo_04_01_do_it_embed_pool_rank_compare.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding and one rank request, well under a rupee) |
| s5 · window 17 | [demo_05_01_do_it_offline_the_kit_s_fallback_on_the_pool_you.py](demo_05_01_do_it_offline_the_kit_s_fallback_on_the_pool_you.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine) |
| s5 · window 19 | [demo_05_02_do_it_on_a_candidate_a_deadline_no_call_can_meet.py](demo_05_02_do_it_on_a_candidate_a_deadline_no_call_can_meet.py) | bash — run in the operator shell (one new revision, no traffic; one question to it; one log read) |
| s5 · window 21 | [demo_05_03_do_it_on_a_candidate_a_deadline_no_call_can_meet.py](demo_05_03_do_it_on_a_candidate_a_deadline_no_call_can_meet.py) | bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live service asked once) |
| s6 · window 27 | [demo_06_01_do_it_the_selftest_then_the_lane_s_last_day_then.py](demo_06_01_do_it_the_selftest_then_the_lane_s_last_day_then.py) | bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the selftest touches nothing, and reading the log is free) |
| s6 · window 30 | [demo_06_02_do_it_the_selftest_then_the_lane_s_last_day_then.py](demo_06_02_do_it_the_selftest_then_the_lane_s_last_day_then.py) | bash — run in the operator shell (the rows themselves, one JSON line each, for the reader in step 1) |
| s7 · window 35 | [demo_07_01_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py](demo_07_01_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py) | bash — run in the operator shell (a Python cell; Rs 0: two files on disk) |
| s7 · window 37 | [demo_07_02_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py](demo_07_02_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read) |
| s7 · window 39 | [demo_07_03_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py](demo_07_03_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py) | bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee) |
| s8 · window 43 | [demo_08_01_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py](demo_08_01_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: pure Python over the saved pool and a file in the kit) |
| s8 · window 45 | [demo_08_02_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py](demo_08_02_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py) | bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read) |

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

### demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py

**HTML: Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index endpoint and the deployed index are for step 4's pool; the reranker's settings say what the API is running with, and an empty value means the setting's default. Step 4's rank call and the in-process calls in steps 5 and 7 need the API's Ranking client in the venv at the API's own pin; the pip line is harmless if it is already there. A name the service does not set is unset here rather than exported empty, because the kit's settings class reads an empty variable as a value, not as an absence, and a cell that imports the kit would refuse it.

Run instruction: bash — run in the operator shell, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
backend: vector  mode: dense (default)  top_k_retrieve: 20 (default)
rerank timeout: 5.0 (default)  answer cache: off (default)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_the_same_question_at_top_k_5_and_top_k_20.py

**HTML: One answer, read end to end: the citations, their scores, the stages / Do it: the same question at top_k 5 and top_k 20**

The cell asks the notice-period question twice and prints, for each answer, the stages block on one line and every citation with its score, its chunk position, its source and the start of its quote. The second answer offers the model twenty chunks instead of five.

Run instruction: bash — run in the operator shell (a Python cell; two questions, the second with twenty chunks: a few rupees).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_embed_pool_rank_compare.py

**HTML: The Ranking API by hand: the API's pool, the API's request, the API's order / Do it: embed, pool, rank, compare**

Do it: embed, pool, rank, compare

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding and one rank request, well under a rupee).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_offline_the_kit_s_fallback_on_the_pool_you.py

**HTML: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, offline: the kit's fallback on the pool you saved**

Do it, offline: the kit's fallback on the pool you saved

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
rerank_fell_back: True | every chunk marked: True
the pool by retrieval score, what the caller gets while the ranker is down:
   score 0.7xxx  pool # 1  NP-03     hr_policy_2026.md
   score 0.7xxx  pool # 2  ...       hr_policy_2026.md
   ...
the ranker's five (step 4): ['NP-03', '...', '...', '...', '...']
kept by the fallback: x of 5 | first is the same: True
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_on_a_candidate_a_deadline_no_call_can_meet.py

**HTML: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, on a candidate: a deadline no call can meet**

Do it, on a candidate: a deadline no call can meet

Run instruction: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
candidate: rerank_fallback 1 | rerank_ms 1x | pool 20 | answerable True
   score 0.7xxx  #1  hr_policy_2026.md
   score 0.7xxx  #4  hr_policy_2026.md
   score 0.6xxx  #2  hr_policy_2026.md
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	DeadlineExceeded
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_03_do_it_on_a_candidate_a_deadline_no_call_can_meet.py

**HTML: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate / Do it, on a candidate: a deadline no call can meet**

Do it, on a candidate: a deadline no call can meet

Run instruction: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live service asked once).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
live: rerank_fallback 0 | rerank_ms 3xx | first score 0.9xxx
100;documind-api-00044-xyz
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_selftest_then_the_lane_s_last_day_then.py

**HTML: make usage: where the time went, p95 per stage, and the view behind it / Do it: the selftest, then the lane's last day, then its rows into the reader**

Do it: the selftest, then the lane's last day, then its rows into the reader

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the selftest touches nothing, and reading the log is free).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_the_selftest_then_the_lane_s_last_day_then.py

**HTML: make usage: where the time went, p95 per stage, and the view behind it / Do it: the selftest, then the lane's last day, then its rows into the reader**

Do it: the selftest, then the lane's last day, then its rows into the reader

Run instruction: bash — run in the operator shell (the rows themselves, one JSON line each, for the reader in step 1).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
NN rows; 1 with rerank_fallback 1; 0 with an empty pool
{"event": "query", "tenant": "acme", "user": "documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com", "tokens_in": xxxx.0, "tokens_out": xxx.0, "cached_tokens": 0.0, "cost_usd": 0.00xxxx, "latency_ms": 2xxx.0, "answerable": true, "retrieve_ms": 6xx.0, "rerank_ms": 3xx.0, "generate_ms": 1xxx.0, "pool": 20.0, "rerank_fallback": 0.0, ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py

**HTML: found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Run instruction: bash — run in the operator shell (a Python cell; Rs 0: two files on disk).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the answer's counts: pool 20 | vector_chunks 20 | graph_chunks 0 | managed_chunks 0 | retrieval_backend vector
a citation's fields: ['chunk_id', 'end', 'kind', 'media_url', 'page', 'quote', 'score', 'source_uri', 'start']
   #  1 hr_policy_2026.md          found_by vector   (by the join)
   #  4 hr_policy_2026.md          found_by vector   (by the join)
   #  2 hr_policy_2026.md          found_by vector   (by the join)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py

**HTML: found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
20 chunks in the pool, found_by: {'vector': 20}
first three: [('NP-03', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx)]
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_do_it_the_join_then_the_kit_s_own_retrieval_in_y.py

**HTML: found_by: stamped on every chunk, counted on the answer, absent from the citation / Do it: the join, then the kit's own retrieval in your process, then the smoke**

Do it: the join, then the kit's own retrieval in your process, then the smoke

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the smoke: one question, the same without a token, a version read; a rupee).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
[PASS] health  {"status":"ok"}
  [PASS] ready  ...
  [PASS] query  answerable=True citations=3  '...'
  [PASS] vector tier  20 of 20 chunks came from the index
  [PASS] no token refused  status=403
  ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py

**HTML: What the funnel costs, its knobs, and the packed set the citations come from / Do it: the API's packer offline, then a pool of Act pages on the lane**

The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: pure Python over the saved pool and a file in the kit).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the budget: 7,832 tokens for the chunks, 168 for the fixed prompt, 2,048 reserved for the answer
your ranked pool, top_k 5    packed  5, dropped  0, context   7xx tokens
your ranked pool, top_k 20   packed 20, dropped  0, context  2xxx tokens
twenty full CGST Act pages   packed 15, dropped  5, context  7633 tokens
the first header the model reads: [Source 1] hr_policy_2026.md
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_02_do_it_the_api_s_packer_offline_then_a_pool_of_ac.py

**HTML: What the funnel costs, its knobs, and the packed set the citations come from / Do it: the API's packer offline, then a pool of Act pages on the lane**

The cell runs the kit's packer with the API's own budget over three lists: your ranked pool at top_k 5 and 20, and twenty full pages of the CGST Act's mirror, cut by the kit's own chunker from the file in evals/corpus. Then a golden question whose pool is Act pages goes to the API at top_k 20, and the log says what the packer dropped.

Run instruction: bash — run in the operator shell (one question with twenty Act pages offered to the model, a couple of rupees; one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
pool 20 | citations 2 | generate_ms 3xxx | tokens_in 8xxx | sources ['cgst_act_2017.pdf']
2026-09-2xT1x:xx:xx.xxxxxxZ	1x	x
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

46 code windows mapped: 15 IDE demo files, 1 shared setup blocks, 30 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
