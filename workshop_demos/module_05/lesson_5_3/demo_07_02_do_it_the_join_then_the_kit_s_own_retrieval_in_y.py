"""Lesson 5.3 / s7: found_by: stamped on every chunk, counted on the answer, absent from the citation

Summary and purpose:
Do it: the join, then the kit's own retrieval in your process, then the smoke

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it_the_join_then_the_kit_s_own_retrieval_in_y
Expected observation: 20 chunks in the pool, found_by: {'vector': 20}
first three: [('NP-03', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx), ('...', 'vector', 0.7xxx)]

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L823

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; the kit's retrieve() in this process: one embedding, one index query, one Firestore read).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings, collections
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path[:0] = [".", "services/rag-api"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])          # settings.project_id; REGION and the index names are already exported
    for k in ("RETRIEVAL_MODE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY", "TOP_K_RETRIEVE", "RERANK_TIMEOUT_S", "SEMANTIC_CACHE"):
        if os.environ.get(k) == "":
            del os.environ[k]                                                      # an empty export from an earlier names box means the default
    from retriever import retrieve                                                # the kit's own path: the index, the Firestore fan-out, prefer_current, the stamps
    pool = retrieve("What is the notice period for a confirmed E3?", "acme", 5)
    print(len(pool), "chunks in the pool, found_by:", dict(collections.Counter(c["found_by"] for c in pool)))
    print("first three:", [(c.get("locator", "?"), c["found_by"], round(c["score"], 4)) for c in pool[:3]])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
