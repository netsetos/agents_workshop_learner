"""Lesson 2.3 / plan-1: Check readiness and smoke

Summary and purpose:
Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL.

HTML instruction: Course-plan experiment — live deployment
Category: required. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Check readiness and smoke at this checkpoint.

    Run the kit's preflight and smoke before closing a deployment session. Preserve their actual exit status instead of inferring readiness from a service URL.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    for target in ("preflight", "smoke"):
        session.command(["make", target, "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
