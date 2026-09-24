"""Lesson 5.4 / s4: Moving one tenant beneath the index by hand, and back

Summary and purpose:
Do it: the same predicates on the chosen rung, and two tenants that do not cross

HTML instruction: bash — run in the operator shell (four questions, a few rupees)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_pin_acme_beneath_the_index_and_wait_for_th
Expected observation: backend firestore | vector_chunks 0 | pool 0 | retrieve_ms 4xx | answerable False | first - | The corpus holds nothing near this question: no passage of this
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first x hr_policy_2026.md | ... Rs 40,000 ...
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first x hr_policy_zeta_2026.md | ... Rs 25,000 ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L593

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"doc_type":"policy"}}'
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3,"filters":{"kind":"text"}}'
ask '{"query":"What is the per-trip cap on domestic travel reimbursement?","tenant_id":"acme","stream":false,"top_k":3}'
ask '{"query":"What is the per-trip cap on travel reimbursement?","tenant_id":"zeta","stream":false,"top_k":3}'
"""


def demonstrate(session):
    """Run Do it: the same predicates on the chosen rung, and two tenants that do not cross at this checkpoint.

    Do it: the same predicates on the chosen rung, and two tenants that do not cross

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (four questions, a few rupees).
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
