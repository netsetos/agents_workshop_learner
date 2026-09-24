"""Lesson 13.3 / s5: The tier at 85 percent

Summary and purpose:
Do it: the same three at 85 percent

HTML instruction: bash — run in the operator shell, in the kit (the same candidate at 85 percent; the same three questions)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it_routing_on_the_month_as_it_is
Expected observation: gemini-3.1-flash-lite    What is the notice period for a confirmed E3?
                           A confirmed employee at grade E3 or above serves a notice period of 60 days [1].
  gemini-3.1-flash-lite    Explain what happens when a trip costs more than the per-trip travel cap.
                           Travel is capped at Rs 40,000 per trip [1]; a trip above the cap needs the function head's written approval before travel [1].
  gemini-3.6-flash         Work out, step by step, the total reimbursed for three domestic trips costing Rs 38,000, Rs 45,000 and Rs 22,000.
                           Each trip is reimbursed up to the cap of Rs 40,000 [1]: Rs 38,000 + Rs 40,000 + Rs 22,000 = Rs 1,00,000; the Rs 5,000 above the cap ...

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/13-operations/13.3-cost-controls/Netsetos_GCP_Capstone_13.3_Cost_Controls_WIX.html#L612

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """gcloud run services update documind-api --region "$REGION" --project "$PROJECT" --no-traffic --tag candidate \\
  --update-env-vars SPEND_PCT=85 --quiet     # the replay: the breaker reads 85, the counter is not touched
ask133 "$CAND"
"""


def demonstrate(session):
    """Run Do it: the same three at 85 percent at this checkpoint.

    Do it: the same three at 85 percent

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the same candidate at 85 percent; the same three questions).
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
