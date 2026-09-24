"""Lesson 2.3: finish

Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

Run order inside this file:
1. Lower service floors at session end (source window plan-3)

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


def step_01_lower_service_floors_at_session_end(session):
    """Run Lower service floors at session end at this checkpoint.

    Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.command(["make", "off", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])
    session.command(["gcloud", "run", "services", "list", "--project", session.config.project, "--region", session.config.cloud_run_region, "--format=json"])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_finish_03_lower_service_floors_at_session_end', step_01_lower_service_floors_at_session_end),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=True)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
