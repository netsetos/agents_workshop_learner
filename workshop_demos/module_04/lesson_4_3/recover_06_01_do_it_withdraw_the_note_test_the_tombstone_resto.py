"""Lesson 4.3 / s6: Withdrawn: retire a document by hand, then restore it

Summary and purpose:
The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

HTML instruction: bash — only if the check said DIFFERENT or the bucket had nothing (rebuilds the note from the kit's fixture and the ledger's hash)
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: rebuilt, dated 2026-09-DD

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L681

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: withdraw the note, test the tombstone, restore it at this checkpoint.

    The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — only if the check said DIFFERENT or the bucket had nothing (rebuilds the note from the kit's fixture and the ledger's hash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, hashlib, datetime as dt, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    want = (db.collection("sources").document("acme~smoke_note_v1.md").get().to_dict() or {}).get("sha256")
    base = open("evals/demo/smoke_note_v1.md", "rb").read()
    for d in range(60):
        day = (dt.date.today() - dt.timedelta(days=d)).isoformat()
        text = base + f"\nIndexed for lesson 3.4 by {os.environ['ME']} on {day}.\n".encode()      # 3.4's step 3, byte for byte
        if hashlib.sha256(text).hexdigest() == want:
            open(os.path.expanduser("~/lesson34_note.md"), "wb").write(text); print("rebuilt, dated", day); break
    else:
        print("no match in sixty days: the account that ran 3.4 differs from $ME, or the note was edited before it was uploaded")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
