"""Lesson 5.4: demo 01 firestore predicates

Run the fallback rung directly with the same authorization/current/metadata predicates.

Run order inside this file:
1. Do it: the rung under three predicate sets (source window 11)

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


def step_01_the_rung_under_three_predicate_sets(session):
    """Run Do it: the rung under three predicate sets at this checkpoint.

    Run the cell as it is, then twice more with a filter in front of its first line: F='{"doc_type":"policy"}' python - <<'PY' and F='{"kind":"text"}' python - <<'PY', the rest unchanged. The worker stamped the lane's uploads doc_type: unknown, so the first filter empties the pool on this rung exactly as it did on the index in lesson 5.1, and the second keeps it whole.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; one embedding, a few dozen Firestore reads).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, json, math, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google import genai
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
    from google.cloud.firestore_v1.vector import Vector
    PROJECT, REGION = os.environ["PROJECT"], os.environ["REGION"]
    Q = os.environ.get("Q", "What is the notice period for a confirmed E3?")
    F = json.loads(os.environ.get("F", "{}"))                                 # the caller's filters: doc_type, kind
    CURRENT = os.environ.get("RETRIEVAL_CURRENT_ONLY", "off") == "on"
    client = genai.Client(enterprise=True, project=PROJECT, location=REGION)    # held in a name: a discarded client closes its connection
    vec = list(client.models.embed_content(
        model="text-embedding-005", contents=[Q], config={"output_dimensionality": 768, "task_type": "RETRIEVAL_QUERY"}).embeddings[0].values)
    db = firestore.Client(project=PROJECT)
    q = db.collection("chunks").where("tenant_id", "==", "acme")               # the roster's predicate, never the body's
    if CURRENT:
        q = q.where("current", "==", True)                                     # the ledger's, when RETRIEVAL_CURRENT_ONLY is on
    for k, v in F.items():
        q = q.where(k, "==", v)                                                # the caller's: FILTER_KEYS only, checked by main.py
    hits = q.find_nearest("embedding", Vector(vec), distance_measure=DistanceMeasure.COSINE, limit=20, distance_result_field="d").get()
    pool = []
    for h in hits:
        d = h.to_dict(); d["id"] = h.id; d["score"] = 1.0 - d.pop("d", 1.0); d.pop("embedding", None); d["found_by"] = "firestore"
        pool.append(d)
    entries = db.collection("chunks").where("tenant_id", "==", "acme").count().get()[0][0].value
    fields = "tenant_id" + (", current" if CURRENT else "") + "".join(", " + k for k in F)
    print(f"predicates: {fields}{''.join(f' ({k}={v})' for k, v in F.items())} -> {len(pool)} rows, every one found_by firestore")
    for c in pool[:5]:
        print(f"   {c.get('locator', '?'):9} {c.get('source_uri', '').split('/')[-1][:26]:26} doc_type {str(c.get('doc_type')):8} kind {str(c.get('kind')):6} current {str(c.get('current')):5} score {c['score']:.4f}")
    print(f"index needed: ({fields}, embedding) | reads billed, at most: {math.ceil(entries / 100)} for {entries} index entries + {len(pool)} documents")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_11', step_01_the_rung_under_three_predicate_sets),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
