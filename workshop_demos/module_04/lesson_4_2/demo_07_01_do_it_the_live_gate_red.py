"""Lesson 4.2 / s7: The gate goes red, and the two ways back to green

Summary and purpose:
Ten questions to the API, each a generation call: a few rupees at most. The target mints two identity tokens, the UI's account as the member and the outsider's for the isolation rows, which is why it takes a moment to start.

HTML instruction: bash — run in the operator shell, in $DEMO_ROOT (ten questions; a few rupees)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_read_the_three
Expected observation: >> https://documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate       100.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 10 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 10 rows)
  [FAIL] must_contain_rate      80.0%  (threshold 85%; 10 rows)
  [PASS] correct_rate           80.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  ...

  shape        rows   ok   pass
  lookup          9    9      8
  version         1    1      0
  latency ms  p50  2410  p95  3980   (round trip, 10 rows)

  rows that cost a point (2):
    lk-06  lookup    acme   

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/04-lifecycle/4.2-reindex/Netsetos_GCP_Capstone_4.2_Reindex_WIX.html#L658

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make eval-live PROJECT=$PROJECT SOURCE=hr_policy_2026.md
"""


def demonstrate(session):
    """Run Do it: the live gate, red at this checkpoint.

    Ten questions to the API, each a generation call: a few rupees at most. The target mints two identity tokens, the UI's account as the member and the outsider's for the isolation rows, which is why it takes a moment to start.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in $DEMO_ROOT (ten questions; a few rupees).
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
