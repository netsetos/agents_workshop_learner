# Lesson 10.1: Understand tool contracts and the direct agent loop

**Summary:** `retrieve` in `tool_calls`. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html); Git blob `f1868f835bc67f911ec89f0027a86e55fa9969ab`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 6 | [demo_03_01_do_it_deploy.py](demo_03_01_do_it_deploy.py) | bash — run in the operator shell, in the kit (the chat service built and deployed in your region; several minutes) |
| s3 · window 8 | [demo_03_02_do_it_where_it_points_and_its_brains.py](demo_03_02_do_it_where_it_points_and_its_brains.py) | bash — run in the operator shell, in the kit (where the chat service points, and its brains) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (what the model reads of each tool; reads the source, installs nothing) |
| s5 · window 15 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (the one retrieve(), called from your shell as a roster member) |
| s6 · window 19 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (a small chat function, and the direct brain) |
| s7 · window 22 | [demo_07_01_do_it.py](demo_07_01_do_it.py) | bash — run in the operator shell, in the kit (the LangChain loop on the same question, then a cost question on both brains) |
| s8 · window 24 | [demo_08_01_the_rows_what_each_brain_cost_and_what_no_row_re.py](demo_08_01_the_rows_what_each_brain_cost_and_what_no_row_re.py) | bash — run in the operator shell, in the kit (the rows both services wrote since the retrieve cell; reads only) |

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

### demo_03_01_do_it_deploy.py

**HTML: The chat service, in your lane's region / Do it: deploy**

Do it: deploy

Run instruction: bash — run in the operator shell, in the kit (the chat service built and deployed in your region; several minutes).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> commands/lesson-12.8.sh (DEPLOY block)
Creating temporary archive of ... file(s) totalling ... MiB before compression.
...
DONE ... asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/chat:COMMIT
Deploying container to Cloud Run service [documind-chat] in project [documind-ai-YOUR-ID] region [asia-south1]
...
Service URL: https://documind-chat-NUMBER.asia-south1.run.app
Updated IAM policy for service [documind-chat].   (twice: documind-ui-sa, documind-outsider-sa)
... job exists - continuing   (or: Job [documind-checkpoint-setup] has successfully been created.)
Execution [documind-checkpoint-setup-xxxxx] has successfully completed.
...
>> you@example.com may mint tokens as documind-ui-sa
>> you@example.com may mint tokens as documind-outsider-sa
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_where_it_points_and_its_brains.py

**HTML: The chat service, in your lane's region / Do it: where it points, and its brains**

Do it: where it points, and its brains

Run instruction: bash — run in the operator shell, in the kit (where the chat service points, and its brains).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
RAG_API_URL https://documind-api-NUMBER.asia-south1.run.app | SELF_URL https://documind-chat-NUMBER.asia-south1.run.app | DOCUMIND_BRAIN langchain
{"status":"ok","profile":"gcp","brains":["langchain","langgraph","adk","direct"],"default_brain":"langchain"}
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The contract: what the model reads of each tool / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (what the model reads of each tool; reads the source, installs nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
retrieve(query: str, doc_type: str = 'all', top_k: int = 5)    hidden: runtime
      Retrieve grounded passages from DocuMind's corpus.
  calculate_processing_cost(total_pages: int, num_documents: int = 1, processing_type: str = 'standard')
      Estimate document processing cost in USD and INR.
  get_usage_stats(metric: str, days: int = 7)    hidden: runtime
      Get DocuMind RAG pipeline usage statistics.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The one retrieve(), from your shell / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the one retrieve(), called from your shell as a roster member).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
5 citations | answerable True | confidence high | 2.7 s
  first: {'chunk_id': 'acme:aaaaaaaa#0', 'page': 3, 'score': 0.94}
  rag-api's own answer: Gratuity is payable on termination after not less than five years of continuous service [1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The direct brain: one retrieve(), no loop / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a small chat function, and the direct brain).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
direct    tool_calls ['retrieve']  refusals []  citations 5  3180 ms
      Gratuity is payable on termination after not less than five years of continuous service [1].
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_07_01_do_it.py

**HTML: The loop: the model chooses its tools / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the LangChain loop on the same question, then a cost question on both brains).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
langchain tool_calls ['retrieve']  refusals []  citations 0  7240 ms
      After five years of continuous service, under the Payment of Gratuity Act, 1972.
  langchain tool_calls ['retrieve', 'calculate_processing_cost']  refusals []  citations 0  11350 ms
      At the priority tier (USD 0.12 a page), 283 pages cost USD 33.96, about Rs 2,886.60.
  direct    tool_calls ['retrieve']  refusals []  citations 3  3420 ms
      The documents give no per-page price for processing the handbook; the April invoice bills priori
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_08_01_the_rows_what_each_brain_cost_and_what_no_row_re.py

**HTML: The rows: what each brain cost, and what no row records / The rows: what each brain cost, and what no row records**

rag-api's row for every retrieve(), and the chat service's row for every turn. Each retrieve() posts to rag-api's /v1/query, and rag-api writes its usage row, now labelled with the brain that asked. The chat service writes a row of its own for each turn: the brain, the tenant, the user, the session, the time and the two lists. The cell reads both kinds since step 5, the shell's own retrieval included, labelled ui because it named no brain.

Run instruction: bash — run in the operator shell, in the kit (the rows both services wrote since the retrieve cell; reads only).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
rag-api, one row per retrieve():
    brain ui         in   1790  out   96  Rs 0.2894   2600 ms
    brain direct     in   1790  out   96  Rs 0.2894   2710 ms
    brain langchain  in   1812  out  101  Rs 0.2954   2840 ms
    brain langchain  in   1650  out   88  Rs 0.2665   2390 ms
    brain direct     in   1705  out   92  Rs 0.2760   2620 ms
  the chat service, one row per turn:
    brain direct     tool_calls ['retrieve']    3180 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain langchain  tool_calls ['retrieve']    7240 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain langchain  tool_calls ['retrieve', 'calculate_processing_cost']   11350 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain direct     tool_calls ['retrieve']    3420 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

25 code windows mapped: 9 IDE demo files, 1 shared setup blocks, 15 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
