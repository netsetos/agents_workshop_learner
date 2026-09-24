"""Lesson 5.4 / s4: Moving one tenant beneath the index by hand, and back

Summary and purpose:
Do it: pin acme beneath the index, and wait for the API to notice

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (one field written; up to nine questions while the minute passes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_rung_under_three_predicate_sets
Expected observation: acme: retrieval_backend=firestore
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
backend firestore | vector_chunks 0 | pool 20 | retrieve_ms 5xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L580

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python commands/lane.py tenant-backend acme firestore          # the same as: make tenant-backend PROJECT=$PROJECT TENANT=acme RETRIEVAL_BACKEND=firestore
ask() { curl -s -X POST "$API/v1/query" -H "Authorization: Bearer $(tok "$API")" -H "Content-Type: application/json" -d "$1" \\
  | python -c "import sys, json; j = json.load(sys.stdin); s = j.get('stages', {}); c = j.get('citations') or []; print('backend', s.get('retrieval_backend'), '| vector_chunks', s.get('vector_chunks'), '| pool', s.get('pool'), '| retrieve_ms', s.get('retrieve_ms'), '| answerable', j.get('answerable'), '| first', (c[0]['chunk_id'].rsplit('#', 1)[1] + ' ' + c[0]['source_uri'].split('/')[-1][:22]) if c else '-', '|', j.get('answer', '')[:60])"; }
for i in $(seq 1 9); do
  OUT="$(ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}')"; echo "$OUT"
  case "$OUT" in *"backend firestore"*) break;; esac; sleep 10                     # the pin is read once a minute
done
"""


def demonstrate(session):
    """Run Do it: pin acme beneath the index, and wait for the API to notice at this checkpoint.

    Do it: pin acme beneath the index, and wait for the API to notice

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one field written; up to nine questions while the minute passes).
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
