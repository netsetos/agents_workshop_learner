"""Lesson 3.1 / s6: Page and section: where inside the document

Summary and purpose:
Read it in Firestore

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_call_it_a_question_and_the_page_on_each_citation
Expected observation: hr_policy_2026.md -> 283 current chunks
     0  locator=preamble   page_start=None  section=None
     1  locator=NP-03      page_start=None  section=NP-03 — Notice period
     2  locator=PB-02      page_start=None  section=PB-02 — Probation
     3  locator=LV-01      page_start=None  section=LV-01 — Earned leave
     ...
code_on_wages_2019.pdf -> 67 current chunks
     0  locator=p1-0       page_start=1     section=None
     1  locator=p1-1       page_start=1     section=None
     2  locator=p2-0       page_start=2     section=None

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.1-contracts/Netsetos_GCP_Capstone_3.1_Contracts_WIX.html#L733

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Read it in Firestore at this checkpoint.

    Read it in Firestore

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, warnings
    warnings.filterwarnings("ignore", category=UserWarning)   # the Firestore client warns about positional where(); the kit uses that form
    from google.cloud import firestore
    PROJECT = os.environ["PROJECT"]
    db = firestore.Client(project=PROJECT)
    
    def locators(tenant, name, n=5):
        q = (db.collection("chunks").where("tenant_id", "==", tenant)
             .where("source_uri", "==", f"gs://{PROJECT}-uploads/{tenant}/{name}")
             .where("current", "==", True))
        rows = sorted(q.stream(), key=lambda c: int(c.id.rsplit("#", 1)[1]))
        print(name, "->", len(rows), "current chunks")
        for c in rows[:n]:
            d = c.to_dict()
            print(f"  {c.id.split('#')[1]:>4}  locator={d.get('locator')!s:10} page_start={d.get('page_start')!s:5} section={str(d.get('section'))[:40]}")
    
    locators("acme", "hr_policy_2026.md")
    locators("acme", "code_on_wages_2019.pdf")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
