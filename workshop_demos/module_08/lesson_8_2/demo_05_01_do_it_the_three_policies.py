"""Lesson 8.2 / s5: Residency: each tenant's data_region, and the rule that applies it

Summary and purpose:
Do it: the three policies

HTML instruction: bash — run in the operator shell, in the kit (each tenant's data_region; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: acme: data_region=any
zeta: data_region=any
globex: data_region=in

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/08-security/8.2-access-tests/Netsetos_GCP_Capstone_8.2_Access_Tests_WIX.html#L558

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """for t in acme zeta globex; do make tenant-policy TENANT=$t; done
"""


def demonstrate(session):
    """Run Do it: the three policies at this checkpoint.

    Do it: the three policies

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (each tenant's data_region; reads only).
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
