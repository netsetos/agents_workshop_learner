"""Lesson 4.2 / s4: Measure reuse: six kinds of edit, Rs 0

Summary and purpose:
Do it: the six edits through the worker's planner

HTML instruction: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_the_offline_gate_scoped_to_the_handbook_rs
Expected observation: a figure in NP-03 (60 to 90)         chunks 283 -> 283  reused 282  embedded  1    234 chars  ['NP-03']
a figure in PB-02 (15 to 20)         chunks 283 -> 283  reused 282  embedded  1    212 chars  ['PB-02']
NP-03 re-wrapped (whitespace only)   chunks 283 -> 283  reused 283  embedded  0      0 chars  []
NP-03's heading renamed              chunks 283 -> 283  reused 282  embedded  1    250 chars  ['NP-03']
a clause inserted before PB-02       chunks 283 -> 284  reused 283  embedded  1     84 chars  ['NP-04']
NP-03 and PB-02 swapped              chunks 283 -> 283  reused 283  embedded  0      0 chars  []
wages: a sentence added on page 2    chunks  65 ->  65  reused  63  embedded  2   3261 chars  ['p2-0', 'p2-1']

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html#L513

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: the six edits through the worker's planner at this checkpoint.

    Do it: the six edits through the worker's planner

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell (a Python cell, wrapped so it pastes straight into bash).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os, re, sys
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.environ["PROJECT"])
    sys.path[:0] = [".", "services/ingest"]
    from shared import documind_corpus as dc
    from indexer import plan_carry_over
    def cut(text, slug="hr_policy_2026"):
        return dc.chunk_document({"slug": slug, "doc_type": "policy", "source_uri": "gs://x", "text": text}, "acme")
    def measure(name, old, new, slug="hr_policy_2026"):
        a, b = cut(old, slug), cut(new, slug)
        held = {c["chunk_hash"]: ["held"] for c in a}                     # what held_vectors() would lend
        vectors, misses = plan_carry_over(b, held)
        chars = sum(len(b[i]["text"]) for i in misses)
        print(f"{name:36} chunks {len(a):>3} -> {len(b):>3}  reused {len(b) - len(misses):>3}  embedded {len(misses):>2}  {chars:>5} chars  {[b[i]['locator'] for i in misses]}")
    v1 = open("evals/corpus/acme/hr_policy_2026.md", encoding="utf-8").read()
    measure("a figure in NP-03 (60 to 90)", v1, v1.replace("serves a notice period of 60 days", "serves a notice period of 90 days", 1))
    measure("a figure in PB-02 (15 to 20)", v1, v1.replace("period is 15 days for either side", "period is 20 days for either side", 1))
    measure("NP-03 re-wrapped (whitespace only)", v1, v1.replace("A confirmed employee at grade E3 or above serves a notice period of 60 days. Notice runs", "A confirmed employee at grade E3 or above\nserves a notice period of 60 days. Notice runs", 1))
    measure("NP-03's heading renamed", v1, v1.replace("## NP-03 — Notice period", "## NP-03 — Notice period and pay in lieu", 1))
    measure("a clause inserted before PB-02", v1, v1.replace("## PB-02 — Probation", "## NP-04 — Garden leave\n\nGarden leave may be directed for the notice period at full pay.\n\n## PB-02 — Probation", 1))
    m = re.search(r"(## NP-03 — Notice period\n.*?\n\n)(## PB-02 — Probation\n.*?\n\n)", v1, re.S)
    measure("NP-03 and PB-02 swapped", v1, v1.replace(m.group(0), m.group(2) + m.group(1), 1))
    wg = open("evals/corpus/acme/code_on_wages_2019.md", encoding="utf-8").read()
    pages = wg.split("\f"); pages[1] = "A new opening sentence was inserted at the top of this page. " + pages[1]
    measure("wages: a sentence added on page 2", wg, "\f".join(pages), "code_on_wages_2019")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
