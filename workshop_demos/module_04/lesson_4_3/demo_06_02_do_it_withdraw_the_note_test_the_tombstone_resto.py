"""Lesson 4.3 / s6: Withdrawn: retire a document by hand, then restore it

Summary and purpose:
The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (the withdrawal, then two reads)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_withdraw_the_note_test_the_tombstone_resto
Expected observation: {"event": "reconcile_withdrawn", "gcs_uri": "gs://documind-ai-YOUR-ID-uploads/acme/smoke_note_v1.md", "fingerprint": "7c2e91a4d05b3f68", "retired_doc_keys": ["acme_9c41d0e2b7f5..."], "retired_ids": ["acme:9c41d0e2b7f5...#0", "acme:9c41d0e2b7f5...#1", "acme:9c41d0e2b7f5...#2"], "retired_chunks": 3, "note": "a tombstone: the object is kept and nothing automatic re-ingests it; make restore SOURCE= does"}
acme/smoke_note_v1.md withdrawn chunks 3
fingerprint 7c2e91a4d05b3f68 | last event reconcile_withdrawn
3 rows | current: 0 | with expire_at: 3 | superseded_by: {'None'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.3-versions/Netsetos_GCP_Capstone_4.3_Versions_WIX.html#L697

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make retire PROJECT=$PROJECT SOURCE=acme/smoke_note_v1.md

curl -s "$API/v1/sources?tenant_id=acme" -H "Authorization: Bearer $(tok "$API")" \\
  | python -c "import json,sys; j=json.load(sys.stdin); [print(r['name'], r['status'], 'chunks', r['chunks']) for r in j['sources'] if 'smoke_note' in r['name']]; print('fingerprint', j['fingerprint'], '| last event', j['last_event'])"

python - <<'PY'
import os, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
PROJECT = os.environ["PROJECT"]
db = firestore.Client(project=PROJECT)
rows = [r.to_dict() for r in db.collection("chunks").where("tenant_id", "==", "acme").where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/smoke_note_v1.md").stream()]
print(len(rows), "rows | current:", sum(bool(r.get("current")) for r in rows), "| with expire_at:", sum(r.get("expire_at") is not None for r in rows), "| superseded_by:", {str(r.get("superseded_by")) for r in rows})
PY
"""


def demonstrate(session):
    """Run Do it: withdraw the note, test the tombstone, restore it at this checkpoint.

    The document is the note lesson 3.4 indexed, three chunks under acme/smoke_note_v1.md, with its bytes still at ~/lesson34_note.md; if you skipped that lesson, run its step 3 first. Four blocks: the withdrawal and what the API and Firestore say; a question that now has no source; the same bytes again, refused; the restore, and the same question answered. Everything here is a flag flip: no parse, no embedding. If the file is not on this machine, the box below gets it back before anything else runs. Lesson 3.4 wrote the note into the home directory of the machine it ran on. On another machine, Cloud Shell instead of the workstation or a fresh workstation, the file is gone while the ledger still holds its hash, and a note rewritten with today's date has different bytes: the worker would index it as a new version, and every reactivation on this page would read ingest_ok with three embedded instead. Get the original bytes back and check them against the ledger. The uploads bucket is versioned, so the object itself is the first place to look, and its last generation serves when the object has been deleted, as lesson 4.4 does on purpose. If the bucket has nothing, the second block rebuilds the note the way 3.4 wrote it, the kit's fixture plus one line naming your account and the day, and tries the last sixty days against the ledger's hash.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (the withdrawal, then two reads).
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
