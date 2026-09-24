# Lesson 11.2: Configure and inspect durable conversation storage

**Summary:** the checkpoint tables; one row per thread. The files below follow the main HTML's runnable checkpoints and preserve its examples.

Source: [main lesson HTML](https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.2-durable-storage/Netsetos_GCP_Capstone_11.2_Durable_Storage_WIX.html); Git blob `8ff81098aa551cfdfcea7b74a70b6d674c710765`. Native Python cells can be stepped through in the IDE. Command workflows use the shared Bash/Make/gcloud helper because these are the kit's actual operations.

## Before running

Use `/home/user/rag-shell-venv/bin/python`, run `workshop_demos/setup/bootstrap.py`, and check `workshop_demos/setup/config/settings.local.json`. Open the learner kit root in your IDE. Each file can be Run independently; the session helper sets the working directory and carries this lesson's variables forward.

Run the required files in the table order. A failed step does not satisfy the next file's prerequisite. Read its saved output before continuing. Optional and recovery files are explicit choices; finish files are run at the end even though some HTML pages show their commands in the setup section. Do not use Run All.

**Execution is not live verification:** these examples have source/compile checks, not a recorded run against your GCP project. Numerical sample output is illustrative; use the checks and explanations below. Commands can change cloud resources as described by their HTML instruction.

## Required run order

| HTML | File | Instruction / purpose |
|---|---|---|
| s2 · window 3 | [demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py](demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own.py) | bash — run in the operator shell now, before the lesson's first step |
| s3 · window 7 | [demo_03_01_do_it_the_venv.py](demo_03_01_do_it_the_venv.py) | bash — run in the operator shell, in the kit (lesson 10.2's venv, with the Cloud SQL connector added) |
| s3 · window 9 | [demo_03_02_do_it_two_turns.py](demo_03_02_do_it_two_turns.py) | bash — run in the operator shell, in the kit (two turns, their checkpoints and versions counted; no model, no network) |
| s4 · window 14 | [demo_04_01_do_it.py](demo_04_01_do_it.py) | bash — run in the operator shell, in the kit (what holds the conversations on your lane) |
| s5 · window 16 | [demo_05_01_do_it.py](demo_05_01_do_it.py) | bash — run in the operator shell, in the kit (the tables, their rows, and one row per thread) |
| s6 · window 18 | [demo_06_01_do_it.py](demo_06_01_do_it.py) | bash — run in the operator shell, in the kit (the latest thread, step by step) |

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

**HTML: What a turn writes / Do it: the venv**

Do it: the venv

Run instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the Cloud SQL connector added).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
graph-venv ok: connector 1.22.0
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_03_02_do_it_two_turns.py

**HTML: What a turn writes / Do it: two turns**

Do it: two turns

Run instruction: bash — run in the operator shell, in the kit (two turns, their checkpoints and versions counted; no model, no network).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
a turn with no tool   +3 checkpoints, +2 versions of messages
a turn with retrieve  +5 checkpoints, +4 versions of messages
the messages channel, every version kept:
   version 1  1 message      211 bytes
   version 2  2 messages     472 bytes
   version 3  3 messages     687 bytes
   version 4  4 messages   1,001 bytes
   version 5  5 messages   2,720 bytes
   version 6  6 messages   2,981 bytes
   8,072 bytes kept, for a conversation whose latest version is 2,981 bytes
the ADK brain, given the lane's DSN, with google-adk and no SQLAlchemy - as the chat image has them:
WARNING documind.chat.brains: ADK DatabaseSessionService unavailable (The 'sqlalchemy' package is required to use this feature. Please install it by running: pip install google-adk[db]); using memory
   it keeps its sessions in InMemorySessionService
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_04_01_do_it.py

**HTML: What your lane runs / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (what holds the conversations on your lane).

Implementation: native Python in demonstrate(session). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
instance      documind-checkpoint: POSTGRES_16, db-f1-micro, zonal, 10 GB
  backups       off
  network       public IP on, 0 authorized networks
  databases     postgres, documind
  users         chat, postgres
  the DSN       secret documind-checkpoint-dsn, 1 version(s), the latest enabled
  setup job     last run 2026-09-12T10:41, succeeded 1
  images        job chat:3f9c2a1d0b7e, service chat:8e41d7c2f5a9 - DIFFERENT
  ADK sessions  in memory: ADK DatabaseSessionService unavailable (The 'sqlalchemy' packa
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_05_01_do_it.py

**HTML: The tables, and one row per thread / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the tables, their rows, and one row per thread).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
documind-ai-YOUR-ID:asia-south1:documind-checkpoint, database documind, as chat: 4 tables
  checkpoint_blobs           35 rows
  checkpoint_migrations      10 rows
  checkpoint_writes          37 rows
  checkpoints                29 rows
setup() has applied migrations 0 to 9
one row per thread, the latest first:
  acme  documind-ui-sa  lesson111-4242-b     8 checkpoints  step  6  2026-09-23T10:03
  acme  documind-ui-sa  lesson111-4242       6 checkpoints  step  4  2026-09-23T10:02
  acme  documind-ui-sa  smoke-langgraph      5 checkpoints  step  3  2026-09-23T09:16
  acme  documind-ui-sa  smoke-langchain      5 checkpoints  step  3  2026-09-23T09:15
  acme  documind-ui-sa  lesson103            5 checkpoints  step  3  2026-09-23T08:41
no ADK tables: the ADK brain's sessions are not in this database
```

If it fails, inspect this attempt under `workshop_demos/results/`, plus any report path printed by the example. Keep the session and its fixture files for recovery. Do not rerun a cloud mutation merely to obtain another output line.

### demo_06_01_do_it.py

**HTML: One thread, step by step / Do it**

Do it

Run instruction: bash — run in the operator shell, in the kit (the latest thread, step by step).

Implementation: the existing kit command workflow through session.shell(). The shared helper supplies credentials/settings, preserves this lesson's state and records failures; the file contains the actual example.

Expected shape from the HTML (actual counts/timing can differ):

```text
the latest thread, session lesson111-4242-b: its checkpoints in order
  step -1  input  messages unchanged
  step  0  loop   messages, version 1:    175 bytes
  step  1  loop   messages, version 2:    412 bytes
  step  2  input  messages unchanged
  step  3  loop   messages, version 3:    586 bytes
  step  4  loop   messages, version 4:    866 bytes
  step  5  loop   messages, version 5:  2,285 bytes
  step  6  loop   messages, version 6:  2,522 bytes
every version kept: 6,846 bytes; the latest alone: 2,522 bytes
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
