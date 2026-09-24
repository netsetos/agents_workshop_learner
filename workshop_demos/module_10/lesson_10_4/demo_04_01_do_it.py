"""Lesson 10.4 / s4: Four brains on /health, and the module's gate

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (/health, then the module's gate)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_side_by_side
Expected observation: {"status":"ok","profile":"gcp","brains":["langchain","langgraph","adk","direct"],"default_brain":"langchain"}
  DocuMind chat - live smoke test
  target: https://documind-chat-NUMBER.asia-south1.run.app
  --------------------------------------------------------
  [PASS] health  profile=gcp default=langchain
  [PASS] brain direct  3120 ms  tools=['retrieve']  'Gratuity becomes payable after not less than five years of c'
  [PASS] brain langchain  11840 ms  tools=['retrieve']  'Gratuity becomes payable once you have rendered at least fiv'
  [PASS] brain langgraph  9730 ms  tools=['retrieve']  'Gratuity is payable after at least five years of continuous '
  [PASS] brain adk  14260 ms  tools=['retrieve']  'After five years of continuous service, gratuity becomes pay'
  [PASS] outsider refused  status=403 not a member of any tenant
  --------------------------------------------------------
  

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.4-adapters/Netsetos_GCP_Capstone_10.4_Adapters_WIX.html#L590

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app" SINCE104="$(date -u +%FT%TZ)"
curl -s -H "Authorization: Bearer $(tok "$CHAT")" "$CHAT/health"; echo
make smoke-chat PROJECT="$PROJECT" REGION="$REGION"   # the module's gate: four brains, one question, the outsider refused
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (/health, then the module's gate).
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
