"""Lesson 4.4 / s7: Plan retirement, apply it, then prove zero drift

Summary and purpose:
Keep preview, mutation and verification as three visible operations.

HTML instruction: bash — read-only: require exactly one repair, for this fixture
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_delete_the_cloud_file_and_show_the_stale_index
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L667

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ch44_plan retire
"""


def demonstrate(session):
    """Run Plan retirement, apply it, then prove zero drift at this checkpoint.

    Keep preview, mutation and verification as three visible operations.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — read-only: require exactly one repair, for this fixture.
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
