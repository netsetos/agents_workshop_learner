"""Lesson 4.4 / s9: Watch an incomplete undo refuse

Summary and purpose:
Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

HTML instruction: bash — retire the fixture again; require the exact one-item plan
Category: optional. Read the matching README checkpoint before Run.
Prerequisites: demo_08_01_restore_the_exact_bytes_and_prove_reuse
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L788

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sha256sum -c "$DEMO_DIR/note.sha256" &&
  ch44_plan clean &&
  gcloud storage rm "$OBJECT" &&
  ch44_plan retire &&
  make reconcile PROJECT="$PROJECT" TENANT_ONLY=acme APPLY=1
"""


def demonstrate(session):
    """Run Watch an incomplete undo refuse at this checkpoint.

    Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — retire the fixture again; require the exact one-item plan.
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
