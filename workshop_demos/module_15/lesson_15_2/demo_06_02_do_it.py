"""Lesson 15.2 / s6: The walk in front of the dense pool, on a candidate

Summary and purpose:
First with the walk from Firestore: Then the same candidate, walking from Spanner:

HTML instruction: bash — run in the operator shell, in the kit (the same candidate, the walk from Spanner; the same question)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: gcloud run services update documind-api --region asia-south1 --project documind-ai-YOUR-ID --no-traffic --tag candidate \\
  --update-env-vars "^|^GENERATOR_MODEL=gemini-3.6-flash|...|RETRIEVAL_GRAPH=auto|GRAPH_BACKEND=spanner|SPANNER_INSTANCE=documind-graph|SPANNER_DATABASE=documind" --remove-env-vars GENERATOR_LOCATION
...
>> candidate revision: documind-api-000NN-yyy (deploy/.candidate-revision - make promote moves traffic to it by name)
>> candidate: https://candidate---documind-api-NUMBER.asia-south1.run.app (no traffic; remove with gcloud run services update-traffic documind-api --remove-tags candidate)
/version: retrieval_graph=auto graph_backend=spanner embedding=text-embedding-005@1
Q: Who signs off on a big purchase?
A: Purchases up to Rs 2,00,000 are approved by the function head; above that, the CFO approves [1].
pool 20: the walk put 2 chunk(s) first; retrieval_backend vector

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L796

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make candidate PROJECT="$PROJECT" RETRIEVAL_GRAPH=auto GRAPH_BACKEND=spanner
ask152 "$CAND"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    First with the walk from Firestore: Then the same candidate, walking from Spanner:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same candidate, the walk from Spanner; the same question).
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
