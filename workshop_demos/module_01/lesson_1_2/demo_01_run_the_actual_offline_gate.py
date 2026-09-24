"""Lesson 1.2 / plan-1: Run the actual offline gate

Summary and purpose:
Run the kit's existing validation and offline evaluation. Read PASS/WARN/SKIP honestly: missing Docker or Terraform can mean skipped checks, not ten proven passes.

HTML instruction: Course-plan experiment — local Python/kit inspection
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: No failed checks; actual tool-dependent skips are reported.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
