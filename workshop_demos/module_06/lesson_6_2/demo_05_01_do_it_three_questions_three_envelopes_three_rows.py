"""Lesson 6.2 / s5: Three refusals: the model's twice, the API's once, and how their envelopes differ

Summary and purpose:
Do it: three questions, three envelopes, three rows

HTML instruction: bash — run in the operator shell (three questions, two of them model calls: a rupee; one log read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_one_question_two_halves_three_rows
Expected observation: answerable False | confidence low | citations 0 | backend vertex | tokens 1xxx + 1xx | cost_usd 0.00xxxx | pool 20 | The provided context does not contain information about Globex's not
answerable False | confidence low | citations 0 | backend vertex | tokens 1xxx + 1xx | cost_usd 0.00xxxx | pool 20 | The context covers FY2025 and FY2026; it does not state the revenue f
answerable False | confidence low | citations 0 | backend none | tokens 0 + 0 | cost_usd 0.0 | pool 0 | The corpus holds nothing near this question: no passage of this tena
acme	False	none	0	0.0
acme	False	vertex	1xxx	0.00xxxx
globex	False	vertex	1xxx	0.00xxxx

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/06-generation/6.2-structured-answers/Netsetos_GCP_Capstone_6.2_Structured_Answers_WIX.html#L622

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask() { curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" -d "$1" \\
  | python -c "import sys, json; j = json.load(sys.stdin); print('answerable', j['answerable'], '| confidence', j['confidence'], '| citations', len(j['citations']), '| backend', j['backend'], '| tokens', j['tokens_in'], '+', j['tokens_out'], '| cost_usd', j['cost_usd'], '| pool', j['stages']['pool'], '|', j['answer'][:64])"; }
ask '{"query":"What is the notice period at Globex for a confirmed employee?","tenant_id":"globex","stream":false,"top_k":3}'
ask '{"query":"What was ACME\\u0027s revenue in FY2024?","tenant_id":"acme","stream":false,"top_k":3}'
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"doc_type":"policy"}}'
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" AND jsonPayload.unanswerable_flag=1' \\
  --project "$PROJECT" --freshness 5m --limit 3 --format='value(jsonPayload.tenant,jsonPayload.answerable,jsonPayload.model_backend,jsonPayload.tokens_in,jsonPayload.cost_usd)'
"""


def demonstrate(session):
    """Run Do it: three questions, three envelopes, three rows at this checkpoint.

    Do it: three questions, three envelopes, three rows

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (three questions, two of them model calls: a rupee; one log read).
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
