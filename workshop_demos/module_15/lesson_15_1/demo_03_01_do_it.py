"""Lesson 15.1 / s3: The rules, run

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the rules, run; no model, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: extraction: gemini-3.1-flash-lite, entity types person, org, product, policy, system, location, date
resolution: normalise(), then text-embedding-005 cosine >= 0.92
  normalise('ACME Pvt. Ltd.'        ) = 'acme'
  normalise('Acme Private Limited'  ) = 'acme'
  normalise('ACME Inc'              ) = 'acme'
  normalise('function head'         ) = 'function head'
  normalise('Function Head'         ) = 'function head'
  normalise('CFO'                   ) = 'cfo'
  normalise('Chief Financial Officer') = 'chief financial officer'
resolve_entities(), with an embedding that tells every name apart:
  'ACME Pvt. Ltd.'         -> 'ACME Pvt. Ltd.'
  'Acme Private Limited'   -> 'ACME Pvt. Ltd.'
  'ACME Inc'               -> 'ACME Pvt. Ltd.'
  'function head'          -> 'function head'
  'Function Head'          -> 'function head'
  'CFO'                    -> 'CFO'
  'Chief Financial Officer' -> 'C

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.1-graph-evidence/Netsetos_GCP_Capstone_15.1_Graph_Evidence_WIX.html#L464

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the rules, run; no model, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path[:0] = ["services/ingest", "."]
    import graph                                                   # the kit's own pipeline; nothing below calls a model
    X = graph.GraphExtraction
    print(f"extraction: {graph.EXTRACT_MODEL}, entity types {', '.join(graph.Entity.model_fields['type'].annotation.__args__)}")
    print(f"resolution: normalise(), then {graph.EMBED_MODEL} cosine >= {graph.RESOLVE_THRESHOLD}")
    forms = ["ACME Pvt. Ltd.", "Acme Private Limited", "ACME Inc", "function head", "Function Head", "CFO", "Chief Financial Officer"]
    for f in forms:
        print(f"  normalise({f!r:24}) = {graph.normalise(f)!r}")
    apart = lambda names: [[1.0 if i == j else 0.0 for j in range(len(names))] for i in range(len(names))]
    canon = graph.resolve_entities(forms, apart)                   # an embedding that tells every name apart: only normalise() merges
    print("resolve_entities(), with an embedding that tells every name apart:")
    for f in forms:
        print(f"  {f!r:24} -> {canon[f]!r}")
    ex = [{"chunk_id": "c1", "graph": X.model_validate({"entities": [{"name": "function head", "type": "person"}, {"name": "CFO", "type": "person"},
                                                                     {"name": "Purchase approval", "type": "policy"}],
                                                        "relations": [{"source": "CFO", "target": "Purchase approval", "rel": "APPROVES", "confidence": 0.9},
                                                                      {"source": "CFO", "target": "board", "rel": "REPORTS_TO", "confidence": 0.8}]})},
          {"chunk_id": "c2", "graph": X.model_validate({"entities": [{"name": "Function Head", "type": "person"}, {"name": "Travel reimbursement", "type": "policy"}],
                                                        "relations": [{"source": "Function Head", "target": "Travel reimbursement", "rel": "APPROVES", "confidence": 0.9},
                                                                      {"source": "Function Head", "target": "Function Head", "rel": "IS", "confidence": 0.5}]})}]
    names = [e.name for x in ex for e in x["graph"].entities]
    canon = graph.resolve_entities(names, apart)
    nodes, edges = graph.build_graph(ex, canon)
    print("build_graph() on two passages:")
    for nid, n in sorted(nodes.items(), key=lambda kv: kv[1]["name"]):
        print(f"  node {n['name']!r:24} {n['kind']:7} id {nid[:12]}...  cited by {sorted(n['chunks'])}")
    for (s, d, rel), v in edges.items():
        print(f"  edge {nodes[s]['name']} -[{rel}]-> {nodes[d]['name']}  from {v['chunk_id']}, confidence {v['confidence']}")
    print(f"  {sum(len(x['graph'].relations) for x in ex) - len(edges)} relations dropped: 'board' is no entity (dangling), and Function Head -[IS]-> itself")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
