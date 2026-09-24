"""Lesson 5.2 / s4: Three ways through the index: dense, sparse only, fused

Summary and purpose:
Do it: dense, alpha 0, alpha 0.7

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; one paid embedding of a few dozen characters)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_both_rulers_over_your_rows_rs_0
Expected observation: dense  first five (anchor at rank 1 of 20):
   p1-0       inv_2026_0412.md                     <- anchor
   p36-0      cgst_act_2017.pdf
   ...

sparse first five (anchor at rank None of 20):
   p28-1      industrial_relations_code_2020.pdf
   p32-0      cgst_act_2017.pdf
   ...

hybrid first five (anchor at rank 2 of 20):
   p36-0      cgst_act_2017.pdf
   p1-0       inv_2026_0412.md                     <- anchor
   ...

overlap of 20: dense/hybrid 18 | dense/sparse 2
saved /tmp/legs52.json for step 5

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L564

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
