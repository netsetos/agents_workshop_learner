"""Lesson 5.4 / s8: What the rung costs, where it cannot go, and the policy that sends a tenant home

Summary and purpose:
A tenant's data_region says where its text may be held: any lets the managed mirror copy its current versions abroad, in keeps it on the kit's rows in India, and a missing or unknown value is in, because an unreadable policy is the strict one. retrieval_backend_for() holds every request's backend against it: a managed pin for an in tenant is served from the kit's own rung instead, the deployment's if that is vector or firestore, otherwise Firestore, with policy_fallback 1 on the row, which the warehouse sums into a column. The cell runs the two pure functions behind that decision offline; nothing leaves the machine.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_count_the_tier_plan_its_refill_read_the_ro
Expected observation: {}                       -> policy in
{'data_region': 'any'}   -> policy any
{'data_region': 'in'}    -> policy in
{'data_region': 'eu'}    -> policy in
in   tenant, a store in asia-south1  -> may hold it
in   tenant, a store in us-central1  -> may not
in   tenant, a store in global       -> may not
any  tenant, a store in us-central1  -> may hold it

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.4-fallback/Netsetos_GCP_Capstone_5.4_Fallback_WIX.html#L834

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
