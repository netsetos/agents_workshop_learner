"""Lesson 5.2: demo 02 rrf and ablation

Fuse the saved ranks by hand and compare controlled retrieval arms.

Run order inside this file:
1. Do it: fuse the saved lists, compare with the index's fused list (source window 20)
2. Do it: a wiring check, then acme's rows with a ledger (source window 26)

Prerequisites: demo_01_dense_and_sparse_lists.
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


def step_01_fuse_the_saved_lists_compare_with_the_inde(session):
    """Run Do it: fuse the saved lists, compare with the index's fused list at this checkpoint.

    Do it: fuse the saved lists, compare with the index's fused list

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the lists are on disk).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, sys
    sys.path[:0] = [".", "services/rag-api"]
    from hybrid import rrf_fuse
    d = json.load(open("/tmp/legs52.json"))
    name = lambda cid: f"{d['label'][cid][0]} {d['label'][cid][1][:22]}"
    fused = rrf_fuse(d["dense"], d["sparse"], alpha=0.7)             # the kit's rule on the two lists you fetched
    print("by hand, alpha 0.7:")
    for cid, score in fused[:5]:
        print(f"   {name(cid):36} {score:.5f}   dense rank {d['dense'].index(cid) + 1 if cid in d['dense'] else '-':>2}  sparse rank {d['sparse'].index(cid) + 1 if cid in d['sparse'] else '-':>2}")
    hand = [cid for cid, _ in fused][:5]
    print("the index's fused first five:", [name(c) for c in d["hybrid"][:5]])
    print("heads agree on", len(set(hand) & set(d["hybrid"][:5])), "of 5 | first is the same:", hand[0] == d["hybrid"][0])
    print("alpha 1.0 gives the dense list back:", [c for c, _ in rrf_fuse(d["dense"], d["sparse"], alpha=1.0)][:20] == d["dense"])
    print("alpha 0.0 gives the sparse list back:", [c for c, _ in rrf_fuse(d["dense"], d["sparse"], alpha=0.0)][:20] == d["sparse"])
    print(f"the bound: dense #1 {0.7 / 61:.5f}, dense #20 {0.7 / 80:.5f}, sparse #1 alone {0.3 / 61:.5f}")

# Original CLI workflow for step_02_a_wiring_check_then_acme_s_rows_with_a_led.
COMMANDS_02 = """make ablate PROJECT=$PROJECT ABLATE_ARGS="--tenant acme --limit 5"
# the same without make: python evals/ablate.py --project $PROJECT --region $REGION --tenant acme --limit 5

make ablate PROJECT=$PROJECT ABLATE_ARGS="--tenant acme --ledger ~/ablate.jsonl"
tail -n 4 ~/ablate.jsonl | python -c "import sys, json; [print(j['arm'][:32].ljust(34), 'recall@5', j['recall_at_5'], 'mrr', j['mrr'], 'p95', j['p95_ms'], 'ms') for j in map(json.loads, sys.stdin)]"

"""

def step_02_a_wiring_check_then_acme_s_rows_with_a_led(session):
    """Run Do it: a wiring check, then acme's rows with a ledger at this checkpoint.

    The first run takes five rows and about a minute; the second takes acme's 40 rows and a few minutes, and appends one JSON line per arm to a ledger you keep. make ablate passes your exported REGION as the embedding region, which is where the API embeds; the direct call is the same line without make.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (embeddings in paise; the Ranking API per request, a few rupees).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_20', step_01_fuse_the_saved_lists_compare_with_the_inde),
        ('source_26', step_02_a_wiring_check_then_acme_s_rows_with_a_led),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
