"""Lesson 5.2: demo 01 dense and sparse lists

Compare the two sparse rulers and obtain dense, sparse-only and hybrid index lists.

Run order inside this file:
1. Do it: both rulers over your rows, Rs 0 (source window 12)
2. Do it: dense, alpha 0, alpha 0.7 (source window 16)

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


def step_01_both_rulers_over_your_rows_rs_0(session):
    """Run Do it: both rulers over your rows, Rs 0 at this checkpoint.

    The cell reads the text of every current acme row, no vectors, and scores each row twice for the invoice question; then run it again for the notice-period clause. Firestore reads of this size sit inside the free quota.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell, then the same cell for a second question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, re, sys, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path.insert(0, ".")
    from google.cloud import firestore
    from rank_bm25 import BM25Okapi
    from shared.sparse_encoder import sparse_encode
    Q = os.environ.get("Q", "What is the total payable on invoice INV-2026-0412?")
    ANCHOR = os.environ.get("ANCHOR", "inv_2026_0412")          # a locator (NP-03) or the start of a source name
    db = firestore.Client(project=os.environ["PROJECT"])
    rows = []
    for d in db.collection("chunks").where("tenant_id", "==", "acme").where("current", "==", True).select(["text", "locator", "source_uri"]).stream():
        x = d.to_dict(); rows.append((d.id, x.get("locator", "?"), x.get("source_uri", "").split("/")[-1], x.get("text", "")))
    print(len(rows), "current acme rows read, text only")
    tokens = lambda t: re.findall(r"[a-z0-9\-]+", t.lower())            # the ablation's tokens(), the encoder's _tokens()
    hit = lambda r: r[1] == ANCHOR or r[2].startswith(ANCHOR)
    qv, qd = sparse_encode(Q); qw = dict(zip(qd, qv))
    def index_leg(r):                                                    # what Vector Search computes for a sparse query
        v, dd = sparse_encode(r[3]); return sum(qw[d] * w for d, w in zip(dd, v) if d in qw)
    bm25 = BM25Okapi([tokens(r[3]) for r in rows]).get_scores(tokens(Q))
    for name, scores in (("index leg, hashed TF by dot product", [index_leg(r) for r in rows]), ("ablation leg, BM25", list(bm25))):
        order = sorted(range(len(rows)), key=lambda i: -scores[i])
        rank = next((k + 1 for k, i in enumerate(order) if hit(rows[i])), None)
        print(f"\n{name}: anchor {ANCHOR} at rank {rank} of {len(rows)}")
        for i in order[:3]:
            print(f"   {rows[i][1]:10} {rows[i][2][:34]:34} {scores[i]:8.3f}" + ("   <- anchor" if hit(rows[i]) else ""))

def step_02_dense_alpha_0_alpha_0_7(session):
    """Run Do it: dense, alpha 0, alpha 0.7 at this checkpoint.

    Do it: dense, alpha 0, alpha 0.7

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding of a few dozen characters).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, json, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path[:0] = [".", "services/rag-api"]                 # shared/ for the encoder, the API's folder for hybrid.py
    from google import genai
    from google.cloud import aiplatform, firestore
    from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
    from hybrid import hybrid_find_neighbors
    PROJECT, REGION = os.environ["PROJECT"], os.environ["REGION"]
    ENDPOINT, DEPLOYED = os.environ["VECTOR_INDEX_ENDPOINT"], os.environ["VECTOR_DEPLOYED_INDEX_ID"]
    Q = os.environ.get("Q", "What is the total payable on invoice INV-2026-0412?")
    ANCHOR = os.environ.get("ANCHOR", "inv_2026_0412")
    client = genai.Client(enterprise=True, project=PROJECT, location=REGION)          # the API embeds in its own region
    vec = list(client.models.embed_content(model="text-embedding-005", contents=[Q],
                                           config={"output_dimensionality": 768, "task_type": "RETRIEVAL_QUERY"}).embeddings[0].values)
    aiplatform.init(project=PROJECT, location=REGION)
    ep = aiplatform.MatchingEngineIndexEndpoint(ENDPOINT)
    tenant = [Namespace(name="tenant_id", allow_tokens=["acme"])]
    lists = {"dense": [n.id for n in ep.find_neighbors(deployed_index_id=DEPLOYED, queries=[vec], num_neighbors=20, filter=tenant)[0]]}
    for name, alpha in (("sparse", 0.0), ("hybrid", 0.7)):
        lists[name] = [n.id for n in hybrid_find_neighbors(ep, DEPLOYED, vec, Q, "acme", k=20, alpha=alpha, restricts=tenant)]
    db = firestore.Client(project=PROJECT)
    label = {}
    for cid in set(sum(lists.values(), [])):
        row = db.collection("chunks").document(cid).get().to_dict() or {}
        label[cid] = (row.get("locator", "?"), row.get("source_uri", "").split("/")[-1])
    hit = lambda cid: label[cid][0] == ANCHOR or label[cid][1].startswith(ANCHOR)
    for name in ("dense", "sparse", "hybrid"):
        rank = next((i + 1 for i, cid in enumerate(lists[name]) if hit(cid)), None)
        print(f"\n{name:6} first five (anchor at rank {rank} of 20):")
        for cid in lists[name][:5]:
            print(f"   {label[cid][0]:10} {label[cid][1][:34]}" + ("   <- anchor" if hit(cid) else ""))
    print("\noverlap of 20: dense/hybrid", len(set(lists["dense"]) & set(lists["hybrid"])), "| dense/sparse", len(set(lists["dense"]) & set(lists["sparse"])))
    json.dump({"question": Q, "label": label, **lists}, open("/tmp/legs52.json", "w"))
    print("saved /tmp/legs52.json for step 5")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_12', step_01_both_rulers_over_your_rows_rs_0),
        ('source_16', step_02_dense_alpha_0_alpha_0_7),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
