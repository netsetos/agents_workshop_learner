"""Lesson 5.2 / s6: The ablation: one knob per arm, no model in the loop

Summary and purpose:
The first run takes five rows and about a minute; the second takes acme's 40 rows and a few minutes, and appends one JSON line per arm to a ledger you keep. make ablate passes your exported REGION as the embedding region, which is where the API embeds; the direct call is the same line without make.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (embeddings in paise; the Ranking API per request, a few rupees)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_fuse_the_saved_lists_compare_with_the_inde
Expected observation: 40 rows with anchors, NN anchors, one knob per arm (project documind-ai-YOUR-ID, embeddings in asia-south1, ranker on global)

arm                                          recall@depth  recall@5    mrr rows@1.0  p95 ms
dense 5, no reranker                                 0.9x      0.9x   0.8x       3x    xxxx
dense 20 -> rerank 5   (the lane)                    0.9x      0.9x   0.9x       3x    xxxx
       lost: lk-xx: PB-02 - ranked out (in the candidates, not the five)
dense 50 -> rerank 5                                 0.9x      0.9x   0.9x       3x    xxxx
hybrid 20 -> rerank 5  (4.5, not wired)              0.9x      0.9x   0.9x       3x    xxxx

Read it in this order: recall@depth is the reranker's ceiling - if the 20 and 50 rows agree, depth is not the knob;
recall@5 of the lane's row minus the first row is the reranker's lift, and p95 is what it costs;
the hybrid row says whethe

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L736

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make ablate PROJECT=$PROJECT ABLATE_ARGS="--tenant acme --limit 5"
# the same without make: python evals/ablate.py --project $PROJECT --region $REGION --tenant acme --limit 5

make ablate PROJECT=$PROJECT ABLATE_ARGS="--tenant acme --ledger ~/ablate.jsonl"
tail -n 4 ~/ablate.jsonl | python -c "import sys, json; [print(j['arm'][:32].ljust(34), 'recall@5', j['recall_at_5'], 'mrr', j['mrr'], 'p95', j['p95_ms'], 'ms') for j in map(json.loads, sys.stdin)]"
"""


def demonstrate(session):
    """Run Do it: a wiring check, then acme's rows with a ledger at this checkpoint.

    The first run takes five rows and about a minute; the second takes acme's 40 rows and a few minutes, and appends one JSON line per arm to a ledger you keep. make ablate passes your exported REGION as the embedding region, which is where the API embeds; the direct call is the same line without make.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (embeddings in paise; the Ranking API per request, a few rupees).
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
