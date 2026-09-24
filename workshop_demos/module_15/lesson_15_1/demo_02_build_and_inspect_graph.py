"""Lesson 15.1: demo 02 build and inspect graph

Build the graph and inspect its nodes/edges against the source material.

Run order inside this file:
1. Do it (source window 12)
2. Do it (source window 14)

Prerequisites: demo_01_graph_contracts.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_example.
COMMANDS_01 = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS="--source hr_policy_2026.md --dry-run"      # the bill, before any call
make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS="--source hr_policy_2026.md --rebuild"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the handbook's clauses: a count, then the build).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_example(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_12', step_01_example),
        ('source_14', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
