# Lesson 2.2: Review and start the prepared deployment

## What to run

Run one complete experiment at a time with the IDE Run/Debug button. Keep the files in the order below; do not use Run All.

| Order | File | What it demonstrates |
|---|---|---|
| 1 | [demo_01_check_the_saved_plan.py](demo_01_check_the_saved_plan.py) | Validate the same saved plan from 2.1; never create a replacement plan implicitly at apply time. |
| 2 | [demo_02_apply_and_deploy_the_prepared_kit.py](demo_02_apply_and_deploy_the_prepared_kit.py) | Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect. |
| 3 | [demo_03_inspect_the_deployed_services.py](demo_03_inspect_the_deployed_services.py) | List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment. |

## Before starting

Select `/home/user/rag-shell-venv/bin/python`. Run `workshop_demos/setup/bootstrap.py` once and edit `workshop_demos/setup/config/settings.local.json`. The helper sets the working directory and resolves project/API settings; terminal exports are unnecessary.

The shared workshop setup and the deployed/local inputs described in the reading guide.

Each demo contains named Python functions in teaching order. Set breakpoints in those functions. Kit CLI operations stay visible as command constants; Python calls use this interpreter. Repeated session, authentication, configuration and command handling live in `workshop_demos/setup/workshop_helpers/`.

## Resume and recovery

Completed functions are saved and skipped when an unfinished demo is run again. A failed/interrupted function may have made partial changes: inspect its attempt under `workshop_demos/results/`, repair the cause, then set `RETRY_FAILED_STEP = True` in that demo to retry only unfinished functions. `REPEAT = True` deliberately replays the entire file. It is not a repair shortcut.

Manual browser actions and long asynchronous waits pause at a named checkpoint. Type `done` only after performing the action. Stopping there retains completed steps so they are not repeated on resume. This acknowledgement alone is not proof that indexing/monitoring succeeded; inspect the following read.

After upgrading from the old per-window layout, finish the saved run first, then set this lesson number in `workshop_demos/setup/start_new_session.py` and run it. It archives evidence; it does not delete your fixtures.

## Conditional recovery

- [recovery/grant_the_build_account_what_a_build_needs.py](recovery/grant_the_build_account_what_a_build_needs.py) — Only if the build stopped at storage.objects.get: 'could not resolve source' and a 403 naming the Compute Engine default account. The kit names no account for Cloud Build, so a build runs as the project's default build account, and in an organization created on or after 3 May 2024 that account is created without the Editor role. Run once, as a project owner: read access to its source in the PROJECT_cloudbuild bucket only, push access to the documind repository, and log writing. Not Editor or roles/cloudbuild.builds.builder: granted on the project, either one can read, write and delete every object in every bucket, the uploads bucket included. IAM applies a grant in about two minutes, sometimes seven or more; then run the build again.

## Functions, observations and effects

The numbered functions below correspond to the source examples. Numerical sample output is illustrative. These files have offline/source checks; live IAM, ingestion, model output and deployed resources must be verified in your workstation.

### demo_01_check_the_saved_plan.py

Validate the same saved plan from 2.1; never create a replacement plan implicitly at apply time.

**`step_01_check_the_saved_plan(session)` — Check the saved plan / Check the saved plan**

Validate the same saved plan from 2.1; never create a replacement plan implicitly at apply time.

Operation: Course-plan experiment — live deployment.

### demo_02_apply_and_deploy_the_prepared_kit.py

Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect.

**`step_01_apply_and_deploy_the_prepared_kit(session)` — Apply and deploy the prepared kit / Apply and deploy the prepared kit**

Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect.

Operation: Course-plan experiment — live deployment.

Expected shape, not a promised result:

```text
The actual kit deployment finishes; any failed build or readiness step stops the demo.
```

### demo_03_inspect_the_deployed_services.py

List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

**`step_01_inspect_the_deployed_services(session)` — Inspect the deployed services / Inspect the deployed services**

List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

Operation: Course-plan experiment — live deployment.

### recovery/grant_the_build_account_what_a_build_needs.py

Only if the build stopped at storage.objects.get: 'could not resolve source' and a 403 naming the Compute Engine default account. The kit names no account for Cloud Build, so a build runs as the project's default build account, and in an organization created on or after 3 May 2024 that account is created without the Editor role. Run once, as a project owner: read access to its source in the PROJECT_cloudbuild bucket only, push access to the documind repository, and log writing. Not Editor or roles/cloudbuild.builds.builder: granted on the project, either one can read, write and delete every object in every bucket, the uploads bucket included. IAM applies a grant in about two minutes, sometimes seven or more; then run the build again.

**`step_01_grant_the_build_account_what_a_build_needs(session)` — Grant the build account what a build needs / Grant the build account what a build needs**

Only if the build stopped at storage.objects.get: 'could not resolve source' and a 403 naming the Compute Engine default account. The kit names no account for Cloud Build, so a build runs as the project's default build account, and in an organization created on or after 3 May 2024 that account is created without the Editor role. Run once, as a project owner: read access to its source in the PROJECT_cloudbuild bucket only, push access to the documind repository, and log writing. Not Editor or roles/cloudbuild.builds.builder: granted on the project, either one can read, write and delete every object in every bucket, the uploads bucket included. IAM applies a grant in about two minutes, sometimes seven or more; then run the build again.

Operation: Course-plan experiment — live deployment.

Expected shape, not a promised result:

```text
Three bindings added for the account the 403 named; the next build reads its source.
```

## Source and coverage

This lesson has no authored main HTML yet. These experiments come from the course plan and actual kit entry points, not an invented HTML sequence. `lesson_map.json` records their attribution.
