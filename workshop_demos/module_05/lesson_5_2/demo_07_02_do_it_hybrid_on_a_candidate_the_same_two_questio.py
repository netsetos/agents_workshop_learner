"""Lesson 5.2 / s7: The knob: hybrid on a candidate that takes no traffic, compared, then removed

Summary and purpose:
Do it: hybrid on a candidate, the same two questions to both revisions, then undo

HTML instruction: bash — run in the operator shell (four questions, one or two rupees)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_hybrid_on_a_candidate_the_same_two_questio
Expected observation: What is the total payable on invoice INV-2026-0412?
   documind-  ['  0 inv_2026_0412.md', ' 36 cgst_act_2017.pdf', ...] | retrieve_ms 6xx | pool 20 | vector_chunks 20
   candidate  ['  0 inv_2026_0412.md', ' 36 cgst_act_2017.pdf', ...] | retrieve_ms 7xx | pool 20 | vector_chunks 20
What is the notice period for a confirmed E3?
   documind-  ['  1 hr_policy_2026.md', '  4 hr_policy_2026.md', '  2 hr_policy_2026.md'] | retrieve_ms 6xx | pool 20 | vector_chunks 20
   candidate  ['  1 hr_policy_2026.md', '  4 hr_policy_2026.md', '  2 hr_policy_2026.md'] | retrieve_ms 7xx | pool 20 | vector_chunks 20

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L805

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """ask() { curl -s -X POST "$1/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" \\
  -d "{\\"query\\":\\"$2\\",\\"tenant_id\\":\\"acme\\",\\"stream\\":false,\\"top_k\\":3}" \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j['stages']; print('  ', '$1'.split('//')[1].split('---')[0].split('.')[0][:9].ljust(10), [c['chunk_id'].rsplit('#', 1)[1].rjust(3) + ' ' + c['source_uri'].split('/')[-1][:22] for c in j['citations']], '| retrieve_ms', s['retrieve_ms'], '| pool', s['pool'], '| vector_chunks', s['vector_chunks'])"; }
for Q in "What is the total payable on invoice INV-2026-0412?" "What is the notice period for a confirmed E3?"; do
  echo "$Q"; ask "$API" "$Q"; ask "$CAND" "$Q"
done
"""


def demonstrate(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (four questions, one or two rupees).
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
