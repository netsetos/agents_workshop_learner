"""Lesson 5.2 / s8: What hybrid costs, where it cannot go, and what the harness does not measure

Summary and purpose:
Two places, one at startup and one at runtime. A managed backend has no sparse leg to fuse and the Firestore rung's vector index takes one dense vector and nothing else, so check_retrieval_modes() refuses both pairs before the service serves; a tenant pinned to a managed store under hybrid mode is served from the deployment's backend with a retrieval_pin_ignored line instead. At runtime the chaos rung applies to hybrid as to dense: an unreachable index degrades to the Firestore rung, which is dense only, with a vector_search_fallback line and never a 500. The cell asks the validator the two questions offline.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: no call leaves the machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_03_do_it_hybrid_on_a_candidate_the_same_two_questio
Expected observation: vector     hybrid -> allowed
firestore  hybrid -> refused: RETRIEVAL_MODE=hybrid needs RETRIEVAL_BACKEND=vector: the Firestore backend is dense-only. Set RETR...
rag_engine hybrid -> refused: RETRIEVAL_MODE=hybrid needs RETRIEVAL_BACKEND=vector: rag_engine embeds and searches on its own ...
firestore  dense  -> allowed

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L857

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Where hybrid cannot go at this checkpoint.

    Two places, one at startup and one at runtime. A managed backend has no sparse leg to fuse and the Firestore rung's vector index takes one dense vector and nothing else, so check_retrieval_modes() refuses both pairs before the service serves; a tenant pinned to a managed store under hybrid mode is served from the deployment's backend with a retrieval_pin_ignored line instead. At runtime the chaos rung applies to hybrid as to dense: an unreachable index degrades to the Firestore rung, which is dense only, with a vector_search_fallback line and never a 500. The cell asks the validator the two questions offline.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: no call leaves the machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys
    sys.path[:0] = [".", "services/rag-api"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    for k in ("RETRIEVAL_MODE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY", "TOP_K_RETRIEVE", "RERANK_TIMEOUT_S", "SEMANTIC_CACHE"):
        if os.environ.get(k) == "":
            del os.environ[k]                                  # an empty export from an earlier names box means the default
    from config import check_retrieval_modes
    for backend, mode in (("vector", "hybrid"), ("firestore", "hybrid"), ("rag_engine", "hybrid"), ("firestore", "dense")):
        try:
            check_retrieval_modes(backend, mode); print(f"{backend:10} {mode:6} -> allowed")
        except ValueError as e:
            print(f"{backend:10} {mode:6} -> refused: {str(e)[:96]}...")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
