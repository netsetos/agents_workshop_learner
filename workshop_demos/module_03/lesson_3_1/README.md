# Lesson 3.1: Understand source, tenant, page and chunk contracts

**Summary:** a re-wrapped paragraph keeps its hash; a root-level object refused. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html); Git blob `9be3b915fa81df25778e35f6eaa825f0b365ec21`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_call_it_the_roster_from_the_shell_and_two_rest_c.py](demo_03_01_call_it_the_roster_from_the_shell_and_two_rest_c.py) | bash — run in the operator shell |
| s3 · window 10 | [demo_03_02_call_it_the_roster_from_the_shell_and_two_rest_c.py](demo_03_02_call_it_the_roster_from_the_shell_and_two_rest_c.py) | bash — run in the operator shell |
| s3 · window 12 | [demo_03_03_read_it_in_firestore.py](demo_03_03_read_it_in_firestore.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s4 · window 16 | [demo_04_01_call_it_the_bucket_then_the_api.py](demo_04_01_call_it_the_bucket_then_the_api.py) | bash — run in the operator shell |
| s4 · window 18 | [demo_04_02_read_it_in_firestore.py](demo_04_02_read_it_in_firestore.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s5 · window 21 | [demo_05_01_do_it_one_file_two_tenants.py](demo_05_01_do_it_one_file_two_tenants.py) | bash — run in the operator shell, in $DEMO_ROOT |
| s5 · window 23 | [demo_05_02_read_it_in_firestore.py](demo_05_02_read_it_in_firestore.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s6 · window 26 | [demo_06_01_call_it_a_question_and_the_page_on_each_citation.py](demo_06_01_call_it_a_question_and_the_page_on_each_citation.py) | bash — run in the operator shell |
| s6 · window 28 | [demo_06_02_read_it_in_firestore.py](demo_06_02_read_it_in_firestore.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |
| s7 · window 32 | [demo_07_01_call_it_a_filter_the_contract_allows_one_that_fi.py](demo_07_01_call_it_a_filter_the_contract_allows_one_that_fi.py) | bash — run in the operator shell |
| s7 · window 34 | [demo_07_02_read_it_in_firestore_the_twin_rows_from_step_5.py](demo_07_02_read_it_in_firestore_the_twin_rows_from_step_5.py) | bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash) |

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

### demo_03_01_call_it_the_roster_from_the_shell_and_two_rest_c.py

**HTML: Tenant: something you are, never something you send / Call it: the roster from the shell, and two REST calls**

First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_call_it_the_roster_from_the_shell_and_two_rest_c.py

**HTML: Tenant: something you are, never something you send / Call it: the roster from the shell, and two REST calls**

First, see how a tenant is created and a member added on your lane. make roster adds every address in MEMBERS to TENANT, then puts the UI's and the MCP server's accounts on all three golden tenants. Run it with your own address - $ME, the account gcloud is signed in as - once; a second run is harmless, it sets the same document again. Now the same question through the API three times. As the UI's account, which is on acme's roster, a query for acme is answered. As the outsider account - a fixture account that IAM admits into the service but no roster lists - the same request gets through Cloud Run's door and is then refused by the roster. With no token at all, Cloud Run's door refuses it before the API ever runs. Both refusals are 403s, so print the body too: the roster's refusal is a one-line JSON from the API, the door's is Cloud Run's HTML page. That difference is the tenant contract at work: the second caller got in, and was still told no.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...,"latency_ms":1840,"stages":{"retrieval_backend":"vector",...},"cache_hit":"none"}
HTTP 200
{"detail":"not a member of this tenant"}
HTTP 403
<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title> ...
HTTP 403
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_03_read_it_in_firestore.py

**HTML: Tenant: something you are, never something you send / Read it in Firestore**

Three reads, in a Python cell. The first lists acme's roster. The second is the UI's reverse lookup, run by you. The third is the tenant's settings document - the data_region: any the Documents page caption showed you.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com | {'email': 'documind-mcp-sa@...', 'added_at': DatetimeWithNanoseconds(...)}
documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com  | {'email': 'documind-ui-sa@...', 'added_at': DatetimeWithNanoseconds(...)}
you@your-company.com                                        | {'email': 'you@your-company.com', 'added_at': DatetimeWithNanoseconds(...)}
tenant for you: ['acme']
{'data_region': 'any', 'data_region_set_at': DatetimeWithNanoseconds(...)}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_call_it_the_bucket_then_the_api.py

**HTML: Source: the object path is the document's identity / Call it: the bucket, then the API**

The source lives in two places that must agree: the object in the bucket, and the ledger row. Cloud Storage numbers every rewrite of an object with a generation; the ledger records the generation it indexed. List the tenant's folder, describe one object, then ask the API for the ledger.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
gs://documind-ai-YOUR-ID-uploads/acme/annual_report_2026.md
gs://documind-ai-YOUR-ID-uploads/acme/code_on_wages_2019.pdf
gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md
...
1758540123456789    40096    text/markdown
{
    "tenant_id": "acme",
    "versions": 18,
    "fingerprint": "3fd2258b1264f744",
    "last_event": "ingest_ok",
    "data_region": "any",
    "sources": [
        {
            "name": "acme/hr_policy_2026.md",
            "status": "indexed",
            "doc_key": "acme_497809ff...",
            "generation": "1758540123456789",
            "chunks": 283,
            "reused": 0,
            "embedded": 283,
            "retired": 0,
            "effective_from": null,
            "embedding": "text-embedding-005@1",
            "indexed_at": "2026-09-22T...",
            "mirrored": {}
        },
        ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_read_it_in_firestore.py

**HTML: Source: the object path is the document's identity / Read it in Firestore**

Read it in Firestore

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme~annual_report_2026.md                    indexed  chunks=   4 gen=1758540... key=acme_6b0c2f4d1e...
acme~code_on_wages_2019.pdf                   indexed  chunks=  67 gen=1758540... key=acme_a3f9d0c7b2...
acme~hr_policy_2026.md                        indexed  chunks= 283 gen=1758540... key=acme_497809ff2a...
...
{'tenant_id': 'acme', 'name': 'acme/hr_policy_2026.md', 'gcs_uri': 'gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md',
 'doc_key': 'acme_497809ff...', 'generation': '1758540123456789', 'sha256': '497809ff...', 'chunks': 283,
 'effective_from': None, 'status': 'indexed', 'reused': 0, 'embedded': 283, 'retired': 0,
 'indexed_at': DatetimeWithNanoseconds(...), 'embedding_model': 'text-embedding-005', 'embedding_version': '1'}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it_one_file_two_tenants.py

**HTML: Version: the bytes decide, and the same file in two tenants proves it / Do it: one file, two tenants**

The UI wrote the object under your tenant's folder as its own service account; it never touched Firestore. The worker did the rest. "Upload complete" is not "indexed" - the page says so itself. From the shell, the same bytes to zeta. There is no UI session for zeta here, so the copy goes straight to the bucket, which is exactly what the UI does behind its Upload button.

Run instruction: bash — run in the operator shell, in $DEMO_ROOT.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
5b62d236e0c1...  evals/demo/gratuity_amendment_2026.md
acme    acme_5b62d236e0c1...    3    3
zeta    zeta_5b62d236e0c1...    3    3
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_02_read_it_in_firestore.py

**HTML: Version: the bytes decide, and the same file in two tenants proves it / Read it in Firestore**

The per-version claim lives in documents/{doc_key}. Build both keys from the local hash and read both claims. They differ in exactly one field.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
acme indexed 3 acme gs://documind-ai-YOUR-ID-uploads/acme/gratuity_amendment_2026.md
zeta indexed 3 zeta gs://documind-ai-YOUR-ID-uploads/zeta/gratuity_amendment_2026.md
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_call_it_a_question_and_the_page_on_each_citation.py

**HTML: Page and section: where inside the document / Call it: a question, and the page on each citation**

Call it: a question, and the page on each citation

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
A confirmed employee at grade E3 or above serves a notice period of 60 days [Source 1].
acme:497809ff...#1 hr_policy_2026.md page None | NP-03 — Notice period Confirmed employees at
acme:497809ff...#2 hr_policy_2026.md page None | PB-02 — Probation ...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_read_it_in_firestore.py

**HTML: Page and section: where inside the document / Read it in Firestore**

Read it in Firestore

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
hr_policy_2026.md -> 283 current chunks
     0  locator=preamble   page_start=None  section=None
     1  locator=NP-03      page_start=None  section=NP-03 — Notice period
     2  locator=PB-02      page_start=None  section=PB-02 — Probation
     3  locator=LV-01      page_start=None  section=LV-01 — Earned leave
     ...
code_on_wages_2019.pdf -> 67 current chunks
     0  locator=p1-0       page_start=1     section=None
     1  locator=p1-1       page_start=1     section=None
     2  locator=p2-0       page_start=2     section=None
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_call_it_a_filter_the_contract_allows_one_that_fi.py

**HTML: Chunk: the unit a question can find / Call it: a filter the contract allows, one that finds nothing, and one it refuses**

The API lets a caller narrow a search by kind or doc_type, because both are stamps on every row. It refuses any other key with a 400 that names the allowed ones - including tenant_id and current, which a caller might try to use as a filter and which are never theirs to set. One honest detail first: the worker stamps kind itself (text, or figure and segment for media), but it does not classify text documents, so every PDF and Markdown file it ingests carries doc_type: unknown. A doc_type: policy filter is allowed, and on your lane it matches nothing, so the API refuses to answer for lack of evidence. A filter is only as good as the stamp the writer put on the row.

Run instruction: bash — run in the operator shell.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
True ['acme:497809ff...#1', 'acme:497809ff...#2', 'acme:497809ff...#4']
False []
{"detail":"unknown filter key(s) tenant_id; allowed: doc_type, kind"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_02_read_it_in_firestore_the_twin_rows_from_step_5.py

**HTML: Chunk: the unit a question can find / Read it in Firestore: the twin rows from step 5**

The file you uploaded to both tenants is the cleanest proof of the two identities. Read its chunk rows on each side and compare: the same number of rows, no id in common, and the same set of hashes.

Run instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
rows: 3 3
ids in common: set()
same hashes: True
tenant_id              acme
doc_key                acme_5b62d236e0c1...
current                True
locator                preamble
chunk_hash             9c1e6f2a...
embedding_model        text-embedding-005
embedding_task_type    RETRIEVAL_DOCUMENT
schema_version         2
id: acme:5b62d236e0c1...#0 | vector dims: 768
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

36 code windows mapped: 13 IDE demo files, 1 shared setup blocks, 22 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
