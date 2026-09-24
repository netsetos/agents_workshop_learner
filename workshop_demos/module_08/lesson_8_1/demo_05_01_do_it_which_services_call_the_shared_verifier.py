"""Lesson 8.1 / s5: The surfaces: who calls the shared verifier, and who still keeps a copy

Summary and purpose:
Do it: which services call the shared verifier

HTML instruction: bash — run in the operator shell, in the kit (which services call the shared verifier)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_plan_make_roster_would_write_for_you
Expected observation: services/chat/agent.py
services/mcp/server.py
services/rag-api/auth.py

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.1-identity-tenancy/Netsetos_GCP_Capstone_8.1_Identity_Tenancy_WIX.html#L678

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """grep -rl "iap.identity(" --include=*.py services smoke | sort
"""


def demonstrate(session):
    """Run Do it: which services call the shared verifier at this checkpoint.

    Do it: which services call the shared verifier

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (which services call the shared verifier).
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
