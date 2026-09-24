# Lesson 11.1: Distinguish agent state, conversation history and knowledge

**Summary:** the memory-checkpointer warning line. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html); Git blob `6e59ae9a8bf97f0a9675aa8338318eaeca0e8a23`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 8 | [demo_03_01_do_it_the_venv.py](demo_03_01_do_it_the_venv.py) | bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and the SQLite checkpointer added) |
| s3 · window 10 | [demo_03_02_do_it_one_turn.py](demo_03_02_do_it_one_turn.py) | bash — run in the operator shell, in the kit (one turn taken apart; no model, no network beyond your machine) |
| s4 · window 13 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (the chat service's checkpointer with CHECKPOINT_DSN=memory, then a restart) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (one conversation, four brains, two sessions) |
| s6 · window 18 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the checkpointer your chat service is configured with) |

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

**HTML: One turn, taken apart / Do it: the venv**

Do it: the venv

Run instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and the SQLite checkpointer added).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
graph-venv ok: fastapi 0.141.1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_one_turn.py

**HTML: One turn, taken apart / Do it: one turn**

Do it: one turn

Run instruction: bash — run in the operator shell, in the kit (one turn taken apart; no model, no network beyond your machine).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. turn 1, the LangChain brain, thread acme:you@example.com:lesson111
   kept  HumanMessage What is the notice period?
   kept  AIMessage    retrieve(...)
   kept  ToolMessage  {"citations": [{"chunk_id": "acme:hr_policy_2026#NP-03", "quote"
   kept  AIMessage    Sixty days [1].
   the system prompt among them: False; checkpoints written: 5
2. turn 2, the LangGraph brain, the same thread: 6 messages, turn 1's among them
   the history still quotes: The notice period is 60 days.
   the corpus now says:      The notice period is 90 days.
3. a new session, the same person: 0 messages
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: The memory checkpointer, and the line it logs / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the chat service's checkpointer with CHECKPOINT_DSN=memory, then a restart).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
1. the chat service's own checkpointer, with CHECKPOINT_DSN=memory
WARNING documind.chat.agent: CHECKPOINT_DSN=memory: conversations die with the instance (8.5). Tests only - never a deployment.
   InMemorySaver: 2 messages in acme:you@example.com:lesson111
WARNING documind.chat.agent: CHECKPOINT_DSN=memory: conversations die with the instance (8.5). Tests only - never a deployment.
   after a restart: 0 messages
2. the laptop lane's SqliteSaver, a file (agent.py's DOCUMIND_PROFILE=local branch)
   after a restart: 2 messages
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: One conversation, four brains, two sessions / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (one conversation, four brains, two sessions).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
langchain session A  tools []            tamarind yes  "Got it: tamarind. I'll keep it for this "
  langgraph session A  tools []            tamarind yes  'You asked me to remember "tamarind".'
  adk       session A  tools []            tamarind no   "I don't have a word from you in this con"
  direct    session A  tools ['retrieve']  tamarind no   'The documents do not say which word you '
  langchain session B  tools []            tamarind no   "I don't have a word from you in this con"
  langchain session B  tools ['retrieve']  tamarind no   'Gratuity becomes payable after not less '
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: Which checkpointer your lane runs / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the checkpointer your chat service is configured with).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
CHECKPOINT_DSN  from the secret documind-checkpoint-dsn, version latest
  Cloud SQL       documind-ai-YOUR-ID:asia-south1:documind-checkpoint
  the memory warning in 30 days of the service's log: none
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
