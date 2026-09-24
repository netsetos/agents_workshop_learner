"""Lesson 5.2 / s7: The knob: hybrid on a candidate that takes no traffic, compared, then removed

Summary and purpose:
Do it: hybrid on a candidate, the same two questions to both revisions, then undo

HTML instruction: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live mode read again)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_02_do_it_hybrid_on_a_candidate_the_same_two_questio
Expected observation: live mode: dense
100;documind-api-00042-xyz

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L819

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --remove-env-vars RETRIEVAL_MODE --quiet
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
curl -s "$API/version" -H "Authorization: Bearer $(tok "$API")" | python -c "import sys, json; print('live mode:', json.load(sys.stdin)['retrieval_mode'])"
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'
"""


def demonstrate(session):
    """Run Do it: hybrid on a candidate, the same two questions to both revisions, then undo at this checkpoint.

    Do it: hybrid on a candidate, the same two questions to both revisions, then undo

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (the undo: the variable removed, the tag dropped, the live mode read again).
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
