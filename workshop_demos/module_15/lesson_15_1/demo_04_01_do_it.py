"""Lesson 15.1 / s4: Build the handbook's graph

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --dry-run
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend firestore --source hr_policy_2026.md --rebuild
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 11}
tenant acme: 0 graph_edges deleted
tenant acme: 0 graph_nodes deleted
25 nodes, 15 edges written for tenant acme (Firestore)
{"event": "graph_built", "

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.1-graph-evidence/Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html#L551

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS="--source hr_policy_2026.md --dry-run"      # the bill, before any call
make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS="--source hr_policy_2026.md --rebuild"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build).
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
