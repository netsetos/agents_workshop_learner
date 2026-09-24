# Lesson 9.2: Test cache scope, configuration changes and freshness

**Summary:** the miss after `make reindex`; a hit again after `make cache`. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.2-cache-freshness/Netsetos_GCP_Capstone_9.2_Cache_Freshness_WIX.html); Git blob `11e9ef8b32dc608b3b9fcb57cae1cd8145b29fa7`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it_the_two_caches.py](demo_03_01_do_it_the_two_caches.py) | bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on) |
| s3 · window 10 | [demo_03_02_do_it_the_state_and_three_asks.py](demo_03_02_do_it_the_state_and_three_asks.py) | bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks) |
| s4 · window 13 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes) |
| s5 · window 17 | [demo_05_01_do_it_the_release.py](demo_05_01_do_it_the_release.py) | bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release) |
| s5 · window 19 | [demo_05_02_do_it_the_state_both_asks_and_the_log.py](demo_05_02_do_it_the_state_both_asks_and_the_log.py) | bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines) |
| s6 · window 22 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the pack again, under the new fingerprint) |
| s7 · window 24 | [demo_07_01_the_corpus_comes_back_version_1_and_the_old_answ.py](demo_07_01_the_corpus_comes_back_version_1_and_the_old_answ.py) | bash — run in the operator shell, in the kit (version 1's bytes again: the undo) |
| s7 · window 26 | [demo_07_02_the_corpus_comes_back_version_1_and_the_old_answ.py](demo_07_02_the_corpus_comes_back_version_1_and_the_old_answ.py) | bash — run in the operator shell, in the kit (the state, and the candidate's ask) |
| s7 · window 28 | [demo_07_03_every_row_of_the_walk.py](demo_07_03_every_row_of_the_walk.py) | bash — run in the operator shell, in the kit (every acme usage row since the start; reads only) |
| s7 · window 30 | [demo_07_04_clean_up.py](demo_07_04_clean_up.py) | bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted) |

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

### demo_03_01_do_it_the_two_caches.py

**HTML: Both caches, and the corpus they follow / Do it: the two caches**

Do it: the two caches

Run instruction: bash — run in the operator shell, in the kit (acme's context cache, and a candidate with the answer cache on).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_the_state_and_three_asks.py

**HTML: Both caches, and the corpus they follow / Do it: the state, and three asks**

Do it: the state, and three asks

Run instruction: bash — run in the operator shell, in the kit (two small functions, a start time, the state, and three asks).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ledger 1ef46119bd89b143 (17 versions, last ingest_ok) | context cache packed from 1ef46119bd89b143: current
  vertex none     in  43109 cached  41259  2480 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2530 ms | A confirmed employee at grade E3 or above serves a
  cache  semantic in      0 cached      0   170 ms | A confirmed employee at grade E3 or above serves a
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Scope: the same words under other settings / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the same question under two other scopes, and four scope hashes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
vertex none     in  43349 cached  41259  2610 ms | A confirmed employee at grade E3 or above serves a
  vertex none     in  43109 cached  41259  2440 ms | A confirmed employee at grade E3 or above serves a
  scope as asked   7a0875abc72b0f7b
  scope top_k 8    bcc480117460bf66
  scope kind: text 8d8d4a1d9912dc52
  scope prompt v4  1d409edacc15c1d1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_the_release.py

**HTML: The corpus moves: revision 2, and both caches react / Do it: the release**

Do it: the release

Run instruction: bash — run in the operator shell, in the kit (revision 2 of the handbook, as a release).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_5560308823a62dc8...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_the_state_both_asks_and_the_log.py

**HTML: The corpus moves: revision 2, and both caches react / Do it: the state, both asks, and the log**

Do it: the state, both asks, and the log

Run instruction: bash — run in the operator shell, in the kit (the state, both asks again, and the API's cache_stale lines).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ledger 1441fb4775d21e13 (17 versions, last ingest_reactivated) | context cache packed from 1ef46119bd89b143: STALE
  vertex none     in   1880 cached      0  2390 ms | From 1 October 2026 the notice period for a confir
  vertex none     in   1880 cached      0  2455 ms | From 1 October 2026 the notice period for a confir
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13
  cache_stale acme: packed from 1ef46119bd89b143, ledger now 1441fb4775d21e13
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: make cache again: attached again, and what it packed / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the pack again, under the new fingerprint).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_the_corpus_comes_back_version_1_and_the_old_answ.py

**HTML: The corpus comes back: version 1, and the old answer with it / The corpus comes back: version 1, and the old answer with it**

Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

Run instruction: bash — run in the operator shell, in the kit (version 1's bytes again: the undo).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md - waiting for the worker (up to 5 min)
>> event doc_key chunks reused embedded retired effective_from
>> ingest_reactivated	acme_497809ffbaa603c4...	283	283	0	283
>> the gate, scoped to this document, on a candidate: make eval-live PROJECT=documind-ai-YOUR-ID SOURCE=hr_policy_2026.md API=<candidate url>
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_the_corpus_comes_back_version_1_and_the_old_answ.py

**HTML: The corpus comes back: version 1, and the old answer with it / The corpus comes back: version 1, and the old answer with it**

Version 1's bytes again, the state, one ask, every row, and the clean-up. The same release command with version 1's file puts the handbook back. The worker finds bytes it retired minutes ago, flips their rows back to current, retires revision 2 in turn, and recomputes the fingerprint. Because the set of current doc_keys is the same as at the start, the fingerprint is the same as at the start too.

Run instruction: bash — run in the operator shell, in the kit (the state, and the candidate's ask).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
ledger 1ef46119bd89b143 (17 versions, last ingest_reactivated) | context cache packed from 1441fb4775d21e13: STALE
  cache  semantic in      0 cached      0   165 ms | A confirmed employee at grade E3 or above serves a
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_every_row_of_the_walk.py

**HTML: The corpus comes back: version 1, and the old answer with it / Every row of the walk**

Every row of the walk

Run instruction: bash — run in the operator shell, in the kit (every acme usage row since the start; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_04_clean_up.py

**HTML: The corpus comes back: version 1, and the old answer with it / Clean up**

Clean up

Run instruction: bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

31 code windows mapped: 12 IDE demo files, 1 shared setup blocks, 18 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
