"""Lesson 10.4: demo 03 costs and missing observability

Compare recorded cost lines and identify work those rows do not measure.

Run order inside this file:
1. Do it (source window 17)
2. Do it (source window 19)

Prerequisites: demo_02_four_brains_and_gate.
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
COMMANDS_01 = """sleep 20   # Cloud Logging needs a moment to show the rows
python - <<'PY'
import json, os, subprocess
from collections import defaultdict
f = ('resource.type="cloud_run_revision" AND resource.labels.service_name="documind-api" AND jsonPayload.event="query" '
     f'AND timestamp>="{os.environ["SINCE104"]}"')
out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--limit", "50", "--format", "json"],
                     capture_output=True, text=True, check=True).stdout
lines = defaultdict(lambda: {"calls": 0, "tokens_in": 0, "tokens_out": 0, "rs": 0.0})
for e in json.loads(out or "[]"):
    j = e["jsonPayload"]
    line = lines[j.get("brain") or "ui"]
    line["calls"] += 1; line["tokens_in"] += j["tokens_in"]; line["tokens_out"] += j["tokens_out"]; line["rs"] += j["cost_usd"] * 85
for brain in ("direct", "langchain", "langgraph", "adk"):
    n = lines[brain]
    print(f"  {brain:9} {n['calls']} retrieve()  in {n['tokens_in']:>6,}  out {n['tokens_out']:>4}  Rs {n['rs']:.4f}")
json.dump(lines, open(os.path.expanduser("~/lesson104_lines.json"), "w"))
PY

"""

def step_01_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

# Original CLI workflow for step_02_example.
COMMANDS_02 = """GOOGLE_CLOUD_PROJECT="$PROJECT" RAG_API_URL="$API" RAG_TIMEOUT_S=90 \\
DOCUMIND_IMPERSONATE_SA="documind-ui-sa@$PROJECT.iam.gserviceaccount.com" ~/graph-venv/bin/python - <<'PY'
import asyncio, json, logging, os, sys, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
sys.path[:0] = [".", "services/chat"]
from langgraph.checkpoint.memory import InMemorySaver
import brains
Q = "After how many years of continuous service does gratuity become payable?"
IN, OUT = 1.50, 7.50                               # cost.py's rate for gemini-3.6-flash, USD per 1M tokens; thinking bills as output
own = {}
for name in ("langchain", "langgraph", "adk"):
    b = brains.build(name, InMemorySaver())
    cfg = {"configurable": {"thread_id": f"acme:lesson104:{name}"}}
    b.answer(Q, config=cfg, context={"tenant_id": "acme", "user_id": "lesson104", "assertion": "", "brain": name})
    if name == "adk":                              # ADK keeps each model call's usage on the session's events
        s = asyncio.run(b.svc.get_session(app_name="documind", user_id="lesson104", session_id=cfg["configurable"]["thread_id"]))
        calls = [(u.prompt_token_count or 0, (u.candidates_token_count or 0) + (u.thoughts_token_count or 0), u.thoughts_token_count or 0)
                 for u in (e.usage_metadata for e in s.events) if u]
    else:                                          # LangChain keeps it on each AIMessage; output_tokens already counts thinking
        g = b.agent if name == "langchain" else b.graph
        calls = [(u["input_tokens"], u["output_tokens"], u.get("output_token_details", {}).get("reasoning", 0))
                 for u in (getattr(m, "usage_metadata", None) for m in g.get_state(cfg).values["messages"]) if u]
    tin, tout, think = (sum(c[i] for c in calls) for i in range(3))
    own[name] = (tin * IN + tout * OUT) / 1e6 * 85
    print(f"  {name:9} {len(calls)} model calls  in {tin:>6,}  out {tout:>5,} (thinking {think:>5,})  Rs {own[name]:.4f}")
lines = json.load(open(os.path.expanduser("~/lesson104_lines.json")))
print("the four cost lines, whole: the brain's own model calls + rag-api's, from step 5")
for name in ("direct", "langchain", "langgraph", "adk"):
    mine, rag = own.get(name, 0.0), lines.get(name, {}).get("rs", 0.0)
    print(f"  {name:9} Rs {mine:.4f} + Rs {rag:.4f} = Rs {mine + rag:.4f}")
PY

"""

def step_02_example(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (the kit's three agent brains on your machine, their own model calls counted).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_02)

def demonstrate(session):
    """Run this experiment in order, resuming only completed checkpoints safely."""
    run_steps(session, [
        ('source_17', step_01_example),
        ('source_19', step_02_example),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False)


def main():
    """Open the lesson session with the selected IDE interpreter and explicit settings."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
