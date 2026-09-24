# Lesson 11.3: Verify restart recovery and session isolation

**Summary:** the conversation continues after a redeploy; another user finds nothing. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.3-restart-isolation/Netsetos_GCP_Capstone_11.3_Restart_Isolation_WIX.html); Git blob `0f3fb29f23b886b2a6493c5a3474f442b8af3c17`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 9 | [demo_03_01_do_it_the_venv.py](demo_03_01_do_it_the_venv.py) | bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and 11.2's connector) |
| s3 · window 11 | [demo_03_02_do_it_eight_callers.py](demo_03_02_do_it_eight_callers.py) | bash — run in the operator shell, in the kit (the kit's chat app on your machine; no model, no network) |
| s4 · window 14 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (a word, a redeploy, the word again) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell (the address of your UI) |
| s6 · window 18 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the rows behind steps 4 and 5) |

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

**HTML: Isolation, on the kit's own app / Do it: the venv**

Do it: the venv

Run instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and 11.2's connector).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
graph-venv ok: fastapi 0.141.1
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_eight_callers.py

**HTML: Isolation, on the kit's own app / Do it: eight callers**

Do it: eight callers

Run instruction: bash — run in the operator shell, in the kit (the kit's chat app on your machine; no model, no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
alice gives the word, lesson113        200  Got it: saffron.
  alice asks for it                      200  You asked me to remember saffron.
  alice, a new session                   200  I have no word from you in this conversation.
  bob, her tenant, same session name     200  I have no word from you in this conversation.
  carol, another tenant, the same name   200  I have no word from you in this conversation.
  alice, the body naming zeta            200  You asked me to remember saffron.
  alice, a session id with a colon       422  String should match pattern '^[A-Za-z0-9_-]{1,64}$'
  the outsider                           403  not a member of any tenant
  a token that names nobody              401  the bearer token carries no verified email
  the threads the checkpointer holds:
    acme:alice@acme.example:lesson113
    acme:alice@acme.example:lesson113-b
    acme:bob@acme.example:lesson113
    zeta:carol@zeta.example:lesson113
  after a restart, alice asks again      200  I have no word from you in this conversation.
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: A conversation across a redeploy / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (a word, a redeploy, the word again).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
serving documind-chat-00007-x4q
  langchain lesson113-4242-langchain  "Got it: saffron. I'll keep it for this conve"
  adk       lesson113-4242-adk        "Got it: saffron. I'll keep it for this conve"
serving documind-chat-00008-m2k, redeployed at 2026-09-23T11:20:41Z
  langchain lesson113-4242-langchain  saffron yes  'You asked me to remember "saffron"'
  adk       lesson113-4242-adk        saffron no   "I don't have a word from you in th"
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: Another person finds nothing / Do it**

Do it

Run instruction: bash — run in the operator shell (the address of your UI).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
open https://documind-ui-NUMBER.asia-south1.run.app and sign in as you@example.com
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: The rows behind both / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the rows behind steps 4 and 5).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
lesson113-4242-langchain: 6 checkpoints, 3 before the redeploy and 3 after
  lesson113-4242-adk: no rows - the ADK brain keeps none
  threads of you: 1; the latest is session 3f9c2a1d0b7e, 3 checkpoints
  threads of documind-ui-sa: 2; the latest is session lesson113-4242-langchain, 6 checkpoints
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
