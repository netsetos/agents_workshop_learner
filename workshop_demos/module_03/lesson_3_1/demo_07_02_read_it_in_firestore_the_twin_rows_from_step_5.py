"""Lesson 3.1 / s7: Chunk: the unit a question can find

Summary and purpose:
The file you uploaded to both tenants is the cleanest proof of the two identities. Read its chunk rows on each side and compare: the same number of rows, no id in common, and the same set of hashes.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_call_it_a_filter_the_contract_allows_one_that_fi
Expected observation: rows: 3 3
ids in common: set()
same hashes: True
tenant_id              acme
doc_key                acme_5b62d236e0c1...
current                True
locator                preamble
chunk_hash             9c1e6f2a...
embedding_model        text-embedding-005
embedding_task_type    RETRIEVAL_DOCUMENT
schema_version         2
id: acme:5b62d236e0c1...#0 | vector dims: 768

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L822

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read it in Firestore: the twin rows from step 5 at this checkpoint.

    The file you uploaded to both tenants is the cleanest proof of the two identities. Read its chunk rows on each side and compare: the same number of rows, no id in common, and the same set of hashes.

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
    
    def rows_for(tenant, name):
        q = (db.collection("chunks").where("tenant_id", "==", tenant)
             .where("source_uri", "==", f"gs://{PROJECT}-uploads/{tenant}/{name}")
             .where("current", "==", True))
        return {c.id: c.to_dict() for c in q.stream()}
    
    a = rows_for("acme", "gratuity_amendment_2026.md")
    z = rows_for("zeta", "gratuity_amendment_2026.md")
    print("rows:", len(a), len(z))
    print("ids in common:", set(a) & set(z))
    print("same hashes:", sorted(r["chunk_hash"] for r in a.values()) == sorted(r["chunk_hash"] for r in z.values()))
    
    # one row, every stamp the contract promises
    cid, row = next(iter(a.items()))
    for k in ("tenant_id", "doc_key", "current", "locator", "chunk_hash", "embedding_model", "embedding_task_type", "schema_version"):
        print(f"{k:22} {str(row.get(k))[:40]}")
    print("id:", cid, "| vector dims:", len(row["embedding"]))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
