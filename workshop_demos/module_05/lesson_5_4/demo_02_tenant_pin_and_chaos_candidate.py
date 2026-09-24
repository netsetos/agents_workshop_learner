"""Lesson 5.4: demo 02 tenant pin and chaos candidate

Choose the Firestore rung, restore the pin, then force an unavailable index on a candidate.

Run order inside this file:
1. Do it: pin acme beneath the index, and wait for the API to notice (source window 16)
2. Do it: the same predicates on the chosen rung, and two tenants that do not cross (source window 18)
3. Do it: the smoke's line for a chosen rung, then the pin back (source window 20)
4. Do it: a candidate that cannot reach the index (source window 25)
5. Do it: a candidate that cannot reach the index (source window 27)

Prerequisites: demo_01_firestore_predicates.
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


# Original CLI workflow for step_01_pin_acme_beneath_the_index_and_wait_for_th.
COMMANDS_01 = """python commands/lane.py tenant-backend acme firestore          # the same as: make tenant-backend PROJECT=$PROJECT TENANT=acme RETRIEVAL_BACKEND=firestore
ask() { curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" -d "$1" \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j.get('stages', {}); c = j.get('citations') or []; print('backend', s.get('retrieval_backend'), '| vector_chunks', s.get('vector_chunks'), '| pool', s.get('pool'), '| retrieve_ms', s.get('retrieve_ms'), '| answerable', j.get('answerable'), '| first', (c[0]['chunk_id'].rsplit('#', 1)[1] + ' ' + c[0]['source_uri'].split('/')[-1][:22]) if c else '-', '|', j.get('answer', '')[:60])"; }
for i in $(seq 1 9); do
  OUT="$(ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}')"; echo "$OUT"
  case "$OUT" in *"backend firestore"*) break;; esac; sleep 10                     # the pin is read once a minute
done

"""

def step_01_pin_acme_beneath_the_index_and_wait_for_th(session):
    """Run Do it: pin acme beneath the index, and wait for the API to notice at this checkpoint.

    Do it: pin acme beneath the index, and wait for the API to notice

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one field written; up to nine questions while the minute passes).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_same_predicates_on_the_chosen_rung_and.
COMMANDS_02 = """ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"doc_type":"policy"}}'
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"kind":"text"}}'
ask '{"query":"What is the per-trip cap on domestic travel reimbursement?","tenant_id":"acme","stream":false,"top_k":3}'
ask '{"query":"What is the per-trip cap on travel reimbursement?","tenant_id":"zeta","stream":false,"top_k":3}'

"""

def step_02_the_same_predicates_on_the_chosen_rung_and(session):
    """Run Do it: the same predicates on the chosen rung, and two tenants that do not cross at this checkpoint.

    Do it: the same predicates on the chosen rung, and two tenants that do not cross

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (four questions, a few rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

# Original CLI workflow for step_03_the_smoke_s_line_for_a_chosen_rung_then_th.
COMMANDS_03 = """DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep "vector tier"
python commands/lane.py tenant-backend acme vector
for i in $(seq 1 9); do OUT="$(ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}')"; case "$OUT" in *"backend vector"*) echo "$OUT"; break;; esac; sleep 10; done
DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep "vector tier"

"""

def step_03_the_smoke_s_line_for_a_chosen_rung_then_th(session):
    """Run Do it: the smoke's line for a chosen rung, then the pin back at this checkpoint.

    Do it: the smoke's line for a chosen rung, then the pin back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (two smokes, a rupee each; one field written).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

# Original CLI workflow for step_04_a_candidate_that_cannot_reach_the_index.
COMMANDS_04 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars VECTOR_DEPLOYED_INDEX_ID=documind_chunks_nonesuch --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
curl -s -X POST "$CAND/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}' \\
  | python -c "
import sys, json
j = json.load(sys.stdin); s = j['stages']
print('candidate: backend', s['retrieval_backend'], '| vector_chunks', s['vector_chunks'], '| pool', s['pool'], '| answerable', j['answerable'], '| citations', len(j['citations']))
ok = s['retrieval_backend'] != 'vector' or s.get('vector_chunks', 0) > 0                   # smoke.py check 3a, by hand
print('the smoke would say:', '[PASS] vector tier' if ok else '[FAIL] vector tier  RETRIEVAL_BACKEND=vector and no chunk came from the index - the Firestore rung answered. make vector-status; make backfill-vectors APPLY=1')"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="vector_search_fallback"' \\
  --project "$PROJECT" --freshness 10m --limit 2 --format='value(timestamp,jsonPayload.tenant,jsonPayload.error)'

"""

def step_04_a_candidate_that_cannot_reach_the_index(session):
    """Run Do it: a candidate that cannot reach the index at this checkpoint.

    Do it: a candidate that cannot reach the index

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read; ask() from step 4).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_04)

# Original CLI workflow for step_05_a_candidate_that_cannot_reach_the_index.
COMMANDS_05 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars VECTOR_DEPLOYED_INDEX_ID="$VECTOR_DEPLOYED_INDEX_ID" --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
echo "template now: $(svc_env documind-api VECTOR_DEPLOYED_INDEX_ID)"
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}'
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'

"""

def step_05_a_candidate_that_cannot_reach_the_index(session):
    """Run Do it: a candidate that cannot reach the index at this checkpoint.

    Do it: a candidate that cannot reach the index

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the undo: the real name back on the template, the tag dropped, the live service asked once).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_05)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_16', step_01_pin_acme_beneath_the_index_and_wait_for_th),
        ('source_18', step_02_the_same_predicates_on_the_chosen_rung_and),
        ('source_20', step_03_the_smoke_s_line_for_a_chosen_rung_then_th),
        ('source_25', step_04_a_candidate_that_cannot_reach_the_index),
        ('source_27', step_05_a_candidate_that_cannot_reach_the_index),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
