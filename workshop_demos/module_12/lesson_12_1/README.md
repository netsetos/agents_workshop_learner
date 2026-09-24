# Lesson 12.1: Expose, discover and invoke MCP tools

**Summary:** `tools/list` names four; `retrieve` from a local client. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html); Git blob `b81be587a267019af54628b140280c63f1a4bd46`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 7 | [demo_03_01_do_it_fastmcp.py](demo_03_01_do_it_fastmcp.py) | bash — run in the operator shell, in the kit (fastmcp in the operator venv) |
| s3 · window 9 | [demo_03_02_do_it_what_the_server_declares.py](demo_03_02_do_it_what_the_server_declares.py) | bash — run in the operator shell, in the kit (the server imported and listed in memory; no network) |
| s4 · window 13 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the kit's server on your machine, in the background) |
| s5 · window 15 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (tools/list, raw) |
| s6 · window 17 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (tools/call from fastmcp's client) |
| s6 · window 19 | [demo_06_02_do_it_stop_the_server.py](demo_06_02_do_it_stop_the_server.py) | bash — run in the operator shell, in the kit (stop the server, read what it logged) |

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

### demo_03_01_do_it_fastmcp.py

**HTML: Expose: what the server declares / Do it: fastmcp**

Do it: fastmcp

Run instruction: bash — run in the operator shell, in the kit (fastmcp in the operator venv).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
fastmcp 3.4.7
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_what_the_server_declares.py

**HTML: Expose: what the server declares / Do it: what the server declares**

Do it: what the server declares

Run instruction: bash — run in the operator shell, in the kit (the server imported and listed in memory; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
server DocuMind, protocol 2025-11-25
instructions: DocuMind answers questions about a tenant's documents with citations. Use `ret...
retrieve: Retrieve grounded passages from DocuMind's corpus, with the...
   query            string          required            The question, in natural...
   doc_type         string          default 'all'       policy, contract, invoice,...
   top_k            integer         default 5           How many passages to return...
   tenant           string or null  default None        Only if you belong to several...
list_documents: What is in the caller's corpus: one row per uploaded document,...
   status           string          default 'indexed'   indexed, processing, failed,...
   tenant           string or null  default None        Only if you belong to several...
corpus_stats: Chunks and documents in the caller's corpus, by document type...
   tenant           string or null  default None        Only if you belong to several...
calculate_processing_cost: Estimate document processing cost in USD and INR.
   total_pages      integer         required            Total page count across all...
   num_documents    integer         default 1           How many documents those...
   processing_type  string          default 'standard'  Service tier - standard,...
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Start the server on your machine / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the kit's server on your machine, in the background).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"status":"ok","profile":"gcp","self_url":"http://localhost:8121"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Discover: tools/list on the wire / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (tools/list, raw).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
HTTP 200, text/event-stream, first line: event: message
tools/list: 4 tools
  retrieve                   needs query        may take doc_type, top_k, tenant
  list_documents             needs nothing      may take status, tenant
  corpus_stats               needs nothing      may take tenant
  calculate_processing_cost  needs total_pages  may take num_documents, processing_type
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: Invoke: retrieve from a local client / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (tools/call from fastmcp's client).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
retrieve: answerable True, 5 citations, confidence high
  'Gratuity becomes payable after not less than five years of continuous serv'
  [1] payment_of_gratuity_act_1972.pdf p.2  'rendered continuous service for not '
  [2] payment_of_gratuity_act_1972.pdf p.2  'the completion of continuous service'
  [3] payment_of_gratuity_act_1972.pdf p.2  'for every completed year of service '
an argument it refuses: doc_type must be one of ('policy', 'contract', 'invoice',
    'report', 'statute', 'guidance', 'form', 'research_paper') or all, not 'memo'
a tenant not on your roster: documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com
    is not on tenant 'initech''s roster
a token without an email lists 4 tools, and calls:
  not authenticated: the bearer token carries no verified email
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_stop_the_server.py

**HTML: Invoke: retrieve from a local client / Do it: stop the server**

Do it: stop the server

Run instruction: bash — run in the operator shell, in the kit (stop the server, read what it logged).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
mcp_call retrieve  tenant acme  caller documind-ui-sa  via iam  {'answerable': True, 'citations': 5, 'error': None}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

20 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 11 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
