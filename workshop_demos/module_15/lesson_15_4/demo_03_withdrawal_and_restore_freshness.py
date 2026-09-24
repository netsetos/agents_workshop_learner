"""Lesson 15.4: demo 03 withdrawal and restore freshness

Withdraw and restore the source, checking each store's resulting evidence.

Run order inside this file:
1. Do it (source window 20)
2. Do it (source window 22)

Prerequisites: demo_02_update_freshness.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make retire PROJECT="$PROJECT" SOURCE=zeta/hr_policy_zeta_2026.md
fresh154 withdrawn

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook withdrawn by hand, then the check).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """export SINCE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
make restore PROJECT="$PROJECT" SOURCE=zeta/hr_policy_zeta_2026.md
fresh154 indexed

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Then the restore:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook brought back, then the check).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_20', step_01_example),
        ('source_22', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
