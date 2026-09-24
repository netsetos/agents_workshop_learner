"""Lesson 3.3 / s6: Validate: the stamp, and the function that reads it

Summary and purpose:
Read the stamp off one row, Rs 0

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_plan_the_handbook_rs_0
Expected observation: row id: acme:9f3c...#1
  locator                  'NP-03'
  chunk_hash               'f4512754ae41...'
  embedding_model          'text-embedding-005'
  embedding_version        '1'
  embedding_task_type      'RETRIEVAL_DOCUMENT'
  sparse_encoder_version   'blake2b-tf-v1'
  schema_version           2
  kind                     'text'
  doc_type                 'unknown'
  embedding                768 numbers, first three [0.0213, -0.0117, 0.0388]

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L715

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read the stamp off one row, Rs 0 at this checkpoint.

    Read the stamp off one row, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    snap = next(db.collection("chunks").where("tenant_id", "==", "acme")
                  .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md")
                  .where("current", "==", True).where("locator", "==", "NP-03").stream())
    row = snap.to_dict()
    print("row id:", snap.id)
    for k in ("locator", "chunk_hash", "embedding_model", "embedding_version", "embedding_task_type",
              "sparse_encoder_version", "schema_version", "kind", "doc_type"):
        print(f"  {k:24} {row.get(k)!r}")
    print(f"  {'embedding':24} {len(row['embedding'])} numbers, first three {[round(v, 4) for v in list(row['embedding'])[:3]]}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
