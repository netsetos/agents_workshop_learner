# Lesson 2.1: Understand the project, identities and resource map

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [demo_01_read_the_resource_and_identity_definitions.py](demo_01_read_the_resource_and_identity_definitions.py) | Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint. |
| 2 | [demo_02_create_a_saved_infrastructure_plan.py](demo_02_create_a_saved_infrastructure_plan.py) | Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_read_the_resource_and_identity_definitions.py

Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

**`step_01_read_the_resource_and_identity_definitions(session)` — Read the resource and identity definitions / Read the resource and identity definitions**

Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

Operation: Course-plan experiment — local Python/kit inspection.

### demo_02_create_a_saved_infrastructure_plan.py

Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

**`step_01_create_a_saved_infrastructure_plan(session)` — Create a saved infrastructure plan / Create a saved infrastructure plan**

Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

Operation: Course-plan experiment — live deployment.

Expected shape, not a promised result:

```text
A saved checked plan and its resource changes; inspect them before the apply lesson.
```

## Source and coverage

This lesson has no authored main HTML yet. These experiments come from the course plan and actual kit entry points, not an invented HTML sequence. `lesson_map.json` records their attribution.
