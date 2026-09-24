"""Lesson 12.3 / s6: One task, traced

Summary and purpose:
Do it: what the lane saw

HTML instruction: bash — run in the operator shell, in the kit (who the lane saw)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_the_task
Expected observation: documind-mcp - who asked it:
  retrieve        tenant acme   caller documind-agent-sa
documind-api - who it served:
  retrieve        tenant acme   user   documind-mcp-sa

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.3-a2a-peer/Netsetos_GCP_Capstone_12.3_A2A_Peer_WIX.html#L564

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """sleep 20   # Cloud Logging needs a moment to show the lines
python - <<'PY'
import json, os, subprocess
def rows(service, flt):
    f = (f'resource.type="cloud_run_revision" AND resource.labels.service_name="{service}" AND {flt} '
         f'AND timestamp>="{os.environ["SINCE123"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    return [e["jsonPayload"] for e in json.loads(out or "[]")]
print("documind-mcp - who asked it:")
for j in rows("documind-mcp", 'jsonPayload.event="mcp_call"'):
    print(f"  {j['tool']:15} tenant {j['tenant']:6} caller {j['caller'].split('@')[0]}")
print("documind-api - who it served:")
for j in rows("documind-api", 'jsonPayload.brain="mcp"'):
    print(f"  retrieve        tenant {j['tenant']:6} user   {j['user'].split('@')[0]}")
PY
"""


def demonstrate(session):
    """Run Do it: what the lane saw at this checkpoint.

    Do it: what the lane saw

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (who the lane saw).
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
