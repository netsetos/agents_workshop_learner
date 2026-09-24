"""Lesson 5.3 / s5: The fallback: the pool by retrieval score, flagged on the row, forced on a candidate

Summary and purpose:
Do it, offline: the kit's fallback on the pool you saved

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_embed_pool_rank_compare
Expected observation: rerank_fell_back: True | every chunk marked: True
the pool by retrieval score, what the caller gets while the ranker is down:
   score 0.7xxx  pool # 1  NP-03     hr_policy_2026.md
   score 0.7xxx  pool # 2  ...       hr_policy_2026.md
   ...
the ranker's five (step 4): ['NP-03', '...', '...', '...', '...']
kept by the fallback: x of 5 | first is the same: True

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L633

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it, offline: the kit's fallback on the pool you saved at this checkpoint.

    Do it, offline: the kit's fallback on the pool you saved

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (a Python cell; Rs 0: nothing leaves the machine).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, json, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path[:0] = [".", "services/rag-api"]
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    for k in ("RETRIEVAL_MODE", "RETRIEVAL_BACKEND", "RETRIEVAL_CURRENT_ONLY", "TOP_K_RETRIEVE", "RERANK_TIMEOUT_S", "SEMANTIC_CACHE"):
        if os.environ.get(k) == "":
            del os.environ[k]                                                # an empty export from an earlier names box means the default
    from retriever import _by_retrieval_score, rerank_fell_back              # the kit's own fallback, in this process
    d = json.load(open("/tmp/pool53.json"))
    pool, ranked = d["pool"], [i for i, _ in d["ranked"]]
    pos = {c["id"]: i + 1 for i, c in enumerate(pool)}
    stood_in = _by_retrieval_score([dict(c) for c in pool], 5)
    print("rerank_fell_back:", rerank_fell_back(stood_in), "| every chunk marked:", all(c.get("rerank_fallback") for c in stood_in))
    print("the pool by retrieval score, what the caller gets while the ranker is down:")
    for c in stood_in:
        print(f"   score {c['score']:.4f}  pool #{pos[c['id']]:>2}  {c['locator']:9} {c['source'][:28]}")
    print("the ranker's five (step 4):", [pool[i]["locator"] for i in ranked[:5]])
    print("kept by the fallback:", sum(1 for c in stood_in if c["id"] in {pool[i]["id"] for i in ranked[:5]}), "of 5 | first is the same:", stood_in[0]["id"] == pool[ranked[0]]["id"])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
