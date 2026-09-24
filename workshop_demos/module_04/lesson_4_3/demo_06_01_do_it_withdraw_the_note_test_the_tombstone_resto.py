"""Lesson 4.3 / s6: Withdrawn: retire a document by hand, then restore it

Summary and purpose:
The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the object, or its last generation; then the hash against the ledger)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_three_events_three_verdicts_rs_0
Expected observation: ledger abcdef0123456789 | file abcdef0123456789 | the same bytes

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L668

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud storage cp "gs://$PROJECT-uploads/acme/smoke_note_v1.md" "$HOME/lesson34_note.md" 2>/dev/null \\
  || { GEN="$(gcloud storage ls -a "gs://$PROJECT-uploads/acme/smoke_note_v1.md" | sed -n 's/.*#//p' | sort -n | tail -1)"; \\
       gcloud storage cp "gs://$PROJECT-uploads/acme/smoke_note_v1.md#$GEN" "$HOME/lesson34_note.md"; }
python - <<'PY'
import os, hashlib, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
db = firestore.Client(project=os.environ["PROJECT"])
want = (db.collection("sources").document("acme~smoke_note_v1.md").get().to_dict() or {}).get("sha256")
have = hashlib.sha256(open(os.path.expanduser("~/lesson34_note.md"), "rb").read()).hexdigest() if os.path.exists(os.path.expanduser("~/lesson34_note.md")) else "no file"
print("ledger", (want or "no ledger row: run lesson 3.4 step 3 first")[:16], "| file", have[:16], "|", "the same bytes" if want == have else "DIFFERENT: run the rebuild block")
PY
"""


def demonstrate(session):
    """Run Do it: withdraw the note, test the tombstone, restore it at this checkpoint.

    The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the object, or its last generation; then the hash against the ledger).
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
