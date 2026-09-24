"""Lesson 3.1 / s6: Page and section: where inside the document

Summary and purpose:
Call it: a question, and the page on each citation

HTML instruction: bash — run in the operator shell
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_read_it_in_firestore
Expected observation: A confirmed employee at grade E3 or above serves a notice period of 60 days [Source 1].
acme:497809ff...#1 hr_policy_2026.md page None | NP-03 — Notice period Confirmed employees at
acme:497809ff...#2 hr_policy_2026.md page None | PB-02 — Probation ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L722

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","top_k":5,"stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:120]); [print(c['chunk_id'], c['source_uri'].split('/')[-1], 'page', c['page'], '|', c['quote'][:50]) for c in j['citations']]"
"""


def demonstrate(session):
    """Run Call it: a question, and the page on each citation at this checkpoint.

    Call it: a question, and the page on each citation

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell.
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
