"""Lesson 7.1 / s3: The set as it stands: the gate, the rows that cite the handbook, and the clause no row asks about

Summary and purpose:
The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3.

HTML instruction: bash — run in the operator shell, in the kit (the offline gate, then the rows that cite the handbook)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_02_01_which_store_answers_acme_pin_it_to_the_kit_s_own
Expected observation: python evals/run_eval.py
== eval gate: OFFLINE (no credentials, no cost) ==
  65 golden rows over 3 tenants, 27 documents

  [PASS] falsifiable
  [PASS] anchors
  [PASS] coverage

  The golden set is sound. It can go red, and it still contains the rows that would.
  rows citing hr_policy_2026.md: 10 - the scoped live gate judges these
    lk-01  lookup    What is the per-trip cap on domestic travel reimbursement?
    lk-02  lookup    By when is Form 16 issued?
    lk-03  lookup    How many days of earned leave can I carry forward?
    lk-04  lookup    What notice period applies during probation?
    lk-05  lookup    Are USB drives allowed on a company laptop?
    lk-06  lookup    What is the notice period for a confirmed E3?
    lk-07  lookup    At what rate does earned leave accrue?
    lk-08  lookup    Who approves a purchase of Rs 3,00,000?
    lk-09  lookup    How many days a month c

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L464

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make eval
python evals/run_eval.py --source hr_policy_2026.md | sed -n '/rows citing/,$p'
"""


def demonstrate(session):
    """Run Do it: the gate, the rows that cite the handbook, and the handbook's clauses at this checkpoint.

    The second line lists the rows that cite hr_policy_2026.md. They are the set a reindex of that one document is judged on, in lesson 7.3.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the offline gate, then the rows that cite the handbook).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
