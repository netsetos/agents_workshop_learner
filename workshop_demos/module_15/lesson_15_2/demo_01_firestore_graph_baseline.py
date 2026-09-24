"""Lesson 15.2: demo 01 firestore graph baseline

Read the graph backend and establish the Firestore path.

Run order inside this file:
1. Do it (source window 9)
2. Do it (source window 11)

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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """python - <<'PY'
import sys
sys.path.insert(0, ".")
from shared.documind_graph import _candidate_names, _seed_match, choose_mode   # the kit's seeding rules; no model, no network
NAMES = ["Purchase approval", "function head", "CFO", "Travel reimbursement", "Notice period", "probation", "India", "Remote work"]
QUESTIONS = ["Who signs off on a big purchase?", "Which purchases need the CFO?", "What does the CFO approve?",
             "Who approves a purchase above two lakh?", "Who approves a Purchase above two lakh?", "Who handles Indian travel claims?"]
print("eight names from the handbook's graph:", ", ".join(NAMES))
for q in QUESTIONS:
    cands, ql = _candidate_names(q), q.lower()
    seeds = sorted((n for n in NAMES if _seed_match(n.lower(), ql, cands)), key=len, reverse=True)[:5]
    print(q)
    print(f"  candidate names {cands}")
    print(f"  seeds by containment: {', '.join(seeds) or 'none'}   auto: {choose_mode(q, seeds)}")
PY
python -m unittest discover -s commands/tests -p test_spanner_graph.py      # the kit's own tests of the Spanner walk, against a strict fake

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the seeding rules, run; then the kit's tests; no model, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS='--ask "Who signs off on a big purchase?"'
make graph PROJECT="$PROJECT" TENANT=acme GRAPH_ARGS='--ask "Which purchases need the CFO?"'

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two walks of the Firestore graph; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_9', step_01_example),
        ('source_11', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
