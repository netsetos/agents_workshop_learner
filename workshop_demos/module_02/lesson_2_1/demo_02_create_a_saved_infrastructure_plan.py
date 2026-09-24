"""Lesson 2.1: Create a saved infrastructure plan

Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

Run order inside this file:
1. Create a saved infrastructure plan (source window plan-2)

Prerequisites: demo_01_read_the_resource_and_identity_definitions.
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


def step_01_create_a_saved_infrastructure_plan(session):
    """Run Create a saved infrastructure plan at this checkpoint.

    Call the existing infrastructure planner, which saves verified inputs and refuses unexpected deletion/replacement. Initialize the intended Terraform backend and project prerequisites described in INFRASTRUCTURE.md first.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: A saved checked plan and its resource changes; inspect them before the apply lesson.
    """
    import sys
    session.command([sys.executable, "commands/infrastructure.py", "plan", "--project", session.config.project, "--region", session.config.cloud_run_region])

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_02_create_a_saved_infrastructure_plan', step_01_create_a_saved_infrastructure_plan),
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
