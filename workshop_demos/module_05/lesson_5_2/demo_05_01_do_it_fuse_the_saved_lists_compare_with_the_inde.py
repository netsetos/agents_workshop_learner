"""Lesson 5.2 / s5: RRF by hand: the kit's rule reproduces the server's order

Summary and purpose:
Do it: fuse the saved lists, compare with the index's fused list

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (Rs 0: the lists are on disk)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it_dense_alpha_0_alpha_0_7
Expected observation: by hand, alpha 0.7:
   p36-0 cgst_act_2017.pdf               0.01594   dense rank  2  sparse rank  4
   p1-0 inv_2026_0412.md                 0.01148   dense rank  1  sparse rank  -
   ...
the index's fused first five: ['p36-0 cgst_act_2017.pdf', 'p1-0 inv_2026_0412.md', ...]
heads agree on 5 of 5 | first is the same: True
alpha 1.0 gives the dense list back: True
alpha 0.0 gives the sparse list back: True
the bound: dense #1 0.01148, dense #20 0.00875, sparse #1 alone 0.00492

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.2-hybrid/Netsetos_GCP_Capstone_5.2_Hybrid_WIX.html#L649

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
