"""Lesson 18.1 / s5: The gateway, deployed and smoke-tested

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: ...
>> gateway: https://documind-gateway-NUMBER.asia-south1.run.app (the API and the UI's account may call it)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L588

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make deploy-gateway PROJECT="$PROJECT"            # builds the image from services/litellm: the first build takes a while
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit where make up ran (it reads the database URL from Terraform's state).
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
