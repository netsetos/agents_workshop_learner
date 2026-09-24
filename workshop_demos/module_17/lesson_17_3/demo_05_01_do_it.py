"""Lesson 17.3 / s5: The gate on both revisions

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (every golden row, on each revision: about twenty minutes)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_02_do_it_the_audit
Expected observation: report: /home/YOU/base173.json
  All thresholds met.
>> https://candidate---documind-api-NUMBER.asia-south1.run.app
  65 rows (47 answerable, 18 not) against https://candidate---documind-api-NUMBER.asia-south1.run.app

  [PASS] request_success_rate  100.0%  (threshold 100%; 65 rows)
  [PASS] answerable_rate        97.9%  (threshold 80%; 47 rows)
  [PASS] citation_rate         100.0%  (threshold 95%; 46 rows)
  [PASS] citation_valid_rate   100.0%  (threshold 100%; 46 rows)
  [PASS] must_contain_rate      95.7%  (threshold 85%; 46 rows)
  [PASS] correct_rate           93.6%  (threshold 68%; 47 rows)
  [PASS] refusal_rate          100.0%  (threshold 90%; 18 rows)
  [PASS] media_kind_rate       100.0%  (threshold 80%; 3 rows)
  [PASS] isolation_403_rate    100.0%  (threshold 100%; 11 rows)
  [info] quote_support_rate      ...  (quoted words found in the tenant's corpus text; not a threshold 

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/17-tuning/17.3-tuned-candidate/Netsetos_GCP_Capstone_17.3_Tuned_Candidate_WIX.html#L598

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make eval-live PROJECT="$PROJECT" REPORT="$HOME/base173.json" | tail -3
make eval-live PROJECT="$PROJECT" API="$CAND" REPORT="$HOME/cand173.json"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (every golden row, on each revision: about twenty minutes).
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
