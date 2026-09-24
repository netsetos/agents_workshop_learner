"""Lesson 11.1 / s5: One conversation, four brains, two sessions

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (one conversation, four brains, two sessions)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: langchain session A  tools []            tamarind yes  "Got it: tamarind. I'll keep it for this "
  langgraph session A  tools []            tamarind yes  'You asked me to remember "tamarind".'
  adk       session A  tools []            tamarind no   "I don't have a word from you in this con"
  direct    session A  tools ['retrieve']  tamarind no   'The documents do not say which word you '
  langchain session B  tools []            tamarind no   "I don't have a word from you in this con"
  langchain session B  tools ['retrieve']  tamarind no   'Gratuity becomes payable after not less '

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.1-state-history/Netsetos_GCP_Capstone_11.1_State_History_WIX.html#L561

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
CHAT_TOKEN="$(tok "$CHAT")" python - <<'PY'
import json, os, urllib.error, urllib.request
def text(answer):   # a chat service built before 24 September 2026 can send Gemini's content blocks instead of a string
    return answer if isinstance(answer, str) else "".join(p if isinstance(p, str) else p.get("text", "") for p in answer
                                                          if isinstance(p, str) or p.get("type") == "text")
S = {"A": f"lesson111-{os.getpid()}", "B": f"lesson111-{os.getpid()}-b"}   # two fresh sessions each run
TURNS = [("langchain", "A", "Remember this word for me: tamarind. Just confirm you have it."),
         ("langgraph", "A", "Which word did I ask you to remember?"),
         ("adk", "A", "Which word did I ask you to remember?"),
         ("direct", "A", "Which word did I ask you to remember?"),
         ("langchain", "B", "Which word did I ask you to remember?"),
         ("langchain", "B", "After how many years of continuous service does gratuity become payable?")]
for brain, s, q in TURNS:
    req = urllib.request.Request(os.environ["CHAT"] + "/v1/chat", method="POST",
                                 data=json.dumps({"question": q, "session_id": S[s], "brain": brain}).encode(),
                                 headers={"Authorization": "Bearer " + os.environ["CHAT_TOKEN"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            b = json.loads(r.read())
        said = " ".join(text(b["answer"]).split())
        print(f"  {brain:9} session {s}  tools {str(b['tool_calls']):13} tamarind {'yes' if 'tamarind' in said.lower() else 'no '}  {said[:40]!r}")
    except urllib.error.HTTPError as e:
        print(f"  {brain:9} session {s}  HTTP {e.code}  {e.read()[:80]!r}")
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one conversation, four brains, two sessions).
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
