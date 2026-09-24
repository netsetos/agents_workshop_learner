# Lesson 12.2: Deploy MCP and verify authorized access

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_mcp_identity_and_deployment.py](demo_01_mcp_identity_and_deployment.py) | Read the MCP identity, build/deploy the server and inspect the deployed configuration. |
| 3 | [demo_02_invoke_deployed_mcp.py](demo_02_invoke_deployed_mcp.py) | Discover and invoke tools on the deployed server. |
| 4 | [demo_03_mcp_access_boundaries.py](demo_03_mcp_access_boundaries.py) | Test every admission/authorization gate and read both sides of the call. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### setup/prepare.py

Prepare this lesson's saved settings and dependencies before its live experiments.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors.

Operation: bash — run in the operator shell now, before the lesson's first step.

IDE adaptation: Save the actual previous pin before selecting vector; cleanup restores it instead of assuming rag_engine.

Expected shape, not a promised result:

```text
acme: retrieval_backend=vector
```

### demo_01_mcp_identity_and_deployment.py

Read the MCP identity, build/deploy the server and inspect the deployed configuration.

**`step_01_example(session)` — The door, as the kit writes it down / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the door as the kit writes it down; no network).

Expected shape, not a promised result:

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

**`step_02_build_and_deploy(session)` — Deploy, and read it back / Do it: build and deploy**

Do it: build and deploy

Operation: bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers).

Expected shape, not a promised result:

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

**`step_03_read_it_back(session)` — Deploy, and read it back / Do it: read it back**

Do it: read it back

Operation: bash — run in the operator shell, in the kit (the service as deployed, against the script).

Expected shape, not a promised result:

```text
serving     documind-mcp-00004-k7w at https://documind-mcp-NUMBER.asia-south1.run.app
  runs as     documind-mcp-sa
  ingress     all
  SELF_URL    https://documind-mcp-NUMBER.asia-south1.run.app
  invokers    documind-agent-sa, documind-outsider-sa, documind-ui-sa
  the script  documind-agent-sa, documind-outsider-sa, documind-ui-sa - the same
```

### demo_02_invoke_deployed_mcp.py

Discover and invoke tools on the deployed server.

**`step_01_example(session)` — The gate: make smoke-mcp / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the module's gate).

Expected shape, not a promised result:

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

### demo_03_mcp_access_boundaries.py

Test every admission/authorization gate and read both sides of the call.

**`step_01_every_door(session)` — One call at each door, and both sides of the answer / Do it: every door**

Do it: every door

Operation: bash — run in the operator shell, in the kit (one call at each door).

Expected shape, not a promised result:

```text
no token                              HTTP 403 - Cloud Run, before the server ran
  ui-sa, a token for rag-api's address  HTTP 401 - Cloud Run, before the server ran
  ui-sa, no email in the token          tool error - not authenticated: the bearer token carries no verified email
  the outsider, naming acme             tool error - documind-outsider-sa is not on tenant 'acme''s roster
  ui-sa, naming zeta                    answered - answerable True, 5 citations
```

**`step_02_both_sides(session)` — One call at each door, and both sides of the answer / Do it: both sides**

Do it: both sides

Operation: bash — run in the operator shell, in the kit (both sides of the answered calls).

Expected shape, not a promised result:

```text
documind-mcp, a line per answered call - who asked:
  retrieve  tenant acme   caller documind-ui-sa
  retrieve  tenant zeta   caller documind-ui-sa
documind-api, a row per retrieval it served for the MCP server - who it served:
  retrieve  tenant acme   user   documind-mcp-sa
  retrieve  tenant zeta   user   documind-mcp-sa
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html). All 21 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `f1670b27aee13cd8c5083246399ffea5d2a1ac20`.
