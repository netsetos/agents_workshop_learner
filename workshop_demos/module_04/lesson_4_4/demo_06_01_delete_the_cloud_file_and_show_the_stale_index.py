"""Lesson 4.4 / s6: Delete the cloud file and show the stale index

Summary and purpose:
The local original stays safe. Delete only this demonstration's live object.

HTML instruction: bash — check the backup before deleting; observe before running reconciliation
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_prove_the_document_works
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L660

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sha256sum -c "$DEMO_DIR/note.sha256" &&
  gcloud storage rm "$OBJECT" &&
  ch44_source &&
  ch44_ask present
"""


def demonstrate(session):
    """Run Delete the cloud file and show the stale index at this checkpoint.

    The local original stays safe. Delete only this demonstration's live object.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — check the backup before deleting; observe before running reconciliation.
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
