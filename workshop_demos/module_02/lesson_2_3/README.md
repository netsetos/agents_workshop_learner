# Lesson 2.3: Check readiness, save progress and close the session

**Summary:** smoke green; zero instances after `make off`; a restored session.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_check_readiness_and_smoke.py

[Check readiness and smoke](demo_01_check_readiness_and_smoke.py) — required

Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_record_restart_inputs.py

[Record restart inputs](demo_02_record_restart_inputs.py) — required

Save non-secret project/region/kit identifiers and identify the kit's existing restart helper. Terraform state and credentials remain in their intended stores, not in a copied evidence JSON.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### finish_03_lower_service_floors_at_session_end.py

[Lower service floors at session end](finish_03_lower_service_floors_at_session_end.py) — cleanup

Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
