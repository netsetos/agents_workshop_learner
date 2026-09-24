"""Lesson 3.3 / s6: Validate: the stamp, and the function that reads it

Summary and purpose:
The backfill target prints a plan when APPLY=1 is absent: it reads every current row and counts the ones that fail the same function. On a healthy lane the count is zero, and the target is how you would find out otherwise. It needs the index name from Terraform's outputs; if your checkout has no Terraform state, the second form takes the name from the API instead. The unit tests run the worker's file against doubled SDKs, offline, in a fraction of a second.

HTML instruction: bash — run in the operator shell (both read-only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_validate_every_current_row_of_a_tenant_with_the
Expected observation: {"event": "backfill_vectors_plan", "index": "projects/NUMBER/locations/asia-south1/indexes/1234567890123456789", "tenant": "acme", "current_chunks": N, "needs_document_embedding": 0, "invalid_chunks": 0, "embedding_task_type": "RETRIEVAL_DOCUMENT", "note": "Pause uploads/undo/batch writers; keep answer caches off during repair and validation."}
............
----------------------------------------------------------------------
Ran 12 tests in 0.014s

OK

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L771

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme

# if the line above says VECTOR_INDEX_NAME is empty (no Terraform state in this checkout):
VECTOR_INDEX_NAME="$(gcloud ai indexes list --region="$REGION" --project="$PROJECT" --filter='displayName=documind-chunks' --format='value(name)')" \\
PYTHONPATH=.:services/ingest GOOGLE_CLOUD_PROJECT="$PROJECT" \\
  python services/ingest/reconcile.py --project "$PROJECT" --tenant acme --backfill-vectors

python -m unittest discover -s commands/tests -p test_document_embeddings.py
"""


def demonstrate(session):
    """Run The same check as an operator runs it, and as the tests run it at this checkpoint.

    The backfill target prints a plan when APPLY=1 is absent: it reads every current row and counts the ones that fail the same function. On a healthy lane the count is zero, and the target is how you would find out otherwise. It needs the index name from Terraform's outputs; if your checkout has no Terraform state, the second form takes the name from the API instead. The unit tests run the worker's file against doubled SDKs, offline, in a fraction of a second.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
