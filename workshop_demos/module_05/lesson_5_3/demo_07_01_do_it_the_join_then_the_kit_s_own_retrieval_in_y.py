"""Lesson 5.3 / s7: found_by: stamped on every chunk, counted on the answer, absent from the citation

Summary and purpose:
Do it: the join, then the kit's own retrieval in your process, then the smoke

HTML instruction: bash — run in the operator shell (a Python cell; Rs 0: two files on disk)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_02_do_it_the_selftest_then_the_lane_s_last_day_then
Expected observation: the answer's counts: pool 20 | vector_chunks 20 | graph_chunks 0 | managed_chunks 0 | retrieval_backend vector
a citation's fields: ['chunk_id', 'end', 'kind', 'media_url', 'page', 'quote', 'score', 'source_uri', 'start']
   #  1 hr_policy_2026.md          found_by vector   (by the join)
   #  4 hr_policy_2026.md          found_by vector   (by the join)
   #  2 hr_policy_2026.md          found_by vector   (by the join)

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/05-retrieval/5.3-rerank/Netsetos_GCP_Capstone_5.3_Rerank_WIX.html#L806

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the join, then the kit's own retrieval in your process, then the smoke at this checkpoint.

    Do it: the join, then the kit's own retrieval in your process, then the smoke

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell; Rs 0: two files on disk).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json
    ans, d = json.load(open("/tmp/ans53_5.json")), json.load(open("/tmp/pool53.json"))
    stamp = {c["id"]: c["found_by"] for c in d["pool"]}
    s = ans["stages"]
    print(f"the answer's counts: pool {s['pool']} | vector_chunks {s['vector_chunks']} | graph_chunks {s['graph_chunks']} | managed_chunks {s['managed_chunks']} | retrieval_backend {s['retrieval_backend']}")
    print("a citation's fields:", sorted(ans["citations"][0]))
    for c in ans["citations"]:
        print(f"   #{c['chunk_id'].rsplit('#', 1)[1]:>3} {c['source_uri'].split('/')[-1][:26]:26} found_by {stamp.get(c['chunk_id'], 'not in the pool you fetched')}   (by the join)")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
