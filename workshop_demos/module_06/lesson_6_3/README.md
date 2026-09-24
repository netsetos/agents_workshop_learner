# Lesson 6.3: Stream answers and handle failures

**Summary:** a stream; one forced fallback line with the answer still served. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.3-streaming/Netsetos_GCP_Capstone_6.3_Streaming_WIX.html); Git blob `c6e58b623f6b0a931efccb868a7e7dc1ba3f7f54`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, in $DEMO_ROOT, once per shell |
| s3 · window 12 | [demo_03_01_do_it_one_stream_timed_then_the_query_s_citation.py](demo_03_01_do_it_one_stream_timed_then_the_query_s_citation.py) | bash — run in the operator shell (a Python cell; one stream and one query, two rupees) |
| s4 · window 16 | [demo_04_01_do_it_the_empty_pool_as_one_token_then_the_strea.py](demo_04_01_do_it_the_empty_pool_as_one_token_then_the_strea.py) | bash — run in the operator shell (one stream that costs nothing; one log read) |
| s5 · window 22 | [demo_05_01_read_the_lane_rs_0.py](demo_05_01_read_the_lane_rs_0.py) | bash — run in the operator shell (two log reads) |
| s6 · window 27 | [demo_06_01_do_it_the_ranker_silent_for_one_revision_the_str.py](demo_06_01_do_it_the_ranker_silent_for_one_revision_the_str.py) | bash — run in the operator shell (one new revision, no traffic; one stream to it; two log reads; the undo) |
| s8 · window 35 | [demo_08_01_do_it_the_day_by_surface_rs_0.py](demo_08_01_do_it_the_day_by_surface_rs_0.py) | bash — run in the operator shell, in $DEMO_ROOT (one log read) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The guard, the answer cache, the router and the ranker's deadline live in the API's environment, each with a default the page names; a name the service does not set is unset rather than exported empty. /version reports the cache and the model.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
guard: off (default)  template: documind-guard (default)  cache: off (default)  routing: off (default)  rerank timeout: 5.0 (default)
version: gemini-3.6-flash | documind-rag@v3 | semantic_cache off
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_one_stream_timed_then_the_query_s_citation.py

**HTML: A stream in curl: the raw events, their order, and a clock on each / Do it: one stream, timed, then the query's citations beside it**

Do it: one stream, timed, then the query's citations beside it

Run instruction: bash — run in the operator shell (a Python cell; one stream and one query, two rupees).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
first citation at 1xxx ms | first token at 2xxx ms | done at 4xxx ms | the API's own latency_ms 4xxx
5 citation events, then 3x token events, then done
   citation 1 #  1 hr_policy_2026.md      kind text effective_from None quote 'NP-03 — Notice period\nA confirmed em'
   citation 2 #  4 hr_policy_2026.md      kind text effective_from None quote '...'
   ...
the answer: A confirmed employee in grade E3 must serve a notice period of ... [1] ...
done: {'tokens_in': 1xxx, 'tokens_out': 4xx, 'cached_tokens': 0, 'model': 'gemini-3.6-flash', 'backend': 'vertex', 'cache_hit': 'none', 'prompt': 'documind-rag@v3'}
stages: {'policy_fallback': 0, 'retrieval_backend': 'vector', 'retrieve_ms': 6xx, 'pool': 20, 'graph_chunks': 0, 'managed_chunks': 0, 'vector_chunks': 20, 'rerank_ms': 3xx, 'generate_ms': 2xxx}
the query's answer to the same question: 3 citations, the ones the model used; the stream's 5 were the packed set
saved /tmp/stream63.txt: paste it into the reader in step 1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_the_empty_pool_as_one_token_then_the_strea.py

**HTML: What a stream's citations are, and the streams of one token / Do it: the empty pool as one token, then the stream rows**

Do it: the empty pool as one token, then the stream rows

Run instruction: bash — run in the operator shell (one stream that costs nothing; one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the one token: The corpus holds nothing near this question: no passage of this tenant's current documents was ...
done: backend none | tokens_in 0 | pool 0 | rerank_ms 0 | generate_ms 0
events: {'token': 1, 'done': 1}
False	none	0	0	0	off	ui
True	vertex	1xxx	4xx	20	off	ui
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_read_the_lane_rs_0.py

**HTML: The guard: a prompt refused before the stream, an answer held until it is screened / Read the lane, Rs 0**

Read the lane, Rs 0

Run instruction: bash — run in the operator shell (two log reads).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
NN off
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_ranker_silent_for_one_revision_the_str.py

**HTML: A failure forced on a candidate: the ranker silent, the stream still served, the line in the log / Do it: the ranker silent for one revision, the stream read, the line read, the undo**

Do it: the ranker silent for one revision, the stream read, the line read, the undo

Run instruction: bash — run in the operator shell (one new revision, no traffic; one stream to it; two log reads; the undo).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
done.stages: rerank_fallback 1 | rerank_ms 1x | pool 20 | vector_chunks 20
events: {'citation': 3, 'token': 3x, 'done': 1} | the answer: A confirmed employee in grade E3 must serve a notice period of ...
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	DeadlineExceeded
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_do_it_the_day_by_surface_rs_0.py

**HTML: What a stream costs, what its row says, and who reads it / Do it: the day by surface, Rs 0**

Do it: the day by surface, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one log read).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
by surface
event                  answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
query                       NN     xxxxx     xxxx    0.0xxx      x.xx    4xxx   0.xx
stream                       4      xxxx      xxx    0.0xxx      x.xx    4xxx   0.25
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

36 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 27 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
