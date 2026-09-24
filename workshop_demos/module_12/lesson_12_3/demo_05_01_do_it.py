"""Lesson 12.3 / s5: The gate: make smoke-agent

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (the module's A2A gate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: DocuMind A2A peer - live smoke test
  target: https://documind-agent-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  question: After how many years of continuous service does gratuity become payable?
  expected answer pattern: \\b(?:five|5)(?:\\s*\\(\\s*(?:five|5)\\s*\\))?[\\s-]+years?\\b
  [PASS] card refused without a token  status=403
  [PASS] agent card  name=documind_peer url=https://documind-agent-NUMBER.asia-south1.run.app skills=['documind_peer']
  [PASS] task answered  state=completed  'Gratuity is payable after not less than five years of continuous service [1]. Source: paym'
  [PASS] zeta refused by the roster  'The DocuMind server refused this: documind-agent-sa@documind-ai-YOUR-ID.iam.gserviceaccount.com is not on tena'
  [PASS] outsider refused at the door  status=403
  --------------------------------------------------------
  5 passed, 0 fa

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html#L507

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """make smoke-agent PROJECT="$PROJECT" REGION="$REGION"   # the module's A2A gate: five checks
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the module's A2A gate).
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
