"""Lesson 4.5: Label the frozen rows yourself, blind

Do it: your sheet Open evals/reports/judge_labels.csv in a spreadsheet or a text editor. For each row, read the context first, then the answer, then the question again, and write yes or no under both label columns. Write a note on any row you hesitate over, now: step 4 prints it beside the other reader's. Here is one filled row of the kit's fixture, as a sheet holds it: The answer refuses, so it claims nothing: grounded, yes. But the context holds the cap, so a refusal does not answer the question: no. The reader's note says why: "the cap is in the context". Save the sheet as CSV with every column kept and in the same order. A spreadsheet may add a byte-order mark, Windows line endings or a capitalised YES; the check reads all three. Then check it:

Run order inside this file:
1. Do it: your sheet (source window 11)
2. Do it: your sheet (source window 13)

Prerequisites: setup_prepare.
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


# Original CLI workflow for step_01_your_sheet.
COMMANDS_01 = """make label-sheet

"""

def step_01_your_sheet(session):
    """Run Do it: your sheet at this checkpoint.

    Do it: your sheet

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (Rs 0: a blank sheet of the frozen rows for you; it never overwrites one).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: [awaiting the author's run: data/judge_set.json]
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_your_sheet.
COMMANDS_02 = """python evals/build_judge_set.py --check evals/reports/judge_labels.csv
python evals/build_judge_set.py --check evals/judge_labels.L1.csv      # the author's sheet, shipped with the kit

"""

def step_02_your_sheet(session):
    """Run Do it: your sheet at this checkpoint.

    Open evals/reports/judge_labels.csv in a spreadsheet or a text editor. For each row, read the context first, then the answer, then the question again, and write yes or no under both label columns. Write a note on any row you hesitate over, now: step 4 prints it beside the other reader's. Here is one filled row of the kit's fixture, as a sheet holds it: The answer refuses, so it claims nothing: grounded, yes. But the context holds the cap, so a refusal does not answer the question: no. The reader's note says why: "the cap is in the context". Save the sheet as CSV with every column kept and in the same order. A spreadsheet may add a byte-order mark, Windows line endings or a capitalised YES; the check reads all three. Then check it:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (Rs 0: holds a filled sheet to the frozen set).
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
        ('source_11', step_01_your_sheet),
        ('source_13', step_02_your_sheet),
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
