"""Lesson 15.1 / s5: Read it back: the counts, and one edge with its source

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: tenant acme: 25 nodes, 15 edges in Firestore
the nodes the most chunks cite:
  Earned leave                     policy  3 chunk(s)
  Notice period                    policy  2 chunk(s)
  function head                    person  2 chunk(s)
  probation                        policy  2 chunk(s)
one edge, read back with its source chunk:
  CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval   confidence 0.9
  stated in acme:497809ffbaa6...#9 (FIN-02, hr_policy_2026.md):
    FIN-02 — Purchase approval
    Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
    approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  both names in the passage as written: CFO yes, Purchase approval yes

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.1-graph-evidence/Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html#L581

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    P, TENANT = os.environ["PROJECT"], "acme"
    db = firestore.Client(project=P)
    q = lambda coll: db.collection(coll).where(filter=FieldFilter("tenant_id", "==", TENANT))
    nodes = {d.get("node_id"): d.to_dict() for d in q("graph_nodes").stream()}
    edges = [d.to_dict() for d in q("graph_edges").stream()]
    print(f"tenant {TENANT}: {len(nodes)} nodes, {len(edges)} edges in Firestore")
    print("the nodes the most chunks cite:")
    for n in sorted(nodes.values(), key=lambda n: (-len(n["chunk_ids"]), n["name"]))[:4]:
        print(f"  {n['name'][:32]:32} {n['kind']:7} {len(n['chunk_ids'])} chunk(s)")
    pick = [e for e in edges if "cfo" in (nodes[e["node_id"]]["name"] + nodes[e["dst_id"]]["name"]).lower()] or sorted(edges, key=lambda e: -e["confidence"])
    e = pick[0]
    src_name, dst_name = nodes[e["node_id"]]["name"], nodes[e["dst_id"]]["name"]
    chunk = db.collection("chunks").document(e["chunk_id"]).get().to_dict() or {}
    print("one edge, read back with its source chunk:")
    print(f"  {src_name} -[{e['rel']}]-> {dst_name}   confidence {e['confidence']}")
    version, n = e["chunk_id"].split("#")
    print(f"  stated in {version[:17]}...#{n} ({chunk.get('locator')}, {chunk.get('source_uri', '').rsplit('/', 1)[-1]}):")
    for line in chunk.get("text", "").splitlines():
        print("    " + line)
    text = " ".join(chunk.get("text", "").split()).lower()          # a name may wrap across a line
    print(f"  both names in the passage as written: {src_name} {'yes' if src_name.lower() in text else 'NO'}, {dst_name} {'yes' if dst_name.lower() in text else 'NO'}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
