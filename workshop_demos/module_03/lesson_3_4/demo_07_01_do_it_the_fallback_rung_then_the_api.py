"""Lesson 3.4 / s7: Verify: the two rungs that read the records

Summary and purpose:
The first cell runs the Firestore rung's exact query with the note's own vector: itself first, at a cosine distance of zero. The second asks the API a question only the note can answer and prints which rung served it and how many of the pooled chunks came from the index.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_read_the_mirror_rows_then_the_audit_event
Expected observation: acme:9c41d0e2b7f5...#1  SM-01     cosine distance 0.0000   <- itself
  acme:9c41d0e2b7f5...#2  SM-02     cosine distance 0.2xxx
  acme:9c41d0e2b7f5...#0  preamble  cosine distance 0.3xxx
The smoke lantern is kept in bay 4 of the Pune warehouse and is checked on the first Monday of every month ... [Source 1]
[('1', 'smoke_note_v1.md'), ('2', 'smoke_note_v1.md')]
backend vector | pool 20 | from the index 20

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.4-indexed-records/Netsetos_GCP_Capstone_3.4_Indexed_Records_WIX.html#L882

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import os, hashlib, warnings
warnings.filterwarnings("ignore", category=UserWarning)
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
PROJECT = os.environ["PROJECT"]
db = firestore.Client(project=PROJECT)
NOTE = os.environ.get("NOTE", os.path.expanduser("~/lesson34_note.md"))    # the note you wrote in step 3
sha = hashlib.sha256(open(NOTE, "rb").read()).hexdigest()
cid = f"acme:{sha}#1"
vec = list(db.collection("chunks").document(cid).get().to_dict()["embedding"])
q = db.collection("chunks").where("tenant_id", "==", "acme").where("current", "==", True)      # the rung's predicates
hits = q.find_nearest("embedding", Vector(vec), distance_measure=DistanceMeasure.COSINE, limit=3, distance_result_field="d").get()
for h in hits:
    d = h.to_dict()
    print(f"  {h.id.split('#')[0][:18]}...#{h.id.rsplit('#', 1)[1]}  {d['locator']:9} cosine distance {d['d']:.4f}" + ("   <- itself" if h.id == cid else ""))
PY

curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"Where is the smoke lantern kept, and how often is it checked?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:150]); print([(c['chunk_id'].split('#')[1], c['source_uri'].split('/')[-1]) for c in j['citations'][:2]]); s=j['stages']; print('backend', s['retrieval_backend'], '| pool', s['pool'], '| from the index', s['vector_chunks'])"
"""


def demonstrate(session):
    """Run Do it: the fallback rung, then the API at this checkpoint.

    The first cell runs the Firestore rung's exact query with the note's own vector: itself first, at a cosine distance of zero. The second asks the API a question only the note can answer and prints which rung served it and how many of the pooled chunks came from the index.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
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
