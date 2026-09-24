"""Lesson 3.3 / s7: Carry-over: re-issue the handbook, embed only what changed

Summary and purpose:
The worker's planner on the two versions of the handbook, with a stand-in for what held_vectors() would lend: one vector per version-1 hash.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_03_the_same_check_as_an_operator_runs_it_and_as_the
Expected observation: v2: 283 chunks, reused 281, to embed 2: ['preamble', 'NP-03']
  preamble: hash 903e2b39ee92 -> b4736d2f3e52
  NP-03: hash f4512754ae41 -> 876232171dec

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.3-embeddings/Netsetos_GCP_Capstone_3.3_Embeddings_WIX.html#L847

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Plan it locally, Rs 0 at this checkpoint.

    The worker's planner on the two versions of the handbook, with a stand-in for what held_vectors() would lend: one vector per version-1 hash.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    sys.path[:0] = [".", "services/ingest"]
    from shared import documind_corpus as dc
    from indexer import plan_carry_over
    def cut(path):
        text = open(path, encoding="utf-8").read()
        return dc.chunk_document({"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://x", "text": text}, "acme")
    v1, v2 = cut("evals/corpus/acme/hr_policy_2026.md"), cut("evals/demo/hr_policy_2026_v2.md")
    held = {c["chunk_hash"]: ["the v1 vector"] for c in v1}          # what held_vectors() would lend: one per v1 hash
    vectors, misses = plan_carry_over(v2, held)
    print(f"v2: {len(v2)} chunks, reused {len(v2) - len(misses)}, to embed {len(misses)}: {[v2[i]['locator'] for i in misses]}")
    for i in misses:
        old = next(c for c in v1 if c["locator"] == v2[i]["locator"])
        print(f"  {v2[i]['locator']}: hash {old['chunk_hash'][:12]} -> {v2[i]['chunk_hash'][:12]}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
