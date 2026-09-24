"""Lesson 3.4 / s3: Write: the order the worker keeps, and a fresh document to watch

Summary and purpose:
The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes. Two reads tell you what the worker did with an upload. The first lists every ingest event of the last twenty minutes with its verdict: ingest_duplicate means the bytes were already claimed on this lane, ingest_failed carries the error, and no line at all means the event never reached the worker. The second reads the claim for the unchanged demo bytes; its gcs_uri names the object that holds them, which on a lane where the smoke has run is acme/smoke_note.md. The claim is per version, not per name: that is the record this whole step is about.

HTML instruction: bash — run in the operator shell (both read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_index_a_note_and_count_the_datapoints_befo
Expected observation: 2026-09-22T11:58:07.412Z  ingest_duplicate  acme_111510fcf0a6ce7c...
the demo bytes' claim, acme_111510fcf0a6...: {'status': 'indexed', 'gcs_uri': 'gs://documind-ai-YOUR-ID-uploads/acme/smoke_note.md', 'chunks': 3, 'generation': '1758...'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L494

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$(date -u -d '-20 min' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
  --project "$PROJECT" --limit 10 --format='value(timestamp,jsonPayload.event,jsonPayload.doc_key,jsonPayload.error)'

python - <<'PY'
import os, hashlib, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
db = firestore.Client(project=os.environ["PROJECT"])
sha = hashlib.sha256(open("evals/demo/smoke_note_v1.md", "rb").read()).hexdigest()
d = db.collection("documents").document(f"acme_{sha}").get().to_dict() or {}
print("the demo bytes' claim, acme_%s...:" % sha[:12],
      {k: d.get(k) for k in ("status", "gcs_uri", "chunks", "generation")} if d else "no claim: these bytes were never seen on this lane")
PY
"""


def demonstrate(session):
    """Run Do it: index a note, and count the datapoints before and after at this checkpoint.

    The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes. Two reads tell you what the worker did with an upload. The first lists every ingest event of the last twenty minutes with its verdict: ingest_duplicate means the bytes were already claimed on this lane, ingest_failed carries the error, and no line at all means the event never reached the worker. The second reads the claim for the unchanged demo bytes; its gcs_uri names the object that holds them, which on a lane where the smoke has run is acme/smoke_note.md. The claim is per version, not per name: that is the record this whole step is about.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
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
