"""Lesson 2.3 / plan-3: Lower service floors at session end

Summary and purpose:
Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

HTML instruction: Course-plan experiment — live deployment
Category: cleanup. Read the matching README checkpoint before Run.
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
    """Run Lower service floors at session end at this checkpoint.

    Run make off, then inspect the actual configured service floors. A zero minimum is not proof that every warm instance is already gone; the monitoring demonstration in 18.4 verifies eventual instance counts.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.command(["make", "off", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])
    session.command(["gcloud", "run", "services", "list", "--project", session.config.project, "--region", session.config.cloud_run_region, "--format=json"])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
