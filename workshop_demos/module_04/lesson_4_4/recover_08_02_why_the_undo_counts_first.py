"""Lesson 4.4 / s8: Restore the exact bytes and prove reuse

Summary and purpose:
You have shown a working document, a stale index, a planned repair, consistent absence, and a verified return. Steps 9 to 11 are separate extensions. Finish with step 12 even if you skip them: it restores the backend pin saved before the demonstration. Load this run's saved session variables first. Recover the exact generation named in its source ledger, then verify the content hash before writing the local file. Do not invent replacement text and expect a same-version reactivation. If the recorded generation is no longer retained, stop and inspect version recovery options; this path cannot reconstruct deleted bytes.

HTML instruction: bash — read the retained version; this writes only the verified local backup
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.4-restore-reconcile/Netsetos_GCP_Capstone_4.4_Restore_Reconcile_WIX.html#L763

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Why the undo counts first at this checkpoint.

    You have shown a working document, a stale index, a planned repair, consistent absence, and a verified return. Steps 9 to 11 are separate extensions. Finish with step 12 even if you skip them: it restores the backend pin saved before the demonstration. Load this run's saved session variables first. Recover the exact generation named in its source ledger, then verify the content hash before writing the local file. Do not invent replacement text and expect a same-version reactivation. If the recorded generation is no longer retained, stop and inspect version recovery options; this path cannot reconstruct deleted bytes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — read the retained version; this writes only the verified local backup.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import hashlib, os, subprocess, warnings
    from pathlib import Path
    from google.cloud import firestore
    warnings.filterwarnings("ignore", category=UserWarning)
    db=firestore.Client(project=os.environ["PROJECT"])
    row=db.collection("sources").document(os.environ["SOURCE"].replace("/", "~")).get().to_dict()
    assert row, "No source ledger entry for this fixture."
    generation=str(row.get("generation") or "")
    assert generation.isdigit(), "No recoverable generation in this ledger entry."
    data=subprocess.check_output(["gcloud", "storage", "cat",
        os.environ["OBJECT"]+"#"+generation])
    sha=hashlib.sha256(data).hexdigest()
    assert sha==row.get("sha256"), "Recovered bytes do not match the ledger."
    assert "acme_"+sha==os.environ["DOC_KEY"], "These are not this run's original bytes."
    note=Path(os.environ["NOTE"])
    if note.exists():
        assert note.read_bytes()==data, "A different local file exists; inspect it before replacing."
    else:
        note.write_bytes(data)
    print("Recovered and verified:", note)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
