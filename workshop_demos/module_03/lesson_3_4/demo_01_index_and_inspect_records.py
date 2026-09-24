"""Lesson 3.4: demo 01 index and inspect records

Index the chapter note and inspect its exact claim, chunks, source and fingerprint.

Run order inside this file:
1. Do it: index a note, and count the datapoints before and after (source window 13)
2. Do it: index a note, and count the datapoints before and after (source window 15)
3. Read all four, Rs 0 (source window 20)

Prerequisites: setup_prepare.
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


# Original CLI workflow for step_01_index_a_note_and_count_the_datapoints_befo.
COMMANDS_01 = """idx_count() { gcloud ai indexes describe "$(basename "$VECTOR_INDEX_NAME")" --region="$REGION" --project="$PROJECT" --format='value(indexStats.vectorsCount)' 2>/dev/null; }
BEFORE="$(idx_count)"; echo "datapoints before: ${BEFORE:-0}"
export NOTE="$HOME/lesson34_note.md"
{ cat evals/demo/smoke_note_v1.md; printf '\\nIndexed for lesson 3.4 by %s on %s.\\n' "$ME" "$(date -u +%F)"; } > "$NOTE"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gcloud storage cp "$NOTE" "gs://$PROJECT-uploads/acme/smoke_note_v1.md"
for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.doc_key:\\"acme_\\" AND timestamp>=\\"$SINCE\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.event,jsonPayload.doc_key,jsonPayload.chunks,jsonPayload.pages,jsonPayload.embedded)')"
  [ -n "$LINE" ] && { echo ">> event doc_key chunks pages embedded: $LINE"; break; }
done
for i in $(seq 1 30); do N="$(idx_count)"; [ "${N:-0}" -ge $(( ${BEFORE:-0} + 3 )) ] && { echo "datapoints now: $N"; break; }; sleep 20; done

"""

def step_01_index_a_note_and_count_the_datapoints_befo(session):
    """Run Do it: index a note, and count the datapoints before and after at this checkpoint.

    The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one small ingest).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_index_a_note_and_count_the_datapoints_befo.
COMMANDS_02 = """gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND jsonPayload.event:\\"ingest_\\" AND timestamp>=\\"$(date -u -d '-20 min' +%Y-%m-%dT%H:%M:%SZ)\\"" \\
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

def step_02_index_a_note_and_count_the_datapoints_befo(session):
    """Run Do it: index a note, and count the datapoints before and after at this checkpoint.

    The note is the kit's three-clause warehouse memo with one line added: your account and today's date. The line matters. A version is its bytes, and the kit's reindex smoke from Module 2 uploads the unchanged file under another name; if it ever ran on your lane, those bytes are already claimed, and the worker acks the same bytes again as a duplicate and writes nothing. One line of your own makes a new version key. The note is a Markdown file of about 500 characters with no PII: no Document AI, three embeddings, about a hundredth of a paisa. The block reads the index's datapoint count, writes and uploads the note, waits for the worker's line, then waits for the count to move. The index's statistics refresh on their own schedule, so the last wait can take a few minutes. Two reads tell you what the worker did with an upload. The first lists every ingest event of the last twenty minutes with its verdict: ingest_duplicate means the bytes were already claimed on this lane, ingest_failed carries the error, and no line at all means the event never reached the worker. The second reads the claim for the unchanged demo bytes; its gcs_uri names the object that holds them, which on a lane where the smoke has run is acme/smoke_note.md. The claim is per version, not per name: that is the record this whole step is about.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_read_all_four_rs_0(session):
    """Run Read all four, Rs 0 at this checkpoint.

    Read all four, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, hashlib, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    NOTE = os.environ.get("NOTE", os.path.expanduser("~/lesson34_note.md"))    # the note you wrote in step 3
    sha = hashlib.sha256(open(NOTE, "rb").read()).hexdigest()
    key = f"acme_{sha}"
    print("doc_key from the note's bytes:", key[:20] + "...")
    claim = db.collection("documents").document(key).get().to_dict() or {}
    print("documents/:", {k: claim.get(k) for k in ("status", "chunks", "reused", "embedded", "generation", "tenant_id")})
    rows = sorted(((s.id, s.to_dict()) for s in db.collection("chunks").where("tenant_id", "==", "acme").where("doc_key", "==", key).stream()),
                  key=lambda r: int(r[0].rsplit("#", 1)[1]))
    print("chunks/:", len(rows), "rows | current:", sum(d.get("current") is True for _, d in rows),
          "| staged:", sum(bool(d.get("staged")) for _, d in rows), "| with expire_at:", sum(d.get("expire_at") is not None for _, d in rows))
    for cid, d in rows:
        print(f"  {cid.split('#')[0][:18]}...#{cid.rsplit('#', 1)[1]}  {d['locator']:9} section={d.get('section')!r} hash={d['chunk_hash'][:12]} vector={len(d['embedding'])} doc_type={d.get('doc_type')}")
    src = db.collection("sources").document("acme~smoke_note_v1.md").get().to_dict() or {}
    print("sources/acme~smoke_note_v1.md:", {k: src.get(k) for k in ("status", "chunks", "reused", "embedded", "retired", "effective_from")},
          "| doc_key matches:", src.get("doc_key") == key, "| sha256 matches:", src.get("sha256") == sha)
    led = db.collection("ledger").document("acme").get().to_dict() or {}
    print("ledger/acme:", {k: led.get(k) for k in ("fingerprint", "versions", "last_event")})

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_index_a_note_and_count_the_datapoints_befo),
        ('source_15', step_02_index_a_note_and_count_the_datapoints_befo),
        ('source_20', step_03_read_all_four_rs_0),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
