"""Lesson 15.2 / s5: The Spanner path: build it, read it, walk it by meaning

Summary and purpose:
The CFO's edge came back two ways. As tables, GraphEdge is joined to GraphNode twice, for the names at both ends. As a graph, the kit's GQL walk goes from the CFO. Both reach Purchase approval and FIN-02. Now the kit's question, seeded by meaning. On Spanner, --ask prints the five nearest names, each with its distance and whether it passed 0.4. Then it walks from the names that passed.

HTML instruction: bash — run in the operator shell, in the kit (one walk of the Spanner graph, seeded by meaning; one embedding call)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend spanner --ask "Who signs off on a big purchase?"
{
 "question": "Who signs off on a big purchase?",
 "backend": "spanner",
 "seeded_by": "meaning",
 "seed_distance": 0.4,
 "nearest": [
  {
   "name": "Purchase approval",
   "kind": "policy",
   "distance": 0.183,
   "seeded": true
  },
  {
   "name": "CFO",
   "kind": "person",
   "distance": 0.415,
   "seeded": false
  },
  {
   "name": "approved cloud bucket",
   "kind": "system",
   "distance": 0.434,
   "seeded": false
  },
  {
   "name": "tax clearance",
   "kind": "policy",
   "distance": 0.434,
   "seeded": false
  },
  {
   "name": "Travel reimbursement",
   "kind": "policy",
   "distance": 0.459,
   "seeded": false
 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L665

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_BACKEND=spanner GRAPH_ARGS='--ask "Who signs off on a big purchase?"'
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    The CFO's edge came back two ways. As tables, GraphEdge is joined to GraphNode twice, for the names at both ends. As a graph, the kit's GQL walk goes from the CFO. Both reach Purchase approval and FIN-02. Now the kit's question, seeded by meaning. On Spanner, --ask prints the five nearest names, each with its distance and whether it passed 0.4. Then it walks from the names that passed.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one walk of the Spanner graph, seeded by meaning; one embedding call).
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
