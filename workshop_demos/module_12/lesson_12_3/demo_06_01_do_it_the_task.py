"""Lesson 12.3 / s6: One task, traced

Summary and purpose:
Do it: the task

HTML instruction: bash — run in the operator shell, in the kit (one task, and its history)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: a task, state completed, 4 messages in its history:
  user  text      'After how many years of continuous service does gratuity become pa'
  agent calls     retrieve(query='After how many years of continuous')
  agent receives  retrieve: 5 citations
  agent text      'Gratuity is payable after not less than five years of continuous s'
the answer: Gratuity is payable after not less than five years of continuous service [1]. Source

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html#L533

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """AGENT_TOKEN="$(tok "$AGENT")" python - <<'PY'
import json, os, urllib.request, uuid
body = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "message/send", "params": {"message": {
    "role": "user", "kind": "message", "messageId": str(uuid.uuid4()),
    "parts": [{"kind": "text", "text": "After how many years of continuous service does gratuity become payable?"}]}}}
req = urllib.request.Request(os.environ["AGENT"] + "/", data=json.dumps(body).encode(),
                             headers={"Authorization": "Bearer " + os.environ["AGENT_TOKEN"], "Content-Type": "application/json"})
task = json.loads(urllib.request.urlopen(req, timeout=180).read())["result"]
print(f"a {task['kind']}, state {task['status']['state']}, {len(task['history'])} messages in its history:")
for m in task["history"]:
    for p in m["parts"]:
        if p["kind"] == "text":
            print(f"  {m['role']:5} text      {p['text'][:66]!r}")
        elif p["metadata"].get("adk_type") == "function_call":
            print(f"  {m['role']:5} calls     {p['data']['name']}({', '.join(f'{k}={str(v)[:34]!r}' for k, v in p['data']['args'].items())})")
        else:
            r = p["data"]["response"]
            got = "an error" if r.get("isError") else f"{len(r.get('structuredContent', {}).get('citations', []))} citations"
            print(f"  {m['role']:5} receives  {p['data']['name']}: {got}")
print("the answer:", " ".join(p["text"] for a in task["artifacts"] for p in a["parts"] if p["kind"] == "text")[:84])
PY
"""


def demonstrate(session):
    """Run Do it: the task at this checkpoint.

    Do it: the task

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one task, and its history).
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
