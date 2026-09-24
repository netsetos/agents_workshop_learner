"""Lesson 15.2 / s4: The Firestore path: a name the question contains

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (two walks of the Firestore graph; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --ask "Who signs off on a big purchase?"
{
 "question": "Who signs off on a big purchase?",
 "backend": "firestore",
 "seeded_by": "containment",
 "seeds": [],
 "nodes": [],
 "chunk_ids": []
}
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --ask "Which purchases need the CFO?"
{
 "question": "Which purchases need the CFO?",
 "backend": "firestore",
 "seeded_by": "containment",
 "seeds": [
  "CFO"
 ],
 "nodes": [
  "CFO",
  "Purchase approval"
 ],
 "chunk_ids": [
  "acme:497809ffbaa603c49577

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L521

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS='--ask "Who signs off on a big purchase?"'
make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS='--ask "Which purchases need the CFO?"'
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two walks of the Firestore graph; reads only).
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
