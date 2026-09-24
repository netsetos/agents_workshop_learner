"""Lesson 3.4: demo 03 mirrors fallback and repair

Trace mirror/audit evidence, test the fallback rung and inspect the backfill plan.

Run order inside this file:
1. Read the mirror rows, then the audit event (source window 32)
2. Do it: the fallback rung, then the API (source window 37)
3. The operator's checks: two commands, and their tests (source window 39)
4. The rows rebuild the tier (source window 43)

Prerequisites: demo_02_search_the_written_datapoints.
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


# Original CLI workflow for step_01_read_the_mirror_rows_then_the_audit_event.
COMMANDS_01 = """bq --project_id="$PROJECT" query --use_legacy_sql=false --format=pretty \\
  "SELECT chunk_id, heading_path, kind, doc_type, pii_flag, FORMAT_TIMESTAMP('%H:%M:%S', ingested_at) AS at
   FROM \\`$BQ_CHUNK_TABLE\\` WHERE tenant_id = 'acme' AND source_uri = 'gs://$PROJECT-uploads/acme/smoke_note_v1.md' ORDER BY chunk_id"

bq --project_id="$PROJECT" query --use_legacy_sql=false --format=pretty \\
  "SELECT COUNT(*) AS rows_ever, COUNT(DISTINCT source_uri) AS documents FROM \\`$BQ_CHUNK_TABLE\\` WHERE tenant_id = 'acme'"

gcloud storage cat "gs://$AUDIT_BUCKET/$(date -u +%Y/%m/%d)/acme/doc.upload-*.json" \\
  | python -c "import json,sys,hashlib,os; sha=hashlib.sha256(open(os.environ.get('NOTE', os.path.expanduser('~/lesson34_note.md')),'rb').read()).hexdigest(); [print(json.dumps(e, indent=1)) for e in map(json.loads, sys.stdin.read().replace('}{', '}\\n{').split('\\n')) if e['target']['id'].endswith(sha)]"

"""

def step_01_read_the_mirror_rows_then_the_audit_event(session):
    """Run Read the mirror rows, then the audit event at this checkpoint.

    Read the mirror rows, then the audit event

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two BigQuery queries, then one read from the audit bucket).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_fallback_rung_then_the_api.
COMMANDS_02 = """python - <<'PY'
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

def step_02_the_fallback_rung_then_the_api(session):
    """Run Do it: the fallback rung, then the API at this checkpoint.

    The first cell runs the Firestore rung's exact query with the note's own vector: itself first, at a cosine distance of zero. The second asks the API a question only the note can answer and prints which rung served it and how many of the pooled chunks came from the index.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_the_operator_s_checks_two_commands_and_the.
COMMANDS_03 = """python commands/verify-vector-index.py --deploy-root "$DEMO_ROOT" --project "$PROJECT" --region "$REGION"

GOOGLE_CLOUD_PROJECT="$PROJECT" python commands/check-firestore-fallback.py

python -m unittest discover -s commands/tests -p test_verify_vector_index.py
python -m unittest discover -s commands/tests -p test_check_firestore_fallback.py

"""

def step_03_the_operator_s_checks_two_commands_and_the(session):
    """Run The operator's checks: two commands, and their tests at this checkpoint.

    The kit ships two read-only commands for exactly this lesson. verify-vector-index.py reads Terraform's outputs and asks the API whether the index Terraform declared is the one attached to the endpoint, streaming, 768-dimensional, deployed exactly once; it needs a checkout with Terraform state, and the two gcloud reads in step 5 are the same checks by hand. check-firestore-fallback.py takes the handbook, proves the ledger row names the bytes in your checkout, and runs the Firestore rung with combined filters in both current modes; it imports the API's own modules, so it needs the API's packages in your venv. Both write their evidence under operator-evidence/. Their tests run offline in a fraction of a second.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (all read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

# Original CLI workflow for step_04_the_rows_rebuild_the_tier.
COMMANDS_04 = """make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme
# make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme APPLY=1

"""

def step_04_the_rows_rebuild_the_tier(session):
    """Run The rows rebuild the tier at this checkpoint.

    Firestore holds everything the index holds and more: the text, the vector, the stamps and the flags. So when the index and the rows disagree, the index is rebuilt from the rows, and nothing in the rows is ever derived from the index. backfill() reads every current row (of one tenant, or all), rebuilds each datapoint with the row's own vector, re-embeds only a row whose stamp fails the check from lesson 3.3, and checkpoints the repaired vector back on the row with optimistic concurrency so that a concurrent writer is never overwritten. Its plan is the count you saw in 3.3; APPLY=1 is the repair, and the two states it exists for are a worker deployed before the index existed and an apply that lost its index and succeeded on the second run.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — the plan (read-only) and the repair (writes to the tier; run it only when the plan is not zero).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_32', step_01_read_the_mirror_rows_then_the_audit_event),
        ('source_37', step_02_the_fallback_rung_then_the_api),
        ('source_39', step_03_the_operator_s_checks_two_commands_and_the),
        ('source_43', step_04_the_rows_rebuild_the_tier),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
