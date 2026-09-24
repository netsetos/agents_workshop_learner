# Lesson 14.2: Evaluate and gate the exact candidate revision

**Summary:** the candidate judged; its name recorded.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_create_the_recorded_candidate.py

[Create the recorded candidate](demo_01_create_the_recorded_candidate.py) — required

Create a no-traffic API revision with the kit's candidate target. The recorded revision name, not whatever is newest later, is the release identity.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_evaluate_the_exact_candidate.py

[Evaluate the exact candidate](demo_02_evaluate_the_exact_candidate.py) — required

Resolve the candidate tag and require it to name the recorded revision before the live gate. Save a project/region/revision-bound gate record only after the evaluator exits successfully.

Expected observation: A successful live gate tied to the same recorded candidate revision.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
