"""Lesson 5.4: demo 03 probe backfill and policy

Read the combined-filter probe, tier/backfill evidence and residency policy decision.

Run order inside this file:
1. Do it: the probe, then its evidence (source window 31)
2. Do it: count the tier, plan its refill, read the rows by rung, Rs 0 (source window 37)
3. The policy that sends a tenant home (source window 42)

Prerequisites: demo_02_tenant_pin_and_chaos_candidate.
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


# Original CLI workflow for step_01_the_probe_then_its_evidence.
COMMANDS_01 = """export GOOGLE_CLOUD_PROJECT="$PROJECT"                                    # the probe insists the two agree
python commands/check-firestore-fallback.py
python -c "import json; r = json.load(open('operator-evidence/firestore-combined-filters.json')); print('evidence:', r['filters'], '| current off:', len(r['results']['off']['ids']), 'rows | current on:', len(r['results']['on']['ids']), 'rows | doc_key', r['doc_key'][:17] + '...')"

"""

def step_01_the_probe_then_its_evidence(session):
    """Run Do it: the probe, then its evidence at this checkpoint.

    Do it: the probe, then its evidence

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (one embedding read off a row, a few dozen Firestore reads; nothing written to the cloud).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_count_the_tier_plan_its_refill_read_the_ro.
COMMANDS_02 = """python commands/lane.py vector-status                             # the same as: make vector-status PROJECT=$PROJECT
python commands/lane.py backfill-vectors --tenant acme            # the same as: make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme
make usage PROJECT=$PROJECT HOURS=1 | sed -n '/by retrieval backend/,/^$/p'

"""

def step_02_count_the_tier_plan_its_refill_read_the_ro(session):
    """Run Do it: count the tier, plan its refill, read the rows by rung, Rs 0 at this checkpoint.

    Do it: count the tier, plan its refill, read the rows by rung, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (read-only: the plan writes nothing without --apply).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def step_03_the_policy_that_sends_a_tenant_home(session):
    """Run The policy that sends a tenant home at this checkpoint.

    A tenant's data_region says where its text may be held: any lets the managed mirror copy its current versions abroad, in keeps it on the kit's rows in India, and a missing or unknown value is in, because an unreadable policy is the strict one. retrieval_backend_for() holds every request's backend against it: a managed pin for an in tenant is served from the kit's own rung instead, the deployment's if that is vector or firestore, otherwise Firestore, with policy_fallback 1 on the row, which the warehouse sums into a column. The cell runs the two pure functions behind that decision offline; nothing leaves the machine.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path.insert(0, ".")
    from shared.tenancy import policy_of, permits
    for doc in ({}, {"data_region": "any"}, {"data_region": "in"}, {"data_region": "eu"}):
        print(f"{str(doc):24} -> policy {policy_of(doc)}")
    for policy, region in (("in", "asia-south1"), ("in", "us-central1"), ("in", "global"), ("any", "us-central1")):
        print(f"{policy:4} tenant, a store in {region:12} -> {'may hold it' if permits(policy, region) else 'may not'}")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_31', step_01_the_probe_then_its_evidence),
        ('source_37', step_02_count_the_tier_plan_its_refill_read_the_ro),
        ('source_42', step_03_the_policy_that_sends_a_tenant_home),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
