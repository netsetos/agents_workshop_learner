"""Lesson 12.2 / s6: One call at each door, and both sides of the answer

Summary and purpose:
Do it: every door

HTML instruction: bash — run in the operator shell, in the kit (one call at each door)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_05_01_do_it
Expected observation: no token                              HTTP 403 - Cloud Run, before the server ran
  ui-sa, a token for rag-api's address  HTTP 401 - Cloud Run, before the server ran
  ui-sa, no email in the token          tool error - not authenticated: the bearer token carries no verified email
  the outsider, naming acme             tool error - documind-outsider-sa is not on tenant 'acme''s roster
  ui-sa, naming zeta                    answered - answerable True, 5 citations

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L551

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Do it: every door at this checkpoint.

    Do it: every door

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (one call at each door).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess, urllib.error, urllib.request
    MCP, P = os.environ["MCP"], os.environ["PROJECT"]
    def mint(account, email=True, audience=MCP):      # a Google ID token, as gcloud mints it for the smoke test
        cmd = ["gcloud", "auth", "print-identity-token", f"--audiences={audience}", f"--impersonate-service-account={account}@{P}.iam.gserviceaccount.com"]
        return subprocess.run(cmd + (["--include-email"] if email else []), capture_output=True, text=True, check=True).stdout.strip()
    def call(token, arguments):                        # one raw tools/call to retrieve; which door answered
        rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "retrieve", "arguments": arguments}}
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if token:
            headers["Authorization"] = "Bearer " + token
        try:
            with urllib.request.urlopen(urllib.request.Request(MCP + "/mcp", data=json.dumps(rpc).encode(), headers=headers), timeout=180) as r:
                result = json.loads(next(line[6:] for line in r.read().decode().splitlines() if line.startswith("data: ")))["result"]
        except urllib.error.HTTPError as e:
            return f"HTTP {e.code} - Cloud Run, before the server ran"
        if result.get("isError"):
            return "tool error - " + result["content"][0]["text"].replace(f"@{P}.iam.gserviceaccount.com", "")
        return f"answered - answerable {result['structuredContent']['answerable']}, {len(result['structuredContent']['citations'])} citations"
    Q = {"query": "After how many years of continuous service does gratuity become payable?"}
    for label, token, args in (("no token", None, Q),
                               ("ui-sa, a token for rag-api's address", mint("documind-ui-sa", audience=os.environ["API"]), Q),
                               ("ui-sa, no email in the token", mint("documind-ui-sa", email=False), Q),
                               ("the outsider, naming acme", mint("documind-outsider-sa"), {**Q, "tenant": "acme"}),
                               ("ui-sa, naming zeta", mint("documind-ui-sa"), {**Q, "tenant": "zeta"})):
        print(f"  {label:37} {call(token, args)}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
