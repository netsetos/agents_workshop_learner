"""Lesson 4.2: demo 03 failing gate and undo

Observe the expected live-gate failure, undo the revision and prove recovery.

Run order inside this file:
1. Do it: the live gate, red (source window 21)
2. The undo, then the gate, green (source window 23)

Prerequisites: demo_02_reissue_and_measure.
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


def step_01_the_live_gate_red(session):
    """Run Do it: the live gate, red at this checkpoint.

    Ten questions to the API, each a generation call: a few rupees at most. The target mints two identity tokens, the UI's account as the member and the outsider's for the isolation rows, which is why it takes a moment to start.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (ten questions; a few rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    from workshop_helpers.gates import live_gate
    live_gate(session, report=session.directory / "lesson42-red-gate.json", source="hr_policy_2026.md", expect_red=True)

# Original CLI workflow for step_02_the_undo_then_the_gate_green.
COMMANDS_02 = """make reindex PROJECT=$PROJECT TENANT=acme FILE=evals/corpus/acme/hr_policy_2026.md

make eval-live PROJECT=$PROJECT SOURCE=hr_policy_2026.md

"""

def step_02_the_undo_then_the_gate_green(session):
    """Run The undo, then the gate, green at this checkpoint.

    Version 1's bytes again, through the same release command. The offline gate passes, the upload lands, and the worker finds a version it has retired within the window: ingest_reactivated, nothing embedded, revision 3 retired in turn. The live gate then passes with the rows as they are.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the undo, then ten questions again).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_the_live_gate_red),
        ('source_23', step_02_the_undo_then_the_gate_green),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
