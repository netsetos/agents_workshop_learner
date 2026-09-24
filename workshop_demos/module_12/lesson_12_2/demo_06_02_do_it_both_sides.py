"""Lesson 12.2 / s6: One call at each door, and both sides of the answer

Summary and purpose:
Do it: both sides

HTML instruction: bash — run in the operator shell, in the kit (both sides of the answered calls)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it_every_door
Expected observation: documind-mcp, a line per answered call - who asked:
  retrieve  tenant acme   caller documind-ui-sa
  retrieve  tenant zeta   caller documind-ui-sa
documind-api, a row per retrieval it served for the MCP server - who it served:
  retrieve  tenant acme   user   documind-mcp-sa
  retrieve  tenant zeta   user   documind-mcp-sa

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/12-protocols/12.2-mcp-deploy/Netsetos_GCP_Capstone_12.2_MCP_Deploy_WIX.html#L587

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
         f'AND timestamp>="{os.environ["SINCE122"]}"')
    out = subprocess.run(["gcloud", "logging", "read", f, "--project", os.environ["PROJECT"], "--order", "asc", "--limit", "20",
                          "--format", "json"], capture_output=True, text=True, check=True).stdout
    return [e["jsonPayload"] for e in json.loads(out or "[]")]
print("documind-mcp, a line per answered call - who asked:")
for j in rows("documind-mcp", 'jsonPayload.event="mcp_call"'):
    print(f"  {j['tool']:9} tenant {j['tenant']:6} caller {j['caller'].split('@')[0]}")
print("documind-api, a row per retrieval it served for the MCP server - who it served:")
for j in rows("documind-api", 'jsonPayload.brain="mcp"'):
    print(f"  retrieve  tenant {j['tenant']:6} user   {j['user'].split('@')[0]}")
PY
"""


def demonstrate(session):
    """Run Do it: both sides at this checkpoint.

    Do it: both sides

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (both sides of the answered calls).
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
