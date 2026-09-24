"""Lesson 16.1: demo 02 index and inspect segments

Handle the old text fixture, index the media and inspect segment records.

Run order inside this file:
1. Definition (source window 13)
2. Definition (source window 16)
3. Definition (source window 18)

Prerequisites: demo_01_media_contract_and_upload.
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


# Original CLI workflow for step_01_definition.
COMMANDS_01 = """make retire PROJECT="$PROJECT" SOURCE=acme/townhall_2026_q1.md

"""

def step_01_definition(session):
    """Run Definition at this checkpoint.

    Next, the transcript goes. upload.sh keeps a transcript home once its video exists, as it keeps a PDF's text mirror home, but it removes nothing already sent: make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the transcript withdrawn from acme).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_definition.
COMMANDS_02 = """make reindex PROJECT="$PROJECT" TENANT=acme FILE=evals/corpus/acme/townhall_2026_q1.mp4

"""

def step_02_definition(session):
    """Run Definition at this checkpoint.

    make retire withdraws it as lesson 15.4 showed. The rows are retired, acme's two managed stores delete their copies, and the ledger row becomes a tombstone. The object stays in the bucket, and make restore would bring it back. Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the video uploaded; waits for the worker).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_definition(session):
    """Run Definition at this checkpoint.

    Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call: Last, read the video's rows from acme's index, and hold them against the ground truth:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    P = os.environ["PROJECT"]
    URI = f"gs://{P}-uploads/acme/townhall_2026_q1.mp4"
    db = firestore.Client(project=P)
    rows = [d.to_dict() for d in db.collection("chunks").where(filter=FieldFilter("tenant_id", "==", "acme"))
            .where(filter=FieldFilter("source_uri", "==", URI)).where(filter=FieldFilter("current", "==", True)).stream()]
    truth = json.load(open("evals/corpus/acme/townhall_2026_q1.segments.json", encoding="utf-8"))["segments"]
    mmss = lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
    print(f"{len(rows)} segments of townhall_2026_q1.mp4 in acme's index, against the ground truth's {len(truth)} turns:")
    for r in sorted(rows, key=lambda r: r["start"]):
        heard = [f"{t['speaker']} {mmss(t['start'])}" for t in truth if min(t["end"], r["end"]) - max(t["start"], r["start"]) > 1]   # a second of the turn or more
        print(f"  {r['kind']} {r['locator']:9} {mmss(r['start'])}-{mmss(r['end'])} {r['end'] - r['start']:4.0f} s  over {', '.join(heard) or 'nobody'}")
        print(f"      {r['text'][:104]}...")
    longest = max(r["end"] - r["start"] for r in rows)
    bad = [r["locator"] for r in rows if not 0 <= r["start"] < r["end"]]
    video_end = truth[-1]["end"]
    print(f"checks: longest {longest:.0f} s (the prompt asks for at most 60) -> {'PASS' if longest <= 60 else 'FAIL'}; "
          f"start before end in every row -> {'PASS' if not bad else 'FAIL ' + ', '.join(bad)}; "
          f"last end {mmss(max(r['end'] for r in rows))} against the speech's end {mmss(video_end)}")
    said = next(t for t in truth if "5.2 per cent" in t["text"])
    hit = [r["locator"] for r in rows if r["start"] <= said["end"] and r["end"] >= said["start"] and "5.2 per cent" in r["text"]]
    print(f"the EMEA line: {said['speaker']} says '5.2 per cent' in the turn at {mmss(said['start'])}-{mmss(said['end'])}; "
          f"the segment that quotes it: {', '.join(hit) or 'none'}")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_13', step_01_definition),
        ('source_16', step_02_definition),
        ('source_18', step_03_definition),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
