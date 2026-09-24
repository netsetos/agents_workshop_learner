"""Lesson 4.4 / s9: Watch an incomplete undo refuse

Summary and purpose:
The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents. Checkpoint: a reactivate_incomplete event explains the shortfall, followed by fresh ingest_ok; the restored source and answer are valid again. The reused-N/embedded-0 checkpoint belongs to the successful undo in step 8, not this fault. The strict generation filter may exclude reactivate_incomplete because that event is emitted by the lower-level undo function; use the read below to see it for this version and time window.

HTML instruction: bash — read the undo refusal for this version; no cloud writes
Category: optional. Read the matching README checkpoint before Run.
Prerequisites: demo_09_03_optional_watch_an_incomplete_undo_refuse
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L818

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.doc_key=\\"$DOC_KEY\\" AND jsonPayload.event=\\"reactivate_incomplete\\" AND timestamp>=\\"$CH44_SINCE\\"" \\
  --project "$PROJECT" --limit 5 \\
  --format='table(timestamp,jsonPayload.event,jsonPayload.rows,jsonPayload.chunks,jsonPayload.reason)'
"""


def demonstrate(session):
    """Run Watch an incomplete undo refuse at this checkpoint.

    The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents. Checkpoint: a reactivate_incomplete event explains the shortfall, followed by fresh ingest_ok; the restored source and answer are valid again. The reused-N/embedded-0 checkpoint belongs to the successful undo in step 8, not this fault. The strict generation filter may exclude reactivate_incomplete because that event is emitted by the lower-level undo function; use the read below to see it for this version and time window.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — read the undo refusal for this version; no cloud writes.
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
