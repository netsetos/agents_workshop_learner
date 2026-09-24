"""Lesson 10.4 / s5: Four cost lines, as rag-api's rows draw them

Summary and purpose:
Do it

HTML instruction: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_01_do_it
Expected observation: direct    1 retrieve()  in  2,561  out   68  Rs 0.3699
  langchain 1 retrieve()  in  2,498  out   64  Rs 0.3593
  langgraph 1 retrieve()  in  2,504  out   66  Rs 0.3613
  adk       1 retrieve()  in  2,537  out   71  Rs 0.3687

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/10-agents/10.4-adapters/Netsetos_GCP_Capstone_10.4_Adapters_WIX.html#L619

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sleep 20   # Cloud Logging needs a moment to show the rows
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


def demonstrate(session):
    """Run Do it at this checkpoint.

    Do it

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (rag-api's rows since step 4, one line per brain).
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
