"""Lesson 12.1 / s3: Expose: what the server declares

Summary and purpose:
Do it: fastmcp

HTML instruction: bash — run in the operator shell, in the kit (fastmcp in the operator venv)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: fastmcp 3.4.7

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L402

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q "fastmcp==3.4.7" "uvicorn==0.52.4"   # the MCP image's pins, in the operator venv
python -c 'import fastmcp; print("fastmcp", fastmcp.__version__)'
"""


def demonstrate(session):
    """Run Do it: fastmcp at this checkpoint.

    Do it: fastmcp

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (fastmcp in the operator venv).
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
