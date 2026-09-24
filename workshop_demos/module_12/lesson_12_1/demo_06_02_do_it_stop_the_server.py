"""Lesson 12.1 / s6: Invoke: retrieve from a local client

Summary and purpose:
Do it: stop the server

HTML instruction: bash — run in the operator shell, in the kit (stop the server, read what it logged)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: mcp_call retrieve  tenant acme  caller documind-ui-sa  via iam  {'answerable': True, 'citations': 5, 'error': None}

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L579

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """kill "$MCP_PID"
python - <<'PY'
import json
for line in open("/tmp/mcp121.log"):
    if line.startswith('{"event": "mcp_call"'):
        e = json.loads(line)
        rest = {k: v for k, v in e.items() if k not in ("event", "tool", "tenant", "caller", "via", "query_sha")}
        print(f"  mcp_call {e['tool']}  tenant {e['tenant']}  caller {e['caller'].split('@')[0]}  via {e['via']}  {rest}")
PY
"""


def demonstrate(session):
    """Run Do it: stop the server at this checkpoint.

    Do it: stop the server

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (stop the server, read what it logged).
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
