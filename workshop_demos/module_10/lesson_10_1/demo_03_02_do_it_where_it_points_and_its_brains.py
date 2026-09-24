"""Lesson 10.1 / s3: The chat service, in your lane's region

Summary and purpose:
Do it: where it points, and its brains

HTML instruction: bash — run in the operator shell, in the kit (where the chat service points, and its brains)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_01_do_it_deploy
Expected observation: RAG_API_URL https://documind-api-NUMBER.asia-south1.run.app | SELF_URL https://documind-chat-NUMBER.asia-south1.run.app | DOCUMIND_BRAIN langchain
{"status":"ok","profile":"gcp","brains":["langchain","langgraph","adk","direct"],"default_brain":"langchain"}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L412

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
gcloud run services describe documind-chat --region "$REGION" --project "$PROJECT" --format=json \\
  | python -c 'import json, sys; s = json.load(sys.stdin); env = {e["name"]: e.get("value") for e in s["spec"]["template"]["spec"]["containers"][0].get("env", [])}; print("  RAG_API_URL", env.get("RAG_API_URL"), "| SELF_URL", env.get("SELF_URL"), "| DOCUMIND_BRAIN", env.get("DOCUMIND_BRAIN"))'
curl -s "$CHAT/health" -H "Authorization: Bearer $(tok "$CHAT")"; echo
"""


def demonstrate(session):
    """Run Do it: where it points, and its brains at this checkpoint.

    Do it: where it points, and its brains

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (where the chat service points, and its brains).
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
