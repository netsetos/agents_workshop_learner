"""Lesson 10.1 / s8: The rows: what each brain cost, and what no row records

Summary and purpose:
rag-api's row for every retrieve(), and the chat service's row for every turn. Each retrieve() posts to rag-api's /v1/query, and rag-api writes its usage row, now labelled with the brain that asked. The chat service writes a row of its own for each turn: the brain, the tenant, the user, the session, the time and the two lists. The cell reads both kinds since step 5, the shell's own retrieval included, labelled ui because it named no brain.

HTML instruction: bash — run in the operator shell, in the kit (the rows both services wrote since the retrieve cell; reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_07_01_do_it
Expected observation: rag-api, one row per retrieve():
    brain ui         in   1790  out   96  Rs 0.2894   2600 ms
    brain direct     in   1790  out   96  Rs 0.2894   2710 ms
    brain langchain  in   1812  out  101  Rs 0.2954   2840 ms
    brain langchain  in   1650  out   88  Rs 0.2665   2390 ms
    brain direct     in   1705  out   92  Rs 0.2760   2620 ms
  the chat service, one row per turn:
    brain direct     tool_calls ['retrieve']    3180 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain langchain  tool_calls ['retrieve']    7240 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain langchain  tool_calls ['retrieve', 'calculate_processing_cost']   11350 ms  (keys: brain, event, latency_ms, refusals, session_id, surface, tenant, tool_calls, user)
    brain direct     tool_calls ['retrieve']    3

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.1-agent-loop/Netsetos_GCP_Capstone_10.1_Agent_Loop_WIX.html#L647

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run The rows: what each brain cost, and what no row records at this checkpoint.

    rag-api's row for every retrieve(), and the chat service's row for every turn. Each retrieve() posts to rag-api's /v1/query, and rag-api writes its usage row, now labelled with the brain that asked. The chat service writes a row of its own for each turn: the brain, the tenant, the user, the session, the time and the two lists. The cell reads both kinds since step 5, the shell's own retrieval included, labelled ui because it named no brain.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the rows both services wrote since the retrieve cell; reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os, subprocess
    def rows(service, event):
        f = (f'resource.type="cloud_run_revision" AND resource.labels.service_name="{service}" AND jsonPayload.event="{event}" '
             f'AND timestamp>="{os.environ["SINCE101"]}"')
        out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "30",
                              "--format", "json"], capture_output=True, text=True, check=True).stdout
        return [e["jsonPayload"] for e in json.loads(out or "[]")]
    print("  rag-api, one row per retrieve():")
    for j in rows("documind-api", "query"):
        print(f"    brain {j.get('brain', ''):9}  in {j['tokens_in']:>6}  out {j['tokens_out']:>4}  Rs {j['cost_usd'] * 85:.4f}  {j['latency_ms']:>5} ms")
    print("  the chat service, one row per turn:")
    for j in rows("documind-chat", "chat"):
        print(f"    brain {j['brain']:9}  tool_calls {j['tool_calls']}  {j['latency_ms']:>6} ms  (keys: {', '.join(sorted(j))})")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
