# Lesson 12.3: Trace the implemented A2A peer and its permissions

**Summary:** the card refused without a token; `message/send` completes. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html); Git blob `2d4eced3a474cc6fd41eaa365bb525484d950cc5`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 10 | [demo_03_01_do_it.py](demo_03_01_do_it.py) | bash — run in the operator shell, in the kit (the peer's permissions, as the kit writes them; no network) |
| s4 · window 12 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the card, without a token and with one) |
| s5 · window 14 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (the module's A2A gate) |
| s6 · window 16 | [demo_06_01_do_it_the_task.py](demo_06_01_do_it_the_task.py) | bash — run in the operator shell, in the kit (one task, and its history) |
| s6 · window 18 | [demo_06_02_do_it_what_the_lane_saw.py](demo_06_02_do_it_what_the_lane_saw.py) | bash — run in the operator shell, in the kit (who the lane saw) |

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

**HTML: The peer's permissions, as the kit writes them / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the peer's permissions, as the kit writes them; no network).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The card: refused without a token, read with one / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the card, without a token and with one).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the card without a token: HTTP 403
the card with a token: documind_peer, version 0.0.1
  answers at https://documind-agent-NUMBER.asia-south1.run.app over JSONRPC, A2A 1.0
  streaming False, input ['text/plain'], output ['text/plain']
  skills: model
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The gate: make smoke-agent / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the module's A2A gate).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

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

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it_the_task.py

**HTML: One task, traced / Do it: the task**

Do it: the task

Run instruction: bash — run in the operator shell, in the kit (one task, and its history).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
a task, state completed, 4 messages in its history:
  user  text      'After how many years of continuous service does gratuity become pa'
  agent calls     retrieve(query='After how many years of continuous')
  agent receives  retrieve: 5 citations
  agent text      'Gratuity is payable after not less than five years of continuous s'
the answer: Gratuity is payable after not less than five years of continuous service [1]. Source
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_02_do_it_what_the_lane_saw.py

**HTML: One task, traced / Do it: what the lane saw**

Do it: what the lane saw

Run instruction: bash — run in the operator shell, in the kit (who the lane saw).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-mcp - who asked it:
  retrieve        tenant acme   caller documind-agent-sa
documind-api - who it served:
  retrieve        tenant acme   user   documind-mcp-sa
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

## Source coverage

19 code windows mapped: 7 IDE demo files, 1 shared setup blocks, 11 read-only excerpts/output blocks. `lesson_map.json` records every window and source line. Reading-only headings and UI observations remain in the source lesson; they are not turned into fake runnable examples.

## Helper functions

- `DemoSession`: resumes this lesson, checks prerequisite files and records attempts.
- `session.shell(code)`: invokes the existing CLI workflow, preserving named variables and shell functions between IDE runs.
- `session.service_environment(service, keys)`: reads the actual serving configuration as JSON, without saving secrets.
- `session.pin_vector()` / `restore_backend()`: save and restore the prior tenant setting when the lesson has the common vector setup.
- `session.command(args)`: runs a CLI argument list and retains its actual output/exit status.
