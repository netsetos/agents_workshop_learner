"""Lesson 5.2 / s3: The lane runs dense, and two sparse rulers over its own rows

Summary and purpose:
The cell reads the text of every current acme row, no vectors, and scores each row twice for the invoice question; then run it again for the notice-period clause. Firestore reads of this size sit inside the free quota.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell, then the same cell for a second question)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_02_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: N current acme rows read, text only

index leg, hashed TF by dot product: anchor inv_2026_0412 at rank 9xx of N
   p28-1      industrial_relations_code_2020.pdf     35.500
   p32-0      cgst_act_2017.pdf                      34.000
   p7-0       payment_of_gratuity_act_1972.pdf       32.000

ablation leg, BM25: anchor inv_2026_0412 at rank 1 of N
   p1-0       inv_2026_0412.md                       21.949   <- anchor
   p36-0      cgst_act_2017.pdf                      16.609
   p40-0      cgst_act_2017.pdf                      16.514

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L467

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
