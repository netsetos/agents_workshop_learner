"""Lesson 1.2: Break an assertion in memory

Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

Run order inside this file:
1. Break an assertion in memory (source window plan-2)

Prerequisites: demo_01_run_the_actual_offline_gate.
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


def step_01_break_an_assertion_in_memory(session):
    """Run Break an assertion in memory at this checkpoint.

    Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: A named must_contain failure followed by a passing original row.
    """
    import copy, sys
    sys.path.insert(0, "evals")
    import run_eval
    corpus = run_eval.load_corpus()
    original = next(row for row in run_eval.load_golden() if row["answerable"] and row.get("must_contain"))
    assert not run_eval.check_falsifiable([original], corpus)
    broken = copy.deepcopy(original)
    broken["must_contain"] = []
    failures = run_eval.check_falsifiable([broken], corpus)
    print("Deliberate failure:", failures)
    assert any("no must_contain" in failure for failure in failures)
    assert not run_eval.check_falsifiable([original], corpus)
    print("Restored original: checker passes; disk data was unchanged.")

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_02_break_an_assertion_in_memory', step_01_break_an_assertion_in_memory),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
