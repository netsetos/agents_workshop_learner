"""Lesson 12.1: demo 02 discover tools

List the server's tools over the actual transport.

Run order inside this file:
1. Do it (source window 15)

Prerequisites: demo_01_expose_and_start_mcp.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (tools/list, raw).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import os
    os.environ["MCP_TOKEN"] = session.identity_token("http://localhost:8121")
    import json, os, urllib.request
    rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}      # one JSON-RPC request; this server needs no session first
    req = urllib.request.Request("http://localhost:8121/mcp", method="POST", data=json.dumps(rpc).encode(),
                                 headers={"Authorization": "Bearer " + os.environ["MCP_TOKEN"], "Content-Type": "application/json",
                                          "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req) as r:
        body = r.read().decode()
        print(f"HTTP {r.status}, {r.headers['Content-Type']}, first line: {body.splitlines()[0]}")
    msg = json.loads(next(line[6:] for line in body.splitlines() if line.startswith("data: ")))
    print(f"tools/list: {len(msg['result']['tools'])} tools")
    for t in msg["result"]["tools"]:
        s = t["inputSchema"]
        need = s.get("required", [])
        print(f"  {t['name']:26} needs {', '.join(need) or 'nothing':12} may take {', '.join(p for p in s['properties'] if p not in need)}")

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_15', step_01_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
