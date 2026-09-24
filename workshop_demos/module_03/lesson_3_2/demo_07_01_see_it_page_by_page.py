"""Lesson 3.2 / s7: Compare the boundaries: two parsers, one document

Summary and purpose:
See it, page by page

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_03_read_it_on_the_lane_and_ask_a_question_that_land
Expected observation: lane 67 windows, mirror 65 windows
pages with a different number of windows: [(7, 3, 2), (23, 3, 2)]
p2-0 on the lane: 2000 chars, hash 4c19e0b7a2d8
p2-0 in the mirror: 2000 chars, hash 6a3f7e9c01b5
lane text starts: 'THE CODE ON WAGES, 2019\\nCHAPTER I\\nPRELIMINARY\\n1. (1) This Code may be called ...'
mirror text starts: 'THE CODE ON WAGES, 2019 CHAPTER I PRELIMINARY 1. (1) This Code may be called ...'

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L719

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run See it, page by page at this checkpoint.

    See it, page by page

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, sys, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    sys.path.insert(0, ".")
    from collections import Counter
    from google.cloud import firestore
    from shared import documind_corpus as dc
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    NAME = "code_on_wages_2019"
    
    q = (db.collection("chunks").where("tenant_id", "==", "acme")
         .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/{NAME}.pdf").where("current", "==", True))
    lane = sorted(q.stream(), key=lambda c: int(c.id.rsplit("#", 1)[1]))
    lane_rows = [c.to_dict() for c in lane]
    text = open(f"evals/corpus/acme/{NAME}.md", encoding="utf-8").read()
    local = dc.chunk_document({"slug": NAME, "doc_type": "act", "source_uri": "gs://x", "text": text}, "acme")
    
    lp = Counter(r["page_start"] for r in lane_rows); mp = Counter(c["page_start"] for c in local)
    print(f"lane {len(lane_rows)} windows, mirror {len(local)} windows")
    diff = [p for p in sorted(set(lp) | set(mp)) if lp[p] != mp[p]]
    print("pages with a different number of windows:", [(p, lp[p], mp[p]) for p in diff])
    a = next(r for r in lane_rows if r["locator"] == "p2-0"); b = next(c for c in local if c["locator"] == "p2-0")
    print(f"p2-0 on the lane: {len(a['text'])} chars, hash {a['chunk_hash'][:12]}")
    print(f"p2-0 in the mirror: {len(b['text'])} chars, hash {b['chunk_hash'][:12]}")
    print("lane text starts:", repr(a["text"][:80]))
    print("mirror text starts:", repr(b["text"][:80]))


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
