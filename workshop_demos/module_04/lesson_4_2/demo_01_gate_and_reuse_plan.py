"""Lesson 4.2: demo 01 gate and reuse plan

Run the handbook's offline gate and compare six edits through the worker's planner.

Run order inside this file:
1. Do it: the offline gate, scoped to the handbook, Rs 0 (source window 9)
2. Do it: the six edits through the worker's planner (source window 13)

Prerequisites: setup_prepare.
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


# Original CLI workflow for step_01_the_offline_gate_scoped_to_the_handbook_rs.
COMMANDS_01 = """python evals/run_eval.py --source hr_policy_2026.md

"""

def step_01_the_offline_gate_scoped_to_the_handbook_rs(session):
    """Run Do it: the offline gate, scoped to the handbook, Rs 0 at this checkpoint.

    Do it: the offline gate, scoped to the handbook, Rs 0

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (no credentials, no cost).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_the_six_edits_through_the_worker_s_planner(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_the_offline_gate_scoped_to_the_handbook_rs),
        ('source_13', step_02_the_six_edits_through_the_worker_s_planner),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
