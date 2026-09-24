"""Lesson 14.1: demo 02 build the deployment images

Use the actual kit build target and the current authenticated identity. Record the build output and image tags; a successful local credential check alone does not prove a deployed GitHub workload-identity run.

Run order inside this file:
1. Build the deployment images (source window plan-2)

Prerequisites: demo_01_inspect_the_keyless_build_identity.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_build_the_deployment_images(session):
    """Run Build the deployment images at this checkpoint.

    Use the actual kit build target and the current authenticated identity. Record the build output and image tags; a successful local credential check alone does not prove a deployed GitHub workload-identity run.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    session.command(["make", "build", "PROJECT=" + session.config.project, "REGION=" + session.config.cloud_run_region, "PY=" + sys.executable])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_02_build_the_deployment_images', step_01_build_the_deployment_images),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
