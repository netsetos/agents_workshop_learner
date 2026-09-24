"""Lesson 5.1 / s5: Filters: two keys, a 400 for everything else

Summary and purpose:
Do it: four filters, four verdicts

HTML instruction: bash — run in the operator shell (two 400s cost nothing; two questions, paise)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_one_identity_two_tenants_one_outsider
Expected observation: 400 | unknown filter key(s) tenant_id; allowed: doc_type, kind
400 | filter doc_type must be a non-empty string
200 | answerable False pool 0 | The corpus holds nothing near this question: no passage of this
200 | answerable True pool 20 | A confirmed employee at grade E3 or above serves a notice period

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.1-query-filters/Netsetos_GCP_Capstone_5.1_Query_Filters_WIX.html#L737

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask() { curl -s -w "\\nHTTP %{http_code}" -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d "{\\"query\\":\\"What is the notice period for a confirmed E3?\\",\\"tenant_id\\":\\"acme\\",\\"stream\\":false,\\"filters\\":$1}" \\
  | python -c "import sys,json; raw=sys.stdin.read(); body,code=raw.rsplit('HTTP ',1); j=json.loads(body); print(code.strip(), '|', (j.get('detail') or f\\"answerable {j['answerable']} pool {j['stages']['pool']} | {j['answer'][:60]}\\"))"; }
ask '{"tenant_id":"zeta"}'
ask '{"doc_type":3}'
ask '{"doc_type":"policy"}'
ask '{"kind":"text"}'
"""


def demonstrate(session):
    """Run Do it: four filters, four verdicts at this checkpoint.

    Do it: four filters, four verdicts

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (two 400s cost nothing; two questions, paise).
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
