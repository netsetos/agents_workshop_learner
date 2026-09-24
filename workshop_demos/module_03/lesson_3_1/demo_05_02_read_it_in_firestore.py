"""Lesson 3.1 / s5: Version: the bytes decide, and the same file in two tenants proves it

Summary and purpose:
The per-version claim lives in documents/{doc_key}. Build both keys from the local hash and read both claims. They differ in exactly one field.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_one_file_two_tenants
Expected observation: acme indexed 3 acme gs://documind-ai-YOUR-ID-uploads/acme/gratuity_amendment_2026.md
zeta indexed 3 zeta gs://documind-ai-YOUR-ID-uploads/zeta/gratuity_amendment_2026.md

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L666

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read it in Firestore at this checkpoint.

    The per-version claim lives in documents/{doc_key}. Build both keys from the local hash and read both claims. They differ in exactly one field.

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
    
    import hashlib
    sha = hashlib.sha256(open("evals/demo/gratuity_amendment_2026.md", "rb").read()).hexdigest()
    for tenant in ("acme", "zeta"):
        claim = db.collection("documents").document(f"{tenant}_{sha}").get().to_dict()
        print(tenant, claim["status"], claim["chunks"], claim["tenant_id"], claim["gcs_uri"])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
