# Lesson 18.4: Compare actual backends and verify shutdown behavior

**Summary:** the comparison table; zero GPU instances. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.4-compare-shutdown/Netsetos_GCP_Capstone_18.4_Compare_Shutdown_WIX.html); Git blob `e7f21fbe70306e17ea9822bec16d034a4a8176cc`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the script's own check of its maths; no network) |
| s3 · window 11 | [demo_03_02_do_it.py](demo_03_02_do_it.py) | bash — run in the operator shell, in the kit (reads the script, the tools module and config.yaml; no network) |
| s4 · window 14 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (20 questions to the API, then to three routes; the GPU wakes; about five minutes) |
| s5 · window 17 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit, when the comparison is done |
| s6 · window 20 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, at least 10 minutes after make off (reads Cloud Monitoring; changes nothing) |

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

### demo_03_01_do_it.py

**HTML: The table's maths, read / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the script's own check of its maths; no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend            rows  groundedness  cite-precision   p95 ms  Rs/1k queries
------------------------------------------------------------------------------
documind-general      3         0.500           0.667     1200          42.00
documind-slm          3         1.000           0.500     3100        1951.33

selftest OK - groundedness excludes refusal rows, precision is per cited chunk, p95 is the 95th latency, Rs/1k is mean cost x 1000
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it.py

**HTML: The table's maths, read / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (reads the script, the tools module and config.yaml; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
a row asks the gateway for a route by name: documind-general, documind-slm (make compare's default)
  its context: the citations' quotes of the API's own answer - retrieve() posts to /v1/query
  if that answer takes more than 20 s, the row's context is empty, and only the log says so
from the gateway's reply a row keeps the answer and the token counts, and reads neither the model that answered nor x-litellm-response-cost
its price is the script's own, by the route asked (USD a million tokens, in / out):
  documind-general    table  1.50 /  7.50   config.yaml  1.50 /  7.50
  documind-reasoning  table  1.50 /  7.50   config.yaml  2.00 / 12.00  <- no entry: documind-general's
  documind-slm        table 20.50 / 20.50   config.yaml 20.50 / 20.50
  documind-sensitive  table  1.50 /  7.50   config.yaml 20.50 / 20.50  <- no entry: documind-general's
  documind-inference  table  1.50 /  7.50   config.yaml  6.80 /  6.80  <- no entry: documind-general's
  documind-gke        table 20.50 / 20.50   config.yaml 20.50 / 20.50
p95 on 20 rows is sorted row 19 of 20: the slowest row never shows
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The comparison, with the actual backends / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (20 questions to the API, then to three routes; the GPU wakes; about five minutes).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
backend            rows  groundedness  cite-precision   p95 ms  Rs/1k queries
------------------------------------------------------------------------------
documind-general     20         1.000           1.000     1500          38.69
documind-slm         20         0.850           1.000     3100         262.77
documind-inference   20         0.850           1.000     3400          38.50

what answered each route - the gateway's reply, which the table does not keep:
  documind-general    gemini-3.6-flash            20 rows
  documind-slm        ollama_chat/documind-slm    20 rows
  documind-inference  ollama_chat/documind-slm    20 rows
the rupees for these rows, the gateway's price against the table's:
  documind-general    Rs   0.77   Rs   0.77
  documind-slm        Rs   5.26   Rs   5.26
  documind-inference  Rs   5.26   Rs   0.77
the slowest documind-slm row: 55.7 s; the p95 the table prints is row 19 of 20, 3.1 s
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Everything off / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit, when the comparison is done.

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
...
documind-slm scaled to zero
...
documind-gateway scaled to zero
...
vLLM workload removed; the cluster and any Standard lab node remain (gke.tf) - make down removes them
documind-slm: min-instances 0
documind-vllm: min-instances absent
documind-gateway: min-instances 0
documind-ui: min-instances 0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: Zero GPU instances / Do it**

Do it

Run instruction: bash — run in the operator shell, at least 10 minutes after make off (reads Cloud Monitoring; changes nothing).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
instance_count per service, 09:40 to 10:25 UTC, one point a minute (Cloud Monitoring):
  documind-slm      last instance at 10:13 UTC    a GPU service
  documind-vllm     no instance in the window     a GPU service
  documind-gateway  last instance at 10:09 UTC
  documind-ui       no instance in the window
GPU services with an instance in the last 3 minutes: none - zero GPU instances
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

21 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 13 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
