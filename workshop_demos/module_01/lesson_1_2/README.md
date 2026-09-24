# Lesson 1.2: Prove a first success and diagnose a first failure

**Summary:** ten PASS lines, one FAIL with its reason, green again.

**Source:** this lesson has no main HTML yet. These examples are authored from the existing course plan and actual kit entry points, not presented as an HTML conversion. Read the module prerequisites and each file's top summary before Run.

Use the existing rag-shell-venv interpreter and workshop setup. Each file is independent to Run/Debug; session state persists. Optional long-running services run in a separate console. Cloud-changing steps are separate from inspection/planning steps.

## Run order

### demo_01_run_the_actual_offline_gate.py

[Run the actual offline gate](demo_01_run_the_actual_offline_gate.py) — required

Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

Expected observation: No failed checks; actual tool-dependent skips are reported.

### demo_02_break_an_assertion_in_memory.py

[Break an assertion in memory](demo_02_break_an_assertion_in_memory.py) — required

Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

Expected observation: A named must_contain failure followed by a passing original row.

## Limits and evidence

These additions have offline source/runtime checks but have not been run against your GCP project. They do not replace the missing lesson prose, browser/UI observations, or a human review of the capstone rubric. Evidence is saved under workshop_demos/results; credentials are not copied into handover data.
