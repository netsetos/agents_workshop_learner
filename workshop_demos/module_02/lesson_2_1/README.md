# Lesson 2.1: Understand the project, identities and resource map

**Summary:** `make plan` lists every resource; each service's account named.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_read_the_resource_and_identity_definitions.py

[Read the resource and identity definitions](demo_01_read_the_resource_and_identity_definitions.py) — required

Read the actual Terraform resources and service-account names instead of assuming the deployed project has every optional service. The saved plan is the next checkpoint.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_create_a_saved_infrastructure_plan.py

[Create a saved infrastructure plan](demo_02_create_a_saved_infrastructure_plan.py) — required

Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

Expected observation: A saved checked plan and its resource changes; inspect them before the apply lesson.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
