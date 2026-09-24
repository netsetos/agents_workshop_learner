"""Lesson 14.3: demo 02 roll back and verify recovery

Return traffic to the exact previous revision recorded by the kit. Measure actual elapsed time, then run smoke; a quick traffic command alone is not proof of a healthy recovered service.

Run order inside this file:
1. Roll back and verify recovery (source window plan-2)

Prerequisites: demo_01_promote_the_gated_revision.
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


def step_01_roll_back_and_verify_recovery(session):
    """Run Roll back and verify recovery at this checkpoint.

    Return traffic to the exact previous revision recorded by the kit. Measure actual elapsed time, then run smoke; a quick traffic command alone is not proof of a healthy recovered service.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys, time
    started = time.perf_counter()
    session.command(["make", "rollback", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])
    print("Rollback command seconds:", round(time.perf_counter() - started, 2))
    session.command(["make", "smoke", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_02_roll_back_and_verify_recovery', step_01_roll_back_and_verify_recovery),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
