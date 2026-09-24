"""Lesson 3.3 / s6: Validate: the stamp, and the function that reads it

Summary and purpose:
This cell imports the worker's indexer.py as deployed and runs its test over every current acme row. The import builds the worker's embedding client (which is why the project must be in the environment) but nothing is embedded.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_read_the_stamp_off_one_row_rs_0
Expected observation: acme current rows: N  compatible: N  incompatible: 0
   N rows stamped ('text-embedding-005', '1', 'RETRIEVAL_DOCUMENT', 768)
the worker expects: ('text-embedding-005', '1', 'RETRIEVAL_DOCUMENT', 768)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L746

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
