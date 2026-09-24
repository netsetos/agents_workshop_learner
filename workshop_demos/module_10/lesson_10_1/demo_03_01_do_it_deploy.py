"""Lesson 10.1 / s3: The chat service, in your lane's region

Summary and purpose:
Do it: deploy

HTML instruction: bash — run in the operator shell, in the kit (the chat service built and deployed in your region; several minutes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: >> commands/lesson-12.8.sh (DEPLOY block)
Creating temporary archive of ... file(s) totalling ... MiB before compression.
...
DONE ... asia-south1-docker.pkg.dev/documind-ai-YOUR-ID/documind/chat:COMMIT
Deploying container to Cloud Run service [documind-chat] in project [documind-ai-YOUR-ID] region [asia-south1]
...
Service URL: https://documind-chat-NUMBER.asia-south1.run.app
Updated IAM policy for service [documind-chat].   (twice: documind-ui-sa, documind-outsider-sa)
... job exists - continuing   (or: Job [documind-checkpoint-setup] has successfully been created.)
Execution [documind-checkpoint-setup-xxxxx] has successfully completed.
...
>> you@example.com may mint tokens as documind-ui-sa
>> you@example.com may mint tokens as documind-outsider-sa

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L394

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make deploy-services PROJECT="$PROJECT" REGION="$REGION" SCRIPTS=commands/lesson-12.8.sh ADMIN_EMAILS="$ME"
"""


def demonstrate(session):
    """Run Do it: deploy at this checkpoint.

    Do it: deploy

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the chat service built and deployed in your region; several minutes).
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
