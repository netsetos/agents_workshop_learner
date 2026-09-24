# Lesson 10.3: Diagnose tool arguments, access failures and timeouts

**Summary:** `refusals` non-empty; a timed-out tool reported. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.3-tool-failures/Netsetos_GCP_Capstone_10.3_Tool_Failures_WIX.html); Git blob `8c8650c57c7da57795b534e5c7b86462f1357233`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it_the_venv.py](demo_03_01_do_it_the_venv.py) | bash — run in the operator shell, in the kit (the venv from lesson 10.2, made if it is missing) |
| s3 · window 12 | [demo_03_02_do_it_five_failures.py](demo_03_02_do_it_five_failures.py) | bash — run in the operator shell, in the kit (five failures through the kit's LangChain brain; no model, no network beyond your machine) |
| s4 · window 15 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (three identities at the chat service's door) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (one question with and without a doc_type filter, then rag-api's rows) |

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

### demo_03_01_do_it_the_venv.py

**HTML: Five failures through the kit's LangChain brain / Do it: the venv**

Do it: the venv

Run instruction: bash — run in the operator shell, in the kit (the venv from lesson 10.2, made if it is missing).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
graph-venv ok: langchain 1.4.0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_five_failures.py

**HTML: Five failures through the kit's LangChain brain / Do it: five failures**

Do it: five failures

Run instruction: bash — run in the operator shell, in the kit (five failures through the kit's LangChain brain; no model, no network beyond your machine).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
blocked     0.0 s  refusals ['delete_document']
              result [error] {"error": "delete_document requires manual approval"}
  bad args    0.0 s  refusals ['calculate_processing_cost']
              result [error] Error invoking tool 'calculate_processing_cost' with kwargs {'total_page
  no such     0.0 s  refusals ['summon_rain']
              result [error] Error: summon_rain is not a valid tool, try one of [retrieve, calculate_
  timed out   0.5 s  refusals []
              result [success] {"error": "document search is unavailable", "citations": [], "answerable
  over budget 0.0 s  refusals []
              result [success] {"num_documents": 1, "total_pages": 283, "processing_type": "priority", 
  the log lines, from the guard, the adapter and the one retrieve():
    WARNING refused delete_document (blocked list)
    INFO    calculate_processing_cost took 0.00s (budget 10s)
    INFO    summon_rain took 0.00s (budget 30s)
    WARNING retrieve failed: HTTPConnectionPool(host='127.0.0.1', port=PORT): Read timed out. (
    INFO    retrieve took 0.51s
    INFO    retrieve took 0.51s
    WARNING rag-api query failed: document retrieval is unavailable
    INFO    retrieve took 0.51s (budget 30s)
    WARNING calculate_processing_cost took 0.00s (budget 0s)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Access failures at the chat service's door / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (three identities at the chat service's door).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
403  {"detail":"not a member of any tenant"}
  401  {"detail":"the bearer token carries no verified email"}
  200  {"answer":"Gratuity becomes payable after not less than five years of continuous service [1].","tool
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: An argument the corpus cannot honour / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (one question with and without a doc_type filter, then rag-api's rows).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
doc_type None     5 citations | answerable True | The total payable on invoice INV-2026-0412 is Rs 1,84,500 
  doc_type invoice  0 citations | answerable False | The corpus holds nothing near this question: no passage of
  pool 20  answerable True   backend vertex  Rs 0.2831
  pool  0  answerable False  backend none    Rs 0.0000
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

18 code windows mapped: 6 IDE demo files, 1 shared setup blocks, 11 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
