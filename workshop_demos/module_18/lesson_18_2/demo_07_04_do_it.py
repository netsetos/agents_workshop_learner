"""Lesson 18.2 / s7: The small model behind the gateway and the API

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the gate, scoped to the HR policy's rows)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_03_do_it
Expected observation: >> https://candidate---documind-api-NUMBER.asia-south1.run.app
== eval gate: LIVE ==
  scoped to hr_policy_2026.md: 10 row(s) cite it
  10 rows (10 answerable, 0 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 10 rows)
  [PASS] answerable_rate        90.0%  (threshold 80%; 10 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 9 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 9 rows)
  [PASS] must_contain_rate      88.9%  (threshold 85%; 9 rows)
  [PASS] correct_rate           80.0%  (threshold 68%; 10 rows)
  [ -- ] refusal_rate            0.0%  (threshold 90%; no rows in scope; 0 rows)
  [ -- ] media_kind_rate         0.0%  (threshold 80%; no rows in scope; 0 rows)
  [ -- ] isolation_403_rate      0.0%  (threshold 100%; no rows in scope; 0 rows)
  [info] quote_support_rate      ... 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.2-ollama-slm/Netsetos_GCP_Capstone_18.2_Ollama_SLM_WIX.html#L804

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make eval-live PROJECT="$PROJECT" API="$CAND" SOURCE=hr_policy_2026.md REPORT="$HOME/slm182.json"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the gate, scoped to the HR policy's rows).
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
