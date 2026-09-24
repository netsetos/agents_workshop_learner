"""Lesson 2.2 / plan-3: Inspect the deployed services

Summary and purpose:
List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

HTML instruction: Course-plan experiment — live deployment
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_apply_and_deploy_the_prepared_kit
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/plan/course-plan-v5-story-2026-09-22.md#L1

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Inspect the deployed services at this checkpoint.

    List the real Cloud Run services and their accounts, URLs and traffic so the resource diagram can be checked against the deployment.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: Course-plan experiment — live deployment.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    session.command(["gcloud", "run", "services", "list", "--project", session.config.project, "--region", session.config.cloud_run_region,
                     "--format=table(metadata.name,spec.template.spec.serviceAccountName,status.url)"])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
