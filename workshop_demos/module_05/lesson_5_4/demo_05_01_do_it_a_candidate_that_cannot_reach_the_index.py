"""Lesson 5.4 / s5: The chaos rung: an index that will not answer, on a candidate that takes no traffic

Summary and purpose:
Do it: a candidate that cannot reach the index

HTML instruction: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read; ask() from step 4)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_03_do_it_the_smoke_s_line_for_a_chosen_rung_then_th
Expected observation: candidate: backend vector | vector_chunks 0 | pool 20 | answerable True | citations 3
the smoke would say: [FAIL] vector tier  RETRIEVAL_BACKEND=vector and no chunk came from the index - the Firestore rung answered. make vector-status; make backfill-vectors APPLY=1
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	... documind_chunks_nonesuch ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L646

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
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


def demonstrate(session):
    """Run Do it: a candidate that cannot reach the index at this checkpoint.

    Do it: a candidate that cannot reach the index

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read; ask() from step 4).
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
