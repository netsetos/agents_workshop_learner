"""Lesson 15.2 / s5: The Spanner path: build it, read it, walk it by meaning

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the same graph written to Spanner, then read back)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=documind \\
  python graph.py --project documind-ai-YOUR-ID --tenant acme --backend spanner --source hr_policy_2026.md --rebuild
11 current text chunks for tenant 'acme' from 'hr_policy_2026.md'
{"event": "graph_extracted", "tenant": "acme", "chunks": 11, "extracted": 11, "fresh": 0}
{"event": "graph_built", "tenant": "acme", "backend": "spanner", "chunks": 11, "surface_forms": 28, "nodes": 25, "edges": 15}
tenant acme: 25 nodes (25 with a 768-number vector), 15 edges in Spanner
the edges that name the CFO, as tables (the names joined from GraphNode):
  CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval   stated in FIN-02
one hop from CFO, by the kit's GQL walk: CFO, Purchase approval
  the chunks they cite: FIN-02

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L616

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_BACKEND=spanner GRAPH_ARGS="--source hr_policy_2026.md --rebuild"
python - <<'PY'
import os, sys
sys.path.insert(0, ".")
from google.cloud import firestore, spanner
from google.cloud.spanner_v1 import param_types as T
from shared.documind_graph import SpannerGraph
P, TENANT = os.environ["PROJECT"], "acme"
db = spanner.Client(project=P).instance("documind-graph").database("documind")
fs = firestore.Client(project=P)
loc = lambda cid: (fs.collection("chunks").document(cid).get().to_dict() or {}).get("locator")
p, t = {"t": TENANT}, {"t": T.STRING}
with db.snapshot(multi_use=True) as s:                         # one consistent read of both tables
    nodes, vectors, dims = list(s.execute_sql('SELECT COUNT(*), COUNTIF(embedding IS NOT NULL), MAX(ARRAY_LENGTH(embedding)) FROM GraphNode WHERE tenant_id = @t',
                                              params=p, param_types=t))[0]
    edges = list(s.execute_sql('SELECT COUNT(*) FROM GraphEdge WHERE tenant_id = @t', params=p, param_types=t))[0][0]
    named = list(s.execute_sql('SELECT n.node_id, n.name, e.rel, d.name, e.chunk_id FROM GraphEdge e '
                               'JOIN GraphNode n ON n.tenant_id = e.tenant_id AND n.node_id = e.node_id '
                               'JOIN GraphNode d ON d.tenant_id = e.tenant_id AND d.node_id = e.dst_id '
                               'WHERE e.tenant_id = @t ORDER BY n.name, e.rel', params=p, param_types=t))
print(f"tenant {TENANT}: {nodes} nodes ({vectors} with a {dims}-number vector), {edges} edges in Spanner")
cfo = [r for r in named if "cfo" in (r[1] + " " + r[3]).lower()] or named[:1]
print("the edges that name the CFO, as tables (the names joined from GraphNode):")
for nid, a, rel, b, cid in cfo:
    print(f"  {a} -[{rel}]-> {b}   stated in {loc(cid)}")
walked = SpannerGraph(db).expand([cfo[0][0]], TENANT, hops=1)       # the same rows as a graph: the kit's GQL walk
print(f"one hop from {cfo[0][1]}, by the kit's GQL walk: {', '.join(n['name'] for n in walked)}")
print(f"  the chunks they cite: {', '.join(sorted({loc(c) for n in walked for c in n['chunk_ids']}))}")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same graph written to Spanner, then read back).
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
