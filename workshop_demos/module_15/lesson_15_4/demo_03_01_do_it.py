"""Lesson 15.4 / s3: The four events through the kit's mirror, run

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the kit's mirror through the four events; no store, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: 1. v1 is ingested: the worker's swap, then after_swap()
     mirror_ok     rag_engine    upsert            v1 uploaded, 73 characters
     mirror_ok     vertex_search upsert            v1 uploaded, 73 characters
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
2. v2 replaces it: after_swap(), with v1 in the swap's retired_doc_keys
     mirror_ok     rag_engine    upsert            v2 uploaded, 73 characters
     mirror_ok     vertex_search upsert            v2 uploaded, 73 characters
     mirror_ok     rag_engine    delete:superseded 1
     mirror_ok     vertex_search delete:superseded 1
   make managed-status: rag_engine    in sync
   make managed-status: vertex_search in sync
3. the undo, v1's bytes again: the worker flips the rows back, then after_undo(), which is given no text
     mirror_ok     rag_engine    upsert            v1 uploaded, 7

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L436

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's mirror through the four events; no store, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, logging, sys
    from types import SimpleNamespace
    sys.path[:0] = ["services/ingest", "."]
    import managed                                        # the kit's mirror and make managed-status's check; the stores and the ledger are stand-ins
    
    
    class Brief(logging.Handler):                         # the mirror's JSON lines, one short line each
        def emit(self, r):
            j = json.loads(r.getMessage())
            print(f"     {j['event']:13} {j.get('store', ''):13} {j.get('op', ''):17} {j.get('result', j.get('error', ''))}")
    logging.getLogger("documind.ingest").addHandler(Brief())
    logging.getLogger("documind.ingest").setLevel(logging.INFO)
    
    
    class Store:                                          # a store: upsert, delete, and the listing make managed-status reads
        def __init__(self, name, region):
            self.name, self.region, self.docs, self.fail_next = name, region, {}, False
    
        def upsert(self, tenant, doc_key, source_uri, text, meta):
            if self.fail_next:
                self.fail_next = False
                raise TimeoutError("the import did not finish")
            self.docs[doc_key] = text
            return f"{doc_key} uploaded, {len(text)} characters"
    
        def delete(self, tenant, doc_key):
            return int(self.docs.pop(doc_key, None) is not None)
    
        def listing(self, tenant):
            return dict.fromkeys(self.docs)
    
    
    class Table:                                          # the two collections the mirror and status() read: chunks and sources
        def __init__(self, rows, filters=()):
            self.rows, self.filters = rows, filters
    
        def where(self, field, op, value):
            return Table(self.rows, self.filters + ((field, value),))
    
        def stream(self):
            return [SimpleNamespace(id=k, to_dict=lambda d=d: dict(d)) for k, d in self.rows.items()
                    if all(d.get(f) == v for f, v in self.filters)]
    
    
    db = SimpleNamespace(chunks={}, sources={})
    db.collection = lambda name: Table(getattr(db, name))
    stores = [Store("rag_engine", "us-central1"), Store("vertex_search", "global")]
    m = managed.Mirror(db, stores, "both", policy_for=lambda tenant: "any", audit=lambda *a, **kw: None)
    URI = "gs://documind-ai-YOUR-ID-uploads/zeta/hr_policy_zeta_2026.md"
    V = {"v1": ["# Zeta HR policy", "A confirmed employee serves a notice period of 30 days."]}
    V["v2"] = [V["v1"][0], V["v1"][1].replace("30 days", "45 days")]
    
    
    def current(key, status="indexed"):                   # the rows after the worker's swap (or make retire), and the ledger row
        for k in V:
            for i, text in enumerate(V[k]):
                db.chunks[f"zeta:{k}#{i}"] = {"tenant_id": "zeta", "doc_key": k, "text": text, "kind": "text", "current": k == key and status == "indexed"}
        db.sources["zeta~hr_policy_zeta_2026.md"] = {"tenant_id": "zeta", "doc_key": key, "status": status}
    
    
    def doc(key):
        return SimpleNamespace(tenant_id="zeta", doc_key=key, gcs_uri=URI, doc_type="policy", effective_from=None)
    
    
    def check():
        for s in managed.status(db, stores, "zeta"):
            print(f"   make managed-status: {s['store']:13} {s['status']}" + "".join(f", {k} {s[k + '_doc_keys']}" for k in ("missing", "orphan") if s[k + "_doc_keys"]))
    
    
    print("1. v1 is ingested: the worker's swap, then after_swap()")
    current("v1"); m.after_swap(doc("v1"), "\n\n".join(V["v1"]), {})
    check()
    print("2. v2 replaces it: after_swap(), with v1 in the swap's retired_doc_keys")
    current("v2"); m.after_swap(doc("v2"), "\n\n".join(V["v2"]), {"retired_doc_keys": ["v1"]})
    check()
    print("3. the undo, v1's bytes again: the worker flips the rows back, then after_undo(), which is given no text")
    current("v1"); m.after_undo("zeta", URI, "v1", {"retired_doc_keys": ["v2"]})
    print("   the stores now hold for v1:", {s.name: "..." + s.docs["v1"].split("serves ")[1] for s in stores})
    check()
    print("4. make retire: the rows retired, the ledger row withdrawn, then retired(..., 'withdrawn')")
    current("v1", "withdrawn"); m.retired("zeta", ["v1"], "withdrawn")
    check()
    print("5. make restore, while Vertex AI Search refuses one import: the worker's reactivation, then after_undo()")
    stores[1].fail_next = True
    current("v1"); m.after_undo("zeta", URI, "v1", {"retired_doc_keys": []})
    check()


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
