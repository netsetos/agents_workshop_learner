"""Lesson 10.1 / s6: The direct brain: one retrieve(), no loop

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a small chat function, and the direct brain)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: direct    tool_calls ['retrieve']  refusals []  citations 5  3180 ms
      Gratuity is payable on termination after not less than five years of continuous service [1].

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L580

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """chat10() {   # one /v1/chat turn as documind-ui-sa: $1 = the brain, $2 = the question
TOKEN="$(tok "$CHAT")" B="$1" Q="$2" python - <<'PY'
import json, os, urllib.error, urllib.request
def text(answer):   # a chat service built before 24 September 2026 can send Gemini's content blocks instead of a string
    return answer if isinstance(answer, str) else "".join(p if isinstance(p, str) else p.get("text", "") for p in answer
                                                          if isinstance(p, str) or p.get("type") == "text")
body = json.dumps({"question": os.environ["Q"], "session_id": "lesson101-" + os.environ["B"], "brain": os.environ["B"]}).encode()
req = urllib.request.Request(os.environ["CHAT"] + "/v1/chat", data=body, method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["TOKEN"]})
try:
    a = json.load(urllib.request.urlopen(req, timeout=300))
    print(f"  {a['brain']:9} tool_calls {a['tool_calls']}  refusals {a['refusals']}  citations {len(a.get('citations', []))}  {a['latency_ms']} ms")
    print(f"      {text(a['answer'])[:96]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}  {e.read().decode(errors='replace')[:100]}")
PY
}
chat10 direct "After how many years of continuous service does gratuity become payable?"
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a small chat function, and the direct brain).
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
