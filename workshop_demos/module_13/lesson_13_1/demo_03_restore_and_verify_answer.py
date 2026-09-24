"""Lesson 13.1: demo 03 restore and verify answer

Put version 1 back and verify recovery through the same pipeline.

Run order inside this file:
1. Do it: put version 1 back (source window 20)

Prerequisites: demo_02_introduce_and_trace_wrong_answer.
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


# Original CLI workflow for step_01_put_version_1_back.
COMMANDS_01 = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/corpus/acme/hr_policy_2026.md
ask131 restored
GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py | tail -1

"""

def step_01_put_version_1_back(session):
    """Run Do it: put version 1 back at this checkpoint.

    Do it: put version 1 back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (version 1 back, the question again, the probe again).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_20', step_01_put_version_1_back),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
