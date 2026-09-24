"""Lesson 2.2: Inspect the deployed services

List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

Run order inside this file:
1. Inspect the deployed services (source window plan-3)

Prerequisites: demo_02_apply_and_deploy_the_prepared_kit.
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


def step_01_inspect_the_deployed_services(session):
    """Run Inspect the deployed services at this checkpoint.

    List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe the printed/saved evidence for this heading; a zero exit alone is not proof.
    """
    session.command(["gcloud", "run", "services", "list", "--project", session.config.project, "--region", session.config.cloud_run_region,
                     "--format=table(metadata.name,spec.template.spec.serviceAccountName,status.url)"])

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_demo_03_inspect_the_deployed_services', step_01_inspect_the_deployed_services),
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
