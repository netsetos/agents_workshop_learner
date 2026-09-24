"""Lesson 1.2: demo 01 run the actual offline gate

Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

Run order inside this file:
1. Run the actual offline gate (source window plan-1)

Prerequisites: workshop setup; see this lesson README.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_run_the_actual_offline_gate(session):
    """Run Run the actual offline gate at this checkpoint.

    Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.command([sys.executable, "validate.py"])
    session.command([sys.executable, "evals/run_eval.py"])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_01_run_the_actual_offline_gate', step_01_run_the_actual_offline_gate),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
