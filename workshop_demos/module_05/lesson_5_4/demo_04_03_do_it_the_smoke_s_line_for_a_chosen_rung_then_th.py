"""Lesson 5.4 / s4: Moving one tenant beneath the index by hand, and back

Summary and purpose:
Do it: the smoke's line for a chosen rung, then the pin back

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (two smokes, a rupee each; one field written)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_same_predicates_on_the_chosen_rung_and
Expected observation: [ -- ] vector tier  this request ran on firestore — skipped
acme: retrieval_backend=vector
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
  [PASS] vector tier  20 of 20 chunks came from the index

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L604

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep "vector tier"
python commands/lane.py tenant-backend acme vector
for i in $(seq 1 9); do OUT="$(ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}')"; case "$OUT" in *"backend vector"*) echo "$OUT"; break;; esac; sleep 10; done
DOCUMIND_PROJECT=$PROJECT DOCUMIND_API_URL=$API DOCUMIND_TENANT=acme DOCUMIND_IMPERSONATE_SA=documind-ui-sa@$PROJECT.iam.gserviceaccount.com make smoke 2>&1 | grep "vector tier"
"""


def demonstrate(session):
    """Run Do it: the smoke's line for a chosen rung, then the pin back at this checkpoint.

    Do it: the smoke's line for a chosen rung, then the pin back

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (two smokes, a rupee each; one field written).
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
