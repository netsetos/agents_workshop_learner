"""Lesson 14.3 / plan-2: Roll back and verify recovery

Summary and purpose:
Return traffic to the exact previous revision recorded by the kit. Measure actual elapsed time, then run smoke; a quick traffic command alone is not proof of a healthy recovered service.

HTML instruction: Course-plan experiment — live deployment
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_promote_the_gated_revision
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Roll back and verify recovery at this checkpoint.

    Return traffic to the exact previous revision recorded by the kit. Measure actual elapsed time, then run smoke; a quick traffic command alone is not proof of a healthy recovered service.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys, time
    started = time.perf_counter()
    session.command(["make", "rollback", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])
    print("Rollback command seconds:", round(time.perf_counter() - started, 2))
    session.command(["make", "smoke", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
