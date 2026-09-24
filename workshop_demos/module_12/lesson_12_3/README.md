# Lesson 12.3: Trace the implemented A2A peer and its permissions

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [setup/prepare.py](setup/prepare.py) | Prepare this lesson's saved settings and dependencies before its live experiments. |
| 2 | [demo_01_peer_contract_and_deployment.py](demo_01_peer_contract_and_deployment.py) | Inspect the implemented A2A peer and deploy/read its advertised contract. |
| 3 | [demo_02_peer_permissions.py](demo_02_peer_permissions.py) | Exercise the peer's actual access boundaries. |
| 4 | [demo_03_peer_task_and_trace.py](demo_03_peer_task_and_trace.py) | Submit the task and inspect the lane's corresponding records. |

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

### demo_01_peer_contract_and_deployment.py

Inspect the implemented A2A peer and deploy/read its advertised contract.

**`step_01_example(session)` — The peer's permissions, as the kit writes them / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the peer's permissions, as the kit writes them; no network).

Expected shape, not a promised result:

```text
documind-agent, as commands/lesson-8.4.sh deploys it:
  runs as documind-agent-sa  model gemini-3.6-flash  knows one URL: MCP_URL
  who may call it: documind-ui-sa, documind-chat-sa
  documind-agent-sa may call documind-mcp: True
  its project roles: aiplatform.user, logging.logWriter, cloudtrace.agent
  the rosters it is on: acme
  agent.py imports: __future__, google, logging, os, starlette, urllib, uvicorn
  the image copies: services/agent/requirements.txt, services/agent/
```

**`step_02_example(session)` — The card: refused without a token, read with one / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the card, without a token and with one).

Expected shape, not a promised result:

```text
the card without a token: HTTP 403
the card with a token: documind_peer, version 0.0.1
  answers at https://documind-agent-NUMBER.asia-south1.run.app over JSONRPC, A2A 1.0
  streaming False, input ['text/plain'], output ['text/plain']
  skills: model
```

### demo_02_peer_permissions.py

Exercise the peer's actual access boundaries.

**`step_01_example(session)` — The gate: make smoke-agent / Do it**

Do it

Operation: bash — run in the operator shell, in the kit (the module's A2A gate).

Expected shape, not a promised result:

```text
DocuMind A2A peer - live smoke test
  target: https://documind-agent-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  question: After how many years of continuous service does gratuity become payable?
  expected answer pattern: \b(?:five|5)(?:\s*\(\s*(?:five|5)\s*\))?[\s-]+years?\b
  [PASS] card refused without a token  status=403
  [PASS] agent card  name=documind_peer url=https://documind-agent-NUMBER.asia-south1.run.app skills=['documind_peer']
  [PASS] task answered  state=completed  'Gratuity is payable after not less than five years of continuous service [1]. Source: paym'
  [PASS] zeta refused by the roster  'The DocuMind server refused this: documind-agent-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com is not on tena'
  [PASS] outsider refused at the door  status=403
  --------------------------------------------------------
  5 passed, 0 failed
```

### demo_03_peer_task_and_trace.py

Submit the task and inspect the lane's corresponding records.

**`step_01_the_task(session)` — One task, traced / Do it: the task**

Do it: the task

Operation: bash — run in the operator shell, in the kit (one task, and its history).

Expected shape, not a promised result:

```text
a task, state completed, 4 messages in its history:
  user  text      'After how many years of continuous service does gratuity become pa'
  agent calls     retrieve(query='After how many years of continuous')
  agent receives  retrieve: 5 citations
  agent text      'Gratuity is payable after not less than five years of continuous s'
the answer: Gratuity is payable after not less than five years of continuous service [1]. Source
```

**`step_02_what_the_lane_saw(session)` — One task, traced / Do it: what the lane saw**

Do it: what the lane saw

Operation: bash — run in the operator shell, in the kit (who the lane saw).

Expected shape, not a promised result:

```text
documind-mcp - who asked it:
  retrieve        tenant acme   caller documind-agent-sa
documind-api - who it served:
  retrieve        tenant acme   user   documind-mcp-sa
```

### setup/finish.py

Run at the end, including after a failed demo. Restore the settings saved by this lesson and retain evidence.

**`step_01_which_store_answers_acme_pin_it_to_the_kit(session)` — Before you run anything: set up the shell / Which store answers acme? Pin it to the kit's own index for this lesson**

DocuMind can answer a tenant's questions from four stores: its own Vector Search index (the ANN tier), the Firestore rung beneath it, or two managed mirrors, Vertex AI RAG Engine and Vertex AI Search. make up pins acme to RAG Engine and zeta to Vertex AI Search so every store the course teaches is exercised. A managed store holds the text of every current version, but not the kit's addresses: its citations come back with ids like acme:acme_497809ff...#rag-532341da71fe, a page of null even for a PDF, and stages.retrieval_backend: rag_engine. This lesson is about the kit's own rows, so point acme at them for the duration and put the pin back at the end. Module 5 compares the four stores; Module 15 studies the mirrors. The pin back is a separate window on purpose: pasted together with the line above, it would put acme straight back on RAG Engine before the lesson began. Leave it until the lesson's last step is done.

Operation: bash — run in the operator shell when you finish the lesson, not now.

IDE adaptation: Run at lesson end despite its early HTML position, as the source label explicitly instructs.

## Source and coverage

[Reading guide](GUIDE.md) retains explanatory prose and UI instructions from the [main HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html). All 19 original windows are accounted for in `lesson_map.json`: executable steps, shared setup, or read-only examples. Reviewed source: `2d4eced3a474cc6fd41eaa365bb525484d950cc5`.
