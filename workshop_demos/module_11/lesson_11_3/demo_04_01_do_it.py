"""Lesson 11.3 / s4: A conversation across a redeploy

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (a word, a redeploy, the word again)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_03_02_do_it_eight_callers
Expected observation: serving documind-chat-00007-x4q
  langchain lesson113-4242-langchain  "Got it: saffron. I'll keep it for this conve"
  adk       lesson113-4242-adk        "Got it: saffron. I'll keep it for this conve"
serving documind-chat-00008-m2k, redeployed at 2026-09-23T11:20:41Z
  langchain lesson113-4242-langchain  saffron yes  'You asked me to remember "saffron"'
  adk       lesson113-4242-adk        saffron no   "I don't have a word from you in th"

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/11-memory/11.3-restart-isolation/Netsetos_GCP_Capstone_11.3_Restart_Isolation_WIX.html#L512

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """export CHAT="https://documind-chat-$NUMBER.$REGION.run.app"
CHAT_TOKEN="$(tok "$CHAT")" python - <<'PY'
import json, os, subprocess, time, urllib.request
def text(answer):   # a chat service built before 24 September 2026 can send Gemini's content blocks instead of a string
    return answer if isinstance(answer, str) else "".join(p if isinstance(p, str) else p.get("text", "") for p in answer
                                                          if isinstance(p, str) or p.get("type") == "text")
P, R, CHAT = os.environ["PROJECT"], os.environ["REGION"], os.environ["CHAT"]
def gc(*a):
    return subprocess.run(["gcloud", *a, "--project", P, "--region", R, "--quiet"], capture_output=True, text=True, check=True).stdout.strip()
def serving():
    return gc("run", "services", "describe", "documind-chat", "--format", "value(status.latestReadyRevisionName)")
def ask(brain, session, question):
    req = urllib.request.Request(CHAT + "/v1/chat", method="POST",
                                 data=json.dumps({"question": question, "session_id": session, "brain": brain}).encode(),
                                 headers={"Authorization": "Bearer " + os.environ["CHAT_TOKEN"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return " ".join(text(json.loads(r.read())["answer"]).split())
state = {"session": f"lesson113-{os.getpid()}", "before": serving()}
print(f"serving {state['before']}")
for brain in ("langchain", "adk"):
    said = ask(brain, f"{state['session']}-{brain}", "Remember this word for me: saffron. Just confirm you have it.")
    print(f"  {brain:9} {state['session']}-{brain:9}  {said[:44]!r}")
state["redeployed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
gc("run", "services", "update", "documind-chat", "--update-env-vars", f"LESSON113_RESTART={int(time.time())}")   # a new revision
gc("run", "services", "update-traffic", "documind-chat", "--to-latest")
state["after"] = serving()
print(f"serving {state['after']}, redeployed at {state['redeployed_at']}Z")
for brain in ("langchain", "adk"):
    said = ask(brain, f"{state['session']}-{brain}", "Which word did I ask you to remember?")
    print(f"  {brain:9} {state['session']}-{brain:9}  saffron {'yes' if 'saffron' in said.lower() else 'no '}  {said[:34]!r}")
json.dump(state, open(os.path.expanduser("~/lesson113.json"), "w"))
PY
"""


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (a word, a redeploy, the word again).
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
