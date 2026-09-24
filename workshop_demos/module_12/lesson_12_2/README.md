# Lesson 12.2: Deploy MCP and verify authorized access

**Summary:** `make smoke-mcp` green; another tenant refused. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html); Git blob `f1670b27aee13cd8c5083246399ffea5d2a1ac20`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the door as the kit writes it down; no network) |
| s4 · window 11 | [demo_04_01_do_it_build_and_deploy.py](demo_04_01_do_it_build_and_deploy.py) | bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers) |
| s4 · window 13 | [demo_04_02_do_it_read_it_back.py](demo_04_02_do_it_read_it_back.py) | bash — run in the operator shell, in the kit (the service as deployed, against the script) |
| s5 · window 15 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (the module's gate) |
| s6 · window 18 | [demo_06_01_do_it_every_door.py](demo_06_01_do_it_every_door.py) | bash — run in the operator shell, in the kit (one call at each door) |
| s6 · window 20 | [demo_06_02_do_it_both_sides.py](demo_06_02_do_it_both_sides.py) | bash — run in the operator shell, in the kit (both sides of the answered calls) |

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

**HTML: The door, as the kit writes it down / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the door as the kit writes it down; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-mcp, as commands/lesson-7.2.sh deploys it:
  --no-allow-unauthenticated  --ingress=all  --min-instances=${MIN_INSTANCES:-0}  --service-account=documind-mcp-sa
  SELF_URL=https://documind-mcp-$PROJECT_NUMBER.${REGION:-us-central1}.run.app
  RAG_API_URL=https://documind-api-$PROJECT_NUMBER.${REGION:-us-central1}.run.app
  FASTMCP_STATELESS_HTTP=true
  RAG_TIMEOUT_S=90
who may call it (roles/run.invoker): documind-ui-sa, documind-agent-sa, documind-outsider-sa
the tenants each caller may read through it (lane.py's roster_plan):
  documind-ui-sa         acme, zeta, globex
  documind-agent-sa      acme
  documind-outsider-sa   none
the account rag-api sees for every MCP retrieval: documind-mcp-sa, on acme, zeta, globex
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it_build_and_deploy.py

**HTML: Deploy, and read it back / Do it: build and deploy**

Do it: build and deploy

Run instruction: bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
>> building asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/mcp:COMMIT from services/mcp
Creating temporary archive of ... file(s) totalling ... MiB before compression.
...
DONE ... asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/mcp:COMMIT
>> commands/lesson-7.2.sh (DEPLOY block)
Deploying container to Cloud Run service [documind-mcp] in project [documind-ai-YOUR-ID] region [asia-south1]
...
Service URL: https://documind-mcp-NUMBER.asia-south1.run.app
Updated IAM policy for service [documind-mcp].   (three times: ui, agent, outsider)
...
>> you@example.com may mint tokens as documind-ui-sa
>> you@example.com may mint tokens as documind-outsider-sa
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_02_do_it_read_it_back.py

**HTML: Deploy, and read it back / Do it: read it back**

Do it: read it back

Run instruction: bash — run in the operator shell, in the kit (the service as deployed, against the script).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
serving     documind-mcp-00004-k7w at https://documind-mcp-NUMBER.asia-south1.run.app
  runs as     documind-mcp-sa
  ingress     all
  SELF_URL    https://documind-mcp-NUMBER.asia-south1.run.app
  invokers    documind-agent-sa, documind-outsider-sa, documind-ui-sa
  the script  documind-agent-sa, documind-outsider-sa, documind-ui-sa - the same
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The gate: make smoke-mcp / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the module's gate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
DocuMind MCP - live smoke test
  target: https://documind-mcp-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] health  {"status":"ok","profile":"gcp","self_url":"https://documind-mcp-NUMBER.asia-south1.run.app"}
  [PASS] tools/list  ['calculate_processing_cost', 'corpus_stats', 'list_documents', 'retrieve']
  [PASS] retrieve  answerable=True citations=5  'Five years of continuous service [1].'
  [PASS] outsider refused  documind-outsider-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com is not on tenant 'acme''s roster
  --------------------------------------------------------
  4 passed, 0 failed
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_every_door.py

**HTML: One call at each door, and both sides of the answer / Do it: every door**

Do it: every door

Run instruction: bash — run in the operator shell, in the kit (one call at each door).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
no token                              HTTP 403 - Cloud Run, before the server ran
  ui-sa, a token for rag-api's address  HTTP 401 - Cloud Run, before the server ran
  ui-sa, no email in the token          tool error - not authenticated: the bearer token carries no verified email
  the outsider, naming acme             tool error - documind-outsider-sa is not on tenant 'acme''s roster
  ui-sa, naming zeta                    answered - answerable True, 5 citations
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_both_sides.py

**HTML: One call at each door, and both sides of the answer / Do it: both sides**

Do it: both sides

Run instruction: bash — run in the operator shell, in the kit (both sides of the answered calls).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-mcp, a line per answered call - who asked:
  retrieve  tenant acme   caller documind-ui-sa
  retrieve  tenant zeta   caller documind-ui-sa
documind-api, a row per retrieval it served for the MCP server - who it served:
  retrieve  tenant acme   user   documind-mcp-sa
  retrieve  tenant zeta   user   documind-mcp-sa
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

21 code windows mapped: 8 IDE demo files, 1 shared setup blocks, 12 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
