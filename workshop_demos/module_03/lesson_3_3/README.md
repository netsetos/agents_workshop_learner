# Lesson 3.3: Create and validate compatible embeddings

**Summary:** three 768-number vectors and the cost in paise; a legacy row rejected. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html); Git blob `517b23e8586183331850aae2cc29914890bc82df`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once |
| s3 · window 11 | [demo_03_01_call_it_three_reads_of_one_pair.py](demo_03_01_call_it_three_reads_of_one_pair.py) | bash — run in the operator shell |
| s4 · window 14 | [demo_04_01_do_it_embed_one_clause_yourself_both_ways.py](demo_04_01_do_it_embed_one_clause_yourself_both_ways.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash; two paid calls) |
| s5 · window 18 | [demo_05_01_do_it_plan_the_handbook_rs_0.py](demo_05_01_do_it_plan_the_handbook_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 23 | [demo_06_01_read_the_stamp_off_one_row_rs_0.py](demo_06_01_read_the_stamp_off_one_row_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 25 | [demo_06_02_validate_every_current_row_of_a_tenant_with_the.py](demo_06_02_validate_every_current_row_of_a_tenant_with_the.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 27 | [demo_06_03_the_same_check_as_an_operator_runs_it_and_as_the.py](demo_06_03_the_same_check_as_an_operator_runs_it_and_as_the.py) | bash — run in the operator shell (both read-only) |
| s7 · window 33 | [demo_07_01_plan_it_locally_rs_0.py](demo_07_01_plan_it_locally_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s7 · window 35 | [demo_07_02_do_it_on_the_lane_revision_2_over_the_same_name.py](demo_07_02_do_it_on_the_lane_revision_2_over_the_same_name.py) | bash — run in the operator shell, in $DEMO_ROOT (one re-issue; the worker takes under a minute) |
| s7 · window 37 | [demo_07_03_see_it_in_the_ui_then_read_it_three_more_ways.py](demo_07_03_see_it_in_the_ui_then_read_it_three_more_ways.py) | bash — run in the operator shell |
| s7 · window 39 | [demo_07_04_undo_it_the_same_bytes_again_and_nothing_is_embe.py](demo_07_04_undo_it_the_same_bytes_again_and_nothing_is_embe.py) | bash — run in the operator shell, in $DEMO_ROOT (the undo; no model call) |
| s8 · window 44 | [demo_08_01_run_it_on_the_lane_s_text_rs_0.py](demo_08_01_run_it_on_the_lane_s_text_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. Steps 6 and 7 import the worker's own indexer.py, which imports the Vector Search and Gemini SDKs at the top. The setup block installed only the Firestore client; add the other two once. Nothing in this lesson writes to Vector Search.

Run instruction: bash — run in the operator shell, once.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_call_it_three_reads_of_one_pair.py

**HTML: One declared embedding, from Terraform to the row / Call it: three reads of one pair**

All read-only. The first prints the worker's environment, the second asks the API what it is serving, the third reads the pair off the ledger rows the Versions table renders.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{'name': 'EMBEDDING_MODEL', 'value': 'text-embedding-005'}
{'name': 'EMBEDDING_VERSION', 'value': '1'}
api serves embedding text-embedding-005@1 | generator gemini-3.6-flash | retrieval hybrid vector
acme/code_on_wages_2019.pdf                  chunks   67  reused    0  embedded   67  text-embedding-005@1
acme/dpdp_act_2023.pdf                       chunks   44  reused    0  embedded   44  text-embedding-005@1
acme/hr_policy_2026.md                       chunks  283  reused    0  embedded  283  text-embedding-005@1
...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_embed_one_clause_yourself_both_ways.py

**HTML: The call: 768 numbers under the document task type / Do it: embed one clause yourself, both ways**

This cell costs money, a very small amount: two calls on a 234-character clause, about a tenth of a paisa. It reads NP-03's text and stored vector off the lane, embeds the same text under the document profile with the worker's exact settings, and compares by cosine. Then it embeds the same text under the query profile and compares again.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash; two paid calls).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lane vector: 768 numbers; first three [0.0213, -0.0117, 0.0388]
same text, RETRIEVAL_DOCUMENT: cosine to the lane's vector 1.0
same text, RETRIEVAL_QUERY:    cosine to the lane's vector 0.9xxx
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_plan_the_handbook_rs_0.py

**HTML: Batches: 250 texts and 15,000 tokens per request / Do it: plan the handbook, Rs 0**

The loader's copy of the rule, on the chunks you cut in lesson 3.2. No call is made; a plan is printed.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
handbook: 283 chunks, 158,692 chars -> 4 requests of [85, 78, 78, 42] texts, est tokens [14833, 14949, 14944, 8057]
wages mirror: 65 chunks, 102,444 chars -> 3 requests of [28, 28, 9] texts, est tokens [...]
the handbook in one request would carry about 52,783 estimated tokens: over 20,000, refused whole
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_read_the_stamp_off_one_row_rs_0.py

**HTML: Validate: the stamp, and the function that reads it / Read the stamp off one row, Rs 0**

Read the stamp off one row, Rs 0

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
row id: acme:9f3c...#1
  locator                  'NP-03'
  chunk_hash               'f4512754ae41...'
  embedding_model          'text-embedding-005'
  embedding_version        '1'
  embedding_task_type      'RETRIEVAL_DOCUMENT'
  sparse_encoder_version   'blake2b-tf-v1'
  schema_version           2
  kind                     'text'
  doc_type                 'unknown'
  embedding                768 numbers, first three [0.0213, -0.0117, 0.0388]
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_validate_every_current_row_of_a_tenant_with_the.py

**HTML: Validate: the stamp, and the function that reads it / Validate every current row of a tenant, with the worker's own function**

This cell imports the worker's indexer.py as deployed and runs its test over every current acme row. The import builds the worker's embedding client (which is why the project must be in the environment) but nothing is embedded.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme current rows: N  compatible: N  incompatible: 0
   N rows stamped ('text-embedding-005', '1', 'RETRIEVAL_DOCUMENT', 768)
the worker expects: ('text-embedding-005', '1', 'RETRIEVAL_DOCUMENT', 768)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_03_the_same_check_as_an_operator_runs_it_and_as_the.py

**HTML: Validate: the stamp, and the function that reads it / The same check as an operator runs it, and as the tests run it**

The backfill target prints a plan when APPLY=1 is absent: it reads every current row and counts the ones that fail the same function. On a healthy lane the count is zero, and the target is how you would find out otherwise. It needs the index name from Terraform's outputs; if your checkout has no Terraform state, the second form takes the name from the API instead. The unit tests run the worker's file against doubled SDKs, offline, in a fraction of a second.

Run instruction: bash — run in the operator shell (both read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"event": "backfill_vectors_plan", "index": "projects/NUMBER/locations/asia-south1/indexes/1234567890123456789", "tenant": "acme", "current_chunks": N, "needs_document_embedding": 0, "invalid_chunks": 0, "embedding_task_type": "RETRIEVAL_DOCUMENT", "note": "Pause uploads/undo/batch writers; keep answer caches off during repair and validation."}
............
----------------------------------------------------------------------
Ran 12 tests in 0.014s

OK
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_plan_it_locally_rs_0.py

**HTML: Carry-over: re-issue the handbook, embed only what changed / Plan it locally, Rs 0**

The worker's planner on the two versions of the handbook, with a stand-in for what held_vectors() would lend: one vector per version-1 hash.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
v2: 283 chunks, reused 281, to embed 2: ['preamble', 'NP-03']
  preamble: hash 903e2b39ee92 -> b4736d2f3e52
  NP-03: hash f4512754ae41 -> 876232171dec
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_do_it_on_the_lane_revision_2_over_the_same_name.py

**HTML: Carry-over: re-issue the handbook, embed only what changed / Do it on the lane: revision 2 over the same name**

The upload must keep the object name, acme/hr_policy_2026.md, or it is a new source and nothing is held. The loop then waits for the worker's ingest_ok line and prints its counts. Cost: two clauses, 453 characters, about a hundredth of a paisa; a Markdown file pays no Document AI.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one re-issue; the worker takes under a minute).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> chunks reused embedded retired effective_from: 283	281	2	283	2026-10-01
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_03_see_it_in_the_ui_then_read_it_three_more_ways.py

**HTML: Carry-over: re-issue the handbook, embed only what changed / See it in the UI, then read it three more ways**

Refresh Documents. The handbook's row in the Versions table now reads reused 281, embedded 2, retired 283, with an effective date of 1 October 2026 that the revision declares in its first lines. The first call below is the same row from the API; the second reads the rows themselves and checks the thing the counts claim: an unchanged clause's new row carries the same numbers as its retired predecessor, and a changed clause's does not. The third asks the question the revision changed the answer to.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme/hr_policy_2026.md chunks 283 reused 281 embedded 2 retired 283 effective 2026-10-01 text-embedding-005@1
rows for the source: 566 | current: 283 | retired: 283
  LV-01     hash ff463cede286 -> ff463cede286   same vector: True
  NP-03     hash f4512754ae41 -> 876232171dec   same vector: False
  preamble  hash 903e2b39ee92 -> b4736d2f3e52   same vector: False
A confirmed employee at grade E3 or above serves a notice period of 90 days ... [Source 1]
[('1', 'hr_policy_2026.md'), ('2', 'hr_policy_2026.md')] vector
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_04_undo_it_the_same_bytes_again_and_nothing_is_embe.py

**HTML: Carry-over: re-issue the handbook, embed only what changed / Undo it: the same bytes again, and nothing is embedded**

Upload version 1 again under the same name. Its doc_key is the one the lane retired a minute ago, so the worker does not parse, chunk or embed anything: it flips the retired rows back to current, retires revision 2, and logs ingest_reactivated with embedded 0. This is the undo from lesson 3.1, seen from the embedding side: nothing was ever deleted, so nothing has to be made again.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (the undo; no model call).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> reactivated: chunks reused embedded retired: 283	283	0	283
A confirmed employee at grade E3 or above serves a notice period of 60 days ... [Source 1]
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_run_it_on_the_lane_s_text_rs_0.py

**HTML: The sparse twin, the notebook twin, and what embedding bills / Run it on the lane's text, Rs 0**

Run it on the lane's text, Rs 0

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
row stamp: blake2b-tf-v1 | encoder here: blake2b-tf-v1
NP-03: 41 words, 33 distinct -> 33 sparse dimensions, max weight 2.5
the question: 13 dimensions, 9 shared with NP-03: ['a', 'at', 'confirmed', 'days', 'e3', 'employee', 'grade', 'notice', 'of']
same text twice, same dimensions: True
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

48 code windows mapped: 14 IDE demo files, 1 shared setup blocks, 33 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
