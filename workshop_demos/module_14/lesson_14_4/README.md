# Lesson 14.4: Complete the independent capstone and operational handover

**Summary:** the five rubric criteria scored.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_run_the_operational_gate.py

[Run the operational gate](demo_01_run_the_operational_gate.py) — required

Run the real smoke-all gate and preserve its output, including unavailable optional services and failures. Do not mark the capstone complete merely because earlier individual demos ran.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

### demo_02_write_an_evidence_handover.py

[Write an evidence handover](demo_02_write_an_evidence_handover.py) — required

Summarize actual lesson attempts and retain the exact candidate gate, failures and evidence locations. This is an evidence index for a human capstone review, not an automatic rubric score.

Expected observation: Inspect the actual command/read output; a nonzero exit stops the attempt.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
