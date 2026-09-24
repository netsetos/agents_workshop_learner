# Lesson 14.3: Promote, roll back and repair a controlled failure

**Summary:** rollback under two minutes; `make smoke-all` green.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_promote_the_gated_revision.py

[Promote the gated revision](demo_01_promote_the_gated_revision.py) — required

Require the saved gate from 14.2 to match this project, region and candidate, then use the kit's by-name promotion. The kit records the previous serving revision for rollback.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_roll_back_and_verify_recovery.py

[Roll back and verify recovery](demo_02_roll_back_and_verify_recovery.py) — required

Return traffic to the exact previous revision recorded by the kit. Measure actual elapsed time, then run smoke; a quick traffic command alone is not proof of a healthy recovered service.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
