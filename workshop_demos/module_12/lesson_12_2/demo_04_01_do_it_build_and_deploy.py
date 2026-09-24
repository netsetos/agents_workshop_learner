"""Lesson 12.2 / s4: Deploy, and read it back

Summary and purpose:
Do it: build and deploy

HTML instruction: bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: >> building asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/mcp:COMMIT from services/mcp
Creating temporary archive of ... file(s) totalling ... MiB before compression.
...
DONE ... asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/mcp:COMMIT
>> commands/lesson-7.2.sh (DEPLOY block)
Deploying container to Cloud Run service [documind-mcp] in project [documind-ai-YOUR-ID] region [asia-south1]
...
Service URL: https://documind-mcp-NUMBER.asia-south1.run.app
Updated IAM policy for service [documind-mcp].   (three times: ui, agent, outsider)
...
>> you@example.com may mint tokens as documind-ui-sa
>> you@example.com may mint tokens as documind-outsider-sa

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L459

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make build deploy-services PROJECT="$PROJECT" REGION="$REGION" SERVICES=mcp SCRIPTS=commands/lesson-7.2.sh ADMIN_EMAILS="$ME"
"""


def demonstrate(session):
    """Run Do it: build and deploy at this checkpoint.

    Do it: build and deploy

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (build the image, deploy it, bind its callers).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
