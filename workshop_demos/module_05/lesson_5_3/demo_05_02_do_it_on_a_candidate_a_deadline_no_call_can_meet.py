"""Lesson 5.3 / s5: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate

Summary and purpose:
Do it, on a candidate: a deadline no call can meet

HTML instruction: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_offline_the_kit_s_fallback_on_the_pool_you
Expected observation: candidate: rerank_fallback 1 | rerank_ms 1x | pool 20 | answerable True
   score 0.7xxx  #1  hr_policy_2026.md
   score 0.7xxx  #4  hr_policy_2026.md
   score 0.6xxx  #2  hr_policy_2026.md
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	DeadlineExceeded

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L663

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RERANK_TIMEOUT_S=0.001 --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
curl -s -X POST "$CAND/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":5}' \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('candidate: rerank_fallback', s.get('rerank_fallback', 0), '| rerank_ms', s['rerank_ms'], '| pool', s['pool'], '| answerable', j['answerable']); [print('   score %.4f  #%s  %s' % (c['score'], c['chunk_id'].rsplit('#', 1)[1], c['source_uri'].split('/')[-1][:26])) for c in j['citations']]"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="rerank_fallback"' \\
  --project "$PROJECT" --freshness 10m --limit 3 --format='value(timestamp,jsonPayload.tenant,jsonPayload.error)'
"""


def demonstrate(session):
    """Run Do it, on a candidate: a deadline no call can meet at this checkpoint.

    Do it, on a candidate: a deadline no call can meet

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one question to it; one log read).
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
