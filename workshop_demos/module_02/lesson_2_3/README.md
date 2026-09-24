# Lesson 2.3: Check readiness, save progress and close the session

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [demo_01_check_readiness_and_smoke.py](demo_01_check_readiness_and_smoke.py) | Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL. |
| 2 | [demo_02_record_restart_inputs.py](demo_02_record_restart_inputs.py) | Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Finish and restore

- [setup/finish.py](setup/finish.py) — Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_check_readiness_and_smoke.py

Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL.

**`step_01_check_readiness_and_smoke(session)` — Check readiness and smoke / Check readiness and smoke**

Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL.

Operation: Course-plan experiment — live deployment.

### demo_02_record_restart_inputs.py

Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

**`step_01_record_restart_inputs(session)` — Record restart inputs / Record restart inputs**

Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

Operation: Course-plan experiment — local Python/kit inspection.

### setup/finish.py

Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

**`step_01_lower_service_floors_at_session_end(session)` — Lower service floors at session end / Lower service floors at session end**

Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

Operation: Course-plan experiment — live deployment.

## Source and coverage

This lesson has no authored main HTML yet. These experiments come from the course plan and actual kit entry points, not an invented HTML sequence. `lesson_map.json` records their attribution.
