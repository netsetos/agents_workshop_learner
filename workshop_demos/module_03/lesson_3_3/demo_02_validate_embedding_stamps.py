"""Lesson 3.3: demo 02 validate embedding stamps

Read and validate stored stamps, then run the operator's checks.

Run order inside this file:
1. Read the stamp off one row, Rs 0 (source window 23)
2. Validate every current row of a tenant, with the worker's own function (source window 25)
3. The same check as an operator runs it, and as the tests run it (source window 27)

Prerequisites: demo_01_embedding_contract_and_batches.
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


def step_01_read_the_stamp_off_one_row_rs_0(session):
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

def step_02_validate_every_current_row_of_a_tenant_wit(session):
    """Run Validate every current row of a tenant, with the worker's own function at this checkpoint.

    This cell imports the worker's indexer.py as deployed and runs its test over every current acme row. The import builds the worker's embedding client (which is why the project must be in the environment) but nothing is embedded.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings, collections
    warnings.filterwarnings("ignore", category=UserWarning)
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    sys.path[:0] = [".", "services/ingest"]              # shared/ for the sparse encoder, the worker's folder for indexer
    from google.cloud import firestore
    import indexer                                        # the worker's file, exactly as deployed
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    rows = [s.to_dict() for s in db.collection("chunks").where("tenant_id", "==", "acme").where("current", "==", True).stream()]
    ok = [r for r in rows if indexer.document_embedding_matches(r)]
    stamps = collections.Counter((r.get("embedding_model"), str(r.get("embedding_version")), r.get("embedding_task_type"),
                                  len(r["embedding"]) if r.get("embedding") is not None else 0) for r in rows)
    print(f"acme current rows: {len(rows)}  compatible: {len(ok)}  incompatible: {len(rows) - len(ok)}")
    for stamp, n in stamps.most_common():
        print("  ", n, "rows stamped", stamp)
    print("the worker expects:", (indexer.EMBEDDING_MODEL, indexer.EMBEDDING_VERSION, indexer.EMBEDDING_TASK_TYPE, indexer.EMBEDDING_DIMENSIONS))

# Original CLI workflow for step_03_the_same_check_as_an_operator_runs_it_and.
COMMANDS_03 = """make backfill-vectors PROJECT=$PROJECT TENANT_ONLY=acme

# if the line above says VECTOR_INDEX_NAME is empty (no Terraform state in this checkout):
VECTOR_INDEX_NAME="$(gcloud ai indexes list --region="$REGION" --project="$PROJECT" --filter='displayName=documind-chunks' --format='value(name)')" \\
PYTHONPATH=.:services/ingest GOOGLE_CLOUD_PROJECT="$PROJECT" \\
  python services/ingest/reconcile.py --project "$PROJECT" --tenant acme --backfill-vectors

python -m unittest discover -s commands/tests -p test_document_embeddings.py

"""

def step_03_the_same_check_as_an_operator_runs_it_and(session):
    """Run The same check as an operator runs it, and as the tests run it at this checkpoint.

    The backfill target prints a plan when APPLY=1 is absent: it reads every current row and counts the ones that fail the same function. On a healthy lane the count is zero, and the target is how you would find out otherwise. It needs the index name from Terraform's outputs; if your checkout has no Terraform state, the second form takes the name from the API instead. The unit tests run the worker's file against doubled SDKs, offline, in a fraction of a second.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (both read-only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_23', step_01_read_the_stamp_off_one_row_rs_0),
        ('source_25', step_02_validate_every_current_row_of_a_tenant_wit),
        ('source_27', step_03_the_same_check_as_an_operator_runs_it_and),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
