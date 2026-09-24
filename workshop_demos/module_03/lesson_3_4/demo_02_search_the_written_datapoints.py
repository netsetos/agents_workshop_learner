"""Lesson 3.4: demo 02 search the written datapoints

Inspect the deployed index and read/search the note's datapoints.

Run order inside this file:
1. The index and its deployment, as gcloud sees them (source window 24)
2. Read one datapoint back, then search for it (source window 27)

Prerequisites: demo_01_index_and_inspect_records.
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


# Original CLI workflow for step_01_the_index_and_its_deployment_as_gcloud_see.
COMMANDS_01 = """gcloud ai indexes describe "$(basename "$VECTOR_INDEX_NAME")" --region="$REGION" --project="$PROJECT" \\
  --format='yaml(displayName,indexStats.vectorsCount,indexStats.shardsCount,indexUpdateMethod,metadata.config.dimensions,metadata.config.distanceMeasureType)'
gcloud ai index-endpoints describe "$(basename "$VECTOR_INDEX_ENDPOINT")" --region="$REGION" --project="$PROJECT" \\
  --format='yaml(displayName,deployedIndexes[].id,deployedIndexes[].indexSyncTime,deployedIndexes[].dedicatedResources.machineSpec.machineType)'

"""

def step_01_the_index_and_its_deployment_as_gcloud_see(session):
    """Run The index and its deployment, as gcloud sees them at this checkpoint.

    Three things exist: the index, the endpoint, and the deployed index that joins them and is the one that costs money per hour. The kit's make vector-status runs commands/vector-status.sh, which takes the two names from the shell (the variables you exported above) or, failing that, from Terraform's outputs; the two commands below are the same reads by hand.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_read_one_datapoint_back_then_search_for_it(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_24', step_01_the_index_and_its_deployment_as_gcloud_see),
        ('source_27', step_02_read_one_datapoint_back_then_search_for_it),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
