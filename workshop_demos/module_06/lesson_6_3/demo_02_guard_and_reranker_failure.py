"""Lesson 6.3: demo 02 guard and reranker failure

Read guard configuration and force degraded streaming on a no-traffic candidate.

Run order inside this file:
1. Read the lane, Rs 0 (source window 22)
2. Do it: the ranker silent for one revision, the stream read, the line read, the undo (source window 27)

Prerequisites: demo_01_stream_events_and_empty_pool.
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


# Original CLI workflow for step_01_read_the_lane_rs_0.
COMMANDS_01 = """gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="query" OR jsonPayload.event="stream")' \\
  --project "$PROJECT" --freshness 24h --limit 200 --format='value(jsonPayload.guard)' | sort | uniq -c
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="guard"' \\
  --project "$PROJECT" --freshness 7d --limit 3 --format='value(timestamp,jsonPayload.verdict,jsonPayload.reason)'

"""

def step_01_read_the_lane_rs_0(session):
    """Run Read the lane, Rs 0 at this checkpoint.

    Read the lane, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two log reads).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_the_ranker_silent_for_one_revision_the_str.
COMMANDS_02 = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
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

def step_02_the_ranker_silent_for_one_revision_the_str(session):
    """Run Do it: the ranker silent for one revision, the stream read, the line read, the undo at this checkpoint.

    Do it: the ranker silent for one revision, the stream read, the line read, the undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one new revision, no traffic; one stream to it; two log reads; the undo).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_22', step_01_read_the_lane_rs_0),
        ('source_27', step_02_the_ranker_silent_for_one_revision_the_str),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
