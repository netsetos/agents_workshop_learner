# Lesson 14.1: Build and deploy using keyless identity

**Summary:** a build and a deploy with no key.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_inspect_the_keyless_build_identity.py

[Inspect the keyless build identity](demo_01_inspect_the_keyless_build_identity.py) — required

Read the kit's workload-identity and build definitions. Verify repository/ref conditions in the real deployment configuration before submitting a build; no service-account key is generated.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_build_the_deployment_images.py

[Build the deployment images](demo_02_build_the_deployment_images.py) — required

Use the actual kit build target and the current authenticated identity. Record the build output and image tags; a successful local credential check alone does not prove a deployed GitHub workload-identity run.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
