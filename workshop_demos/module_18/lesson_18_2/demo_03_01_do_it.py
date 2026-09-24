"""Lesson 18.2 / s3: A Modelfile from the tokenizer

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell (once: a venv with a transformers that can read the tokenizer)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L436

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python3 -m venv ~/tf-venv && ~/tf-venv/bin/pip install -q "transformers==5.17.0" jinja2   # not the kit's pin: see below
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (once: a venv with a transformers that can read the tokenizer).
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
