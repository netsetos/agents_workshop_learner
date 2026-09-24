"""Lesson 15.4 / s4: Six arms, one golden set: is a store as good?

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (retrieval only, no model: a few minutes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it
Expected observation: python evals/ablate.py --project documind-ai-YOUR-ID --region asia-south1 --arms all
47 rows with anchors, 66 anchors, one knob per arm (project documind-ai-YOUR-ID, embeddings in asia-south1, ranker on global)

arm                                          recall@depth  recall@5    mrr rows@1.0  p95 ms
dense 5, no reranker                                 0.94      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - not retrieved at depth 5
       lost: lk-21: code_on_wages_2019 - not retrieved at depth 5
       lost: jn-11: labour_codes_compliance_handbook - not retrieved at depth 5
dense 20 -> rerank 5   (the lane)                    1.00      0.94   0.81       44     ...
       lost: lk-19: payment_of_bonus_act_1965 - ranked out (in the candidates, not the five)
       lost: lk-21: code_on_wages_2019 - ranked out (in the candidates, not the five)
       lost: j

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.4-mirror-freshness/Netsetos_GCP_Capstone_15.4_Mirror_Freshness_WIX.html#L593

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python -m pip install -q rank-bm25==0.2.2      # the hybrid arm's BM25 (lesson 5.2 installed it; safe to repeat)
make ablate PROJECT="$PROJECT" ABLATE_ARGS="--arms all"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (retrieval only, no model: a few minutes).
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
