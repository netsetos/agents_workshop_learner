"""Lesson 3.1 / s3: Tenant: something you are, never something you send

Summary and purpose:
Three reads, in a Python cell. The first lists acme's roster. The second is the UI's reverse lookup, run by you. The third is the tenant's settings document - the data_region: any the Documents page caption showed you.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_call_it_the_roster_from_the_shell_and_two_rest_c
Expected observation: documind-mcp-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com | {'email': 'documind-mcp-sa@...', 'added_at': DatetimeWithNanoseconds(...)}
documind-ui-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com  | {'email': 'documind-ui-sa@...', 'added_at': DatetimeWithNanoseconds(...)}
you@your-company.com                                        | {'email': 'you@your-company.com', 'added_at': DatetimeWithNanoseconds(...)}
tenant for you: ['acme']
{'data_region': 'any', 'data_region_set_at': DatetimeWithNanoseconds(...)}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L491

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read it in Firestore at this checkpoint.

    Three reads, in a Python cell. The first lists acme's roster. The second is the UI's reverse lookup, run by you. The third is the tenant's settings document - the data_region: any the Documents page caption showed you.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings
    warnings.filterwarnings("ignore", category=UserWarning)   # the Firestore client warns about positional where(); the kit uses that form
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]          # exported by the setup block; on Colab, assign your project id here instead
    db = firestore.Client(project=PROJECT)
    
    # 1. the roster: tenants/acme/members/{email}
    for m in db.collection("tenants").document("acme").collection("members").stream():
        print(m.id, "|", m.to_dict())
    
    # 2. the reverse lookup the UI runs for the sidebar line
    hits = db.collection_group("members").where("email", "==", os.environ["ME"].lower()).limit(1).get()
    print("tenant for you:", [h.reference.parent.parent.id for h in hits])
    
    # 3. the tenant's settings: data residency and any backend pins
    print(db.collection("tenant_settings").document("acme").get().to_dict())


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
