"""Lesson 3.4 / s5: Inspect Vector Search: the datapoint, its restricts, and a search for itself

Summary and purpose:
Read one datapoint back, then search for it

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_the_index_and_its_deployment_as_gcloud_sees_them
Expected observation: datapoint acme:9c41d0e2b7f5...#1: 768 numbers | same as the row's vector: True
restricts: [('tenant_id', ['acme']), ('kind', ['text']), ('doc_type', ['unknown']), ('current', ['true'])]
sparse dimensions: 24
  acme:9c41d0e2b7f5...#1  distance 1.0000   <- itself
  acme:9c41d0e2b7f5...#2  distance 0.7xxx
  acme:9c41d0e2b7f5...#0  distance 0.6xxx

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L697

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read one datapoint back, then search for it at this checkpoint.

    Read one datapoint back, then search for it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, hashlib, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import aiplatform, firestore
    from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
    PROJECT, REGION = os.environ["PROJECT"], os.environ["REGION"]
    ENDPOINT, DEPLOYED = os.environ["VECTOR_INDEX_ENDPOINT"], os.environ["VECTOR_DEPLOYED_INDEX_ID"]
    db = firestore.Client(project=PROJECT)
    NOTE = os.environ.get("NOTE", os.path.expanduser("~/lesson34_note.md"))    # the note you wrote in step 3
    sha = hashlib.sha256(open(NOTE, "rb").read()).hexdigest()
    cid = f"acme:{sha}#1"                                                  # SM-01, the smoke lantern
    vec = list(db.collection("chunks").document(cid).get().to_dict()["embedding"])
    aiplatform.init(project=PROJECT, location=REGION)
    ep = aiplatform.MatchingEngineIndexEndpoint(ENDPOINT)
    dp = ep.read_index_datapoints(deployed_index_id=DEPLOYED, ids=[cid])[0]
    same = len(dp.feature_vector) == len(vec) and all(abs(a - b) < 1e-6 for a, b in zip(dp.feature_vector, vec))
    print(f"datapoint {dp.datapoint_id.split('#')[0][:18]}...#1: {len(dp.feature_vector)} numbers | same as the row's vector: {same}")
    print("restricts:", [(r.namespace, list(r.allow_list)) for r in dp.restricts])
    print("sparse dimensions:", len(dp.sparse_embedding.dimensions))
    hits = ep.find_neighbors(deployed_index_id=DEPLOYED, queries=[vec], num_neighbors=3,
                             filter=[Namespace(name="tenant_id", allow_tokens=["acme"]), Namespace(name="current", allow_tokens=["true"])])[0]
    for n in hits:
        print(f"  {n.id.split('#')[0][:18]}...#{n.id.rsplit('#', 1)[1]}  distance {n.distance:.4f}" + ("   <- itself" if n.id == cid else ""))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
