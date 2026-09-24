"""Lesson 6.4 / s5: The answer: asked in Chat, streamed, and the row that names you

Summary and purpose:
In the browser, open Chat and ask: What colour badge do visitors wear at the Pune warehouse? The sources arrive first and the answer streams after them. The answer ends with a pill. Hover over it to see the note's clause, and open Sources under the answer. Then ask the same question from the shell and read the two newest rows:

HTML instruction: bash — run in the operator shell (one question, a rupee; one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_write_the_note_upload_it_in_the_browser_fo
Expected observation: from the shell: Every visitor to the Pune warehouse wears an amber badge, issued at gate | ['pune_visitor_rules.md']
2026-09-2xT1x:xx:xx.xxxxxxZ	query	documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com	ui	acme	20
2026-09-2xT1x:xx:xx.xxxxxxZ	stream	you@example.com	ui	acme	20

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.4-ui-journey/Netsetos_GCP_Capstone_6.4_UI_Journey_WIX.html#L609

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d '{"query":"What colour badge do visitors wear at the Pune warehouse?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; raw=sys.stdin.read(); j=json.loads(raw) if raw.startswith('{') else {'answer': 'not JSON: ' + raw[:80], 'citations': []}; print('from the shell:', j.get('answer', j)[:70], '|', [c['source_uri'].split('/')[-1] for c in j.get('citations', [])[:1]])"
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND (jsonPayload.event="stream" OR jsonPayload.event="query")' \\
  --project "$PROJECT" --freshness 15m --limit 2 --format='value(timestamp,jsonPayload.event,jsonPayload.user,jsonPayload.brain,jsonPayload.tenant,jsonPayload.pool)'
"""


def demonstrate(session):
    """Run Do it: ask in the browser, ask from the shell, read both rows at this checkpoint.

    In the browser, open Chat and ask: What colour badge do visitors wear at the Pune warehouse? The sources arrive first and the answer streams after them. The answer ends with a pill. Hover over it to see the note's clause, and open Sources under the answer. Then ask the same question from the shell and read the two newest rows:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (one question, a rupee; one log read).
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
