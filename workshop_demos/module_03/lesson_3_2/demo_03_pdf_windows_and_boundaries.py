"""Lesson 3.2: demo 03 pdf windows and boundaries

Cut the Act into page windows, inspect citations and compare parser boundaries.

Run order inside this file:
1. Do it: cut the Code on Wages, Rs 0 (source window 22)
2. Read it on the lane, and ask a question that lands on a page (source window 24)
3. Read it on the lane, and ask a question that lands on a page (source window 25)
4. See it, page by page (source window 27)

Prerequisites: demo_02_handbook_sections.
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


def step_01_cut_the_code_on_wages_rs_0(session):
    """Run Do it: cut the Code on Wages, Rs 0 at this checkpoint.

    Your kit has a text mirror of every Act, made by pypdf when the corpus was fetched, with a form feed between pages. Cut the mirror of the Code on Wages and look at one seam.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path.insert(0, ".")
    from shared import documind_corpus as dc
    text = open("evals/corpus/acme/code_on_wages_2019.md", encoding="utf-8").read()
    print("pages in the mirror:", text.count("\f") + 1)
    chunks = dc.chunk_document({"slug": "code_on_wages_2019", "doc_type": "act", "source_uri": "gs://x", "text": text}, "acme")
    print(len(chunks), "windows; the first six locators:", [c["locator"] for c in chunks[:6]])
    a, b = chunks[1], chunks[2]                      # p2-0 and p2-1: two windows on the same page
    print(f"{a['locator']} is {len(a['text'])} chars; {b['locator']} is {len(b['text'])} chars")
    print("end of", a["locator"], "->", repr(a["text"][-60:]))
    print("start of", b["locator"], "->", repr(b["text"][:60]))
    print("the overlap: the last 200 characters of", a["locator"], "reappear at the start of", b["locator"], "->", a["text"][-200:] == b["text"][:200])

def step_02_on_the_lane_and_ask_a_question_that_lands(session):
    """Run Read it on the lane, and ask a question that lands on a page at this checkpoint.

    Read it on the lane, and ask a question that lands on a page

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    q = (db.collection("chunks").where("tenant_id", "==", "acme")
         .where("source_uri", "==", f"gs://{PROJECT}-uploads/acme/code_on_wages_2019.pdf")
         .where("current", "==", True))
    rows = sorted(q.stream(), key=lambda c: int(c.id.rsplit("#", 1)[1]))
    print(len(rows), "windows on the lane; first six:", [c.to_dict().get("locator") for c in rows[:6]])
    print("pages seen:", sorted({c.to_dict().get("page_start") for c in rows})[:5], "...", max(c.to_dict().get("page_start") for c in rows))

# Original CLI workflow for step_03_on_the_lane_and_ask_a_question_that_lands.
COMMANDS_03 = """curl -s -X POST $API/v1/query -H "Authorization: Bearer $(tok $API)" -H "Content-Type: application/json" \\
  -d '{"query":"Within how many days must wages be paid after the wage period ends under the Code on Wages?","tenant_id":"acme","stream":false}' \\
  | python -c "import json,sys; j=json.load(sys.stdin); print(j['answer'][:160]); [print(c['chunk_id'].split('#')[1], c['source_uri'].split('/')[-1], 'page', c['page'], '|', c['quote'][:60]) for c in j['citations']]"

"""

def step_03_on_the_lane_and_ask_a_question_that_lands(session):
    """Run Read it on the lane, and ask a question that lands on a page at this checkpoint.

    Read it on the lane, and ask a question that lands on a page

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (acme pinned to vector, see the setup).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_03)

def step_04_see_it_page_by_page(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_22', step_01_cut_the_code_on_wages_rs_0),
        ('source_24', step_02_on_the_lane_and_ask_a_question_that_lands),
        ('source_25', step_03_on_the_lane_and_ask_a_question_that_lands),
        ('source_27', step_04_see_it_page_by_page),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
