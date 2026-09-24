"""Lesson 3.2 / s4: Count pages first: slices, and the 250-page line

Summary and purpose:
The same count, on the PDFs in your kit folder, with the same library. The cell prints pages and slices per PDF, then the totals and what one parse of the whole corpus would cost at each processor's list price - the rates as the course reads them on the pricing page, to re-verify before quoting.

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_call_it_which_reader_does_your_lane_have
Expected observation: acme/cgst_act_2017.pdf                           pages= 236 slices= 16 inline
acme/code_on_social_security_2020.pdf            pages= 116 slices=  8 inline
acme/code_on_wages_2019.pdf                      pages=  29 slices=  2 inline
acme/maternity_benefit_amendment_act_2017.pdf    pages=   4 slices=  1 inline
acme/posh_act_2013.pdf                           pages=  13 slices=  1 inline
...
zeta/osh_code_2020.pdf                           pages=  86 slices=  6 inline

1065 pages in 79 Document AI requests
one full parse: OCR Rs 136   Layout Parser Rs 905

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L480

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: count the corpus, Rs 0 at this checkpoint.

    The same count, on the PDFs in your kit folder, with the same library. The cell prints pages and slices per PDF, then the totals and what one parse of the whole corpus would cost at each processor's list price - the rates as the course reads them on the pricing page, to re-verify before quoting.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import glob, math, os
    from pypdf import PdfReader
    LIMIT, INLINE, USD_INR = 15, 250, 85
    OCR_USD, LAYOUT_USD = 1.50, 10.00            # per 1,000 pages, list price as read on the pricing page - re-verify
    total = calls = 0
    for path in sorted(glob.glob("evals/corpus/*/*.pdf")):
        n = len(PdfReader(path).pages)
        s = math.ceil(n / LIMIT)
        total += n; calls += s
        lane = "BATCH LANE" if n > INLINE else "inline"
        print(f"{path[13:]:48} pages={n:4} slices={s:3} {lane}")
    print(f"\n{total} pages in {calls} Document AI requests")
    print(f"one full parse: OCR Rs {total/1000*OCR_USD*USD_INR:,.0f}   Layout Parser Rs {total/1000*LAYOUT_USD*USD_INR:,.0f}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
