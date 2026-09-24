# Lesson 10.4: Compare the LangChain and ADK adapters

**Summary:** four brains on `/health`; four cost lines. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.4-adapters/Netsetos_GCP_Capstone_10.4_Adapters_WIX.html); Git blob `4d85e128644454856f18a930ac9e3dfcec8d55e1`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it_the_venv.py](demo_03_01_do_it_the_venv.py) | bash — run in the operator shell, in the kit (lesson 10.2's venv, with google-adk added) |
| s3 · window 12 | [demo_03_02_do_it_side_by_side.py](demo_03_02_do_it_side_by_side.py) | bash — run in the operator shell, in the kit (the two adapters side by side; no model, no network beyond your machine) |
| s4 · window 15 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (/health, then the module's gate) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain) |
| s6 · window 19 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted) |

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

**HTML: Two adapters over one tool, side by side / Do it: the venv**

Do it: the venv

Run instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with google-adk added).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
graph-venv ok: google-adk 2.8.0 langchain 1.4.0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_side_by_side.py

**HTML: Two adapters over one tool, side by side / Do it: side by side**

Do it: side by side

Run instruction: bash — run in the operator shell, in the kit (the two adapters side by side; no model, no network beyond your machine).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. what each model is shown for retrieve (* = required)
   langchain query*, doc_type, top_k                                465 characters
   adk       query*, tenant_id*, top_k, doc_type, assertion, brain  2,572 characters
   langchain tools: retrieve, calculate_processing_cost, get_usage_stats
   adk tools:       retrieve, calculate_processing_cost
2. one retrieve(); the ADK model writes tenant_id "globex" and assertion "anything"
   langchain rag-api got tenant acme, brain langchain, assertion header None
             the model read: citations, answerable, confidence
   adk       rag-api got tenant acme, brain adk, assertion header 'anything'
             the model read: citations, answerable, confidence, answer
3. three calls that go wrong
   delete_document(doc="x")
     langchain [error] {"error": "delete_document requires manual approval"}
               refusals ['delete_document']
     adk       the turn raises ValueError: Tool 'delete_document' not found.
   calculate_processing_cost(total_pages="many")
     langchain [error] Error invoking tool 'calculate_processing_cost' with kwargs
               {'total_pages': 'many'} with error: total_pages: Input should be a valid
               [...]
               refusals ['calculate_processing_cost']
     adk       the turn raises TypeError: '<=' not supported between instances of 'str' and
               'int'
   calculate_processing_cost(total_pages=10, processing_type="express")
     langchain [success] {"num_documents": 1, "total_pages": 10, "processing_type":
               "express", "rate_per_page": 0.05, "cost_usd": 0.5, "cost_inr": 42.5}
               refusals []
     adk       the turn raises ValueError: unknown tier 'express'; expected one of ['bulk',
               'priority', 'standard']
4. ADK's sessions with no CHECKPOINT_DSN: InMemorySessionService, at most 12 model calls a turn
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: Four brains on /health, and the module's gate / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (/health, then the module's gate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
{"status":"ok","profile":"gcp","brains":["langchain","langgraph","adk","direct"],"default_brain":"langchain"}
  DocuMind chat - live smoke test
  target: https://documind-chat-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] health  profile=gcp default=langchain
  [PASS] brain direct  3120 ms  tools=['retrieve']  'Gratuity becomes payable after not less than five years of c'
  [PASS] brain langchain  11840 ms  tools=['retrieve']  'Gratuity becomes payable once you have rendered at least fiv'
  [PASS] brain langgraph  9730 ms  tools=['retrieve']  'Gratuity is payable after at least five years of continuous '
  [PASS] brain adk  14260 ms  tools=['retrieve']  'After five years of continuous service, gratuity becomes pay'
  [PASS] outsider refused  status=403 not a member of any tenant
  --------------------------------------------------------
  6 passed, 0 failed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Four cost lines, as rag-api's rows draw them / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
direct    1 retrieve()  in  2,561  out   68  Rs 0.3699
  langchain 1 retrieve()  in  2,498  out   64  Rs 0.3593
  langgraph 1 retrieve()  in  2,504  out   66  Rs 0.3613
  adk       1 retrieve()  in  2,537  out   71  Rs 0.3687
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The half the rows cannot see / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
langchain 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  langgraph 2 model calls  in  1,429  out    51 (thinking     0)  Rs 0.2147
  adk       2 model calls  in  2,477  out    47 (thinking     0)  Rs 0.3458
the four cost lines, whole: the brain's own model calls + rag-api's, from step 5
  direct    Rs 0.0000 + Rs 0.3699 = Rs 0.3699
  langchain Rs 0.2147 + Rs 0.3593 = Rs 0.5740
  langgraph Rs 0.2147 + Rs 0.3613 = Rs 0.5760
  adk       Rs 0.3458 + Rs 0.3687 = Rs 0.7145
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

20 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 12 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
