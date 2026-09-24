"""Lesson 10.1: demo 03 agent loop and usage

Run the tool-selection loop and compare the cost records it produces.

Run order inside this file:
1. Do it (source window 22)
2. The rows: what each brain cost, and what no row records (source window 24)

Prerequisites: demo_02_retrieval_and_direct_brain.
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


# Original CLI workflow for step_01_example.
COMMANDS_01 = """chat10 langchain "After how many years of continuous service does gratuity become payable?"
chat10 langchain "The ACME handbook has 283 pages. What would processing it cost at the priority tier?"
chat10 direct "The ACME handbook has 283 pages. What would processing it cost at the priority tier?"

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the LangChain loop on the same question, then a cost question on both brains).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def step_02_the_rows_what_each_brain_cost_and_what_no(session):
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

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_22', step_01_example),
        ('source_24', step_02_the_rows_what_each_brain_cost_and_what_no),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
