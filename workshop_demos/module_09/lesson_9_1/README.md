# Lesson 9.1: Compare context caching and answer caching

**Summary:** `cached_tokens` on a row; `model_backend=cache` on the second ask. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/09-caching/9.1-cache-compare/Netsetos_GCP_Capstone_9.1_Cache_Compare_WIX.html); Git blob `ee993d0dd1999f045798aa2dc6a500e1d3d86122`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it_the_question_uncached.py](demo_03_01_do_it_the_question_uncached.py) | bash — run in the operator shell, in the kit (a small ask function, a start time for the rows, and one question to the live API) |
| s3 · window 12 | [demo_03_02_do_it_the_cache.py](demo_03_02_do_it_the_cache.py) | bash — run in the operator shell, in the kit (acme's context cache: its pack, on Gemini, for an hour) |
| s3 · window 14 | [demo_03_03_do_it_the_same_question_with_the_cache.py](demo_03_03_do_it_the_same_question_with_the_cache.py) | bash — run in the operator shell, in the kit (the same question again, to the live API) |
| s4 · window 17 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (every acme usage row since the first ask; reads only) |
| s5 · window 23 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on and no traffic) |
| s6 · window 25 | [demo_06_01_four_asks_a_miss_two_hits_and_a_paraphrase.py](demo_06_01_four_asks_a_miss_two_hits_and_a_paraphrase.py) | bash — run in the operator shell, in the kit (four asks to the candidate) |
| s6 · window 27 | [demo_06_02_four_asks_a_miss_two_hits_and_a_paraphrase.py](demo_06_02_four_asks_a_miss_two_hits_and_a_paraphrase.py) | bash — run in the operator shell, in the kit (the same rows cell, now with the candidate's) |
| s7 · window 29 | [demo_07_01_what_each_cache_is_holding_and_the_clean_up.py](demo_07_01_what_each_cache_is_holding_and_the_clean_up.py) | bash — run in the operator shell, in the kit (what each cache is holding; reads only) |
| s7 · window 31 | [demo_07_02_what_each_cache_is_holding_and_the_clean_up.py](demo_07_02_what_each_cache_is_holding_and_the_clean_up.py) | bash — run in the operator shell, in the kit (the candidate's tag and recorded name removed, the context cache deleted) |

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

### demo_03_01_do_it_the_question_uncached.py

**HTML: The context cache: a pack, a cache, and the next answer / Do it: the question, uncached**

Do it: the question, uncached

Run instruction: bash — run in the operator shell, in the kit (a small ask function, a start time for the rows, and one question to the live API).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend vertex cache_hit none     tokens_in   1812  cached_tokens      0   2410 ms  | Employees may work remotely up to eight days
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_the_cache.py

**HTML: The context cache: a pack, a cache, and the next answer / Do it: the cache**

Do it: the cache

Run instruction: bash — run in the operator shell, in the kit (acme's context cache: its pack, on Gemini, for an hour).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
cd services/rag-api && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID GENERATOR_MODEL=gemini-3.6-flash \
  python cache_admin.py ${CACHE_OP:-create} --project documind-ai-YOUR-ID --tenant acme
  cache projects/NUMBER/locations/global/cachedContents/CACHE_ID
  location global (global or regional: the answer to CLAUDE.md's question)
  model gemini-3.6-flash | tokens 41259 | expires YYYY-MM-DD HH:MM:SS.ssssss+00:00 | corpus 75b21a03f12f | ledger fingerprint FINGERPRINT
  the next /v1/query for acme carries cached_content; read cached_tokens in its usage row
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_03_do_it_the_same_question_with_the_cache.py

**HTML: The context cache: a pack, a cache, and the next answer / Do it: the same question, with the cache**

Do it: the same question, with the cache

Run instruction: bash — run in the operator shell, in the kit (the same question again, to the live API).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend vertex cache_hit none     tokens_in  43071  cached_tokens  41259   2650 ms  | Employees may work remotely up to eight days
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The rows: what the context cache did to the bill / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (every acme usage row since the first ask; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
00041-kqz  vertex  in   1812  cached      0  Rs 0.4937   2410 ms
  00041-kqz  vertex  in  43071  cached  41259  Rs 1.0197   2650 ms
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The answer cache: a candidate that remembers answers / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a revision with SEMANTIC_CACHE=on and no traffic).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|RAG_MODEL_BASE=gemini-3.6-flash|ROUTING=off|MODEL_BACKEND=vertex|ARMOR=off|SEMANTIC_CACHE=on|..."
...
>> candidate revision: documind-api-00044-rtv (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
CAND=https://candidate---documind-api-NUMBER.asia-south1.run.app
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_four_asks_a_miss_two_hits_and_a_paraphrase.py

**HTML: Four asks: a miss, two hits and a paraphrase / Four asks: a miss, two hits and a paraphrase**

One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

Run instruction: bash — run in the operator shell, in the kit (four asks to the candidate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend vertex cache_hit none     tokens_in  43071  cached_tokens  41259   2590 ms  | Employees may work remotely up to eight days
  backend cache  cache_hit semantic tokens_in      0  cached_tokens      0    182 ms  | Employees may work remotely up to eight days
  backend cache  cache_hit semantic tokens_in      0  cached_tokens      0    176 ms  | Employees may work remotely up to eight days
  backend vertex cache_hit none     tokens_in  43053  cached_tokens  41259   2720 ms  | Employees may work remotely up to eight days
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_four_asks_a_miss_two_hits_and_a_paraphrase.py

**HTML: Four asks: a miss, two hits and a paraphrase / Four asks: a miss, two hits and a paraphrase**

One question four ways, then the rows. The first ask is a miss: the candidate has never seen the question, so it retrieves, calls the model and stores the answer. The second is the same words, for the exact rung. The third is the same words in lower case without the question mark, which qhash treats as identical. The fourth says the same thing in other words. It is a hit only if its embedding lands within 0.95 of the first question's; otherwise it is a miss, and its own answer is stored beside the first.

Run instruction: bash — run in the operator shell, in the kit (the same rows cell, now with the candidate's).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
00041-kqz  vertex  in   1812  cached      0  Rs 0.4937   2410 ms
  00041-kqz  vertex  in  43071  cached  41259  Rs 1.0197   2650 ms
  00044-rtv  vertex  in  43071  cached  41259  Rs 1.0197   2590 ms
  00044-rtv  cache   in      0  cached      0  Rs 0.0000    182 ms
  00044-rtv  cache   in      0  cached      0  Rs 0.0000    176 ms
  00044-rtv  vertex  in  43053  cached  41259  Rs 1.0085   2720 ms
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_what_each_cache_is_holding_and_the_clean_up.py

**HTML: What each cache is holding, and the clean-up / What each cache is holding, and the clean-up**

The record behind the context cache, the entry behind the hit, and both caches put away. The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it.

Run instruction: bash — run in the operator shell, in the kit (what each cache is holding; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
context cache  (Firestore holds a pointer; the pack itself is on Google's side)
    cache_name: projects/NUMBER/locations/global/cachedContents/CACHE_ID
    location: global
    model: gemini-3.6-flash
    tokens: 41259
    expire_time: YYYY-MM-DD HH:MM:SS.ssssss+00:00
    corpus_fingerprint: FINGERPRINT
answer cache  (2 acme entries; 1 for this question's words)
    question: How many days a month can I work remotely?
    qhash: 79ae9ca70e9e21c4c23aca5b  scope: 7a0875abc72b0f7b  fingerprint: FINGERPRINT_
    model: gemini-3.6-flash  expire_at: YYYY-MM-DD HH:MM:SS+00:00  embedding: 768 numbers
    answer: Employees may work remotely up to eight days per month with   citations: 1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_what_each_cache_is_holding_and_the_clean_up.py

**HTML: What each cache is holding, and the clean-up / What each cache is holding, and the clean-up**

The cell prints tenant_caches/acme, then the answer-cache entry for the question's words. It uses the kit's own qhash, imported from services/rag-api, so the key is computed exactly as the API computes it. The two records show where each cache keeps its weight. For the context cache, Firestore holds only a pointer and a few facts, and the pack's forty-odd thousand tokens sit on Google's side, billed by the hour until they expire or are deleted. For the answer cache, Firestore holds everything: the answer, its citations and the question's 768-number embedding. That costs Firestore storage and reads, for 24 hours. The clean-up removes the candidate's tag and recorded name, and deletes the context cache. The next acme question to the live API finds no record and runs uncached at once.

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

32 code windows mapped: 11 IDE demo files, 1 shared setup blocks, 20 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
