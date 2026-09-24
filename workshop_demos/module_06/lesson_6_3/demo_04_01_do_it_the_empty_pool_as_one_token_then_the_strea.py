"""Lesson 6.3 / s4: What a stream's citations are, and the streams of one token

Summary and purpose:
Do it: the empty pool as one token, then the stream rows

HTML instruction: bash — run in the operator shell (one stream that costs nothing; one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_one_stream_timed_then_the_query_s_citation
Expected observation: the one token: The corpus holds nothing near this question: no passage of this tenant's current documents was ...
done: backend none | tokens_in 0 | pool 0 | rerank_ms 0 | generate_ms 0
events: {'token': 1, 'done': 1}
False	none	0	0	0	off	ui
True	vertex	1xxx	4xx	20	off	ui

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.3-streaming/Netsetos_GCP_Capstone_6.3_Streaming_WIX.html#L525

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","filters":{"doc_type":"policy"}}' \\
  | python -c "
import sys, json
ev, n = None, {}
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: '): ev = line[7:]; n[ev] = n.get(ev, 0) + 1
    elif line.startswith('data: ') and ev == 'token': print('the one token:', json.loads(line[6:])['t'][:88], '...')
    elif line.startswith('data: ') and ev == 'done': d = json.loads(line[6:]); print('done: backend', d['backend'], '| tokens_in', d['tokens_in'], '| pool', d['stages']['pool'], '| rerank_ms', d['stages']['rerank_ms'], '| generate_ms', d['stages']['generate_ms'])
print('events:', n)"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="stream"' \\
  --project "$PROJECT" --freshness 15m --limit 3 --format='value(jsonPayload.answerable,jsonPayload.model_backend,jsonPayload.tokens_in,jsonPayload.tokens_out,jsonPayload.pool,jsonPayload.guard,jsonPayload.brain)'
"""


def demonstrate(session):
    """Run Do it: the empty pool as one token, then the stream rows at this checkpoint.

    Do it: the empty pool as one token, then the stream rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one stream that costs nothing; one log read).
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
