"""Lesson 3.2 / s5: Chunk by section: the handbook becomes 283 clauses

Summary and purpose:
Do it: cut the handbook, Rs 0

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_prove_it_on_the_lane_one_small_pdf_four_pages
Expected observation: 283 chunks from 282 headings
  preamble   section=None                               chars=   97  hash=903e2b39ee92
  NP-03      section=NP-03 — Notice period              chars=  234  hash=f4512754ae41
  PB-02      section=PB-02 — Probation                  chars=  212  hash=bb65ccc2494c
  LV-01      section=LV-01 — Earned leave               chars=  189  hash=ff463cede286
  LV-07      section=LV-07 — Leave on exit              chars=  167  hash=7b5538b88f78
sections windowed within themselves: []

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/03-ingestion/3.2-parse-and-chunk/Netsetos_GCP_Capstone_3.2_Parse_Chunk_WIX.html#L553

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: cut the handbook, Rs 0 at this checkpoint.

    Do it: cut the handbook, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import sys
    sys.path.insert(0, "."); sys.path.insert(0, "services/ingest")
    from shared import documind_corpus as dc
    text = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    doc = {"slug": "hr_policy_2026", "doc_type": "policy", "source_uri": "gs://x/acme/hr_policy_2026.md", "text": text}
    chunks = dc.chunk_document(doc, "acme")
    print(len(chunks), "chunks from", text.count("\n## "), "headings")
    for c in chunks[:5]:
        print(f"  {c['locator']:10} section={str(c['section'])[:32]:34} chars={len(c['text']):5}  hash={c['chunk_hash'][:12]}")
    from collections import Counter
    per_section = Counter(c["section"] for c in chunks)
    print("sections windowed within themselves:", [t for t, n in per_section.items() if n > 1])


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
