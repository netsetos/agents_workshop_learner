"""Lesson 2.1 / plan-2: Create a saved infrastructure plan

Summary and purpose:
Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

HTML instruction: Course-plan experiment — live deployment
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_01_read_the_resource_and_identity_definitions
Expected observation: A saved checked plan and its resource changes; inspect them before the apply lesson.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Create a saved infrastructure plan at this checkpoint.

    Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.command([sys.executable, "commands/infrastructure.py", "plan", "--project", session.config.project, "--region", session.config.cloud_run_region])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
