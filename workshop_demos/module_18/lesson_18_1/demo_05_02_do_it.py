"""Lesson 18.1 / s5: The gateway, deployed and smoke-tested

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: DocuMind gateway - live smoke test
  target: https://documind-gateway-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] no token is refused at the door  HTTP 403
  [PASS] liveliness as the member's account  HTTP 200 in ...s
  [PASS] documind-general answers JSON  '{"ok": true}' in ...s, model gemini-3.6-flash
  [PASS] the cost header rag-api prices from  x-litellm-response-cost=3.45e-05
  [PASS] a PAN is routed by the guardrail  served by 'gemini-3.6-flash' in ...s (the sensitive route is the self-hosted model, no fallback)
  [PASS] documind-slm answers, or its fallback does  model 'gemini-3.6-flash' in ...s, cost 1.8e-05
  --------------------------------------------------------
  6 passed, 0 failed

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/18-serving/18.1-gateway-routes/Netsetos_GCP_Capstone_18.1_Gateway_Routes_WIX.html#L593

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make smoke-gateway PROJECT="$PROJECT"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit.
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
