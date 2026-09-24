"""Lesson 6.3 / s6: A failure forced on a candidate: the ranker silent, the stream still served, the line in the log

Summary and purpose:
Do it: the ranker silent for one revision, the stream read, the line read, the undo

HTML instruction: bash — run in the operator shell (one new revision, no traffic; one stream to it; two log reads; the undo)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_read_the_lane_rs_0
Expected observation: done.stages: rerank_fallback 1 | rerank_ms 1x | pool 20 | vector_chunks 20
events: {'citation': 3, 'token': 3x, 'done': 1} | the answer: A confirmed employee in grade E3 must serve a notice period of ...
2026-09-2xT1x:xx:xx.xxxxxxZ	acme	DeadlineExceeded

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.3-streaming/Netsetos_GCP_Capstone_6.3_Streaming_WIX.html#L629

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RERANK_TIMEOUT_S=0.001 --quiet
export CAND="https://candidate---documind-api-$NUMBER.$REGION.run.app"
curl -N -s -X POST "$CAND/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","top_k":3}' \\
  | python -c "
import sys, json
ev, n, text = None, {}, []
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: '): ev = line[7:]; n[ev] = n.get(ev, 0) + 1
    elif line.startswith('data: ') and ev == 'token': text.append(json.loads(line[6:])['t'])
    elif line.startswith('data: ') and ev == 'done': s = json.loads(line[6:])['stages']; print('done.stages: rerank_fallback', s.get('rerank_fallback', 0), '| rerank_ms', s['rerank_ms'], '| pool', s['pool'], '| vector_chunks', s['vector_chunks'])
print('events:', n, '| the answer:', ' '.join(''.join(text).split())[:70], '...')"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="rerank_fallback"' \\
  --project "$PROJECT" --freshness 10m --limit 2 --format='value(timestamp,jsonPayload.tenant,jsonPayload.error)'
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="telemetry_not_instrumented"' \\
  --project "$PROJECT" --freshness 7d --limit 1 --format='value(timestamp,jsonPayload.error)'
gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate --remove-env-vars RERANK_TIMEOUT_S --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
"""


def demonstrate(session):
    """Run Do it: the ranker silent for one revision, the stream read, the line read, the undo at this checkpoint.

    Do it: the ranker silent for one revision, the stream read, the line read, the undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one stream to it; two log reads; the undo).
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
