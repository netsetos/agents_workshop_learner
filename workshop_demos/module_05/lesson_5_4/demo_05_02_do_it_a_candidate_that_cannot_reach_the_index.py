"""Lesson 5.4 / s5: The chaos rung: an index that will not answer, on a candidate that takes no traffic

Summary and purpose:
Do it: a candidate that cannot reach the index

HTML instruction: bash — run in the operator shell (the undo: the real name back on the template, the tag dropped, the live service asked once)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_a_candidate_that_cannot_reach_the_index
Expected observation: template now: documind_chunks_v1
backend vector | vector_chunks 20 | pool 20 | retrieve_ms 6xx | answerable True | first 1 hr_policy_2026.md | A confirmed employee in grade E3 ...
100;documind-api-00048-xyz

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L664

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars VECTOR_DEPLOYED_INDEX_ID="$VECTOR_DEPLOYED_INDEX_ID" --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
echo "template now: $(svc_env documind-api VECTOR_DEPLOYED_INDEX_ID)"
ask '{"query":"What is the notice period for a confirmed E3?","tenant_id":"acme","stream":false,"top_k":3}'
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'
"""


def demonstrate(session):
    """Run Do it: a candidate that cannot reach the index at this checkpoint.

    Do it: a candidate that cannot reach the index

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the undo: the real name back on the template, the tag dropped, the live service asked once).
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
