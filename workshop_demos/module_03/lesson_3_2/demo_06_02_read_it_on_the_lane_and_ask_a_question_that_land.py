"""Lesson 3.2 / s6: Chunk by window: an Act becomes page windows

Summary and purpose:
Read it on the lane, and ask a question that lands on a page

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_cut_the_code_on_wages_rs_0
Expected observation: Compare the printed observations with this heading in README.md.

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L671

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
