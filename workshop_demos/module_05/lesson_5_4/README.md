# Lesson 5.4: Test fallback without losing tenant or metadata filters

**Summary:** `found_by: firestore` with the filter still applied. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html); Git blob `9553c89dce4181161137e7caeba0cf202f30a3ac`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, in $DEMO_ROOT, once per shell |
| s3 · window 11 | [demo_03_01_do_it_the_rung_under_three_predicate_sets.py](demo_03_01_do_it_the_rung_under_three_predicate_sets.py) | bash — run in the operator shell (a Python cell; one embedding, a few dozen Firestore reads) |
| s4 · window 16 | [demo_04_01_do_it_pin_acme_beneath_the_index_and_wait_for_th.py](demo_04_01_do_it_pin_acme_beneath_the_index_and_wait_for_th.py) | bash — run in the operator shell, in $DEMO_ROOT (one field written; up to nine questions while the minute passes) |
| s4 · window 18 | [demo_04_02_do_it_the_same_predicates_on_the_chosen_rung_and.py](demo_04_02_do_it_the_same_predicates_on_the_chosen_rung_and.py) | bash — run in the operator shell (four questions, a few rupees) |
| s4 · window 20 | [demo_04_03_do_it_the_smoke_s_line_for_a_chosen_rung_then_th.py](demo_04_03_do_it_the_smoke_s_line_for_a_chosen_rung_then_th.py) | bash — run in the operator shell, in $DEMO_ROOT (two smokes, a rupee each; one field written) |
| s5 · window 25 | [demo_05_01_do_it_a_candidate_that_cannot_reach_the_index.py](demo_05_01_do_it_a_candidate_that_cannot_reach_the_index.py) | bash — run in the operator shell (one new revision, no traffic; one question to it; one log read; ask() from step 4) |
| s5 · window 27 | [demo_05_02_do_it_a_candidate_that_cannot_reach_the_index.py](demo_05_02_do_it_a_candidate_that_cannot_reach_the_index.py) | bash — run in the operator shell (the undo: the real name back on the template, the tag dropped, the live service asked once) |
| s6 · window 31 | [demo_06_01_do_it_the_probe_then_its_evidence.py](demo_06_01_do_it_the_probe_then_its_evidence.py) | bash — run in the operator shell, in $DEMO_ROOT (one embedding read off a row, a few dozen Firestore reads; nothing written to the cloud) |
| s7 · window 37 | [demo_07_01_do_it_count_the_tier_plan_its_refill_read_the_ro.py](demo_07_01_do_it_count_the_tier_plan_its_refill_read_the_ro.py) | bash — run in the operator shell, in $DEMO_ROOT (read-only: the plan writes nothing without --apply) |
| s8 · window 42 | [demo_08_01_the_policy_that_sends_a_tenant_home.py](demo_08_01_the_policy_that_sends_a_tenant_home.py) | bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index names and the retrieval settings live in the API's environment; a name the service does not set is unset rather than exported empty, because the kit's settings class reads an empty variable as a value, and steps 5 and 6 import the kit. The pins live in Firestore, one document per tenant, and the lane helper prints them.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT, once per shell.

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

IDE adaptations:

- Read literal environment values as JSON from the serving revision; absent keys are unset. Repeated text parsing is removed.

Expected shape from the HTML (actual counts/timing can differ):

```text
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
backend: vector  mode: dense (default)  current_only: off (default)  top_k_retrieve: 20 (default)
acme: retrieval_backend=vector
zeta: retrieval_backend=default (the deployment RETRIEVAL_BACKEND)
acme: data_region=any
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_the_rung_under_three_predicate_sets.py

**HTML: The Firestore rung by hand: the API's three predicates on Firestore's own vector index / Do it: the rung under three predicate sets**

Run the cell as it is, then twice more with a filter in front of its first line: F='{"doc_type":"policy"}' python - <<'PY' and F='{"kind":"text"}' python - <<'PY', the rest unchanged. The worker stamped the lane's uploads doc_type: unknown, so the first filter empties the pool on this rung exactly as it did on the index in lesson 5.1, and the second keeps it whole.

Run instruction: bash — run in the operator shell (a Python cell; one embedding, a few dozen Firestore reads).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
predicates: tenant_id -> 20 rows, every one found_by firestore
   NP-03     hr_policy_2026.md          doc_type unknown  kind text   current True  score 0.7xxx
   ...
index needed: (tenant_id, embedding) | reads billed, at most: 1x for 1xxx index entries + 20 documents

predicates: tenant_id, doc_type (doc_type=policy) -> 0 rows, every one found_by firestore
index needed: (tenant_id, doc_type, embedding) | reads billed, at most: 1x for 1xxx index entries + 0 documents

predicates: tenant_id, kind (kind=text) -> 20 rows, every one found_by firestore
   NP-03     hr_policy_2026.md          doc_type unknown  kind text   current True  score 0.7xxx
   ...
index needed: (tenant_id, kind, embedding) | reads billed, at most: 1x for 1xxx index entries + 20 documents
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_pin_acme_beneath_the_index_and_wait_for_th.py

**HTML: Moving one tenant beneath the index by hand, and back / Do it: pin acme beneath the index, and wait for the API to notice**

Do it: pin acme beneath the index, and wait for the API to notice

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one field written; up to nine questions while the minute passes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme: retrieval_backend=firestore
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_the_same_predicates_on_the_chosen_rung_and.py

**HTML: Moving one tenant beneath the index by hand, and back / Do it: the same predicates on the chosen rung, and two tenants that do not cross**

Do it: the same predicates on the chosen rung, and two tenants that do not cross

Run instruction: bash — run in the operator shell (four questions, a few rupees).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend firestore | vector_chunks 0 | pool 0 | retrieve_ms 4xx | answerable False | first - | The corpus holds nothing near this question: no passage of this
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first x hr_policy_2026.md | ... Rs 40,000 ...
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first x hr_policy_zeta_2026.md | ... Rs 25,000 ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_03_do_it_the_smoke_s_line_for_a_chosen_rung_then_th.py

**HTML: Moving one tenant beneath the index by hand, and back / Do it: the smoke's line for a chosen rung, then the pin back**

Do it: the smoke's line for a chosen rung, then the pin back

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (two smokes, a rupee each; one field written).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
[ -- ] vector tier  this request ran on firestore — skipped
acme: retrieval_backend=vector
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
  [PASS] vector tier  20 of 20 chunks came from the index
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_a_candidate_that_cannot_reach_the_index.py

**HTML: The chaos rung: an index that will not answer, on a candidate that takes no traffic / Do it: a candidate that cannot reach the index**

Do it: a candidate that cannot reach the index

Run instruction: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read; ask() from step 4).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
candidate: backend vector | vector_chunks 0 | pool 20 | answerable True | citations 3
the smoke would say: [FAIL] vector tier  RETRIEVAL_BACKEND=vector and no chunk came from the index - the Firestore rung answered. make vector-status; make backfill-vectors APPLY=1
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	... documind_chunks_nonesuch ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_do_it_a_candidate_that_cannot_reach_the_index.py

**HTML: The chaos rung: an index that will not answer, on a candidate that takes no traffic / Do it: a candidate that cannot reach the index**

Do it: a candidate that cannot reach the index

Run instruction: bash — run in the operator shell (the undo: the real name back on the template, the tag dropped, the live service asked once).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
template now: documind_chunks_v1
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
100;documind-api-00048-xyz
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_probe_then_its_evidence.py

**HTML: The probe: the kit's read-only check of the combined filters / Do it: the probe, then its evidence**

Do it: the probe, then its evidence

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one embedding read off a row, a few dozen Firestore reads; nothing written to the cloud).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"project": "documind-ai-YOUR-ID", "collection": "chunks", "source_uri": "gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md", "source_status": "indexed", "source_doc_key": "acme_497809ff..."}
Verified HR source: 283 current chunks; stored doc_type='unknown'; manifest doc_type='policy'
NOTE: stored metadata differs from the manifest. This probe tests the stored equality filters; it does not certify policy classification or repair metadata.
PASS: combined doc_type='unknown'+kind='text', current=off, rows=5
PASS: combined doc_type='unknown'+kind='text', current=on, rows=5
PASS: both Firestore filter modes verified. Evidence: operator-evidence/firestore-combined-filters.json
evidence: {'doc_type': 'unknown', 'kind': 'text'} | current off: 5 rows | current on: 5 rows | doc_key acme_497809ff...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_count_the_tier_plan_its_refill_read_the_ro.py

**HTML: The tier from the rows: vector-status, backfill-vectors, and the rows that count the rung / Do it: count the tier, plan its refill, read the rows by rung, Rs 0**

Do it: count the tier, plan its refill, read the rows by rung, Rs 0

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (read-only: the plan writes nothing without --apply).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
index: documind-chunks  datapoints: 4xxx  shards: 1  update: STREAM_UPDATE
endpoint: documind-endpoint  deployed: documind_chunks_v1  synced: 2026-09-2xT1x:xx:xx.xxxxxxZ
{"event": "backfill_vectors_plan", "index": "projects/NUMBER/locations/asia-south1/indexes/1234567890123456789", "tenant": "acme", "current_chunks": 1xxx, "needs_document_embedding": 0, "invalid_chunks": 0, "embedding_task_type": "RETRIEVAL_DOCUMENT", "note": "Pause uploads/undo/batch writers; keep answer caches off during repair and validation."}

by retrieval backend (which store served the pool; 13 September 2026)
retrieval_backend      answers    tok_in  tok_out       USD       INR  p95 ms  unans
------------------------------------------------------------------------------------
firestore                    5      xxxx      xxx    0.0xxx      x.xx    2xxx   0.20
vector                       6      xxxx      xxx    0.0xxx      x.xx    2xxx   0.00
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_the_policy_that_sends_a_tenant_home.py

**HTML: What the rung costs, where it cannot go, and the policy that sends a tenant home / The policy that sends a tenant home**

A tenant's data_region says where its text may be held: any lets the managed mirror copy its current versions abroad, in keeps it on the kit's rows in India, and a missing or unknown value is in, because an unreadable policy is the strict one. retrieval_backend_for() holds every request's backend against it: a managed pin for an in tenant is served from the kit's own rung instead, the deployment's if that is vector or firestore, otherwise Firestore, with policy_fallback 1 on the row, which the warehouse sums into a column. The cell runs the two pure functions behind that decision offline; nothing leaves the machine.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{}                       -> policy in
{'data_region': 'any'}   -> policy any
{'data_region': 'in'}    -> policy in
{'data_region': 'eu'}    -> policy in
in   tenant, a store in asia-south1  -> may hold it
in   tenant, a store in us-central1  -> may not
in   tenant, a store in global       -> may not
any  tenant, a store in us-central1  -> may hold it
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

43 code windows mapped: 12 IDE demo files, 1 shared setup blocks, 30 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
