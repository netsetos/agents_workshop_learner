"""Lesson 3.2 / s6: Chunk by window: an Act becomes page windows

Summary and purpose:
Your kit has a text mirror of every Act, made by pypdf when the corpus was fetched, with a form feed between pages. Cut the mirror of the Code on Wages and look at one seam.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_02_read_it_on_the_lane
Expected observation: pages in the mirror: 29
65 windows; the first six locators: ['p1-0', 'p2-0', 'p2-1', 'p3-0', 'p3-1', 'p4-0']
p2-0 is 2000 chars; p2-1 is 1201 chars
end of p2-0 -> 'th or without the knowledge of the\\nprincipal employer and includ'
start of p2-1 -> 'in or\\nin connection with the work of an establishment when he'
the overlap: the last 200 characters of p2-0 reappear at the start of p2-1 -> True

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L646

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
