"""Lesson 1.2 / plan-2: Break an assertion in memory

Summary and purpose:
Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_run_the_actual_offline_gate
Expected observation: A named must_contain failure followed by a passing original row.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Break an assertion in memory at this checkpoint.

    Remove must_contain from a copy of one answerable golden row. The real falsifiability checker must reject it; restoring the original copy must pass. No committed dataset is edited.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — local Python/kit inspection.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
