"""Lesson 15.2 / s6: The walk in front of the dense pool, on a candidate

Summary and purpose:
Notice what the first answer says, too. Dense retrieval found FIN-02 without any graph, because the handbook is small and the clause says "purchase". The Spanner walk made sure FIN-02 was in the pool whatever the dense ranking did. On a corpus where the answer's words are far from the question's, that is the difference. Set the threshold on the candidate alone, from your own numbers, and ask again. make candidate cannot pass it (step 7 says why), so this is a gcloud line:

HTML instruction: bash — run only if step 5 seeded nothing (the threshold, on the candidate alone)
Category: recovery. Read the matching README checkpoint before Run.
Prerequisites: shared setup; see README
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L823

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars GRAPH_SEED_DISTANCE=0.45 --quiet     # your number from step 5, not this one
ask152 "$CAND"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Notice what the first answer says, too. Dense retrieval found FIN-02 without any graph, because the handbook is small and the clause says "purchase". The Spanner walk made sure FIN-02 was in the pool whatever the dense ranking did. On a corpus where the answer's words are far from the question's, that is the difference. Set the threshold on the candidate alone, from your own numbers, and ask again. make candidate cannot pass it (step 7 says why), so this is a gcloud line:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run only if step 5 seeded nothing (the threshold, on the candidate alone).
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
