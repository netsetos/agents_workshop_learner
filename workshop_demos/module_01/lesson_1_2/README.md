# Lesson 1.2: Prove a first success and diagnose a first failure

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

This lesson has no authored main HTML. Its file numbers follow the explicitly listed course-plan experiments; they do not claim an HTML heading match. Run those plan steps in the order below.

| HTML section | File | What it demonstrates |
|---|---|---|
| Plan step 1 | [demo_01_run_the_actual_offline_gate.py](demo_01_run_the_actual_offline_gate.py) | Run the actual offline gate |
| Plan step 2 | [demo_02_break_an_assertion_in_memory.py](demo_02_break_an_assertion_in_memory.py) | Break an assertion in memory |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from a previous layout, run the lesson's finish file first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures. Old progress is never silently treated as completion of the new section files.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_run_the_actual_offline_gate.py

Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

**`step_01_run_the_actual_offline_gate(session)` — Run the actual offline gate / Run the actual offline gate**

Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

Operation: Course-plan experiment — local Python/kit inspection.

Expected shape, not a promised result:

```text
No failed checks; actual tool-dependent skips are reported.
```

### demo_02_break_an_assertion_in_memory.py

Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

**`step_01_break_an_assertion_in_memory(session)` — Break an assertion in memory / Break an assertion in memory**

Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

Operation: Course-plan experiment — local Python/kit inspection.

Expected shape, not a promised result:

```text
A named must_contain failure followed by a passing original row.
```

## Source and coverage

This lesson has no authored main HTML yet. These experiments come from the course plan and actual kit entry points, not an invented HTML sequence. `lesson_map.json` records their attribution.
