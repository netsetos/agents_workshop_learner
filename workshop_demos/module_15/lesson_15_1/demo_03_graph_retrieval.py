"""Lesson 15.1: demo 03 graph retrieval

Run the lane's graph retrieval example and inspect the evidence.

Run order inside this file:
1. Do it (source window 16)

Prerequisites: demo_02_build_and_inspect_graph.
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
COMMANDS_01 = """python - <<'PY'
import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
P, TENANT = os.environ["PROJECT"], "acme"
db = firestore.Client(project=P)
rows = [d for d in db.collection("graph_extractions").where(filter=FieldFilter("tenant_id", "==", TENANT)).stream()]
chunks = {d.get("chunk_id"): (db.collection("chunks").document(d.get("chunk_id")).get().to_dict() or {}) for d in rows}
x = next(d.to_dict() for d in rows if chunks[d.get("chunk_id")].get("locator") == "FIN-02")
raw = chunks[x["chunk_id"]]["text"]
text = " ".join(raw.split())                                   # a name may wrap across a line
print(f"the extraction cached for {chunks[x['chunk_id']]['locator']} ({x['model']}), beside its passage:")
for line in raw.splitlines():
    print("  | " + line)
names = [e["name"] for e in x["graph"]["entities"]]
for e in x["graph"]["entities"]:
    print(f"  entity   {e['name']!r:22} {e['type']:7} {'in the passage as written' if e['name'].lower() in text.lower() else 'NOT IN THE PASSAGE'}")
for r in x["graph"]["relations"]:
    ok = r["source"] in names and r["target"] in names
    print(f"  relation {r['source']} -[{r['rel']}]-> {r['target']}  {r['confidence']}  {'both ends are entities' if ok else 'DANGLING: build_graph drops it'}")
stated = sum(e["name"].lower() in text.lower() for e in x["graph"]["entities"])
print(f"{stated} of {len(names)} entity names are in the passage as written; {len(rows)} extractions cached for {TENANT}")
PY
make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS="--source hr_policy_2026.md"      # again: the cache answers

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one extraction against its passage; then the build again).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_16', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
