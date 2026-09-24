"""Lesson 15.2 / s6: The walk in front of the dense pool, on a candidate

Summary and purpose:
Choose a value just past the purchase or approval name, and below the first name that has nothing to do with purchases. The undo below removes it. Last, put the template back. Environment variables carry over from one revision to the next, so the candidate's settings would ride into the next gcloud run services update of the API. The undo writes RETRIEVAL_GRAPH=off and GRAPH_BACKEND=firestore, removes any GRAPH_SEED_DISTANCE, drops the tag, and deletes .candidate-revision.

HTML instruction: bash — run in the operator shell, in the kit (the template put back, the tag dropped; the live revision was never touched)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it
Expected observation: 100	documind-api-000NN-xxx

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L830

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars RETRIEVAL_GRAPH=off,GRAPH_BACKEND=firestore --remove-env-vars GRAPH_SEED_DISTANCE --quiet     # env vars merge: put the template back
gcloud run services update-traffic documind-api --region "$REGION" --project "$PROJECT" --remove-tags candidate --quiet
rm -f .candidate-revision      # make promote flips to the revision this file names, tag or no tag
gcloud run services describe documind-api --region "$REGION" --project "$PROJECT" --format='value(status.traffic[].percent,status.traffic[].revisionName)'
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Choose a value just past the purchase or approval name, and below the first name that has nothing to do with purchases. The undo below removes it. Last, put the template back. Environment variables carry over from one revision to the next, so the candidate's settings would ride into the next gcloud run services update of the API. The undo writes RETRIEVAL_GRAPH=off and GRAPH_BACKEND=firestore, removes any GRAPH_SEED_DISTANCE, drops the tag, and deletes .candidate-revision.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the template put back, the tag dropped; the live revision was never touched).
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
