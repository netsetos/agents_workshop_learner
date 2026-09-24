"""Lesson 15.2 / s6: The walk in front of the dense pool, on a candidate

Summary and purpose:
First with the walk from Firestore:

HTML instruction: bash — run in the operator shell, in the kit (a candidate with no traffic: the walk on, from Firestore; one question)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it
Expected observation: gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|...|RETRIEVAL_GRAPH=auto|GRAPH_BACKEND=firestore|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
/version: retrieval_graph=auto graph_backend=firestore embedding=text-embedding-005@1
Q: Who signs off on a big purchase?
A: Purchases up to Rs 2,00,000 are approved by the function head; above that, the CFO approves [1].
pool 20: the walk put 0 chunk(s) first; retrieval_backend ve

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L755

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make candidate PROJECT="$PROJECT" RETRIEVAL_GRAPH=auto GRAPH_BACKEND=firestore
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    First with the walk from Firestore:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a candidate with no traffic: the walk on, from Firestore; one question).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
