"""Lesson 15.2: demo 03 compare graph candidate

Compare a no-traffic graph candidate and restore its configuration.

Run order inside this file:
1. Do it (source window 21)
2. Do it (source window 23)
3. Do it (source window 26)

Prerequisites: demo_02_spanner_graph_path.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """make candidate PROJECT="$PROJECT" RETRIEVAL_GRAPH=auto GRAPH_BACKEND=firestore
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
ask152() {   # ask152 URL: the CFO question, without the word CFO, as documind-ui-sa - /version, the answer, the walk's share
URL="$1" python - <<'PY'
import json, os, subprocess, urllib.request
from google.cloud import firestore
P, API, URL = os.environ["PROJECT"], os.environ["API"], os.environ["URL"]
Q = "Who signs off on a big purchase?"
tok = subprocess.run(["gcloud", "auth", "print-identity-token", "--include-email", f"--audiences={API}",
                      f"--impersonate-service-account=documind-ui-sa@{P}.iam.gserviceaccount.com"],
                     capture_output=True, text=True, check=True).stdout.strip()
h = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}
v = json.load(urllib.request.urlopen(urllib.request.Request(URL + "/version", headers=h), timeout=60))
print(f"/version: retrieval_graph={v['retrieval_graph']} graph_backend={v['graph_backend']} embedding={v['embedding']}")
req = urllib.request.Request(URL + "/v1/query", data=json.dumps({"query": Q, "tenant_id": "acme"}).encode(), headers=h)
a, db = json.load(urllib.request.urlopen(req, timeout=180)), firestore.Client(project=P)
s = a["stages"]
print(f"Q: {Q}")
print(f"A: {a['answer']}")
print(f"pool {s['pool']}: the walk put {s['graph_chunks']} chunk(s) first; retrieval_backend {s['retrieval_backend']}")
for c in a["citations"]:
    row = db.collection("chunks").document(c["chunk_id"]).get().to_dict() or {}
    print(f"cites {row.get('locator')} ({c['source_uri'].rsplit('/', 1)[-1]}): {c['quote'][:96]}")
print(f"the word CFO: {'in' if 'cfo' in Q.lower() else 'not in'} the question, {'in' if 'CFO' in a['answer'] else 'not in'} the answer")
PY
}
ask152 "$CAND"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    First with the walk from Firestore:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a candidate with no traffic: the walk on, from Firestore; one question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """make candidate PROJECT="$PROJECT" RETRIEVAL_GRAPH=auto GRAPH_BACKEND=spanner
ask152 "$CAND"

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    First with the walk from Firestore: Then the same candidate, walking from Spanner:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same candidate, the walk from Spanner; the same question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_example.
COMMANDS_03 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RETRIEVAL_GRAPH=off,GRAPH_BACKEND=firestore --remove-env-vars GRAPH_SEED_DISTANCE --quiet     # env vars merge: put the template back
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
rm -f .candidate-revision      # make promote flips to the revision this file names, tag or no tag
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'

"""

def step_03_example(session):
    """Run Do it at this checkpoint.

    Choose a value just past the purchase or approval name, and below the first name that has nothing to do with purchases. The undo below removes it. Last, put the template back. Environment variables carry over from one revision to the next, so the candidate's settings would ride into the next gcloud run services update of the API. The undo writes RETRIEVAL_GRAPH=off and GRAPH_BACKEND=firestore, removes any GRAPH_SEED_DISTANCE, drops the tag, and deletes .candidate-revision.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the template put back, the tag dropped; the live revision was never touched).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_21', step_01_example),
        ('source_23', step_02_example),
        ('source_26', step_03_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
