"""Lesson 15.2 / s3: The seeders, run

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the seeding rules, run; then the kit's tests; no model, no network)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: eight names from the handbook's graph: Purchase approval, function head, CFO, Travel reimbursement, Notice period, probation, India, Remote work
Who signs off on a big purchase?
  candidate names ['who signs off on a big purchase?']
  seeds by containment: none   auto: vector
Which purchases need the CFO?
  candidate names ['which purchases need the cfo?']
  seeds by containment: CFO   auto: graph
What does the CFO approve?
  candidate names ['what does the cfo approve?']
  seeds by containment: CFO   auto: vector
Who approves a purchase above two lakh?
  candidate names ['who approves a purchase above two lakh?']
  seeds by containment: none   auto: vector
Who approves a Purchase above two lakh?
  candidate names ['purchase']
  seeds by containment: Purchase approval   auto: graph
Who handles Indian travel claims?
  candidate names ['indian']
  seeds by containment: India   auto: graph


Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/15-graph/15.2-graph-paths/Netsetos_GCP_Capstone_15.2_Graph_Paths_WIX.html#L461

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the seeding rules, run; then the kit's tests; no model, no network).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=False, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
