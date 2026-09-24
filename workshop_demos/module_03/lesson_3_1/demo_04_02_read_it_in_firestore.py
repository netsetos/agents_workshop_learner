"""Lesson 3.1 / s4: Source: the object path is the document's identity

Summary and purpose:
Read it in Firestore

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_call_it_the_bucket_then_the_api
Expected observation: acme~annual_report_2026.md                    indexed  chunks=   4 gen=1758540... key=acme_6b0c2f4d1e...
acme~code_on_wages_2019.pdf                   indexed  chunks=  67 gen=1758540... key=acme_a3f9d0c7b2...
acme~hr_policy_2026.md                        indexed  chunks= 283 gen=1758540... key=acme_497809ff2a...
...
{'tenant_id': 'acme', 'name': 'acme/hr_policy_2026.md', 'gcs_uri': 'gs://documind-ai-YOUR-ID-uploads/acme/hr_policy_2026.md',
 'doc_key': 'acme_497809ff...', 'generation': '1758540123456789', 'sha256': '497809ff...', 'chunks': 283,
 'effective_from': None, 'status': 'indexed', 'reused': 0, 'embedded': 283, 'retired': 0,
 'indexed_at': DatetimeWithNanoseconds(...), 'embedding_model': 'text-embedding-005', 'embedding_version': '1'}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L593

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read it in Firestore at this checkpoint.

    Read it in Firestore

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings
    warnings.filterwarnings("ignore", category=UserWarning)   # the Firestore client warns about positional where(); the kit uses that form
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    
    # every ledger row of the tenant, one line each
    for s in db.collection("sources").where("tenant_id", "==", "acme").stream():
        d = s.to_dict()
        print(f"{s.id:45} {d['status']:8} chunks={d['chunks']:4} gen={d['generation']} key={d['doc_key'][:18]}...")
    
    # one row in full: the source contract, field by field
    print(db.collection("sources").document("acme~hr_policy_2026.md").get().to_dict())


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
