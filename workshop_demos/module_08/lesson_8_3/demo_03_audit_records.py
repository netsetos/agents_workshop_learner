"""Lesson 8.3: demo 03 audit records

Inspect immutable audit objects and the records used by the admin console.

Run order inside this file:
1. Do it (source window 25)
2. Do it (source window 29)

Prerequisites: demo_02_guarded_candidate.
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


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (today's audit objects for acme, one event, the bucket's retention, and a delete it must refuse).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import datetime, json, os
    from google.cloud import storage
    p = os.environ["PROJECT"]
    client = storage.Client(project=p)
    bucket = client.get_bucket(f"{p}-audit")
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    blobs = sorted(bucket.list_blobs(prefix=f"{day}/acme/"), key=lambda b: b.time_created)
    for b in blobs[-3:]:
        print(" ", b.name)
    finding = next((b for b in reversed(blobs) if "/dlp.finding-" in b.name), None)
    for k, v in (json.loads(finding.download_as_text()).items() if finding else [("dlp.finding", "none today")]):
        print(f"    {k}: {json.dumps(v)}")
    rp = bucket.retention_period or 0
    print(f"retention {rp} s ({rp / 31536000:.0f} years), locked {bucket.retention_policy_locked}")
    if finding and rp:                                   # only against a policy: the delete must be refused
        try:
            finding.delete()
            print("DELETED: this bucket did not enforce its retention policy")
        except Exception as e:
            print("delete refused:", getattr(e, "code", ""), type(e).__name__)

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (what the admin console's audit tab can see; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from collections import Counter
    from google.cloud import firestore
    db = firestore.Client(project=os.environ["PROJECT"])
    seen = Counter(d.to_dict().get("action") for d in db.collection("audit_index").limit(500).stream())
    print(dict(seen) if seen else "audit_index is empty", "| doc.upload in it:", seen.get("doc.upload", 0))

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_25', step_01_example),
        ('source_29', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
