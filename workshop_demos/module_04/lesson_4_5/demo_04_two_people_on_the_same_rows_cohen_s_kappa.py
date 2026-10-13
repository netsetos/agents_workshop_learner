"""Lesson 4.5: Two people on the same rows: Cohen's kappa

Do it: the worked table, and the kit's own tests Do it: you against the author, then the author against the peer

Run order inside this file:
1. Do it: the worked table, and the kit's own tests (source window 19)
2. Do it: you against the author, then the author against the peer (source window 21)

Prerequisites: demo_03_label_the_frozen_rows_yourself_blind.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
Example: open this file at the matching HTML heading, Run once, then inspect
the observations below before continuing to the next numbered section.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_the_worked_table_and_the_kit_s_own_tests.
COMMANDS_01 = """python evals/agreement.py --selftest
python -m unittest discover -s evals/tests -p test_agreement.py 2>&1 | tail -3

"""

def step_01_the_worked_table_and_the_kit_s_own_tests(session):
    """Run Do it: the worked table, and the kit's own tests at this checkpoint.

    Do it: the worked table, and the kit's own tests

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (Rs 0: the worked table, then the kit's own tests of the arithmetic).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: selftest: the worked table of 50 rows (20 both yes, 5 and 10 split, 15 both no) agrees on 35/50 = 70.0% [56.2%, 80.9%], 0.50 by chance, kappa 0.40; identical labels 1.00; one label throughout undefined; a reader with one label against one with two 0.00
    Ran 18 tests in ...s

    OK
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_you_against_the_author_then_the_author_aga.
COMMANDS_02 = """make judge-agree PEOPLE=1                       # your sheet against the author's
make judge-agree PEOPLE=1 LABELS=evals/judge_labels.L1.csv AGAINST=evals/judge_labels.L2.csv   # the author against the peer

"""

def step_02_you_against_the_author_then_the_author_aga(session):
    """Run Do it: you against the author, then the author against the peer at this checkpoint.

    Do it: you against the author, then the author against the peer

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (Rs 0: two sheets, kappa per rubric).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/judge_set.json]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_19', step_01_the_worked_table_and_the_kit_s_own_tests),
        ('source_21', step_02_you_against_the_author_then_the_author_aga),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
