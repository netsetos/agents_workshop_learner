"""Lesson 15.3 / s3: The mirror's rules, run

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the mirror's rules, run; no store, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: policy_of: {'None': 'in', 'any': 'any', 'ANY ': 'any', 'us': 'in'}
permits: {'any -> us-central1': True, 'any -> global': True, 'any -> asia-south1': True, 'in -> us-central1': False, 'in -> global': False, 'in -> asia-south1': True}
1. acme (any) makes version v1 current:
     mirror_ok              rag_engine    upsert            acme_v1 uploaded
     mirror_ok              vertex_search upsert            acme_v1 uploaded
   held {'rag_engine': 'us-central1', 'vertex_search': 'global'}
2. globex (in) adds a note:
     mirror_policy_skipped  rag_engine    upsert            in
     mirror_policy_skipped  vertex_search upsert            in
   held {}
3. globex adds a second note:
   held {}
4. acme's policy is turned to in, and version v2 becomes current:
     mirror_policy_skipped  rag_engine    upsert            in
     mirror_policy_skipped  vertex_search upsert            in
   held {

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.3-managed-mirrors/Netsetos_GCP_Capstone_15.3_Managed_Mirrors_WIX.html#L480

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the mirror's rules, run; no store, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, logging, sys
    sys.path[:0] = ["services/ingest", "."]
    import managed                                        # the kit's mirror, as the worker holds it; the two stores below are stand-ins
    from shared.tenancy import permits, policy_of
    
    
    class Brief(logging.Handler):                         # the mirror's JSON lines, one short line each
        def emit(self, r):
            j = json.loads(r.getMessage())
            print(f"     {j['event']:22} {j.get('store', ''):13} {j.get('op', ''):17} {j.get('result', j.get('data_region', ''))}")
    logging.getLogger("documind.ingest").addHandler(Brief())
    logging.getLogger("documind.ingest").setLevel(logging.INFO)
    
    
    class Store:                                          # what the Mirror needs of a store: a name, a region, upsert, delete
        def __init__(self, name, region):
            self.name, self.region, self.docs = name, region, set()
    
        def upsert(self, tenant, doc_key, source_uri, text, meta):
            self.docs.add(doc_key)
            return f"{doc_key} uploaded"
    
        def delete(self, tenant, doc_key):
            gone = doc_key in self.docs
            self.docs.discard(doc_key)
            return int(gone)
    
    
    print("policy_of:", {str(d.get("data_region")): policy_of(d) for d in ({}, {"data_region": "any"}, {"data_region": "ANY "}, {"data_region": "us"})})
    print("permits:", {f"{p} -> {r}": permits(p, r) for p in ("any", "in") for r in ("us-central1", "global", "asia-south1")})
    policy, audit = {"acme": "any", "globex": "in"}, []
    stores = [Store("rag_engine", "us-central1"), Store("vertex_search", "global")]
    m = managed.Mirror(None, stores, "both", policy_for=policy.get,
                       audit=lambda action, actor, target, meta: audit.append(f"{action} {meta['op']} {meta['store']} {target['id']}"))
    print("1. acme (any) makes version v1 current:")
    print("   held", m.upsert("acme", "acme_v1", "gs://b/acme/hr.md", "Notice period: 60 days."))
    print("2. globex (in) adds a note:")
    print("   held", m.upsert("globex", "globex_n1", "gs://b/globex/n1.md", "Visitors sign the register."))
    print("3. globex adds a second note:")
    print("   held", m.upsert("globex", "globex_n2", "gs://b/globex/n2.md", "Badges at all times."))
    policy["acme"] = "in"
    print("4. acme's policy is turned to in, and version v2 becomes current:")
    print("   held", m.upsert("acme", "acme_v2", "gs://b/acme/hr.md", "Notice period: 90 days."))
    print("   the stores still hold", {s.name: sorted(s.docs) for s in stores})
    print("5. v1 is retired:")
    m.retired("acme", ["acme_v1"], "superseded")
    print("   the stores hold", {s.name: sorted(s.docs) for s in stores})
    print("the audit trail:", *audit, sep="\n   ")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
