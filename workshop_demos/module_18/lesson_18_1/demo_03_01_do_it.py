"""Lesson 18.1 / s3: The hook's decisions, traced

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: en_core_web_lg installed: the image's model, 400 MB

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L454

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m venv ~/gw-venv && ~/gw-venv/bin/pip install -q $(grep '^presidio' services/litellm/requirements.txt)   # the gateway image's pins
~/gw-venv/bin/python -m spacy download en_core_web_lg > /dev/null && echo "en_core_web_lg installed: the image's model, 400 MB"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (once: a venv with the gateway image's Presidio and spaCy model).
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
