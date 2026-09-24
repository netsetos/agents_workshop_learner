"""Lesson 2.2: demo 03 inspect the deployed services

List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

Run order inside this file:
1. Inspect the deployed services (source window plan-3)

Prerequisites: demo_02_apply_and_deploy_the_prepared_kit.
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


def step_01_inspect_the_deployed_services(session):
    """Run Inspect the deployed services at this checkpoint.

    List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.command(["gcloud", "run", "services", "list", "--project", session.config.project, "--region", session.config.cloud_run_region,
                     "--format=table(metadata.name,spec.template.spec.serviceAccountName,status.url)"])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_demo_03_inspect_the_deployed_services', step_01_inspect_the_deployed_services),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
