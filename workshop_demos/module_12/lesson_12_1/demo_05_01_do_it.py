"""Lesson 12.1 / s5: Discover: tools/list on the wire

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (tools/list, raw)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: HTTP 200, text/event-stream, first line: event: message
tools/list: 4 tools
  retrieve                   needs query        may take doc_type, top_k, tenant
  list_documents             needs nothing      may take status, tenant
  corpus_stats               needs nothing      may take tenant
  calculate_processing_cost  needs total_pages  may take num_documents, processing_type

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.1-mcp-tools/Netsetos_GCP_Capstone_12.1_MCP_Tools_WIX.html#L500

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (tools/list, raw).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
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


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
