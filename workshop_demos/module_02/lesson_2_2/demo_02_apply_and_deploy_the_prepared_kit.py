"""Lesson 2.2: Apply and deploy the prepared kit

Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect.

Run order inside this file:
1. Apply and deploy the prepared kit (source window plan-2)

Prerequisites: demo_01_check_the_saved_plan.
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


def step_01_apply_and_deploy_the_prepared_kit(session):
    """Run Apply and deploy the prepared kit at this checkpoint.

    Apply the reviewed saved plan and run the kit's image-build, deployment, roster and readiness steps. This creates billed resources; the preceding plan is the concrete set of changes to inspect.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: The actual kit deployment finishes; any failed build or readiness step stops the demo.
    """
    import sys
    session.command(["make", "up", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_02_apply_and_deploy_the_prepared_kit', step_01_apply_and_deploy_the_prepared_kit),
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
