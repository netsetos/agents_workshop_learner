# Lesson 1.1: Reproduce the local environment and read the master diagram

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

This lesson has no authored main HTML. Its file numbers follow the explicitly listed course-plan experiments; they do not claim an HTML heading match. Run those plan steps in the order below.

| HTML section | File | What it demonstrates |
|---|---|---|
| Plan step 1 | [demo_01_inspect_the_workstation_and_corpus.py](demo_01_inspect_the_workstation_and_corpus.py) | Inspect the workstation and corpus |
| Plan step 2 | [demo_02_start_the_local_chat_lane.py](demo_02_start_the_local_chat_lane.py) | Start the local chat lane |
| Plan step 3 | [demo_03_ask_the_local_notice_period_question.py](demo_03_ask_the_local_notice_period_question.py) | Ask the local notice-period question |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from a previous layout, run the lesson's finish file first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures. Old progress is never silently treated as completion of the new section files.

## Finish and restore

- [setup/finish.py](setup/finish.py) — Stop only the background process group started by this lesson, after checking its PID, command and working directory. Preserve its log and lesson evidence.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_inspect_the_workstation_and_corpus.py

Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

**`step_01_inspect_the_workstation_and_corpus(session)` — Inspect the workstation and corpus / Inspect the workstation and corpus**

Locate the selected Python and required CLI tools, then read the source corpus that the local lane will index. This makes missing setup visible before starting a server.

Operation: Course-plan experiment — local Python/kit inspection.

Expected shape, not a promised result:

```text
The IDE interpreter and tool paths are visible; the ACME handbook exists.
```

### demo_02_start_the_local_chat_lane.py

Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

**`step_01_start_the_local_chat_lane(session)` — Start the local chat lane / Start the local chat lane**

Start the kit's local Ollama/Chroma service as an owned background process, save its PID and wait for its health endpoint. The next file can then run in another IDE process. The finish file stops this owned process.

Operation: Course-plan experiment — local Python/kit inspection.

Expected shape, not a promised result:

```text
The local chat server listens on port 8081. Ollama and the model must already be available; inspect the actual service output.
```

### demo_03_ask_the_local_notice_period_question.py

Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

**`step_01_ask_the_local_notice_period_question(session)` — Ask the local notice-period question / Ask the local notice-period question**

Send the course's notice-period question through the local lane. Check the returned citations instead of treating an HTTP success as proof of grounded retrieval.

Operation: Course-plan experiment — local Python/kit inspection.

Expected shape, not a promised result:

```text
A local answer with citations. Starting the server is a prerequisite even though it runs in another console.
```

### setup/finish.py

Stop only the background process group started by this lesson, after checking its PID, command and working directory. Preserve its log and lesson evidence.

**`step_01_stop_this_local_chat_service(session)` — Stop this local chat service / Stop this local chat service**

Stop only the background process group started by this lesson, after checking its PID, command and working directory. Preserve its log and lesson evidence.

Operation: Course-plan experiment — local Python/kit inspection.

## Source and coverage

This lesson has no authored main HTML yet. These experiments come from the course plan and actual kit entry points, not an invented HTML sequence. `lesson_map.json` records their attribution.
