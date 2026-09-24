"""Lesson 10.4: Four cost lines, as rag-api's rows draw them

Do it

Run order inside this file:
1. Do it (source window 17)

Prerequisites: demo_04_four_brains_on_health_and_the_module_s_gate.
Use the existing rag-shell-venv interpreter; Run or Debug this file.
The functions below contain the lesson examples in source order. Helpers
supply configuration, authentication, state and CLI execution. See README.md
for expected observations, effects and the next file; GUIDE.md retains prose.
Example: open this file at the matching HTML heading, Run once, then inspect
the observations below before continuing to the next numbered section.
A successful process is not proof that a live result matched the sample.

"""
from workshop_helpers.session import DemoSession
from workshop_helpers.steps import manual_checkpoint, run_steps

# REPEAT replays the whole file; use only after reviewing its effects.
REPEAT = False
# A failed function may have partial effects. Inspect its saved attempt first.
RETRY_FAILED_STEP = False


# Original CLI workflow for step_01_four_cost_lines_as_rag_api_s_rows_draw_the.
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

def step_01_four_cost_lines_as_rag_api_s_rows_draw_the(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.

    Example: Run this file after its README prerequisites, or set a breakpoint in this function.
    Observe: direct    1 retrieve()  in  2,561  out   68  Rs 0.3699
      langchain 1 retrieve()  in  2,498  out   64  Rs 0.3593
      langgraph 1 retrieve()  in  2,504  out   66  Rs 0.3613
      adk       1 retrieve()  in  2,537  out   71  Rs 0.3687
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS_01)

def demonstrate(session):
    """Run this section in source order, saving each function's outcome.

    Example: main() opens the configured session and calls demonstrate(session).
    A failed step stops this sequence; inspect its evidence before an explicit retry.
    """
    run_steps(session, [
        ('source_17', step_01_four_cost_lines_as_rag_api_s_rows_draw_the),
    ], retry_failed=RETRY_FAILED_STEP, cleanup=False, finalize=False)


def main():
    """Open the lesson session and run this section.

    Example: use Run/Debug on this file with the rag-shell-venv interpreter.
    Project settings and completed prerequisites come from the shared setup.
    """
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
