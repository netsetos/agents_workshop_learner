"""Lesson 4.4 / s9: Watch an incomplete undo refuse

Summary and purpose:
Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

HTML instruction: bash — optional deliberate fault: remove one verified retired row of this fixture
Category: optional. Read the matching README checkpoint before Run.
Prerequisites: demo_09_01_optional_watch_an_incomplete_undo_refuse
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L793

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Watch an incomplete undo refuse at this checkpoint.

    Run this only after the successful round trip. It deliberately removes one retired row from this chapter's fixture. The worker will not reactivate a partial version. It compares the retained row count with the claim's count and checks the age of retirement. A shortfall or a closed window emits reactivate_incomplete, leaves the incomplete undo unapplied, and sends the document through fresh ingestion. This variation deletes a retired fixture row; it is separate from the main demonstration and from unrelated tenant documents.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — optional deliberate fault: remove one verified retired row of this fixture.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, warnings
    from pathlib import Path
    from google.cloud import firestore
    warnings.filterwarnings("ignore", category=UserWarning)
    db=firestore.Client(project=os.environ["PROJECT"])
    key=os.environ["DOC_KEY"]
    source=db.collection("sources").document(os.environ["SOURCE"].replace("/", "~")).get().to_dict() or {}
    claim=db.collection("documents").document(key).get().to_dict() or {}
    assert source.get("status")=="retired" and source.get("doc_key")==key
    assert claim.get("status")=="superseded", "Only the retired fixture's claim may be used."
    rows=list(db.collection("chunks").where("doc_key", "==", key).stream())
    n=int(Path(os.environ["DEMO_DIR"], "initial-chunks.txt").read_text())
    assert len(rows)==n==int(claim["chunks"]), "The complete retained version must exist first."
    assert all(r.to_dict().get("current") is False
               and r.to_dict().get("source_uri")==os.environ["OBJECT"] for r in rows)
    victim=sorted(rows, key=lambda r:r.id)[0]
    victim.reference.delete()
    print("Removed one retired fixture row:", victim.id, "| claim still expects", n)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
