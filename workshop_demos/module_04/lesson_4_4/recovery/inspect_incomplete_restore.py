"""Lesson 4.4: inspect incomplete restore

Explicit recovery: inspect incomplete restore

Run order inside this file:
1. Why the undo counts first (source window 25)

Prerequisites: workshop setup; see this lesson README.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_why_the_undo_counts_first(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_25', step_01_why_the_undo_counts_first),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
