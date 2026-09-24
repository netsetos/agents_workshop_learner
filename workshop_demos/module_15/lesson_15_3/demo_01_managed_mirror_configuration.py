"""Lesson 15.3: demo 01 managed mirror configuration

Inspect managed mirror configuration and residency policy.

Run order inside this file:
1. Do it (source window 9)
2. Do it (source window 13)

Prerequisites: setup_prepare.
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


def step_01_example(session):
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

# Original CLI workflow for step_02_example.
COMMANDS_02 = """for t in acme zeta globex; do
  make tenant-policy PROJECT="$PROJECT" TENANT=$t        # where its text may be held
  make tenant-backend PROJECT="$PROJECT" TENANT=$t       # which store answers it
done
make managed-status PROJECT="$PROJECT"                     # every store, held against the ledger

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_13', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
