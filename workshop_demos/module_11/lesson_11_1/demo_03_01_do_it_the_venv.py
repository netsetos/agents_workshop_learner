"""Lesson 11.1 / s3: One turn, taken apart

Summary and purpose:
Do it: the venv

HTML instruction: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and the SQLite checkpointer added)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: graph-venv ok: fastapi 0.141.1

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html#L403

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """[ -x ~/graph-venv/bin/python ] || python -m venv ~/graph-venv   # lesson 10.2's venv, made here if it is missing
~/graph-venv/bin/pip install -q "langchain==1.4.0" "langchain-core==1.6.2" "requests==2.34.2" "google-auth==2.57.1" \\
  "fastapi==0.141.1" "langgraph-checkpoint-sqlite==3.1.1"   # the chat image's web layer, and the laptop lane's checkpointer
~/graph-venv/bin/python -c 'import fastapi, langgraph.checkpoint.sqlite; print("graph-venv ok: fastapi", fastapi.__version__)'
"""


def demonstrate(session):
    """Run Do it: the venv at this checkpoint.

    Do it: the venv

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (lesson 10.2's venv, with the web layer and the SQLite checkpointer added).
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
