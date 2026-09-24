# Lesson 2.2: Review and start the prepared deployment

**Summary:** seven services up; the UI behind IAP.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_check_the_saved_plan.py

[Check the saved plan](demo_01_check_the_saved_plan.py) — required

Validate the same saved plan from 2.1; never create a replacement plan implicitly at apply time.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_apply_and_deploy_the_prepared_kit.py

[Apply and deploy the prepared kit](demo_02_apply_and_deploy_the_prepared_kit.py) — required

Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect.

Expected observation: The actual kit deployment finishes; any failed build or readiness step stops the demo.

### demo_03_inspect_the_deployed_services.py

[Inspect the deployed services](demo_03_inspect_the_deployed_services.py) — required

List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
