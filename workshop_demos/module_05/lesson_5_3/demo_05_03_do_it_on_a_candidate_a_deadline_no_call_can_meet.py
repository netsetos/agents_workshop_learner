"""Lesson 5.3 / s5: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate

Summary and purpose:
Do it, on a candidate: a deadline no call can meet

HTML instruction: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live service asked once)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_do_it_on_a_candidate_a_deadline_no_call_can_meet
Expected observation: live: rerank_fallback 0 | rerank_ms 3xx | first score 0.9xxx
100;documind-api-00044-xyz

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L678

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --remove-env-vars RERANK_TIMEOUT_S --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}' \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('live: rerank_fallback', s.get('rerank_fallback', 0), '| rerank_ms', s['rerank_ms'], '| first score', round(j['citations'][0]['score'], 4))"
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'
"""


def demonstrate(session):
    """Run Do it, on a candidate: a deadline no call can meet at this checkpoint.

    Do it, on a candidate: a deadline no call can meet

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live service asked once).
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
