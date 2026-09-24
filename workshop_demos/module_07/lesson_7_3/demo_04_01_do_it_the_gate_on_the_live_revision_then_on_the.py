"""Lesson 7.3 / s4: The scoped gate on both revisions, and the rows that moved

Summary and purpose:
Do it: the gate on the live revision, then on the candidate

HTML instruction: bash — run in the operator shell, in the kit (the 10 rows that cite the handbook, on each revision: a few minutes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_prove_it_is_one_change
Expected observation: >> https://documind-api-NUMBER.asia-south1.run.app

  report: evals/reports/base73.json
  All thresholds met.
>> https://candidate---documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate       100.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 10 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 10 rows)
  [PASS] must_contain_rate      90.0%  (threshold 85%; 10 rows)
  [PASS] correct_rate           90.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  [ -- ] media_kind_rate         0.0%  (threshold 80%; no rows in scope; 0 rows)
  [ --

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.3-controlled-change/Netsetos_GCP_Capstone_7.3_Controlled_Change_WIX.html#L478

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make eval-live PROJECT="$PROJECT" SOURCE=hr_policy_2026.md REPORT=evals/reports/base73.json | tail -3
make eval-live PROJECT="$PROJECT" SOURCE=hr_policy_2026.md REPORT=evals/reports/cand73.json API="$CAND"
"""


def demonstrate(session):
    """Run Do it: the gate on the live revision, then on the candidate at this checkpoint.

    Do it: the gate on the live revision, then on the candidate

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the 10 rows that cite the handbook, on each revision: a few minutes).
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
