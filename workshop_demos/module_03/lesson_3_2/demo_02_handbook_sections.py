"""Lesson 3.2: demo 02 handbook sections

Cut the handbook locally and compare its section chunks with indexed rows.

Run order inside this file:
1. Do it: cut the handbook, Rs 0 (source window 17)
2. Read it on the lane (source window 19)

Prerequisites: demo_01_readers_and_page_counts.
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


def step_01_cut_the_handbook_rs_0(session):
    """Run Do it: cut the handbook, Rs 0 at this checkpoint.

    Do it: cut the handbook, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path.insert(0, "."); sys.path.insert(0, "services/ingest")
    from shared import documind_corpus as dc
    text = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    doc = {"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://x/acme/hr_policy_2026.md", "text": text}
    chunks = dc.chunk_document(doc, "acme")
    print(len(chunks), "chunks from", text.count("\n## "), "headings")
    for c in chunks[:5]:
        print(f"  {c['locator']:10} section={str(c['section'])[:32]:34} chars={len(c['text']):5}  hash={c['chunk_hash'][:12]}")
    from collections import Counter
    per_section = Counter(c["section"] for c in chunks)
    print("sections windowed within themselves:", [t for t, n in per_section.items() if n > 1])

def step_02_on_the_lane(session):
    """Run Read it on the lane at this checkpoint.

    The worker cut the same file with the same rule when the corpus was loaded. Its rows for the handbook should be the same 283 locators in the same order.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path.insert(0, ".")
    from google.cloud import firestore
    from shared import documind_corpus as dc
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    
    q = (db.collection("chunks").where("tenant_id", "==", "acme")
         .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md")
         .where("current", "==", True))
    lane = sorted(q.stream(), key=lambda c: int(c.id.rsplit("#", 1)[1]))
    lane_loc = [c.to_dict().get("locator") for c in lane]
    
    text = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    local = dc.chunk_document({"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://x", "text": text}, "acme")
    local_loc = [c["locator"] for c in local]
    print("lane:", len(lane_loc), "local:", len(local_loc), "same locators in the same order:", lane_loc == local_loc)
    print("same hashes:", [c.to_dict().get("chunk_hash") for c in lane] == [c["chunk_hash"] for c in local])

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_cut_the_handbook_rs_0),
        ('source_19', step_02_on_the_lane),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
