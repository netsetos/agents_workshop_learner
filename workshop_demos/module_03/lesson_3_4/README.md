# Lesson 3.4: Write, inspect and verify indexed records

**Summary:** a `chunks` row with every stamp; `vectorsCount` moves. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html); Git blob `919ad0b568337556ab3556373116e42e432c4488`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s2 · window 6 | [demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell, once per shell |
| s3 · window 13 | [demo_03_01_do_it_index_a_note_and_count_the_datapoints_befo.py](demo_03_01_do_it_index_a_note_and_count_the_datapoints_befo.py) | bash — run in the operator shell, in $DEMO_ROOT (one small ingest) |
| s3 · window 15 | [demo_03_02_do_it_index_a_note_and_count_the_datapoints_befo.py](demo_03_02_do_it_index_a_note_and_count_the_datapoints_befo.py) | bash — run in the operator shell (both read-only) |
| s4 · window 20 | [demo_04_01_read_all_four_rs_0.py](demo_04_01_read_all_four_rs_0.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s5 · window 24 | [demo_05_01_the_index_and_its_deployment_as_gcloud_sees_them.py](demo_05_01_the_index_and_its_deployment_as_gcloud_sees_them.py) | bash — run in the operator shell |
| s5 · window 27 | [demo_05_02_read_one_datapoint_back_then_search_for_it.py](demo_05_02_read_one_datapoint_back_then_search_for_it.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 32 | [demo_06_01_read_the_mirror_rows_then_the_audit_event.py](demo_06_01_read_the_mirror_rows_then_the_audit_event.py) | bash — run in the operator shell (two BigQuery queries, then one read from the audit bucket) |
| s7 · window 37 | [demo_07_01_do_it_the_fallback_rung_then_the_api.py](demo_07_01_do_it_the_fallback_rung_then_the_api.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s7 · window 39 | [demo_07_02_the_operator_s_checks_two_commands_and_their_tes.py](demo_07_02_the_operator_s_checks_two_commands_and_their_tes.py) | bash — run in the operator shell, in $DEMO_ROOT (all read-only) |
| s8 · window 43 | [demo_08_01_the_rows_rebuild_the_tier.py](demo_08_01_the_rows_rebuild_the_tier.py) | bash — the plan (read-only) and the repair (writes to the tier; run it only when the plan is not zero) |

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

Calls from the shell impersonate documind-ui-sa, the UI's own account, which make roster put on the three golden tenants (acme, zeta, globex). That is why a shell call can name any of the three. otok mints a token for documind-outsider-sa, an account IAM admits into the service and no roster lists. Tokens last about an hour; the functions mint a fresh one on every call. Your browser session is different: IAP signs you in as yourself, and the roster maps your email to exactly one tenant. Keep the two apart in your head; step 3 makes the difference visible. The index, the endpoint, the BigQuery table and the audit bucket are named in the environment of the two services that use them. Read them once into the shell; every cell below uses these variables. Both reads are read-only.

Run instruction: bash — run in the operator shell, once per shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
index:    projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321  deployed: documind_chunks_v1
mirror:   documind-ai-YOUR-ID.rag_data.chunk_source  audit: documind-ai-YOUR-ID-audit
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_01_do_it_index_a_note_and_count_the_datapoints_befo.py

**HTML: Write: the order the worker keeps, and a fresh document to watch / Do it: index a note, and count the datapoints before and after**

The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (one small ingest).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
datapoints before: N
>> event doc_key chunks pages embedded: ingest_ok  acme_9c41d0e2b7f5a1...  3  1  3
datapoints now: N+3
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_index_a_note_and_count_the_datapoints_befo.py

**HTML: Write: the order the worker keeps, and a fresh document to watch / Do it: index a note, and count the datapoints before and after**

The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes. Two reads tell you what the worker did with an upload. The first lists every ingest event of the last twenty minutes with its verdict: ingest_duplicate means the bytes were already claimed on this lane, ingest_failed carries the error, and no line at all means the event never reached the worker. The second reads the claim for the unchanged demo bytes; its gcs_uri names the object that holds them, which on a lane where the smoke has run is acme/smoke_note.md. The claim is per version, not per name: that is the record this whole step is about.

Run instruction: bash — run in the operator shell (both read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
2026-09-22T11:58:07.412Z  ingest_duplicate  acme_111510fcf0a6ce7c...
the demo bytes' claim, acme_111510fcf0a6...: {'status': 'indexed', 'gcs_uri': 'gs://documind-ai-YOUR-ID-uploads/acme/smoke_note.md', 'chunks': 3, 'generation': '1758...'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_read_all_four_rs_0.py

**HTML: Inspect Firestore: the claim, the rows, the ledger row, the fingerprint / Read all four, Rs 0**

Read all four, Rs 0

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
doc_key from the note's bytes: acme_9c41d0e2b7f5a1...
documents/: {'status': 'indexed', 'chunks': 3, 'reused': 0, 'embedded': 3, 'generation': '1758542671234567', 'tenant_id': 'acme'}
chunks/: 3 rows | current: 3 | staged: 0 | with expire_at: 0
  acme:9c41d0e2b7f5...#0  preamble  section=None hash=70501fc5957f vector=768 doc_type=unknown
  acme:9c41d0e2b7f5...#1  SM-01     section='SM-01 - The smoke lantern' hash=14adcf0a776b vector=768 doc_type=unknown
  acme:9c41d0e2b7f5...#2  SM-02     section='SM-02 - The ladder' hash=(yours) vector=768 doc_type=unknown
sources/acme~smoke_note_v1.md: {'status': 'indexed', 'chunks': 3, 'reused': 0, 'embedded': 3, 'retired': 0, 'effective_from': None} | doc_key matches: True | sha256 matches: True
ledger/acme: {'fingerprint': '9b1d5e7a3c2f4680', 'versions': N, 'last_event': 'ingest_ok'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_the_index_and_its_deployment_as_gcloud_sees_them.py

**HTML: Inspect Vector Search: the datapoint, its restricts, and a search for itself / The index and its deployment, as gcloud sees them**

Three things exist: the index, the endpoint, and the deployed index that joins them and is the one that costs money per hour. The kit's make vector-status runs commands/vector-status.sh, which takes the two names from the shell (the variables you exported above) or, failing that, from Terraform's outputs; the two commands below are the same reads by hand.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
displayName: documind-chunks
indexStats:
  shardsCount: 1
  vectorsCount: '1745'
indexUpdateMethod: STREAM_UPDATE
metadata:
  config:
    dimensions: 768
    distanceMeasureType: DOT_PRODUCT_DISTANCE
displayName: documind-endpoint
deployedIndexes:
- dedicatedResources:
    machineSpec:
      machineType: e2-standard-2
  id: documind_chunks_v1
  indexSyncTime: '2026-09-22T10:41:07.000Z'
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_read_one_datapoint_back_then_search_for_it.py

**HTML: Inspect Vector Search: the datapoint, its restricts, and a search for itself / Read one datapoint back, then search for it**

Read one datapoint back, then search for it

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
datapoint acme:9c41d0e2b7f5...#1: 768 numbers | same as the row's vector: True
restricts: [('tenant_id', ['acme']), ('kind', ['text']), ('doc_type', ['unknown']), ('current', ['true'])]
sparse dimensions: 24
  acme:9c41d0e2b7f5...#1  distance 1.0000   <- itself
  acme:9c41d0e2b7f5...#2  distance 0.7xxx
  acme:9c41d0e2b7f5...#0  distance 0.6xxx
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_read_the_mirror_rows_then_the_audit_event.py

**HTML: Inspect the mirror and the audit trail / Read the mirror rows, then the audit event**

Read the mirror rows, then the audit event

Run instruction: bash — run in the operator shell (two BigQuery queries, then one read from the audit bucket).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
+--------------------------------------------------+---------------------------+------+----------+----------+----------+
|                     chunk_id                     |       heading_path        | kind | doc_type | pii_flag |    at    |
+--------------------------------------------------+---------------------------+------+----------+----------+----------+
| acme:9c41d0e2b7f5...#0                           | NULL                      | text | unknown  |    false | 10:39:52 |
| acme:9c41d0e2b7f5...#1                           | SM-01 - The smoke lantern | text | unknown  |    false | 10:39:52 |
| acme:9c41d0e2b7f5...#2                           | SM-02 - The ladder        | text | unknown  |    false | 10:39:52 |
+--------------------------------------------------+---------------------------+------+----------+----------+----------+
+-----------+-----------+
| rows_ever | documents |
+-----------+-----------+
|      2031 |         9 |
+-----------+-----------+
{
 "id": "3d6d8a5e-...",
 "ts": "2026-09-22T10:39:53.412Z",
 "action": "doc.upload",
 "actor": {"tenant_id": "acme", "email": "system:ingest"},
 "target": {"type": "document", "id": "acme_9c41d0e2b7f5...", "tenant_id": "acme"},
 "meta": {"gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "pages": 1, "chunks": 3, "pii": false, "kinds": ["text"], "reused": 0, "embedded": 3, "retired": 0}
}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it_the_fallback_rung_then_the_api.py

**HTML: Verify: the two rungs that read the records / Do it: the fallback rung, then the API**

The first cell runs the Firestore rung's exact query with the note's own vector: itself first, at a cosine distance of zero. The second asks the API a question only the note can answer and prints which rung served it and how many of the pooled chunks came from the index.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme:9c41d0e2b7f5...#1  SM-01     cosine distance 0.0000   <- itself
  acme:9c41d0e2b7f5...#2  SM-02     cosine distance 0.2xxx
  acme:9c41d0e2b7f5...#0  preamble  cosine distance 0.3xxx
The smoke lantern is kept in bay 4 of the Pune warehouse and is checked on the first Monday of every month ... [Source 1]
[('1', 'smoke_note_v1.md'), ('2', 'smoke_note_v1.md')]
backend vector | pool 20 | from the index 20
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_the_operator_s_checks_two_commands_and_their_tes.py

**HTML: Verify: the two rungs that read the records / The operator's checks: two commands, and their tests**

The kit ships two read-only commands for exactly this lesson. verify-vector-index.py reads Terraform's outputs and asks the API whether the index Terraform declared is the one attached to the endpoint, streaming, 768-dimensional, deployed exactly once; it needs a checkout with Terraform state, and the two gcloud reads in step 5 are the same checks by hand. check-firestore-fallback.py takes the handbook, proves the ledger row names the bytes in your checkout, and runs the Firestore rung with combined filters in both current modes; it imports the API's own modules, so it needs the API's packages in your venv. Both write their evidence under operator-evidence/. Their tests run offline in a fraction of a second.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT (all read-only).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
Project: documind-ai-YOUR-ID (NUMBER)
Terraform index: projects/documind-ai-YOUR-ID/locations/asia-south1/indexes/1234567890123456789
Terraform endpoint: projects/documind-ai-YOUR-ID/locations/asia-south1/indexEndpoints/9876543210987654321
API index: projects/NUMBER/locations/asia-south1/indexes/1234567890123456789
API endpoint: projects/NUMBER/locations/asia-south1/indexEndpoints/9876543210987654321
Index dimensions: 768; update method: STREAM_UPDATE
Global vector count: 1745
Deployment: documind_chunks_v1
Deployment sync time: 2026-09-22T10:41:07.000Z
PASS: the expected index is attached to the expected endpoint.
This verifies attachment and configuration; ingestion and query checks are separate.
{"project": "documind-ai-YOUR-ID", "collection": "chunks", "source_uri": "gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md", "source_status": "indexed", "source_doc_key": "acme_..."}
Verified HR source: 283 current chunks; stored doc_type='unknown'; manifest doc_type='policy'
NOTE: stored metadata differs from the manifest. This probe tests the stored equality filters; it does not certify policy classification or repair metadata.
PASS: combined doc_type='unknown'+kind='text', current=off, rows=5
PASS: combined doc_type='unknown'+kind='text', current=on, rows=5
PASS: both Firestore filter modes verified. Evidence: operator-evidence/firestore-combined-filters.json
Ran 8 tests in 0.005s
OK
Ran 11 tests in 0.006s
OK
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_the_rows_rebuild_the_tier.py

**HTML: Repair, expire, and what the records cost / The rows rebuild the tier**

Firestore holds everything the index holds and more: the text, the vector, the stamps and the flags. So when the index and the rows disagree, the index is rebuilt from the rows, and nothing in the rows is ever derived from the index. backfill() reads every current row (of one tenant, or all), rebuilds each datapoint with the row's own vector, re-embeds only a row whose stamp fails the check from lesson 3.3, and checkpoints the repaired vector back on the row with optimistic concurrency so that a concurrent writer is never overwritten. Its plan is the count you saw in 3.3; APPLY=1 is the repair, and the two states it exists for are a worker deployed before the index existed and an apply that lost its index and succeeded on the second run.

Run instruction: bash — the plan (read-only) and the repair (writes to the tier; run it only when the plan is not zero).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

46 code windows mapped: 12 IDE demo files, 1 shared setup blocks, 33 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
