"""Lesson 3.3 / s8: The sparse twin, the notebook twin, and what embedding bills

Summary and purpose:
Run it on the lane's text, Rs 0

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_04_undo_it_the_same_bytes_again_and_nothing_is_embe
Expected observation: row stamp: blake2b-tf-v1 | encoder here: blake2b-tf-v1
NP-03: 41 words, 33 distinct -> 33 sparse dimensions, max weight 2.5
the question: 13 dimensions, 9 shared with NP-03: ['a', 'at', 'confirmed', 'days', 'e3', 'employee', 'grade', 'notice', 'of']
same text twice, same dimensions: True

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L985

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Run it on the lane's text, Rs 0 at this checkpoint.

    Run it on the lane's text, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path.insert(0, ".")
    from google.cloud import firestore
    from shared.sparse_encoder import sparse_encode, SPARSE_ENCODER_VERSION, _tokens
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    row = next(db.collection("chunks").where("tenant_id", "==", "acme")
                 .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/hr_policy_2026.md")
                 .where("current", "==", True).where("locator", "==", "NP-03").stream()).to_dict()
    dv, dd = sparse_encode(row["text"])
    print("row stamp:", row["sparse_encoder_version"], "| encoder here:", SPARSE_ENCODER_VERSION)
    print(f"NP-03: {len(_tokens(row['text']))} words, {len(dd)} distinct -> {len(dd)} sparse dimensions, max weight {max(dv)}")
    q = "How many days of notice does a confirmed employee at grade E3 serve?"
    qv, qd = sparse_encode(q)
    print(f"the question: {len(qd)} dimensions, {len(set(qd) & set(dd))} shared with NP-03:", sorted(set(_tokens(q)) & set(_tokens(row['text']))))
    print("same text twice, same dimensions:", sparse_encode(row["text"]) == (dv, dd))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
