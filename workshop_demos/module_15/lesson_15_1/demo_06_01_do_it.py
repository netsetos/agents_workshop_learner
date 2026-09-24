"""Lesson 15.1 / s6: Audit an extraction, and build again

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (one extraction against its passage; then the build again)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: the extraction cached for FIN-02 (gemini-3.1-flash-lite), beside its passage:
  | FIN-02 — Purchase approval
  | Purchases up to Rs 2,00,000 are approved by the function head. Above that, the CFO
  | approves. Splitting a purchase to stay under a threshold is a disciplinary matter.
  entity   'Purchase approval'    policy  in the passage as written
  entity   'function head'        person  in the passage as written
  entity   'CFO'                  person  in the passage as written
  relation function head -[APPROVES_UP_TO_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
  relation CFO -[APPROVES_ABOVE_RS_2_00_000]-> Purchase approval  0.9  both ends are entities
3 of 3 entity names are in the passage as written; 11 extractions cached for acme
cd services/ingest && GOOGLE_CLOUD_PROJECT=documind-ai-YOUR-ID PYTHONPATH=../.. \\
  SPANNER_INSTANCE=documind-graph SPANNER_DATABASE=

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.1-graph-evidence/Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html#L635

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one extraction against its passage; then the build again).
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
