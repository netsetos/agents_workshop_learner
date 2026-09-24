"""Lesson 6.1 / s6: A dated document on the lane: the header's date, the rule in the prompt, the citation event

Summary and purpose:
Do it: the dated revision in, the stream read, revision 1 back

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one upload, one streamed question, one upload; paise)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_one_question_its_tokens_its_price_and_the
Expected observation: >> event chunks embedded effective_from: ingest_reactivated	3	0	2026-10-01
citation 1 smoke_note.md | effective_from 2026-10-01 | quote 'The smoke lantern is kept in bay 7 of the Pune wa'
done: tokens_in 1xxx | tokens_out 3xx | latency_ms 2xxx | the price is on the row, not in the event
answer: The smoke lantern is kept in bay 7 of the Pune warehouse [1], effective from 1 October 2026 ...
>> event chunks embedded effective_from: ingest_reactivated	3	0	None

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.1-context-budget/Netsetos_GCP_Capstone_6.1_Context_Budget_WIX.html#L703

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """worker_line() { for i in $(seq 1 30); do sleep 10
  LINE="$(gcloud logging read "resource.type=\\"cloud_run_revision\\" AND resource.labels.service_name=\\"documind-ingest\\" AND (jsonPayload.event=\\"ingest_ok\\" OR jsonPayload.event=\\"ingest_reactivated\\") AND (jsonPayload.tenant=\\"acme\\" OR jsonPayload.doc_key:\\"acme_\\") AND timestamp>=\\"$1\\"" \\
    --project "$PROJECT" --limit 1 --format='value(jsonPayload.event,jsonPayload.chunks,jsonPayload.embedded,jsonPayload.effective_from)')"
  [ -n "$LINE" ] && { echo ">> event chunks embedded effective_from: $LINE"; return; }; done; echo ">> no worker line in five minutes"; }
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; gcloud storage cp evals/demo/smoke_note_v2.md "gs://$PROJECT-uploads/acme/smoke_note.md"; worker_line "$SINCE"
curl -N -s -X POST "$API/v1/stream" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"Where is the smoke lantern kept, and from when?","tenant_id":"acme"}' \\
  | python -c "
import sys, json
ev, text = None, []
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: '): ev = line[7:]
    elif line.startswith('data: ') and ev == 'citation':
        d = json.loads(line[6:]); print('citation', d['n'], d['source'].split('/')[-1], '| effective_from', d.get('effective_from'), '| quote', repr(d['quote'][:50]))
    elif line.startswith('data: ') and ev == 'token': text.append(json.loads(line[6:])['t'])
    elif line.startswith('data: ') and ev == 'done':
        d = json.loads(line[6:]); print('done: tokens_in', d.get('tokens_in'), '| tokens_out', d.get('tokens_out'), '| latency_ms', d.get('latency_ms'), '| the price is on the row, not in the event')
print('answer:', ''.join(text)[:160])"
SINCE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; gcloud storage cp evals/demo/smoke_note_v1.md "gs://$PROJECT-uploads/acme/smoke_note.md"; worker_line "$SINCE"
"""


def demonstrate(session):
    """Run Do it: the dated revision in, the stream read, revision 1 back at this checkpoint.

    Do it: the dated revision in, the stream read, revision 1 back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one upload, one streamed question, one upload; paise).
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
